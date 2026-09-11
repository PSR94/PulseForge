"use client";
import { FormEvent, useState } from "react";
import { Rss } from "lucide-react";

export function AddSourceForm(){
  const [name,setName]=useState("OpenAI News RSS"); const [url,setUrl]=useState("https://openai.com/news/rss.xml"); const [status,setStatus]=useState("");
  async function submit(event:FormEvent){event.preventDefault();setStatus("Validating…");try{const base=process.env.NEXT_PUBLIC_PULSEFORGE_API_URL??"http://localhost:8000";const response=await fetch(`${base}/api/v1/sources`,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({name,source_url:url,source_type:"rss"})});if(!response.ok)throw new Error((await response.json()).detail??"Unable to add source");const source=await response.json();setStatus(`Registered ${source.name} · ${source.id}`)}catch(error){setStatus(error instanceof Error?error.message:"Unable to add source")}}
  return <form onSubmit={submit} className="card card-pad"><div style={{display:"flex",gap:8,alignItems:"center",marginBottom:12}}><Rss size={15}/><strong>Add RSS / Atom source</strong></div><div className="grid-2"><input aria-label="Source name" value={name} onChange={e=>setName(e.target.value)} style={{background:"#080c11",border:"1px solid var(--line-2)",borderRadius:7,color:"var(--text)",padding:10}}/><input aria-label="Source URL" value={url} onChange={e=>setUrl(e.target.value)} style={{background:"#080c11",border:"1px solid var(--line-2)",borderRadius:7,color:"var(--text)",padding:10}}/></div><div style={{display:"flex",alignItems:"center",gap:10,marginTop:10}}><button className="button-primary">Add source</button><span className="card-sub">{status||"URL destinations are validated server-side before registration."}</span></div></form>
}
