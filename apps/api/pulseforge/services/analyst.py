from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Callable

from pulseforge.domain.models import AnalystAnswer, AnalystCitation
from pulseforge.services.demo_repository import DemoRepository, dt


@dataclass(frozen=True)
class AnalystTool:
    name: str
    description: str
    handler: Callable[..., object]


class StructuredAnalyst:
    """Mock/local analyst that demonstrates tool-grounded reasoning with provenance."""

    def __init__(self, repository: DemoRepository):
        self.repository = repository
        self.tools = {
            tool.name: tool
            for tool in [
                AnalystTool("search_events", "Search normalized events", repository.search),
                AnalystTool("search_entities", "Search resolved entities", repository.search),
                AnalystTool("query_graph", "Inspect time-valid graph relationships", repository.graph_at),
                AnalystTool("compare_time_ranges", "Compute a Temporal Graph Diff", repository.temporal_diff),
                AnalystTool("find_claims", "Search extracted source claims", repository.search),
                AnalystTool("find_conflicts", "Inspect unresolved contradictions", lambda: repository.contradictions),
                AnalystTool("calculate_velocity", "Inspect deterministic velocity signals", lambda: [s for s in repository.signals if s.signal_type == "velocity"]),
                AnalystTool("find_related_events", "Inspect event relationships", repository.get_event),
                AnalystTool("inspect_sources", "Inspect source metadata and evidence", lambda: repository.sources),
                AnalystTool("build_timeline", "Build a chronological event view", repository.list_events),
            ]
        }

    def answer(self, question: str) -> AnalystAnswer:
        q = question.casefold()
        if "nvidia" in q and any(term in q for term in ("why", "frequent", "velocity", "appearing", "increase")):
            signal = next(signal for signal in self.repository.signals if signal.id == "sig-nvidia-velocity")
            return AnalystAnswer(
                answer=(
                    "NVIDIA mention velocity is 5.7× its trailing same-hour baseline. Three normalized event clusters "
                    "— the accelerator platform, the Nebula Cloud partnership, and Helix-2 infrastructure testing — "
                    "account for 81% of the increase. This is an inference from deterministic signal and event state, "
                    "not a claim that the model independently established."
                ),
                tools_used=["calculate_velocity", "find_related_events", "inspect_sources"],
                citations=[
                    AnalystCitation(kind="signal", id=signal.id, label=signal.title),
                    AnalystCitation(kind="event", id="evt-nvidia-platform", label="Accelerator platform event"),
                    AnalystCitation(kind="event", id="evt-nebula-partnership", label="Nebula partnership event"),
                    AnalystCitation(kind="event", id="evt-helix", label="Helix-2 infrastructure event"),
                ],
                uncertainty="The velocity metric describes observed coverage, not business impact or future performance.",
            )
        if "changed" in q or "diff" in q:
            after = dt("2026-09-11T15:40:00Z")
            before = after - timedelta(days=1)
            diff = self.repository.temporal_diff(before, after)
            return AnalystAnswer(
                answer=(
                    f"In the last 24 hours PulseForge found {len(diff.added_relationships)} new graph relationships, "
                    f"{len(diff.introduced_contradiction_ids)} newly introduced contradiction, and an emerging "
                    "Inference Efficiency topic. NVIDIA and Inference Efficiency are the strongest accelerating entities."
                ),
                tools_used=["compare_time_ranges", "find_conflicts", "calculate_velocity"],
                citations=[
                    AnalystCitation(kind="relationship", id="rel-nvidia-nebula", label="NVIDIA ↔ Nebula Cloud"),
                    AnalystCitation(kind="claim", id="claim-forge-jan", label="ForgeLM 3 January claim"),
                    AnalystCitation(kind="signal", id="sig-efficiency-emergence", label="Inference efficiency emergence"),
                ],
            )
        if "conflict" in q or "contradiction" in q or "forgelm" in q:
            return AnalystAnswer(
                answer=(
                    "ForgeLM 3 has two incompatible launch-date claims: Orion AI's primary-source notice says October 2026, "
                    "while a newer ModelBeat report says January 2027. PulseForge leaves the contradiction unresolved because "
                    "the evidence does not justify silently choosing one."
                ),
                tools_used=["find_claims", "find_conflicts", "inspect_sources"],
                citations=[
                    AnalystCitation(kind="claim", id="claim-forge-oct", label="October 2026 claim"),
                    AnalystCitation(kind="claim", id="claim-forge-jan", label="January 2027 claim"),
                    AnalystCitation(kind="evidence", id="ev-orion-oct", label="Orion AI evidence"),
                    AnalystCitation(kind="evidence", id="ev-orion-jan", label="ModelBeat evidence"),
                ],
                uncertainty="A newer report is not automatically more reliable than a primary-source statement.",
            )
        return AnalystAnswer(
            answer=(
                "I found no dedicated deterministic rule for that question in mock mode. I can still inspect events, entities, "
                "claims, conflicts, graph state, velocity, related events, sources, and timelines without inventing facts."
            ),
            tools_used=["search_events", "search_entities"],
            citations=[], uncertainty="Connect a model provider for broader synthesis while keeping the same tool/provenance contract.",
        )
