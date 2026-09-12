from __future__ import annotations

from dataclasses import dataclass

from pulseforge.domain.models import SourceObservations


@dataclass(frozen=True, slots=True)
class ReliabilityProfile:
    primary_source: bool
    corroborating_sources: int
    independent_confirmations: int
    direct_quotes: int
    contradiction_count: int
    publication_history_days: int

    @property
    def corroboration_ratio(self) -> float:
        denominator = max(1, self.corroborating_sources + self.contradiction_count)
        return self.corroborating_sources / denominator


def profile(observations: SourceObservations) -> ReliabilityProfile:
    """Expose observable reliability dimensions without collapsing them into a truth score."""
    return ReliabilityProfile(
        primary_source=observations.primary_source,
        corroborating_sources=observations.corroborating_source_count,
        independent_confirmations=observations.independent_confirmation_count,
        direct_quotes=observations.direct_quote_count,
        contradiction_count=observations.contradiction_count,
        publication_history_days=observations.publication_history_days,
    )
