from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    TELEGRAM_TOKEN: str = ""


settings = AppSettings()
