from __future__ import annotations

import json

import httpx

from pulseforge.ai.providers.base import AIProvider, StructuredCompletion
from pulseforge.config import Settings


class LocalOpenAICompatibleProvider(AIProvider):
    name = "local"

    def __init__(self, settings: Settings):
        self.settings = settings

    async def complete_structured(self, *, messages, schema, operation):
        payload = {
            "model": self.settings.local_ai_model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "response_format": {"type": "json_object"},
            "temperature": 0,
        }
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                self.settings.local_ai_base_url.rstrip("/") + "/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            raw = response.json()
        content = raw["choices"][0]["message"]["content"]
        return StructuredCompletion(
            data=json.loads(content),
            model=raw.get("model", self.settings.local_ai_model),
            provider=self.name,
            usage=raw.get("usage") or {},
        )
