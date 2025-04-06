from pydantic_settings import BaseSettings
import logging


class AppSettings(BaseSettings):
    TELEGRAM_TOKEN: str = ""
    LOGFIRE_ENABLED: bool = False
    LOGFIRE_TOKEN: str = ""


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def logfire_init():  # pragma: no cover
    # Check if Logfire is enabled in settings
    if settings.LOGFIRE_ENABLED:
        import logfire

        logfire.configure(token=settings.LOGFIRE_TOKEN)
        logger.addHandler(logfire.LogfireLoggingHandler())
        logger.info("🪵🔥 Logging to Logfire enabled")
    else:
        logger.info("🪵🔥 Logging to Logfire disabled")
        # Define a no-op context manager as fallback
        from contextlib import contextmanager

        @contextmanager
        def noop_span(*args, **kwargs):
            yield

        class DummyLogfire:
            span = noop_span

        logfire = DummyLogfire()
    return logfire


logger = logging.getLogger(__name__)
settings = AppSettings()
logfire = logfire_init()
