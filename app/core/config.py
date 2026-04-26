from pydantic_settings import BaseSettings
import logging


class AppSettings(BaseSettings):
    TELEGRAM_TOKEN: str = ""
    OTEL_ENABLED: bool = False


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def otel_init():  # pragma: no cover
    from opentelemetry import trace

    if settings.OTEL_ENABLED:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry._logs import set_logger_provider
        from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
        from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
        from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

        resource = Resource.create({"service.name": "qrcodegen"})

        trace_provider = TracerProvider(resource=resource)
        # OTLPSpanExporter reads OTEL_EXPORTER_OTLP_ENDPOINT and OTEL_EXPORTER_OTLP_HEADERS from env
        trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
        trace.set_tracer_provider(trace_provider)

        log_provider = LoggerProvider(resource=resource)
        log_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
        set_logger_provider(log_provider)
        logger.addHandler(LoggingHandler(logger_provider=log_provider))

        logger.info("OpenTelemetry enabled")
    else:
        logger.info("OpenTelemetry disabled")

    return trace.get_tracer("qrcodegen")


logger = logging.getLogger(__name__)
settings = AppSettings()
tracer = otel_init()
