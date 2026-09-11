"use client";

import { FormEvent, useState } from "react";
import { Sparkles } from "lucide-react";

const DEFAULT = "NVIDIA mention velocity increased 5.7× during the last six hours. Three normalized event clusters account for 81% of the increase: the accelerator platform, the Nebula Cloud partnership, and Helix-2 infrastructure testing. This is an inference from deterministic signal state, not an independently established fact.";

export function AnalystPanel() {
  const [question,setQuestion] = useState("Why is NVIDIA appearing more frequently today?");
  const [answer,setAnswer] = useState(DEFAULT);
  const [loading,setLoading] = useState(false);
  async function ask(event: FormEvent) {
    event.preventDefault(); setLoading(true);
    try {
      const base = process.env.NEXT_PUBLIC_PULSEFORGE_API_URL ?? "http://localhost:8000";
      const response = await fetch(`${base}/api/v1/analyst/ask`, {method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({question})});
      if (response.ok) setAnswer((await response.json()).answer);
    } catch { setAnswer(DEFAULT); } finally { setLoading(false); }
  }
  return <div className="card" id="analyst"><div className="panel-head"><h2 style={{display:"flex",gap:7,alignItems:"center"}}><Sparkles size={14}/> AI Intelligence Analyst</h2><span>STRUCTURED TOOLS · MOCK MODE</span></div><div className="analyst-box">
    <div className="analyst-answer"><span className="inference-label">INFERENCE</span><div style={{marginTop:8}}>{answer}</div><div className="chips"><span className="chip">calculate_velocity</span><span className="chip">find_related_events</span><span className="chip">inspect_sources</span></div></div>
    <form className="analyst-input" onSubmit={ask}><input value={question} onChange={e=>setQuestion(e.target.value)} aria-label="Ask PulseForge"/><button className="button-primary" disabled={loading}>{loading?"Analyzing…":"Ask"}</button></form>
  </div></div>;
}
