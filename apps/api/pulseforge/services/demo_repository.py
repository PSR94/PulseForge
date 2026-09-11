from __future__ import annotations

from datetime import UTC, datetime
from functools import lru_cache

from pulseforge.domain.models import (
    Briefing,
    Claim,
    ClaimKind,
    Contradiction,
    Entity,
    EntityType,
    Event,
    EvidenceRef,
    GraphSnapshot,
    Signal,
    SignalType,
    Source,
    SourceObservations,
    SourceType,
    TemporalRelationship,
    Workspace,
)
from pulseforge.services.graph_diff import diff_snapshots


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


class DemoRepository:
    """Deterministic repository powering the zero-config product demo and tests."""

    workspace_id = "ai-industry"

    def __init__(self) -> None:
        self.workspace = Workspace(
            id=self.workspace_id,
            name="AI Industry Intelligence",
            description="Live intelligence across models, chips, cloud, research, and open-source AI.",
            updated_at=dt("2026-09-11T15:40:00Z"),
            last_visited_at=dt("2026-09-10T17:00:00Z"),
        )
        self.sources = self._sources()
        self.entities = self._entities()
        self.evidence = self._evidence()
        self.claims = self._claims()
        self.events = self._events()
        self.relationships = self._relationships()
        self.contradictions = self._contradictions()
        self.signals = self._signals()

    def _sources(self) -> list[Source]:
        rows = [
            ("src-orion", "Orion AI Newsroom", "https://example.com/orion" , True),
            ("src-nebula", "Nebula Cloud Newsroom", "https://example.com/nebula", True),
            ("src-chipwire", "ChipWire", "https://example.com/chipwire", False),
            ("src-modelbeat", "ModelBeat", "https://example.com/modelbeat", False),
            ("src-research", "Research Dispatch", "https://example.com/research", False),
            ("src-oss", "Open Source Ledger", "https://example.com/oss", False),
        ]
        return [
            Source(
                id=source_id,
                workspace_id=self.workspace_id,
                name=name,
                source_type=SourceType.RSS,
                source_url=url,
                canonical_url=url,
                observations=SourceObservations(
                    primary_source=primary,
                    publication_history_days=900 if primary else 1300,
                    independent_confirmation_count=4 if primary else 11,
                    contradiction_count=0 if primary else 1,
                ),
            )
            for source_id, name, url, primary in rows
        ]

    def _entities(self) -> list[Entity]:
        return [
            Entity(
                id="ent-nvidia", workspace_id=self.workspace_id, name="NVIDIA",
                entity_type=EntityType.COMPANY, aliases=["NVIDIA Corp.", "NVDA"],
                description="Semiconductor and accelerated-computing company.", importance=0.98,
                activity_velocity=5.7, first_seen=dt("2026-07-01T00:00:00Z"),
                last_seen=dt("2026-09-11T15:34:00Z"), locations=["Santa Clara, US"],
                topics=["AI chips", "datacenter infrastructure"],
            ),
            Entity(
                id="ent-nebula", workspace_id=self.workspace_id, name="Nebula Cloud",
                entity_type=EntityType.COMPANY, aliases=["Nebula"],
                description="Synthetic public-safe cloud provider used in the deterministic demo.",
                importance=0.79, activity_velocity=3.2, first_seen=dt("2026-07-07T00:00:00Z"),
                last_seen=dt("2026-09-11T14:18:00Z"), locations=["Ashburn, US", "Frankfurt, DE"],
                topics=["cloud", "AI infrastructure"],
            ),
            Entity(
                id="ent-orion", workspace_id=self.workspace_id, name="Orion AI",
                entity_type=EntityType.COMPANY, aliases=["Orion"],
                description="Synthetic public-safe model developer used in the deterministic demo.",
                importance=0.84, activity_velocity=2.6, first_seen=dt("2026-06-20T00:00:00Z"),
                last_seen=dt("2026-09-11T13:05:00Z"), locations=["San Francisco, US"],
                topics=["foundation models", "agents"],
            ),
            Entity(
                id="ent-forge", workspace_id=self.workspace_id, name="ForgeLM 3",
                entity_type=EntityType.PRODUCT, aliases=["ForgeLM"],
                description="Synthetic model release tracked by the demo workspace.", importance=0.74,
                activity_velocity=4.1, first_seen=dt("2026-09-02T00:00:00Z"),
                last_seen=dt("2026-09-11T13:05:00Z"), topics=["open weights", "inference"],
            ),
            Entity(
                id="ent-quartz", workspace_id=self.workspace_id, name="Quartz Runtime",
                entity_type=EntityType.PROJECT, aliases=["Quartz"],
                description="Synthetic open-source inference runtime.", importance=0.67,
                activity_velocity=3.8, first_seen=dt("2026-08-09T00:00:00Z"),
                last_seen=dt("2026-09-11T12:10:00Z"), topics=["open source", "inference efficiency"],
            ),
            Entity(
                id="ent-helix", workspace_id=self.workspace_id, name="Helix-2 Interconnect",
                entity_type=EntityType.TECHNOLOGY, aliases=["Helix-2"],
                description="Synthetic high-bandwidth datacenter interconnect technology.", importance=0.61,
                activity_velocity=2.0, first_seen=dt("2026-08-18T00:00:00Z"),
                last_seen=dt("2026-09-11T10:45:00Z"), topics=["networking", "datacenter infrastructure"],
            ),
            Entity(
                id="ent-efficiency", workspace_id=self.workspace_id, name="Inference Efficiency",
                entity_type=EntityType.TOPIC, aliases=["efficient inference"],
                description="Emerging topic cluster around lower-cost, higher-throughput inference.", importance=0.7,
                activity_velocity=3.8, first_seen=dt("2026-09-08T00:00:00Z"),
                last_seen=dt("2026-09-11T15:00:00Z"), topics=["inference efficiency"],
            ),
        ]

    def _evidence(self) -> list[EvidenceRef]:
        rows = [
            ("ev-nv-1", "src-chipwire", "ChipWire", "NVIDIA disclosed a new accelerator platform optimized for large-scale inference deployments.", "2026-09-11T09:12:00Z", False),
            ("ev-nv-2", "src-nebula", "Nebula Cloud Newsroom", "Nebula Cloud will make the new NVIDIA platform available in two regions this quarter.", "2026-09-11T10:47:00Z", True),
            ("ev-partner", "src-nebula", "Nebula Cloud Newsroom", "Nebula Cloud and NVIDIA announced a multi-year infrastructure partnership spanning accelerated compute and Helix-2 networking.", "2026-09-11T11:35:00Z", True),
            ("ev-orion-oct", "src-orion", "Orion AI Newsroom", "Orion AI said ForgeLM 3 is scheduled for general availability in October 2026.", "2026-09-10T16:00:00Z", True),
            ("ev-orion-jan", "src-modelbeat", "ModelBeat", "People familiar with the rollout said broad ForgeLM 3 availability has moved to January 2027.", "2026-09-11T13:05:00Z", False),
            ("ev-quartz", "src-oss", "Open Source Ledger", "Quartz Runtime contributors reported a 38% throughput gain on long-context inference workloads.", "2026-09-11T12:10:00Z", False),
            ("ev-paper", "src-research", "Research Dispatch", "A new systems paper reports reduced KV-cache pressure using adaptive sparsity during inference.", "2026-09-11T08:20:00Z", False),
            ("ev-helix", "src-chipwire", "ChipWire", "Cloud operators are testing Helix-2 interconnects to reduce congestion in dense accelerator clusters.", "2026-09-11T10:45:00Z", False),
        ]
        return [
            EvidenceRef(
                id=eid,
                source_id=sid,
                document_id=f"doc-{eid}",
                source_name=sname,
                excerpt=excerpt,
                published_at=dt(published),
                retrieved_at=dt(published) if primary else dt(published),
                canonical_url=f"https://example.com/evidence/{eid}",
                primary_source=primary,
            )
            for eid, sid, sname, excerpt, published, primary in rows
        ]

    def _e(self, evidence_id: str) -> EvidenceRef:
        return next(item for item in self.evidence if item.id == evidence_id)

    def _claims(self) -> list[Claim]:
        return [
            Claim(
                id="claim-forge-oct", workspace_id=self.workspace_id, subject_entity_id="ent-forge",
                predicate="will launch", object_value="October 2026", normalized_property="launch_date",
                kind=ClaimKind.FACTUAL, extraction_confidence=0.96, observed_at=dt("2026-09-10T16:00:00Z"),
                evidence=[self._e("ev-orion-oct")],
            ),
            Claim(
                id="claim-forge-jan", workspace_id=self.workspace_id, subject_entity_id="ent-forge",
                predicate="will launch", object_value="January 2027", normalized_property="launch_date",
                kind=ClaimKind.FACTUAL, extraction_confidence=0.87, observed_at=dt("2026-09-11T13:05:00Z"),
                evidence=[self._e("ev-orion-jan")],
            ),
            Claim(
                id="claim-nebula-nvidia", workspace_id=self.workspace_id, subject_entity_id="ent-nebula",
                predicate="partners_with", object_value="NVIDIA", normalized_property="strategic_partner",
                extraction_confidence=0.98, observed_at=dt("2026-09-11T11:35:00Z"),
                evidence=[self._e("ev-partner")],
            ),
            Claim(
                id="claim-quartz-gain", workspace_id=self.workspace_id, subject_entity_id="ent-quartz",
                predicate="reported throughput gain", object_value="38%", normalized_property="throughput_gain",
                extraction_confidence=0.91, observed_at=dt("2026-09-11T12:10:00Z"),
                evidence=[self._e("ev-quartz")],
            ),
        ]

    def _events(self) -> list[Event]:
        return [
            Event(
                id="evt-nvidia-platform", workspace_id=self.workspace_id,
                title="NVIDIA introduces inference-focused accelerator platform", event_type="product_announcement",
                first_observed=dt("2026-09-11T09:12:00Z"), latest_confirmation=dt("2026-09-11T10:47:00Z"),
                entity_ids=["ent-nvidia", "ent-nebula"], location="Santa Clara, US", latitude=37.3541, longitude=-121.9552,
                confidence=0.96, novelty_score=0.91, impact_score=0.94, source_count=5,
                related_event_ids=["evt-nebula-partnership", "evt-helix"], evidence=[self._e("ev-nv-1"), self._e("ev-nv-2")],
                explanation="Five reports converge on one underlying accelerator-platform announcement; Nebula Cloud independently confirms deployment plans.",
                cluster_reasons=["shared entity: NVIDIA", "semantic similarity 0.92", "publication window 95 minutes", "same event type"],
                topics=["AI chips", "inference efficiency"],
            ),
            Event(
                id="evt-nebula-partnership", workspace_id=self.workspace_id,
                title="Nebula Cloud expands strategic infrastructure partnership with NVIDIA", event_type="partnership",
                first_observed=dt("2026-09-11T11:35:00Z"), latest_confirmation=dt("2026-09-11T14:18:00Z"),
                entity_ids=["ent-nebula", "ent-nvidia", "ent-helix"], location="Ashburn, US", latitude=39.0438, longitude=-77.4874,
                confidence=0.94, novelty_score=0.88, impact_score=0.86, source_count=4,
                related_event_ids=["evt-nvidia-platform", "evt-helix"], claim_ids=["claim-nebula-nvidia"], evidence=[self._e("ev-partner")],
                explanation="A primary-source announcement establishes a new multi-year infrastructure relationship; three secondary sources report the same scope.",
                cluster_reasons=["shared entities: Nebula Cloud + NVIDIA", "same partnership announcement", "temporal proximity"],
                topics=["cloud", "datacenter infrastructure"],
            ),
            Event(
                id="evt-forgelm-schedule", workspace_id=self.workspace_id,
                title="ForgeLM 3 launch timing becomes disputed", event_type="schedule_change",
                first_observed=dt("2026-09-10T16:00:00Z"), latest_confirmation=dt("2026-09-11T13:05:00Z"),
                entity_ids=["ent-orion", "ent-forge"], location="San Francisco, US", latitude=37.7749, longitude=-122.4194,
                confidence=0.83, novelty_score=0.77, impact_score=0.81, source_count=2,
                claim_ids=["claim-forge-oct", "claim-forge-jan"], evidence=[self._e("ev-orion-oct"), self._e("ev-orion-jan")],
                explanation="PulseForge does not choose between incompatible October and January launch claims; it exposes the contradiction and source context.",
                cluster_reasons=["same subject: ForgeLM 3", "same property: launch date", "incompatible values"], topics=["foundation models"],
            ),
            Event(
                id="evt-quartz", workspace_id=self.workspace_id,
                title="Quartz Runtime reports 38% long-context inference throughput gain", event_type="open_source_release",
                first_observed=dt("2026-09-11T12:10:00Z"), latest_confirmation=dt("2026-09-11T15:00:00Z"),
                entity_ids=["ent-quartz", "ent-efficiency"], confidence=0.88, novelty_score=0.84, impact_score=0.72, source_count=3,
                claim_ids=["claim-quartz-gain"], evidence=[self._e("ev-quartz")],
                explanation="An open-source runtime result joins multiple independent developments around inference efficiency.",
                cluster_reasons=["shared topic: inference efficiency", "benchmark value repeated across coverage"], topics=["open source", "inference efficiency"],
            ),
            Event(
                id="evt-research", workspace_id=self.workspace_id,
                title="Adaptive sparsity research targets lower inference memory pressure", event_type="research_publication",
                first_observed=dt("2026-09-11T08:20:00Z"), latest_confirmation=dt("2026-09-11T08:20:00Z"),
                entity_ids=["ent-efficiency"], confidence=0.9, novelty_score=0.79, impact_score=0.64, source_count=1,
                evidence=[self._e("ev-paper")], explanation="A systems paper contributes a distinct mechanism to the emerging inference-efficiency cluster.",
                cluster_reasons=["topic embedding joins inference-efficiency cluster"], topics=["research", "inference efficiency"],
            ),
            Event(
                id="evt-helix", workspace_id=self.workspace_id,
                title="Cloud operators test Helix-2 networking for dense accelerator clusters", event_type="infrastructure_test",
                first_observed=dt("2026-09-11T10:45:00Z"), latest_confirmation=dt("2026-09-11T12:30:00Z"),
                entity_ids=["ent-helix", "ent-nvidia", "ent-nebula"], location="Frankfurt, DE", latitude=50.1109, longitude=8.6821,
                confidence=0.82, novelty_score=0.73, impact_score=0.69, source_count=2,
                related_event_ids=["evt-nebula-partnership"], evidence=[self._e("ev-helix")],
                explanation="Infrastructure testing links networking capacity to the same accelerator expansion appearing in cloud and chip events.",
                cluster_reasons=["shared infrastructure entities", "same 6-hour escalation window"], topics=["networking", "datacenter infrastructure"],
            ),
        ]

    def _relationships(self) -> list[TemporalRelationship]:
        return [
            TemporalRelationship(
                id="rel-nvidia-nebula", workspace_id=self.workspace_id, source_entity_id="ent-nvidia",
                relationship_type="PARTNERS_WITH", target_entity_id="ent-nebula", valid_from=dt("2026-09-11T11:35:00Z"),
                source_count=4, confidence=0.94, evidence_ids=["ev-partner"], strength=0.91,
            ),
            TemporalRelationship(
                id="rel-nebula-helix", workspace_id=self.workspace_id, source_entity_id="ent-nebula",
                relationship_type="TESTS", target_entity_id="ent-helix", valid_from=dt("2026-09-11T10:45:00Z"),
                source_count=2, confidence=0.82, evidence_ids=["ev-helix"], strength=0.72,
            ),
            TemporalRelationship(
                id="rel-orion-forge", workspace_id=self.workspace_id, source_entity_id="ent-orion",
                relationship_type="DEVELOPS", target_entity_id="ent-forge", valid_from=dt("2026-09-02T00:00:00Z"),
                source_count=8, confidence=0.99, evidence_ids=["ev-orion-oct"], strength=0.98,
            ),
            TemporalRelationship(
                id="rel-quartz-efficiency", workspace_id=self.workspace_id, source_entity_id="ent-quartz",
                relationship_type="ADVANCES", target_entity_id="ent-efficiency", valid_from=dt("2026-09-11T12:10:00Z"),
                source_count=3, confidence=0.88, evidence_ids=["ev-quartz"], strength=0.84,
            ),
            TemporalRelationship(
                id="rel-nvidia-helix", workspace_id=self.workspace_id, source_entity_id="ent-nvidia",
                relationship_type="USES_INTERCONNECT", target_entity_id="ent-helix", valid_from=dt("2026-09-11T09:12:00Z"),
                source_count=3, confidence=0.86, evidence_ids=["ev-nv-1", "ev-helix"], strength=0.77,
            ),
        ]

    def _contradictions(self) -> list[Contradiction]:
        return [
            Contradiction(
                id="con-forge-launch", workspace_id=self.workspace_id, subject_entity_id="ent-forge",
                normalized_property="launch_date", claim_ids=["claim-forge-oct", "claim-forge-jan"],
                explanation="A primary source says October 2026 while a newer secondary report says January 2027. The conflict is unresolved.",
            )
        ]

    def _signals(self) -> list[Signal]:
        return [
            Signal(
                id="sig-nvidia-velocity", workspace_id=self.workspace_id, signal_type=SignalType.VELOCITY,
                title="NVIDIA activity velocity increased 5.7×", detected_at=dt("2026-09-11T15:30:00Z"),
                entity_ids=["ent-nvidia"], event_ids=["evt-nvidia-platform", "evt-nebula-partnership", "evt-helix"],
                confidence=0.97, severity="high",
                metrics={"baseline_mentions_per_hour": 4.2, "current_mentions_per_hour": 23.9, "velocity_ratio": 5.7, "driver_share": 0.81},
                deterministic_basis="6-hour mention rate divided by the trailing 7-day same-hour baseline; event clusters account for 81% of the increase.",
                explanation="The spike is concentrated in three distinct event clusters rather than repeated copies of one article.",
                evidence_ids=["ev-nv-1", "ev-nv-2", "ev-partner", "ev-helix"],
            ),
            Signal(
                id="sig-efficiency-emergence", workspace_id=self.workspace_id, signal_type=SignalType.TOPIC_EMERGENCE,
                title="Inference efficiency emerges as a cross-domain topic", detected_at=dt("2026-09-11T15:10:00Z"),
                entity_ids=["ent-efficiency", "ent-quartz", "ent-nvidia"], event_ids=["evt-quartz", "evt-research", "evt-nvidia-platform"],
                confidence=0.9, severity="medium",
                metrics={"cluster_growth_ratio": 3.8, "independent_domains": 3, "event_count_24h": 4},
                deterministic_basis="Embedding cluster size rose 3.8× week-over-week and now spans research, open-source runtime, and hardware events.",
                explanation="Independent activity in hardware, systems research, and open-source software is converging on lower-cost inference.",
                evidence_ids=["ev-quartz", "ev-paper", "ev-nv-1"],
            ),
            Signal(
                id="sig-novel-relationship", workspace_id=self.workspace_id, signal_type=SignalType.NOVEL_RELATIONSHIP,
                title="New NVIDIA ↔ Nebula Cloud relationship appears", detected_at=dt("2026-09-11T11:40:00Z"),
                entity_ids=["ent-nvidia", "ent-nebula"], event_ids=["evt-nebula-partnership"], confidence=0.94, severity="medium",
                metrics={"prior_cooccurrence_30d": 1, "current_source_count": 4, "relationship_strength": 0.91},
                deterministic_basis="No active PARTNERS_WITH edge existed before 11:35 UTC; four sources now support the relationship.",
                explanation="The relationship is new in the temporal graph, not merely a rise in co-mentions.", evidence_ids=["ev-partner"],
            ),
            Signal(
                id="sig-source-divergence", workspace_id=self.workspace_id, signal_type=SignalType.SOURCE_DIVERGENCE,
                title="ForgeLM 3 launch timing is materially disputed", detected_at=dt("2026-09-11T13:06:00Z"),
                entity_ids=["ent-forge", "ent-orion"], event_ids=["evt-forgelm-schedule"], confidence=0.86, severity="high",
                metrics={"conflicting_claims": 2, "primary_sources": 1, "secondary_sources": 1},
                deterministic_basis="Two claims share subject and normalized property but have incompatible normalized date values.",
                explanation="PulseForge preserves both claims instead of selecting a winner.", evidence_ids=["ev-orion-oct", "ev-orion-jan"],
            ),
        ]

    def list_events(self) -> list[Event]:
        return sorted(self.events, key=lambda event: event.latest_confirmation, reverse=True)

    def get_event(self, event_id: str) -> Event | None:
        return next((event for event in self.events if event.id == event_id), None)

    def get_entity(self, entity_id: str) -> Entity | None:
        return next((entity for entity in self.entities if entity.id == entity_id), None)

    def get_claim(self, claim_id: str) -> Claim | None:
        return next((claim for claim in self.claims if claim.id == claim_id), None)

    def graph_at(self, at: datetime) -> GraphSnapshot:
        active = [
            relationship for relationship in self.relationships
            if relationship.valid_from <= at and (relationship.valid_to is None or relationship.valid_to > at)
        ]
        entity_ids = sorted({item.source_entity_id for item in active} | {item.target_entity_id for item in active})
        return GraphSnapshot(at=at, entity_ids=entity_ids, relationships=active)

    def temporal_diff(self, before: datetime, after: datetime):
        contradiction_ids = ["con-forge-launch"] if before < dt("2026-09-11T13:05:00Z") <= after else []
        return diff_snapshots(
            self.graph_at(before), self.graph_at(after),
            introduced_contradiction_ids=contradiction_ids,
            accelerating_entity_ids=["ent-nvidia", "ent-efficiency"] if after >= dt("2026-09-11T12:00:00Z") else [],
            emerging_topics=["Inference Efficiency"] if before < dt("2026-09-11T08:00:00Z") <= after else [],
        )

    def search(self, query: str) -> dict[str, list]:
        needle = query.casefold().strip()
        return {
            "entities": [entity for entity in self.entities if needle in entity.name.casefold() or any(needle in alias.casefold() for alias in entity.aliases)],
            "events": [event for event in self.events if needle in event.title.casefold() or any(needle in topic.casefold() for topic in event.topics)],
            "claims": [claim for claim in self.claims if needle in claim.object_value.casefold() or needle in claim.predicate.casefold()],
            "signals": [signal for signal in self.signals if needle in signal.title.casefold()],
        }

    def build_briefing(self) -> Briefing:
        markdown = """# 24-Hour AI Industry Brief\n\n## Executive summary\nAI infrastructure activity accelerated, led by NVIDIA-related hardware and cloud events, while inference efficiency emerged across hardware, research, and open-source software. ForgeLM 3 timing remains unresolved.\n\n## Top developments\n1. NVIDIA introduced an inference-focused accelerator platform with five-source convergence.\n2. Nebula Cloud and NVIDIA established a new multi-year infrastructure relationship.\n3. Quartz Runtime reported a 38% throughput gain on long-context inference.\n\n## Contradictions / uncertainty\nForgeLM 3 has incompatible October 2026 and January 2027 launch claims. PulseForge has not resolved the conflict.\n\n## Watch list\n- Additional primary-source confirmation of ForgeLM 3 timing\n- Expansion of the inference-efficiency event cluster\n- Deployment evidence for the Nebula Cloud / NVIDIA partnership\n"""
        return Briefing(
            id="brief-24h", workspace_id=self.workspace_id, title="24-Hour AI Industry Brief",
            generated_at=dt("2026-09-11T15:40:00Z"), period_start=dt("2026-09-10T15:40:00Z"), period_end=dt("2026-09-11T15:40:00Z"),
            executive_summary="AI infrastructure activity accelerated while inference efficiency emerged across three domains; one model-launch contradiction remains unresolved.",
            top_developments=["NVIDIA accelerator platform", "Nebula Cloud partnership", "Quartz Runtime throughput gain"],
            emerging_signals=["NVIDIA velocity 5.7×", "Inference efficiency cluster growth 3.8×"],
            entity_movements=["NVIDIA activity +470% vs baseline", "Inference Efficiency importance rising"],
            contradictions=["ForgeLM 3 launch date: October 2026 vs January 2027"],
            watch_list=["ForgeLM 3 primary-source update", "Nebula/NVIDIA deployment evidence", "Inference efficiency cluster growth"],
            evidence_ids=["ev-nv-1", "ev-nv-2", "ev-partner", "ev-orion-oct", "ev-orion-jan", "ev-quartz"], markdown=markdown,
        )


@lru_cache
def get_demo_repository() -> DemoRepository:
    return DemoRepository()
