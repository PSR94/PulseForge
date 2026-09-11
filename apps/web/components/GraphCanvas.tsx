"use client";

import { Background, Controls, Edge, Node, ReactFlow } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { entities, graphEdges } from "@/lib/demo";

const positions: Record<string,{x:number;y:number}> = {
  "ent-nvidia":{x:340,y:190},"ent-nebula":{x:650,y:120},"ent-helix":{x:680,y:350},
  "ent-orion":{x:80,y:90},"ent-forge":{x:90,y:330},"ent-quartz":{x:360,y:430},"ent-efficiency":{x:380,y:570},
};

const nodes: Node[] = entities.map(entity=>({id:entity.id,position:positions[entity.id]??{x:0,y:0},data:{label:`${entity.name} · ${entity.type}`},style:{background:"#10161e",color:"#e6edf3",border:`1px solid ${entity.id==="ent-nvidia"?"#54d6ff":"#293345"}`,borderRadius:8,fontSize:11,padding:9,width:190}}));
const edges: Edge[] = graphEdges.map(edge=>({id:edge.id,source:edge.source,target:edge.target,label:edge.label,animated:edge.newEdge,style:{stroke:edge.newEdge?"#54d6ff":"#4b5563",strokeWidth:edge.newEdge?1.8:1},labelStyle:{fill:"#8b98aa",fontSize:9},labelBgStyle:{fill:"#090d13"}}));

export function GraphCanvas(){ return <div className="graph-wrap"><ReactFlow nodes={nodes} edges={edges} fitView><Background color="#18202b" gap={24} size={1}/><Controls/></ReactFlow></div> }
