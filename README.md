# Flask app base template

In this repository you will find an empty Flask application base template to kickstart custom app development. The Datarobot client is already set up for you to use, it uses the Application creator's API key by default.

## Setup

You can run the Flask app in DataRobot using a custom application or by running the app locally. Custom applications can be created either via the NextGen Registry's **Applications** page or by using [DRApps](https://github.com/datarobot/dr-apps/blob/main/README.md).

Be sure to define the required variables for the app to communicate with DataRobot. If you run the app locally or in another environment than a custom application, you'll need to set the env variables. When this app is run via a custom application, the variables are set automatically.

```shell
#start-app.sh
export token="$DATAROBOT_API_TOKEN"  # Your API key, accessed from DataRobot's Developer Tools page
export endpoint="$DATAROBOT_ENDPOINT"  # Example: https://app.datarobot.com/api/v2/
```

## Add and use runtime parameters

To add runtime parameters, create a `metadata.yaml` file in your application source folder. Here is an example of a `DEPLOYMENT_ID` that creates an environment variable called `MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID`:

```yaml
runtimeParameterDefinitions:
- fieldName: DEPLOYMENT_ID
  type: string
```

Once this file is part of your application source in DataRobot, it displays the new runtime parameter(s) as part of the
app configuration.

To use the parameters, DataRobot recommends you add them via `start-app.sh`. Add the following conditional export before `gunicorn` starts:

```shell
if [ -n "$MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID" ]; then
  export deployment_id="$MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID"
fi
```

Now you can use `os.getenv("deployment_id")` within your application code.

## Add pages

You can find a sample index page in the `./src/templates` directory. You can add additional HTML templates here, and call them by adding new routes in the `flask_app.py`, as shown in the example below:

```python
@flask_app.route("/new-page")
def new_page_route():
    return render_template("new-page.html", message="Hello World!")
```

Contents of new-page.html:

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
