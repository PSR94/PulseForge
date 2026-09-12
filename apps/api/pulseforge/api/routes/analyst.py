from __future__ import annotations

from fastapi import APIRouter

from pulseforge.api.deps import Repo
from pulseforge.domain.models import AnalystAnswer, AnalystQuestion
from pulseforge.services.analyst import StructuredAnalyst

router = APIRouter(tags=["analyst"])


@router.post("/analyst/ask", response_model=AnalystAnswer)
def ask_analyst(payload: AnalystQuestion, repo: Repo):
    return StructuredAnalyst(repo).answer(payload.question)


@router.get("/analyst/tools")
def analyst_tools(repo: Repo):
    analyst = StructuredAnalyst(repo)
    return [{"name": tool.name, "description": tool.description} for tool in analyst.tools.values()]
