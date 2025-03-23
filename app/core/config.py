from pydantic_settings import BaseSettings
import logging


class AppSettings(BaseSettings):
    TELEGRAM_TOKEN: str = ""


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
settings = AppSettings()
