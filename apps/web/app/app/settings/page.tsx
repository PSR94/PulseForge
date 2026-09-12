import { api } from "@/lib/api";

export const dynamic="force-dynamic";

export default async function SettingsPage(){
  const capabilities=await api.capabilities();
  return <>
    <div className="page-head"><div><h1>Workspace configuration</h1><p>Runtime capabilities are exposed by the API so operators can distinguish demo mode from durable production mode.</p></div></div>
    <div className="grid-4">
      <div className="card card-pad"><div className="card-title">Repository mode</div><div className="card-value">{capabilities.repository_mode}</div></div>
      <div className="card card-pad"><div className="card-title">AI provider</div><div className="card-value">{capabilities.ai_provider}</div></div>
      <div className="card card-pad"><div className="card-title">Authentication</div><div className="card-value">{capabilities.auth_mode}</div></div>
      <div className="card card-pad"><div className="card-title">Demo mode</div><div className="card-value">{String(capabilities.demo_mode)}</div></div>
    </div>
    <div className="card card-pad" style={{marginTop:12}}><div className="card-title">Features</div><table className="table"><tbody>{Object.entries(capabilities.features).map(([key,value])=><tr key={key}><td className="code-like">{key}</td><td>{String(value)}</td></tr>)}</tbody></table></div>
  </>;
}
