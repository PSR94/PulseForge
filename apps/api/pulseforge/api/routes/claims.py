from __future__ import annotations

from fastapi import APIRouter

from pulseforge.api.deps import Repo

router = APIRouter(tags=["claims"])


@router.get("/claims")
def claims(repo: Repo):
    return repo.claims


@router.get("/claims/conflicts")
def conflicts(repo: Repo):
    return [
        {
            "contradiction": contradiction,
            "claims": [
                claim
                for claim_id in contradiction.claim_ids
                if (claim := repo.get_claim(claim_id)) is not None
            ],
        }
        for contradiction in repo.contradictions
    ]
