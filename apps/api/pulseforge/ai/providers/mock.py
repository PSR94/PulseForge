from __future__ import annotations

from pulseforge.ai.providers.base import AIProvider, StructuredCompletion


class MockProvider(AIProvider):
    name = "mock"

    async def complete_structured(self, *, messages, schema, operation):
        text = messages[-1].content if messages else ""
        return StructuredCompletion(
            data={
                "summary": f"Mock analysis for {operation}: {text[:240]}",
                "confidence": 0.5,
                "label": "inference",
            },
            model="deterministic-mock-v1",
            provider=self.name,
            usage={"input_tokens": 0, "output_tokens": 0},
        )
