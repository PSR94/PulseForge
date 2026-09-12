import { api } from "@/lib/api";
import { EventCard } from "@/components/EventCard";
import { SignalCard } from "@/components/SignalCard";

export const dynamic="force-dynamic";

export default async function EntityPage({params}:{params:Promise<{id:string}>}){
  const {id}=await params;
  const dossier=await api.entity(id);
  const entity=dossier.entity;
  return <>
    <div className="page-head entity-hero"><div><div className="chips"><span className="chip">{entity.entity_type}</span>{entity.aliases.map((alias:string)=><span className="chip" key={alias}>{alias}</span>)}</div><h1>{entity.name}</h1><p>{entity.description}</p></div><div className="entity-stats"><div className="card card-pad"><div className="card-title">Importance</div><div className="card-value">{Math.round(entity.importance*100)}%</div></div><div className="card card-pad"><div className="card-title">Velocity</div><div className="card-value metric-up">{entity.activity_velocity.toFixed(1)}×</div></div></div></div>
    <div className="split">
      <div className="card"><div className="panel-head"><h2>Event history</h2><span>{dossier.events.length}</span></div>{dossier.events.map((event:any)=><EventCard key={event.id} event={event}/>)}</div>
      <div className="stack"><div className="card card-pad"><div className="card-title">Temporal relationships</div>{dossier.relationships.map((rel:any)=><div className="diff-item" key={rel.id}>{rel.source_entity_id} <strong>{rel.relationship_type}</strong> {rel.target_entity_id}<br/><small>{new Date(rel.valid_from).toLocaleString()} → {rel.valid_to?new Date(rel.valid_to).toLocaleString():"active"}</small></div>)}</div><div className="card"><div className="panel-head"><h2>Signals</h2><span>{dossier.signals.length}</span></div>{dossier.signals.map((signal:any)=><SignalCard key={signal.id} signal={signal}/>)}</div></div>
    </div>
    <div className="card card-pad" style={{marginTop:12}}><div className="card-title">Claims & contradictions</div><p>{dossier.claims.length} extracted claims · {dossier.contradictions.length} contradiction objects</p>{dossier.contradictions.map((c:any)=><div className="diff-item diff-warn" key={c.id}>⚠ {c.normalized_property}: {c.explanation}</div>)}</div>
  </>;
}
