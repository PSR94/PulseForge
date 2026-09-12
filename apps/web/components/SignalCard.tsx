import { Radar } from "lucide-react";
import type { Signal } from "@/lib/types";

export function SignalCard({ signal }: { signal: Signal }) {
  const metric =
    signal.metrics.multiplier != null
      ? `${signal.metrics.multiplier}×`
      : signal.metrics.current_source_count ??
        signal.metrics.conflicting_claims ??
        signal.severity;

  return (
    <div className="signal-card" style={{ gridTemplateColumns: "34px 1fr auto" }}>
      <div className="signal-icon">
        <Radar size={15} />
      </div>
      <div>
        <div className="chips">
          <span className={`status-pill ${signal.severity}`}>{signal.signal_type}</span>
          <span className="chip">{Math.round(signal.confidence * 100)}%</span>
        </div>
        <h3>{signal.title}</h3>
        <p>{signal.explanation}</p>
        <p className="card-sub">Basis: {signal.deterministic_basis}</p>
      </div>
      <div className="metric">{String(metric)}</div>
    </div>
  );
}
