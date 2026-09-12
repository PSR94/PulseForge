from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, Response

from pulseforge.api.deps import Repo
from pulseforge.domain.models import Briefing
from pulseforge.services.briefing_export import briefing_to_html, briefing_to_pdf

router = APIRouter(tags=["briefings"])


@router.get("/briefings", response_model=list[Briefing])
def briefings(repo: Repo):
    return [repo.build_briefing()]


@router.post("/briefings/generate", response_model=Briefing)
def generate_briefing(repo: Repo):
    return repo.build_briefing()


def _briefing(briefing_id: str, repo):
    briefing = repo.build_briefing()
    if briefing.id != briefing_id:
        raise HTTPException(status_code=404, detail="Briefing not found")
    return briefing


@router.get("/briefings/{briefing_id}/markdown", response_class=PlainTextResponse)
def briefing_markdown(briefing_id: str, repo: Repo):
    return _briefing(briefing_id, repo).markdown


@router.get("/briefings/{briefing_id}/html", response_class=HTMLResponse)
def briefing_html(briefing_id: str, repo: Repo):
    return briefing_to_html(_briefing(briefing_id, repo))


@router.get("/briefings/{briefing_id}/pdf")
def briefing_pdf(briefing_id: str, repo: Repo):
    briefing = _briefing(briefing_id, repo)
    return Response(
        briefing_to_pdf(briefing),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{briefing.id}.pdf"'},
    )
