# Flask app base template

## What's in this repository?
In this repository you will find an empty Flask application base template to kickstart your custom app development.

The Datarobot client is already set up for you to use, it uses the Application owners' API token by default. 

## How do I set it up?
You can run the Flask app in DataRobot via Custom Applications or run the app directly locally.
Custom Applications can be created either via the registry workshop or
using [DRApps](https://github.com/datarobot/dr-apps/blob/main/README.md)

Make sure to define the required variables for the app to talk to DataRobot. If you run the app from local or another
environment than DataRobots Custom Applications you'll need to set the env variables. When this app is run via
custom applications workshop they should be set automatically.

```shell
#start-app.sh
export token="$DATAROBOT_API_TOKEN"  # Your API token from DR developer tools page
export endpoint="$DATAROBOT_ENDPOINT"  # Example: https://app.datarobot.com/api/v2/
```

## How to add and use runtime parameters?
Create a metadata.yaml file in your application source folder. Here is an example of a DEPLOYMENT_ID:
```yaml
runtimeParameterDefinitions:
- fieldName: DEPLOYMENT_ID
  type: string
```

Once this file is part of your Application source in DataRobot, it will display the new runtime parameter(s) as part of the
app configuration.

To use the parameters we recommend to add them via `start-app.sh`, add this conditional export before `gunicorn` starts:
```shell
if [ -n "$MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID" ]; then
  export deployment_id="$MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID"
fi
```

Now you can use `os.getenv("deployment_id")` within your application code.

## How do I add more pages?
In the `./src/templates` directory you will find a sample index page. You can add additional HTML templates here, and
call them by adding new routes in the `flask_app.py` like this:
```python
@flask_app.route("/new-page")
def index_route():
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