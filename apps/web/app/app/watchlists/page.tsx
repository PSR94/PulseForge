import { api } from "@/lib/api";
import { WatchlistBuilder } from "@/components/WatchlistBuilder";

export const dynamic="force-dynamic";

export default async function WatchlistsPage(){
  const [rules,alerts]=await Promise.all([api.watchlists(),api.alerts()]);
  return <>
    <div className="page-head"><div><h1>Watchlists & alerts</h1><p>Monitor entities, topics, relationships, keywords, regions and deterministic thresholds.</p></div></div>
    <div className="split"><div className="stack"><WatchlistBuilder/><div className="card"><div className="panel-head"><h2>Rules</h2><span>{rules.length}</span></div>{rules.length===0?<div className="empty-state">No user rules yet. Create one to evaluate it against current intelligence.</div>:rules.map((rule:any)=><div className="event-row" key={rule.id}><div/><div><div className="event-title">{rule.name}</div><div className="event-explain">{rule.target_type}: {rule.target}</div></div><div className="score">{rule.enabled?"enabled":"paused"}</div></div>)}</div></div><div className="card"><div className="panel-head"><h2>Explainable alerts</h2><span>{alerts.length}</span></div>{alerts.length===0?<div className="empty-state">No alert has fired yet.</div>:alerts.map((alert:any)=><div className="signal-card" key={alert.id}><div/><div><h3>{alert.title}</h3><p>{alert.explanation}</p></div><div className="metric">{alert.severity}</div></div>)}</div></div>
  </>;
}
