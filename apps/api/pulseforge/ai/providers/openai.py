from __future__ import annotations

import json

import httpx

from pulseforge.ai.providers.base import AIProvider, StructuredCompletion
from pulseforge.config import Settings


class OpenAIProvider(AIProvider):
    name = "openai"

    def __init__(self, settings: Settings):
        if not settings.openai_api_key:
            raise ValueError("PULSEFORGE_OPENAI_API_KEY is required for the OpenAI provider")
        self.settings = settings

    async def complete_structured(self, *, messages, schema, operation):
        payload = {
            "model": self.settings.openai_model,
            "input": [{"role": m.role, "content": m.content} for m in messages],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": f"pulseforge_{operation}",
                    "schema": schema,
                    "strict": True,
                }
            },
        }
        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post("https://api.openai.com/v1/responses", json=payload, headers=headers)
            response.raise_for_status()
            raw = response.json()
        text = raw.get("output_text")
        if not text:
            for item in raw.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        text = content.get("text")
                        break
        data = json.loads(text or "{}")
        usage = raw.get("usage") or {}
        return StructuredCompletion(
            data=data,
            model=raw.get("model", self.settings.openai_model),
            provider=self.name,
            usage=usage,
        )
