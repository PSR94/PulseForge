"use client";

import { FormEvent, useState } from "react";
import { publicBase } from "@/lib/api";

export function WatchlistBuilder(){
  const [message,setMessage]=useState("");
  async function submit(event:FormEvent<HTMLFormElement>){
    event.preventDefault();
    const data=new FormData(event.currentTarget);
    const target=String(data.get("target")||"");
    const multiplier=Number(data.get("multiplier")||4);
    const payload={
      workspace_id:"ai-industry",
      name:`Monitor ${target}`,
      target_type:"entity",
      target,
      conditions:[{field:"multiplier",operator:"gte",value:multiplier}],
      enabled:true,
    };
    const response=await fetch(`${publicBase}/api/v1/watchlists`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
    const body=await response.json();
    setMessage(response.ok?`Created ${body.id}`:body.detail||"Could not create rule");
    if(response.ok) event.currentTarget.reset();
  }
  return <form className="card card-pad watch-builder" onSubmit={submit}>
    <div className="card-title">Create monitoring rule</div>
    <label>Entity or topic<input name="target" placeholder="NVIDIA" required/></label>
    <label>Velocity threshold<input name="multiplier" type="number" min="1" step=".1" defaultValue="4"/></label>
    <button className="button-primary" type="submit">Create watchlist</button>
    {message&&<p className="card-sub">{message}</p>}
  </form>;
}
