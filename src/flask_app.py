import logging
import os

from datarobot import Client
from datarobot.client import set_client
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

logger = logging.getLogger(__name__)

# Setup DR client
DR_TOKEN = os.getenv("token")
DR_ENDPOINT = os.getenv("endpoint")
set_client(Client(token=DR_TOKEN, endpoint=DR_ENDPOINT))

base_dir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_prefix=1)

@flask_app.route("/")
def index_route():
    return render_template("index.html", message="Hello from Flask")

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=False, port=8080)
