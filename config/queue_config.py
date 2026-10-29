from pydantic import Field
from config.setting_config import Settings


class QueueConfig(Settings):
    number_processes: int = Field(default=2)
