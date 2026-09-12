import { api } from "@/lib/api";
import { EventCard } from "@/components/EventCard";

export const dynamic="force-dynamic";

export default async function FeedPage(){
  const events=await api.feed();
  return <>
    <div className="page-head"><div><h1>Live intelligence feed</h1><p>Multiple source documents converge into normalized underlying events.</p></div><span className="chip">SSE /api/v1/feed/stream</span></div>
    <div className="card"><div className="panel-head"><h2>Current stream</h2><span>{events.length} EVENTS</span></div>{events.map(event=><EventCard event={event} key={event.id}/>)}</div>
  </>;
}
