import { Activity, AlertTriangle, Link2, Radar } from "lucide-react";
import { signals } from "@/lib/demo";

const iconMap: Record<string, typeof Radar> = {VELOCITY:Activity,"SOURCE DIVERGENCE":AlertTriangle,"NOVEL RELATIONSHIP":Link2};
export default function SignalsPage() {
  return <><div className="page-head"><div><h1>Signal center</h1><p>Deterministic measurements first; AI is allowed to explain the signal, never invent it.</p></div></div>
    <div className="card"><div className="panel-head"><h2>Active intelligence signals</h2><span>4 ACTIVE · 2 HIGH</span></div>{signals.map(signal=>{const Icon=iconMap[signal.kind]??Radar; return <div className="signal-card" key={signal.id}><div className="signal-icon"><Icon size={17}/></div><div><div className="chips" style={{marginTop:0,marginBottom:7}}><span className={`chip ${signal.severity==="HIGH"?"chip-red":"chip-cyan"}`}>{signal.kind}</span><span className="chip">{signal.severity}</span></div><h3>{signal.title}</h3><p>{signal.detail}</p><div className="card-sub" style={{marginTop:8}}>Basis stored with signal · evidence drill-down available</div></div><div className="metric">{signal.metric}<small>observed</small></div></div>})}</div>
  </>;
}
