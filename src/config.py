from datarobot.core.config import DataRobotAppFrameworkBaseSettings


class Config(DataRobotAppFrameworkBaseSettings):
    # Injected by the DataRobot platform — the URL path prefix for this Custom Application
    base_path: str = ""
