import Link from "next/link";
import { ArrowUpRight, GitCompareArrows, Radar, ShieldAlert } from "lucide-react";
import { AnalystPanel } from "@/components/AnalystPanel";
import { events, signals } from "@/lib/demo";

export default function OverviewPage() {
  return <>
    <div className="page-head"><div><h1>Intelligence overview</h1><p>What materially changed since your last visit · Sep 10, 17:00 UTC → now</p></div><Link className="button-secondary" href="/app/graph#diff"><GitCompareArrows size={14}/> Compare periods</Link></div>
    <div className="grid-4">
      <div className="card card-pad"><div className="card-title">Normalized events · 24h</div><div className="card-value">18</div><div className="card-sub">6 high-impact · 42 source documents</div></div>
      <div className="card card-pad"><div className="card-title">Accelerating entity</div><div className="card-value metric-up">NVIDIA 5.7×</div><div className="card-sub">+470% vs trailing baseline</div></div>
      <div className="card card-pad"><div className="card-title">Graph change</div><div className="card-value">+4 edges</div><div className="card-sub">1 relationship discovery · 3 supporting sources+</div></div>
      <div className="card card-pad"><div className="card-title">Unresolved conflict</div><div className="card-value metric-warn">1</div><div className="card-sub">ForgeLM 3 launch date</div></div>
    </div>
    <div className="split" style={{marginTop:12}}>
      <div className="card"><div className="panel-head"><h2>Material changes</h2><span>NORMALIZED EVENTS</span></div>{events.slice(0,4).map(event=><Link className="event-row" key={event.id} href={`/app/events/${event.id}`} style={{gridTemplateColumns:"62px minmax(0,1fr) 90px"}}><div className="timestamp">{event.time}<br/>UTC</div><div><div className="event-title">{event.title}</div><div className="event-explain">{event.explanation}</div><div className="chips">{event.entities.map(entity=><span className="chip" key={entity}>{entity}</span>)}</div></div><div className="score"><strong>{Math.round(event.confidence*100)}%</strong>confidence<br/>{event.sourceCount} sources</div></Link>)}</div>
      <div className="card"><div className="panel-head"><h2>Signal center</h2><span>DETERMINISTIC</span></div>{signals.map(signal=><div className="signal-card" key={signal.id} style={{gridTemplateColumns:"34px 1fr auto"}}><div className="signal-icon"><Radar size={15}/></div><div><h3>{signal.title}</h3><p>{signal.detail}</p></div><div className="metric">{signal.metric}</div></div>)}</div>
    </div>
    <div style={{marginTop:12}}><AnalystPanel/></div>
    <div className="card" style={{marginTop:12}}><div className="panel-head"><h2>What changed? · Temporal Graph Diff</h2><span>24 HOURS</span></div><div className="diff-grid">
      <div className="diff-col"><h3>Added</h3><div className="diff-item diff-plus">+ NVIDIA PARTNERS_WITH Nebula Cloud</div><div className="diff-item diff-plus">+ Quartz ADVANCES Inference Efficiency</div><div className="diff-item diff-plus">+ Helix-2 infrastructure cluster</div></div>
      <div className="diff-col"><h3>Changed</h3><div className="diff-item diff-change">↑ NVIDIA activity velocity 5.7×</div><div className="diff-item diff-change">↑ Inference Efficiency cluster 3.8×</div><div className="diff-item diff-change">~ datacenter infrastructure importance</div></div>
      <div className="diff-col"><h3>Uncertainty</h3><div className="diff-item diff-warn">⚠ ForgeLM 3 launch contradiction introduced</div><div className="diff-item">Primary: October 2026</div><div className="diff-item">Secondary: January 2027</div></div>
    </div></div>
  </>;
}
