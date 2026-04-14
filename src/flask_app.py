import logging
import os
from datetime import datetime, timezone
from urllib.parse import urlparse

import datarobot
import requests
import yaml
from flask import Flask, jsonify, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config

logger = logging.getLogger(__name__)

# BASE_PATH is injected by the DataRobot platform (e.g. "custom_applications/abc123").
# Config reads it from the environment via DataRobotAppFrameworkBaseSettings.
# Setting SCRIPT_NAME makes url_for() generate prefix-aware URLs.
_config = Config()
_BASE_PATH = _config.base_path.strip("/")
_SCRIPT_NAME = f"/{_BASE_PATH}" if _BASE_PATH else ""

base_dir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__, template_folder=os.path.join(base_dir, "templates"))

# ProxyFix handles X-Forwarded-For / X-Forwarded-Proto from the reverse proxy.
# We deliberately omit x_prefix — the prefix is sourced from BASE_PATH instead.
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_for=1, x_proto=1)

if _SCRIPT_NAME:
    _inner = flask_app.wsgi_app
    def _script_name_middleware(environ, start_response, _app=_inner, _sn=_SCRIPT_NAME):
        environ["SCRIPT_NAME"] = _sn
        return _app(environ, start_response)
    flask_app.wsgi_app = _script_name_middleware

# OpenAPI spec is defined in openapi.yaml — edit that file to document new routes
with open(os.path.join(base_dir, "openapi.yaml")) as _f:
    OPENAPI_SPEC = yaml.safe_load(_f)

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _proxy(path):
    """Proxy a GET request to the DataRobot API."""
    try:
        dr = datarobot.Client()
        url = f"{dr.endpoint.rstrip('/')}/{path.lstrip('/')}"
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {dr.token}"},
            params=request.args.to_dict() or None,
            timeout=30,
        )
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.HTTPError as exc:
        return jsonify({"error": str(exc)}), exc.response.status_code
    except Exception as exc:
        logger.exception("Error proxying %s", path)
        return jsonify({"error": str(exc)}), 500


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@flask_app.route("/")
def index():
    try:
        dr = datarobot.Client()
        parsed = urlparse(dr.endpoint.rstrip("/"))
        dr_apidocs_url = f"{parsed.scheme}://{parsed.netloc}/apidocs/"
    except Exception:
        dr_apidocs_url = None
    return render_template("index.html", dr_apidocs_url=dr_apidocs_url)


@flask_app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


@flask_app.route("/api/me")
def api_me():
    return _proxy("/account/info/")


@flask_app.route("/api/projects")
def api_projects():
    return _proxy("/projects/")


@flask_app.route("/api/deployments")
def api_deployments():
    return _proxy("/deployments/")


@flask_app.route("/api/use-cases")
def api_use_cases():
    return _proxy("/useCases/")


@flask_app.route("/api/version")
def api_version():
    return _proxy("/version/")


@flask_app.route("/openapi.json")
def openapi_spec():
    spec = dict(OPENAPI_SPEC)
    spec["servers"] = [{"url": request.url_root.rstrip("/")}]
    return jsonify(spec)


@flask_app.route("/apidocs")
def apidocs():
    return render_template("apidocs.html")


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=False, port=8080)
