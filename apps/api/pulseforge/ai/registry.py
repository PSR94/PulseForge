from __future__ import annotations

from pulseforge.ai.providers.azure import AzureOpenAIProvider
from pulseforge.ai.providers.base import AIProvider
from pulseforge.ai.providers.local import LocalOpenAICompatibleProvider
from pulseforge.ai.providers.mock import MockProvider
from pulseforge.ai.providers.openai import OpenAIProvider
from pulseforge.config import Settings


def build_provider(settings: Settings) -> AIProvider:
    match settings.ai_provider.lower():
        case "mock":
            return MockProvider()
        case "openai":
            return OpenAIProvider(settings)
        case "azure" | "azure_openai":
            return AzureOpenAIProvider(settings)
        case "local":
            return LocalOpenAICompatibleProvider(settings)
        case other:
            raise ValueError(f"Unknown AI provider: {other}")
