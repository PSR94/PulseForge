import { api } from "@/lib/api";
import { GraphCanvas } from "@/components/GraphCanvas";
import { GraphDiffPanel } from "@/components/GraphDiffPanel";

export const dynamic="force-dynamic";

export default async function GraphPage(){
  const [graph,diff]=await Promise.all([api.graph(),api.diff("2026-09-10T15:40:00Z","2026-09-11T15:40:00Z")]);
  return <>
    <div className="page-head"><div><h1>Temporal knowledge graph</h1><p>Relationships are validity-bounded and evidence-linked; the graph is never modeled as timeless.</p></div><span className="chip">{graph.snapshot.relationships.length} active edges</span></div>
    <div className="card"><GraphCanvas entities={graph.entities} relationships={graph.snapshot.relationships}/></div>
    <div style={{marginTop:12}}><GraphDiffPanel diff={diff} entities={graph.entities}/></div>
  </>;
}
