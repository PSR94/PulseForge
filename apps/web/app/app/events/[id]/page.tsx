import Link from "next/link";
import { api } from "@/lib/api";
import { EvidencePanel } from "@/components/EvidencePanel";

export const dynamic="force-dynamic";

export default async function EventPage({params}:{params:Promise<{id:string}>}){
  const {id}=await params;
  const [event,evidence]=await Promise.all([api.event(id),api.eventEvidence(id)]);
  return <>
    <div className="page-head"><div><div className="chips"><span className="chip">{event.event_type}</span><span className="chip">{Math.round(event.confidence*100)}% confidence</span><span className="chip">{event.source_count} sources</span></div><h1>{event.title}</h1><p>{event.explanation}</p></div></div>
    <div className="grid-4">
      <div className="card card-pad kpi"><div className="card-title">First observed</div><div className="card-sub">{new Date(event.first_observed).toLocaleString()}</div></div>
      <div className="card card-pad kpi"><div className="card-title">Novelty</div><div className="card-value">{Math.round(event.novelty_score*100)}%</div></div>
      <div className="card card-pad kpi"><div className="card-title">Impact</div><div className="card-value">{Math.round(event.impact_score*100)}%</div></div>
      <div className="card card-pad kpi"><div className="card-title">Evidence</div><div className="card-value">{event.evidence.length}</div></div>
    </div>
    <div className="split" style={{marginTop:12}}>
      <div className="card card-pad"><div className="card-title">Why these sources were clustered</div><ul>{evidence.cluster_reasons.map(reason=><li key={reason}>{reason}</li>)}</ul><div className="card-title">Topics</div><div className="chips">{event.topics.map(topic=><span className="chip" key={topic}>{topic}</span>)}</div></div>
      <div className="card card-pad"><div className="card-title">Provenance chain</div><div className="provenance-chain"><span>AI insight</span>→<span>claims</span>→<span>event</span>→<span>source excerpts</span>→<span>original source</span></div><p className="card-sub">PulseForge stores inference separately from evidence. Confidence is not a truth score.</p></div>
    </div>
    <div style={{marginTop:12}}><EvidencePanel evidence={event.evidence}/></div>
    {event.related_event_ids.length>0&&<div className="card card-pad" style={{marginTop:12}}><div className="card-title">Related event IDs</div>{event.related_event_ids.map(rel=><Link key={rel} href={`/app/events/${rel}`}>{rel}</Link>)}</div>}
  </>;
}
