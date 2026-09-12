from __future__ import annotations

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from pulseforge.config import Settings


def configure_tracing(settings: Settings) -> None:
    if not settings.enable_tracing:
        return
    provider = TracerProvider(resource=Resource.create({"service.name": "pulseforge-api"}))
    if settings.otlp_endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        except ImportError:
            pass
        else:
            provider.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otlp_endpoint))
            )
    trace.set_tracer_provider(provider)


def tracer():
    return trace.get_tracer("pulseforge")
