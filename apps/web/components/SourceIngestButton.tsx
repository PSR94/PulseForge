"use client";

import { useState } from "react";
import { publicBase } from "@/lib/api";

export function SourceIngestButton({sourceId}:{sourceId:string}) {
  const [state,setState]=useState<string>("Ingest");
  async function ingest(){
    setState("Ingesting…");
    const response=await fetch(`${publicBase}/api/v1/sources/${encodeURIComponent(sourceId)}/ingest`,{method:"POST"});
    const body=await response.json();
    setState(response.ok?`${body.documents_received} docs`:"Failed");
  }
  return <button className="button-secondary" onClick={ingest}>{state}</button>;
}
