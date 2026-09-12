"use client";

import { Background, Controls, Edge, Node, ReactFlow } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import type { Entity, Relationship } from "@/lib/types";

function position(index:number,total:number){
  const angle=(index/Math.max(1,total))*Math.PI*2;
  const radius=260+(index%3)*35;
  return {x:420+Math.cos(angle)*radius,y:330+Math.sin(angle)*radius};
}

export function GraphCanvas({entities,relationships}:{entities:Entity[];relationships:Relationship[]}) {
  const nodes: Node[] = entities.map((entity,index)=>({
    id:entity.id,
    position:position(index,entities.length),
    data:{label:`${entity.name} · ${entity.entity_type}`},
    style:{
      background:"#10161e",
      color:"#e6edf3",
      border:`1px solid ${entity.activity_velocity>=4?"#54d6ff":"#293345"}`,
      borderRadius:8,
      fontSize:11,
      padding:9,
      width:190,
      boxShadow:entity.activity_velocity>=4?"0 0 0 3px rgba(84,214,255,.08)":"none",
    }
  }));
  const edges: Edge[] = relationships.map(edge=>({
    id:edge.id,
    source:edge.source_entity_id,
    target:edge.target_entity_id,
    label:edge.relationship_type,
    animated:edge.confidence>.9,
    style:{stroke:edge.valid_to?"#596579":"#54d6ff",strokeWidth:Math.max(1,edge.strength*1.6)},
    labelStyle:{fill:"#8b98aa",fontSize:9},
    labelBgStyle:{fill:"#090d13"},
  }));
  return <div className="graph-wrap"><ReactFlow nodes={nodes} edges={edges} fitView minZoom={0.2} maxZoom={2}><Background color="#18202b" gap={24} size={1}/><Controls/></ReactFlow></div>;
}
