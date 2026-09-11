"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import {
  Activity, Bell, BookOpen, Boxes, Clock3, Command, FileText, GitCompareArrows,
  Globe2, Home, Map, Network, Radar, Search, Settings, ShieldAlert, Sparkles,
} from "lucide-react";

const primary = [
  ["/app", "Overview", Home],
  ["/app/feed", "Live feed", Activity],
  ["/app/graph", "Knowledge graph", Network],
  ["/app/timeline", "Timeline", Clock3],
  ["/app/map", "Intelligence map", Map],
  ["/app/signals", "Signals", Radar],
];
const manage = [
  ["/app/briefings", "Briefings", FileText],
  ["/app/watchlists", "Watchlists", Bell],
  ["/app/sources", "Sources", Globe2],
  ["/app/settings", "Settings", Settings],
];
const commands = [
  {label:"Search entity", hint:"NVIDIA, Orion AI…", path:"/app/entities/ent-nvidia", icon:Search},
  {label:"Search event", hint:"Normalized intelligence", path:"/app/feed", icon:Activity},
  {label:"Ask PulseForge", hint:"Why did this change?", path:"/app#analyst", icon:Sparkles},
  {label:"Open graph", hint:"Temporal relationships", path:"/app/graph", icon:Network},
  {label:"Open timeline", hint:"Hours → years", path:"/app/timeline", icon:Clock3},
  {label:"Compare time periods", hint:"Temporal Graph Diff", path:"/app/graph#diff", icon:GitCompareArrows},
  {label:"Generate briefing", hint:"Evidence-linked", path:"/app/briefings", icon:BookOpen},
  {label:"Add source", hint:"RSS / Atom", path:"/app/sources", icon:Globe2},
];

function NavGroup({items}:{items:(string | typeof Home)[][]}) {
  const pathname = usePathname();
  return <>{items.map(([href,label,Icon]) => {
    const active = pathname === href || (href !== "/app" && pathname.startsWith(href as string));
    const IconComponent = Icon as typeof Home;
    return <Link key={href as string} className={`nav-link ${active ? "active" : ""}`} href={href as string}>
      <IconComponent size={15}/><span>{label as string}</span>
    </Link>;
  })}</>;
}

export function PulseShell({children}:{children:React.ReactNode}) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
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

  return <div className="shell">
    <aside className="sidebar">
      <Link href="/app" className="brand"><span className="brand-mark"><Activity size={15}/></span><span>PulseForge</span></Link>
      <div className="workspace-switcher"><strong>AI Industry Intelligence</strong><small>Demo workspace · live</small></div>
      <div className="nav-section">Intelligence</div><NavGroup items={primary}/>
      <div className="nav-section">Operations</div><NavGroup items={manage}/>
      <div className="sidebar-foot"><ShieldAlert size={13}/> Evidence-first · mock AI mode</div>
    </aside>
    <main className="main">
      <header className="topbar">
        <div className="topbar-title"><span className="live-dot"/> Stream current <span style={{color:"var(--quiet)"}}>· 6 normalized events</span></div>
        <button className="command-trigger" onClick={() => setOpen(true)}><span className="hint">Search or run a command…</span><span><kbd>⌘</kbd> <kbd>K</kbd></span></button>
      </header>
      <div className="content">{children}</div>
    </main>
    {open && <div className="command-overlay" onMouseDown={() => setOpen(false)}>
      <div className="command" onMouseDown={event => event.stopPropagation()}>
        <input autoFocus value={query} onChange={event => setQuery(event.target.value)} placeholder="Search entities, events, claims, or run a command…"/>
        <div style={{padding:"7px 0"}}>{filtered.map(item => <button key={item.label} className="command-item" style={{width:"100%",border:0,background:"transparent",cursor:"pointer"}} onClick={() => {setOpen(false); router.push(item.path)}}>
          <span style={{display:"flex",gap:9,alignItems:"center"}}><item.icon size={15}/>{item.label}</span><span style={{color:"var(--quiet)"}}>{item.hint}</span>
        </button>)}</div>
      </div>
    </div>}
  </div>;
}
