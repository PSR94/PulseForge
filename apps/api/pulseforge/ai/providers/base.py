from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class AIMessage(BaseModel):
    role: str
    content: str


class StructuredCompletion(BaseModel):
    data: dict[str, Any]
    model: str
    provider: str
    usage: dict[str, int | float] = Field(default_factory=dict)


class AIProvider(ABC):
    name: str

    @abstractmethod
    async def complete_structured(
        self,
        *,
        messages: list[AIMessage],
        schema: dict[str, Any],
        operation: str,
    ) -> StructuredCompletion:
        raise NotImplementedError
