import Link from "next/link";
import { Filter, Radio } from "lucide-react";
import { events } from "@/lib/demo";

export default function FeedPage() {
  return <><div className="page-head"><div><h1>Live intelligence feed</h1><p>Articles converge into normalized events with inspectable evidence and clustering rationale.</p></div><button className="button-secondary"><Filter size={14}/> Filter stream</button></div>
  <div className="card"><div className="panel-head"><h2 style={{display:"flex",gap:8,alignItems:"center"}}><Radio size={14}/> Intelligence stream</h2><span>CONTINUOUS · 42 DOCUMENTS → 18 EVENTS</span></div>{events.map(event=><Link className="event-row" href={`/app/events/${event.id}`} key={event.id}><div className="timestamp">{event.time}<br/>UTC</div><div><div className="event-title">{event.title}</div><div className="event-explain">{event.explanation}</div><div className="chips"><span className={`chip ${event.type.includes("DIVERGENCE")?"chip-red":"chip-cyan"}`}>{event.type}</span>{event.entities.map(entity=><span className="chip" key={entity}>{entity}</span>)}</div></div><div className="score"><strong>{event.sourceCount}</strong>sources<br/>novelty {Math.round(event.novelty*100)}</div><div className="score"><strong>{Math.round(event.confidence*100)}%</strong>confidence<br/>impact {Math.round(event.impact*100)}</div></Link>)}</div></>;
}
