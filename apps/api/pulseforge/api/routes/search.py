from __future__ import annotations

from fastapi import APIRouter, Query

from pulseforge.api.deps import Repo

router = APIRouter(tags=["search"])


@router.get("/search")
def search(repo: Repo, q: str = Query(min_length=1, max_length=500)):
    return repo.search(q)
