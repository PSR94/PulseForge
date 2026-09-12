export type EvidenceRef = {
  id: string;
  source_id: string;
  document_id: string;
  source_name: string;
  excerpt: string;
  published_at: string;
  retrieved_at: string;
  canonical_url: string;
  primary_source: boolean;
};

export type Event = {
  id: string;
  workspace_id: string;
  title: string;
  event_type: string;
  first_observed: string;
  latest_confirmation: string;
  entity_ids: string[];
  location?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  confidence: number;
  novelty_score: number;
  impact_score: number;
  source_count: number;
  related_event_ids: string[];
  claim_ids: string[];
  evidence: EvidenceRef[];
  explanation: string;
  cluster_reasons: string[];
  topics: string[];
};

export type Entity = {
  id: string;
  workspace_id: string;
  name: string;
  entity_type: string;
  aliases: string[];
  description: string;
  external_ids: Record<string, string>;
  importance: number;
  activity_velocity: number;
  first_seen: string;
  last_seen: string;
  locations: string[];
  topics: string[];
};

export type Relationship = {
  id: string;
  workspace_id: string;
  source_entity_id: string;
  relationship_type: string;
  target_entity_id: string;
  valid_from: string;
  valid_to?: string | null;
  source_count: number;
  confidence: number;
  evidence_ids: string[];
  strength: number;
};

export type Signal = {
  id: string;
  workspace_id: string;
  signal_type: string;
  title: string;
  detected_at: string;
  entity_ids: string[];
  event_ids: string[];
  confidence: number;
  severity: "low" | "medium" | "high" | "critical" | string;
  metrics: Record<string, string | number>;
  deterministic_basis: string;
  explanation: string;
  evidence_ids: string[];
};

export type GraphDiff = {
  from_at: string;
  to_at: string;
  added_entity_ids: string[];
  removed_entity_ids: string[];
  added_relationships: Relationship[];
  removed_relationships: Relationship[];
  changed_relationships: { relationship_id: string; before: number; after: number; delta: number }[];
  introduced_contradiction_ids: string[];
  accelerating_entity_ids: string[];
  declining_entity_ids: string[];
  emerging_topics: string[];
  summary: string;
};

export type Briefing = {
  id: string;
  workspace_id: string;
  title: string;
  generated_at: string;
  period_start: string;
  period_end: string;
  executive_summary: string;
  top_developments: string[];
  emerging_signals: string[];
  entity_movements: string[];
  contradictions: string[];
  watch_list: string[];
  evidence_ids: string[];
  markdown: string;
};

export type Source = {
  id: string;
  workspace_id: string;
  name: string;
  source_type: string;
  source_url: string;
  canonical_url: string;
  observations: {
    primary_source: boolean;
    publication_history_days: number;
    corroborating_source_count: number;
    direct_quote_count: number;
    independent_confirmation_count: number;
    contradiction_count: number;
  };
  metadata: Record<string, unknown>;
};
