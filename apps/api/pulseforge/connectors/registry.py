from __future__ import annotations

from pulseforge.config import Settings
from pulseforge.connectors.api import PublicAPIConnector
from pulseforge.connectors.arxiv import ArxivConnector
from pulseforge.connectors.base import Connector
from pulseforge.connectors.github import GitHubConnector
from pulseforge.connectors.hackernews import HackerNewsConnector
from pulseforge.connectors.json_feed import JsonFeedConnector
from pulseforge.connectors.rss import RssConnector
from pulseforge.connectors.web import WebPageConnector
from pulseforge.domain.models import SourceType


class ConnectorRegistry:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._connectors: dict[SourceType, Connector] = {
            SourceType.RSS: RssConnector(settings),
            SourceType.JSON: JsonFeedConnector(settings),
            SourceType.WEB: WebPageConnector(settings),
            SourceType.GITHUB: GitHubConnector(settings),
            SourceType.ARXIV: ArxivConnector(settings),
            SourceType.HACKER_NEWS: HackerNewsConnector(settings),
            SourceType.API: PublicAPIConnector(settings),
        }

    def get(self, source_type: SourceType) -> Connector:
        try:
            return self._connectors[source_type]
        except KeyError as exc:
            raise ValueError(f"No connector registered for {source_type.value}") from exc

    def supported_types(self) -> list[str]:
        return sorted(item.value for item in self._connectors)
