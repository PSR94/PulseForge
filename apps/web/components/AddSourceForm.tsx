"use client";

import { FormEvent, useState } from "react";
import { publicBase } from "@/lib/api";

export function AddSourceForm(){
  const [message,setMessage]=useState("");
  async function submit(event:FormEvent<HTMLFormElement>){
    event.preventDefault();
    const data=new FormData(event.currentTarget);
    const payload={
      workspace_id:"ai-industry",
      name:String(data.get("name")||""),
      source_url:String(data.get("url")||""),
      source_type:String(data.get("type")||"rss"),
    };
    const response=await fetch(`${publicBase}/api/v1/sources`,{
      method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)
    });
    const body=await response.json();
    setMessage(response.ok?`Added ${body.name}`:body.detail||"Could not add source");
    if(response.ok) event.currentTarget.reset();
  }
  return <form className="card card-pad source-form watch-builder" onSubmit={submit}>
    <div className="card-title">Add source</div>
    <label>Name<input name="name" placeholder="OpenAI newsroom" required/></label>
    <label>URL<input name="url" type="url" placeholder="https://example.com/feed.xml" required/></label>
    <label>Connector<select name="type" defaultValue="rss"><option value="rss">RSS / Atom</option><option value="json">JSON feed</option><option value="web">Web page</option><option value="github">GitHub releases</option><option value="arxiv">arXiv</option><option value="hacker_news">Hacker News</option><option value="api">Public JSON API</option></select></label>
    <button className="button-primary" type="submit">Add source</button>
    {message&&<p className="card-sub">{message}</p>}
  </form>;
}
