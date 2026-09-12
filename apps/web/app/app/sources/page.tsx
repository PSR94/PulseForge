import { api } from "@/lib/api";
import { AddSourceForm } from "@/components/AddSourceForm";
import { SourceIngestButton } from "@/components/SourceIngestButton";

export const dynamic="force-dynamic";

export default async function SourcesPage(){
  const sources=await api.sources();
  return <>
    <div className="page-head"><div><h1>Source management</h1><p>RSS, JSON, web pages, GitHub releases, arXiv and Hacker News share one bounded ingestion contract.</p></div></div>
    <div className="split"><div className="card"><div className="panel-head"><h2>Configured sources</h2><span>{sources.length}</span></div><table className="table"><thead><tr><th>Name</th><th>Type</th><th>Observed reliability properties</th><th/></tr></thead><tbody>{sources.map((source:any)=><tr key={source.id}><td><strong>{source.name}</strong><br/><span className="card-sub">{source.source_url}</span></td><td>{source.source_type}</td><td>{source.observations.primary_source?"primary":"secondary"} · {source.observations.independent_confirmation_count} independent confirmations</td><td><SourceIngestButton sourceId={source.id}/></td></tr>)}</tbody></table></div><AddSourceForm/></div>
  </>;
}
