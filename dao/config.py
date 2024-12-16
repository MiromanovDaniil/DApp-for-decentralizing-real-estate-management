from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    DB_PATH: str = "dao/property.py"
