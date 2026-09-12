import { api } from "@/lib/api";
import { SignalCard } from "@/components/SignalCard";

export const dynamic="force-dynamic";

export default async function SignalsPage(){
  const signals=await api.signals();
  return <>
    <div className="page-head"><div><h1>Signal center</h1><p>Thresholds, velocity, divergence, emergence and relationship novelty are detected from stored state; AI explains but does not manufacture the trigger.</p></div></div>
    <div className="card">{signals.map(signal=><SignalCard signal={signal} key={signal.id}/>)}</div>
  </>;
}
