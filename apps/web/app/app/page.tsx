import Link from "next/link";
import { GitCompareArrows } from "lucide-react";
import { api } from "@/lib/api";
import { AnalystPanel } from "@/components/AnalystPanel";
import { EventCard } from "@/components/EventCard";
import { SignalCard } from "@/components/SignalCard";
import { GraphDiffPanel } from "@/components/GraphDiffPanel";

export const dynamic="force-dynamic";

export default async function OverviewPage() {
  const [events,signals,entities,diff,conflicts]=await Promise.all([
    api.feed(),api.signals(),api.entities(),
    api.diff("2026-09-10T15:40:00Z","2026-09-11T15:40:00Z"),
    api.conflicts(),
  ]);
  const fastest=[...entities].sort((a,b)=>b.activity_velocity-a.activity_velocity)[0];
  return <>
    <div className="page-head"><div><h1>Intelligence overview</h1><p>Evidence-linked change detection across events, entities, claims, and temporal relationships.</p></div><Link className="button-secondary" href="/app/graph#diff"><GitCompareArrows size={14}/> Compare periods</Link></div>
    <div className="grid-4">
      <div className="card card-pad"><div className="card-title">Normalized events</div><div className="card-value">{events.length}</div><div className="card-sub">{events.reduce((n,e)=>n+e.source_count,0)} corroborating source references</div></div>
      <div className="card card-pad"><div className="card-title">Accelerating entity</div><div className="card-value metric-up">{fastest?.name??"—"} {fastest?.activity_velocity.toFixed(1)??"0"}×</div><div className="card-sub">Compared with trailing baseline</div></div>
      <div className="card card-pad"><div className="card-title">Graph additions</div><div className="card-value">+{diff.added_relationships.length}</div><div className="card-sub">{diff.added_entity_ids.length} newly active entities</div></div>
      <div className="card card-pad"><div className="card-title">Unresolved conflicts</div><div className="card-value metric-warn">{conflicts.length}</div><div className="card-sub">Claims preserved rather than silently resolved</div></div>
    </div>
    <div className="split" style={{marginTop:12}}>
      <div className="card"><div className="panel-head"><h2>Material changes</h2><span>NORMALIZED EVENTS</span></div>{events.slice(0,5).map(event=><EventCard event={event} key={event.id}/>)}</div>
      <div className="card"><div className="panel-head"><h2>Signal center</h2><span>DETERMINISTIC INPUTS</span></div>{signals.slice(0,5).map(signal=><SignalCard signal={signal} key={signal.id}/>)}</div>
    </div>
    <div style={{marginTop:12}}><AnalystPanel/></div>
    <div style={{marginTop:12}}><GraphDiffPanel diff={diff} entities={entities}/></div>
  </>;
}
