import type { EvidenceRef } from "@/lib/types";

export function EvidencePanel({ evidence }: { evidence: EvidenceRef[] }) {
  return (
    <section className="card">
      <div className="panel-head">
        <h2>Evidence explorer</h2>
        <span>{evidence.length} EXCERPTS</span>
      </div>
      <div className="evidence-list">
        {evidence.map((item) => (
          <article className="evidence-card" key={item.id}>
            <div className="evidence-meta">
              <strong>{item.source_name}</strong>
              <span>{item.primary_source ? "PRIMARY" : "SECONDARY"}</span>
              <span>published {new Date(item.published_at).toLocaleString()}</span>
              <span>retrieved {new Date(item.retrieved_at).toLocaleString()}</span>
            </div>
            <blockquote>{item.excerpt}</blockquote>
            <a href={item.canonical_url} target="_blank" rel="noreferrer">
              Open original source ↗
            </a>
          </article>
        ))}
      </div>
    </section>
  );
}
