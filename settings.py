from pydantic_settings import BaseSettings
from pathlib import Path
from os.path import dirname


class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения
    """

    # bot
    bot_token: str
    logger_id: str
    owner_id: int
    proxy_url: str = "http://api_client:8000"

    # api
    database_url: str
    api_token: str
    api_base_url: str
    secret_key: str
    algorithm: str
    expire_time: int

    # other
    postgres_user: str
    postgres_password: str
    postgres_db: str

    # pg
    pgadmin_default_email: str
    pgadmin_default_password: str
    pgadmin_config_server_mode: bool

    @property
    def bot_workdir(self) -> Path:
        return Path(dirname(__file__)) / "bot"

    class Config:
        env_file = "./.env"
        extra = "ignore"


settings = Settings()
