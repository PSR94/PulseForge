import Link from "next/link";
import { Activity, ArrowRight, GitCompareArrows, Network, Radar, ShieldCheck } from "lucide-react";

export default function LandingPage() {
  return <main className="landing">
    <nav className="landing-nav"><div className="brand"><span className="brand-mark"><Activity size={15}/></span><span>PulseForge</span></div><Link className="button-secondary" href="/app">Open demo workspace</Link></nav>
    <section className="hero">
      <div>
        <div className="eyebrow">Real-time AI event intelligence</div>
        <h1>Understand what changed — and prove why.</h1>
        <p>PulseForge converts continuously changing information into normalized events, evidence-linked claims, a temporal knowledge graph, and deterministic signals. The AI analyst explains structured intelligence without pretending inference is fact.</p>
        <div className="hero-actions"><Link className="button-primary" href="/app">Explore live demo <ArrowRight size={14} style={{verticalAlign:"middle"}}/></Link><a className="button-secondary" href="https://github.com/PSR94/PulseForge">View source</a></div>
        <div className="chips" style={{marginTop:24}}><span className="chip"><ShieldCheck size={11}/> evidence-first</span><span className="chip"><Network size={11}/> temporal graph</span><span className="chip"><Radar size={11}/> signal detection</span><span className="chip"><GitCompareArrows size={11}/> graph diff</span></div>
      </div>
      <div className="preview">
        <div className="preview-top"><span>AI INDUSTRY INTELLIGENCE</span><span>LIVE · 15:40 UTC</span></div>
        <div className="preview-grid">
          <div className="preview-card"><span className="card-title">Entity velocity</span><strong className="metric-up">5.7×</strong><span className="card-sub">NVIDIA · 3 event clusters drive 81%</span></div>
          <div className="preview-card"><span className="card-title">Temporal diff</span><strong>+4 edges</strong><span className="card-sub">1 contradiction · 1 emerging topic</span></div>
          <div className="preview-card"><span className="card-title">Source divergence</span><strong className="metric-warn">⚠ 2 claims</strong><span className="card-sub">ForgeLM 3 · Oct 2026 vs Jan 2027</span></div>
          <div className="preview-card"><span className="card-title">Emerging topic</span><strong>3.8×</strong><span className="card-sub">Inference efficiency · 3 domains</span></div>
        </div>
      </div>
    </section>
  </main>;
}
