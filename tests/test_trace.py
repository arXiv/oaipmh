from unittest import mock

from opentelemetry import trace
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from oaipmh.factory import setup_trace


def test_setup_trace_records_a_span_for_a_request(test_client):
    exporter = InMemorySpanExporter()
    with mock.patch("opentelemetry.exporter.cloud_trace.CloudTraceSpanExporter", return_value=exporter):
        setup_trace("oaipmh-test", test_client.application)

    test_client.get("/oai?verb=Identify")
    trace.get_tracer_provider().force_flush()

    assert [span.name for span in exporter.get_finished_spans()] == ["GET /oai"]
