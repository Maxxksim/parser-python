from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    NUMBER_PROCESSES: int

    model_config = SettingsConfigDict(env_file=".env")
