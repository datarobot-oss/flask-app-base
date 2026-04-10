# Flask app base template

A Flask application template for building Custom Applications on DataRobot. DataRobot credentials and runtime parameters are read automatically — no manual `os.getenv()` or shell exports required.

## Setup

Run locally or deploy as a DataRobot Custom Application via the Registry's **Applications** page or [DRApps](https://github.com/datarobot/dr-apps/blob/main/README.md).

**Dependencies** are managed with [uv](https://github.com/astral-sh/uv):

```shell
uv sync
uv run gunicorn flask_app:flask_app --bind :8080
```

When running locally, set the DataRobot credentials as environment variables:

```shell
export DATAROBOT_API_TOKEN="<your API key>"
export DATAROBOT_ENDPOINT="https://app.datarobot.com/api/v2"
```

When deployed as a Custom Application, these are injected automatically.

## Configuration

App settings are defined in `config.py` using `DataRobotAppFrameworkBaseSettings`, which automatically reads environment variables, `.env` files, and DataRobot Runtime Parameters:

```python
from datarobot.core.config import DataRobotAppFrameworkBaseSettings

class Config(DataRobotAppFrameworkBaseSettings):
    base_path: str = ""
    my_setting: str = "default"
```

Use `Config()` anywhere in your app:

```python
from config import Config

config = Config()
print(config.my_setting)
```

## Add runtime parameters

Declare parameters in `metadata.yaml` in your application source folder:

```yaml
runtimeParameterDefinitions:
  - fieldName: MY_SETTING
    type: string
    defaultValue: "default"
```

Add the corresponding field to `Config` in `config.py`:

```python
class Config(DataRobotAppFrameworkBaseSettings):
    my_setting: str = "default"
```

`Config()` will read the runtime parameter value automatically — no `start-app.sh` changes needed.

## Add pages

Sample templates live in `./src/templates`. Add new routes in `flask_app.py`:

```python
@flask_app.route("/new-page")
def new_page_route():
    return render_template("new-page.html", message="Hello World!")
```

Contents of `new-page.html`:

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Template</title>
</head>
<body>
<h1>{{ message }}</h1>
</body>
</html>
```
