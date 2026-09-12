import type { Briefing, Entity, Event, GraphDiff, Relationship, Signal, Source } from "@/lib/types";

export const publicBase = process.env.NEXT_PUBLIC_PULSEFORGE_API_URL || "http://127.0.0.1:8000";
const serverBase = process.env.PULSEFORGE_SERVER_API_URL || publicBase;

async function get<T>(path: string): Promise<T> {
  const response = await fetch(`${serverBase}${path}`, {
    cache: "no-store",
    headers: { "X-Workspace-ID": "ai-industry" },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`PulseForge API ${response.status}: ${detail}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  feed: () => get<Event[]>("/api/v1/feed?limit=100"),
  event: (id: string) => get<Event>(`/api/v1/events/${encodeURIComponent(id)}`),
  eventEvidence: (id: string) =>
    get<{
      event_id: string;
      claims: unknown[];
      evidence: Event["evidence"];
      source_count: number;
      cluster_reasons: string[];
    }>(`/api/v1/events/${encodeURIComponent(id)}/evidence`),
  entities: () => get<Entity[]>("/api/v1/entities"),
  entity: (id: string) =>
    get<{
      entity: Entity;
      events: Event[];
      relationships: Relationship[];
      claims: unknown[];
      contradictions: unknown[];
      signals: Signal[];
    }>(`/api/v1/entities/${encodeURIComponent(id)}`),
  signals: () => get<Signal[]>("/api/v1/signals"),
  graph: () =>
    get<{
      snapshot: { at: string; entity_ids: string[]; relationships: Relationship[] };
      entities: Entity[];
    }>("/api/v1/graph?at=2026-09-11T15%3A40%3A00Z"),
  diff: (from: string, to: string) =>
    get<GraphDiff>(
      `/api/v1/graph/diff?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`,
    ),
  conflicts: () => get<unknown[]>("/api/v1/claims/conflicts"),
  sources: () => get<Source[]>("/api/v1/sources"),
  briefings: () => get<Briefing[]>("/api/v1/briefings"),
  watchlists: () => get<unknown[]>("/api/v1/watchlists?workspace_id=ai-industry"),
  alerts: () => get<unknown[]>("/api/v1/alerts?workspace_id=ai-industry"),
  capabilities: () =>
    get<{
      demo_mode: boolean;
      repository_mode: string;
      ai_provider: string;
      auth_mode: string;
      features: Record<string, boolean>;
    }>("/api/v1/capabilities"),
};
