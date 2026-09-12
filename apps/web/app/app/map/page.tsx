import { api } from "@/lib/api";
import { IntelMap } from "@/components/IntelMap";

export const dynamic="force-dynamic";

export default async function MapPage(){
  const events=await api.feed();
  const mapped=events.filter(event=>event.latitude!=null&&event.longitude!=null);
  return <>
    <div className="page-head"><div><h1>Geospatial intelligence</h1><p>Mapped normalized events; selecting geographic scope is designed to drive the rest of the workspace.</p></div><span className="chip">{mapped.length} geocoded events</span></div>
    <div className="card"><IntelMap events={mapped}/></div>
  </>;
}
