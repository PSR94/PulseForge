import Link from "next/link";
import { api } from "@/lib/api";

export const dynamic="force-dynamic";

export default async function TimelinePage(){
  const events=(await api.feed()).slice().sort((a,b)=>new Date(a.first_observed).getTime()-new Date(b.first_observed).getTime());
  return <>
    <div className="page-head"><div><h1>Event timeline</h1><p>Temporal sequence of normalized event clusters and evidence-bearing changes.</p></div><div className="chips"><span className="chip">hours</span><span className="chip">days</span><span className="chip">weeks</span><span className="chip">months</span></div></div>
    <div className="card timeline-list">{events.map(event=><div className="timeline-item" key={event.id}><div className="timeline-dot"/><div className="timestamp">{new Date(event.first_observed).toLocaleString()}</div><div><Link href={`/app/events/${event.id}`} className="event-title">{event.title}</Link><div className="event-explain">{event.explanation}</div></div></div>)}</div>
  </>;
}
