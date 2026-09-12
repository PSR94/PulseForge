import { api } from "@/lib/api";
import { GraphDiffPanel } from "@/components/GraphDiffPanel";
import { AnalystPanel } from "@/components/AnalystPanel";

export const dynamic="force-dynamic";

export default async function ComparePage(){
  const [entities,diff]=await Promise.all([
    api.entities(),
    api.diff("2026-09-10T15:40:00Z","2026-09-11T15:40:00Z")
  ]);
  return <>
    <div className="page-head"><div><h1>What changed?</h1><p>Compare temporal graph state, entity velocity, emerging topics, vanished relationships and newly introduced contradictions.</p></div><div className="chips"><span className="chip">Sep 10 · 15:40 UTC</span><span>→</span><span className="chip">Sep 11 · 15:40 UTC</span></div></div>
    <GraphDiffPanel diff={diff} entities={entities}/>
    <div style={{marginTop:12}}><AnalystPanel/></div>
  </>;
}
