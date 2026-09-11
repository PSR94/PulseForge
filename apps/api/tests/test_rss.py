from pulseforge.config import Settings
from pulseforge.domain.models import Source, SourceType
from pulseforge.connectors.rss import RssConnector


def test_rss_fixture_parses_as_document():
    payload = b"""<?xml version='1.0'?><rss><channel><item><title>Company X acquires Company Y</title><link>https://example.com/a</link><pubDate>Fri, 11 Sep 2026 10:00:00 GMT</pubDate><description>Acquisition announced.</description></item></channel></rss>"""
    source = Source(
        id="s1", workspace_id="ai-industry", name="Fixture", source_type=SourceType.RSS,
        source_url="https://example.com/feed.xml", canonical_url="https://example.com/feed.xml",
    )
    docs = list(RssConnector(Settings()).parse(source, payload))
    assert len(docs) == 1
    assert docs[0].title == "Company X acquires Company Y"
    assert docs[0].stage.value == "INGESTED"
