"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import {
  Activity, Bell, BookOpen, Clock3, FileText, GitCompareArrows,
  Home, Map, Network, Radar, Search, Settings, ShieldAlert, Sparkles, Globe2,
} from "lucide-react";
import { publicBase } from "@/lib/api";

const primary = [
  ["/app", "Overview", Home],
  ["/app/feed", "Live feed", Activity],
  ["/app/compare", "What changed?", GitCompareArrows],
  ["/app/graph", "Knowledge graph", Network],
  ["/app/timeline", "Timeline", Clock3],
  ["/app/map", "Intelligence map", Map],
  ["/app/signals", "Signals", Radar],
] as const;
const manage = [
  ["/app/briefings", "Briefings", FileText],
  ["/app/watchlists", "Watchlists", Bell],
  ["/app/sources", "Sources", Globe2],
  ["/app/settings", "Settings", Settings],
] as const;
const commands = [
  {label:"Ask PulseForge", hint:"Why did this change?", path:"/app#analyst", icon:Sparkles},
  {label:"Open graph", hint:"Temporal relationships", path:"/app/graph", icon:Network},
  {label:"Open timeline", hint:"Hours → years", path:"/app/timeline", icon:Clock3},
  {label:"Compare time periods", hint:"Temporal Graph Diff", path:"/app/compare", icon:GitCompareArrows},
  {label:"Generate briefing", hint:"Evidence-linked", path:"/app/briefings", icon:BookOpen},
  {label:"Add source", hint:"RSS, web, GitHub, arXiv…", path:"/app/sources", icon:Globe2},
];

function NavGroup({items}:{items:readonly (readonly [string,string,typeof Home])[]}) {
  const pathname = usePathname();
  return <>{items.map(([href,label,Icon]) => {
    const active = pathname === href || (href !== "/app" && pathname.startsWith(href));
    return <Link key={href} className={`nav-link ${active ? "active" : ""}`} href={href}>
      <Icon size={15}/><span>{label}</span>
    </Link>;
  })}</>;
}

function resultPath(kind:string,id:string){
  if(kind==="entity"||kind==="entities") return `/app/entities/${id}`;
  if(kind==="event"||kind==="events") return `/app/events/${id}`;
  return "/app/feed";
}

export function PulseShell({children}:{children:React.ReactNode}) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results,setResults]=useState<{kind:string;id:string;label:string}[]>([]);
  const router = useRouter();
  const filtered = useMemo(() => commands.filter(item => `${item.label} ${item.hint}`.toLowerCase().includes(query.toLowerCase())), [query]);

  useEffect(() => {
    const handle = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault(); setOpen(value => !value);
      }
      if (event.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", handle);
    return () => window.removeEventListener("keydown", handle);
  }, []);

  useEffect(()=>{
    if(query.trim().length<2){setResults([]);return}
    const controller=new AbortController();
    const timer=setTimeout(async()=>{
      try{
        const response=await fetch(`${publicBase}/api/v1/search?q=${encodeURIComponent(query)}`,{signal:controller.signal});
        if(!response.ok)return;
        const data=await response.json();
        const flat:{kind:string;id:string;label:string}[]=[];
        for(const [kind,items] of Object.entries(data) as [string,any[]][]){
          for(const item of items.slice(0,4)) flat.push({kind,id:item.id,label:item.name??item.title??item.object_value??item.id});
        }
        setResults(flat.slice(0,10));
      }catch{}
    },160);
    return()=>{clearTimeout(timer);controller.abort()}
  },[query]);

  return <div className="shell">
    <aside className="sidebar">
      <Link href="/app" className="brand"><span className="brand-mark"><Activity size={15}/></span><span>PulseForge</span></Link>
      <div className="workspace-switcher"><strong>AI Industry Intelligence</strong><small>Evidence-linked demo · ingestable</small></div>
      <div className="nav-section">Intelligence</div><NavGroup items={primary}/>
      <div className="nav-section">Operations</div><NavGroup items={manage}/>
      <div className="sidebar-foot"><ShieldAlert size={13}/> Facts ≠ inference · provenance first</div>
    </aside>
    <main className="main">
      <header className="topbar">
        <div className="topbar-title"><span className="live-dot"/> Intelligence workspace <span style={{color:"var(--quiet)"}}>· temporal state</span></div>
        <button className="command-trigger" onClick={() => setOpen(true)}><span className="hint">Search or run a command…</span><span><kbd>⌘</kbd> <kbd>K</kbd></span></button>
      </header>
      <div className="content">{children}</div>
    </main>
    {open && <div className="command-overlay" onMouseDown={() => setOpen(false)}>
      <div className="command" onMouseDown={event => event.stopPropagation()}>
        <input autoFocus value={query} onChange={event => setQuery(event.target.value)} placeholder="Search entities, events, claims, signals, or run a command…"/>
        <div style={{padding:"7px 0"}}>
          {results.length>0&&<div className="nav-section">Unified search</div>}
          {results.map(item=><button key={`${item.kind}-${item.id}`} className="command-item" style={{width:"100%",border:0,background:"transparent",cursor:"pointer"}} onClick={()=>{setOpen(false);router.push(resultPath(item.kind,item.id))}}><span style={{display:"flex",gap:9,alignItems:"center"}}><Search size={15}/>{item.label}</span><span style={{color:"var(--quiet)"}}>{item.kind}</span></button>)}
          <div className="nav-section">Commands</div>
          {filtered.map(item => <button key={item.label} className="command-item" style={{width:"100%",border:0,background:"transparent",cursor:"pointer"}} onClick={() => {setOpen(false); router.push(item.path)}}>
            <span style={{display:"flex",gap:9,alignItems:"center"}}><item.icon size={15}/>{item.label}</span><span style={{color:"var(--quiet)"}}>{item.hint}</span>
          </button>)}
        </div>
      </div>
    </div>}
  </div>;
}
