from config.setting_config import Settings
from pydantic import Field


class LoggerConfig(Settings):
    logs_path : str = Field(default="logs/logs.log")
    log_mode : str = Field(default="debug")