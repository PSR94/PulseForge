from __future__ import annotations

import json

import httpx

from pulseforge.ai.providers.base import AIProvider, StructuredCompletion
from pulseforge.config import Settings


class AzureOpenAIProvider(AIProvider):
    name = "azure_openai"

    def __init__(self, settings: Settings):
        required = (
            settings.azure_openai_api_key,
            settings.azure_openai_endpoint,
            settings.azure_openai_deployment,
        )
        if not all(required):
            raise ValueError("Azure OpenAI endpoint, key, and deployment must be configured")
        self.settings = settings

    async def complete_structured(self, *, messages, schema, operation):
        endpoint = self.settings.azure_openai_endpoint.rstrip("/")
        url = (
            f"{endpoint}/openai/deployments/{self.settings.azure_openai_deployment}"
            "/chat/completions?api-version=2025-04-01-preview"
        )
        payload = {
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": f"pulseforge_{operation}", "schema": schema, "strict": True},
            },
        }
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                json=payload,
                headers={"api-key": self.settings.azure_openai_api_key, "Content-Type": "application/json"},
            )
            response.raise_for_status()
            raw = response.json()
        data = json.loads(raw["choices"][0]["message"]["content"])
        return StructuredCompletion(
            data=data,
            model=raw.get("model", self.settings.azure_openai_deployment),
            provider=self.name,
            usage=raw.get("usage") or {},
        )
