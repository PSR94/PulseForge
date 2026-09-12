"use client";

import { FormEvent, useState } from "react";
import { Sparkles } from "lucide-react";
import { publicBase } from "@/lib/api";

type Answer={answer:string;answer_type:string;tools_used:string[];citations:{kind:string;id:string;label:string}[];uncertainty?:string|null};

export function AnalystPanel(){
  const [question,setQuestion]=useState("Why is NVIDIA appearing more frequently today?");
  const [answer,setAnswer]=useState<Answer|null>(null);
  const [loading,setLoading]=useState(false);
  async function ask(event:FormEvent){
    event.preventDefault();setLoading(true);
    try{
      const response=await fetch(`${publicBase}/api/v1/analyst/ask`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question,workspace_id:"ai-industry"})});
      setAnswer(await response.json());
    }finally{setLoading(false)}
  }
  return <section className="card analyst" id="analyst">
    <div className="panel-head"><h2><Sparkles size={15}/> AI intelligence analyst</h2><span>STRUCTURED TOOLS</span></div>
    <form className="analyst-form" onSubmit={ask}><input value={question} onChange={e=>setQuestion(e.target.value)} aria-label="Ask PulseForge"/><button className="button-primary" disabled={loading}>{loading?"Analyzing…":"Ask"}</button></form>
    {answer&&<div className="analyst-answer">
      <div className="chips"><span className="chip">{answer.answer_type.toUpperCase()}</span>{answer.tools_used.map(tool=><span className="chip" key={tool}>{tool}</span>)}</div>
      <p>{answer.answer}</p>
      {answer.uncertainty&&<p className="uncertainty">Uncertainty: {answer.uncertainty}</p>}
      <div className="citations">{answer.citations.map(c=><span key={`${c.kind}-${c.id}`}>[{c.kind}] {c.label}</span>)}</div>
    </div>}
  </section>;
}
