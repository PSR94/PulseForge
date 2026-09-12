import { api, publicBase } from "@/lib/api";

export const dynamic="force-dynamic";

export default async function BriefingsPage(){
  const briefings=await api.briefings();
  return <>
    <div className="page-head"><div><h1>Evidence-linked briefings</h1><p>Generated from stored events, signals, contradictions and source evidence.</p></div></div>
    <div className="stack">{briefings.map(briefing=><article className="card card-pad" key={briefing.id}><div className="page-head"><div><h2>{briefing.title}</h2><p>{new Date(briefing.period_start).toLocaleString()} → {new Date(briefing.period_end).toLocaleString()}</p></div><div className="chips"><a className="button-secondary" href={`${publicBase}/api/v1/briefings/${briefing.id}/markdown`}>Markdown</a><a className="button-secondary" href={`${publicBase}/api/v1/briefings/${briefing.id}/html`}>HTML</a><a className="button-secondary" href={`${publicBase}/api/v1/briefings/${briefing.id}/pdf`}>PDF</a></div></div><h3>Executive summary</h3><p>{briefing.executive_summary}</p><h3>Top developments</h3><ul>{briefing.top_developments.map(item=><li key={item}>{item}</li>)}</ul><h3>Emerging signals</h3><ul>{briefing.emerging_signals.map(item=><li key={item}>{item}</li>)}</ul><h3>Contradictions / uncertainty</h3><ul>{briefing.contradictions.map(item=><li key={item}>{item}</li>)}</ul><div className="card-sub">Evidence: {briefing.evidence_ids.join(", ")}</div></article>)}</div>
  </>;
}
