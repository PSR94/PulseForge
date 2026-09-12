"use client";

import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import type { Event } from "@/lib/types";

export function IntelMap({events}:{events:Event[]}) {
  const ref=useRef<HTMLDivElement>(null);
  useEffect(()=>{
    if(!ref.current)return;
    const map=new maplibregl.Map({
      container:ref.current,
      center:[-20,25],
      zoom:1.25,
      style:{version:8,sources:{},layers:[{id:"bg",type:"background",paint:{"background-color":"#090d13"}}]}
    });
    map.addControl(new maplibregl.NavigationControl(),"top-right");
    map.on("load",()=>{
      for(const event of events.filter(e=>e.latitude!=null&&e.longitude!=null)){
        const el=document.createElement("button");
        el.setAttribute("aria-label",event.title);
        el.style.cssText="width:13px;height:13px;border-radius:50%;background:#54d6ff;border:3px solid rgba(84,214,255,.25);box-sizing:content-box;cursor:pointer";
        new maplibregl.Marker({element:el})
          .setLngLat([event.longitude!,event.latitude!])
          .setPopup(new maplibregl.Popup({offset:18}).setHTML(`<strong>${event.title}</strong><br/><span style='color:#8b98aa;font-size:11px'>${event.source_count} sources · ${Math.round(event.confidence*100)}% confidence</span>`))
          .addTo(map);
      }
    });
    return()=>map.remove();
  },[events]);
  return <div ref={ref} className="map-wrap"/>;
}
