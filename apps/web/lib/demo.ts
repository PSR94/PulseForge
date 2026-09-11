export type EventItem = {
  id: string; time: string; title: string; type: string; sourceCount: number; confidence: number;
  novelty: number; impact: number; entities: string[]; topics: string[]; explanation: string;
  location?: string; lat?: number; lng?: number; evidence: {source: string; excerpt: string; time: string; primary?: boolean}[];
};

export const events: EventItem[] = [
  {id:"evt-nebula-partnership",time:"14:18",title:"Nebula Cloud expands strategic infrastructure partnership with NVIDIA",type:"PARTNERSHIP",sourceCount:4,confidence:.94,novelty:.88,impact:.86,entities:["Nebula Cloud","NVIDIA","Helix-2"],topics:["cloud","datacenter infrastructure"],explanation:"A primary-source announcement establishes a new multi-year infrastructure relationship; three secondary sources report the same scope.",location:"Ashburn, US",lat:39.0438,lng:-77.4874,evidence:[{source:"Nebula Cloud Newsroom",excerpt:"Nebula Cloud and NVIDIA announced a multi-year infrastructure partnership spanning accelerated compute and Helix-2 networking.",time:"11:35 UTC",primary:true}]},
  {id:"evt-forgelm-schedule",time:"13:05",title:"ForgeLM 3 launch timing becomes disputed",type:"SOURCE DIVERGENCE",sourceCount:2,confidence:.83,novelty:.77,impact:.81,entities:["Orion AI","ForgeLM 3"],topics:["foundation models"],explanation:"PulseForge does not choose between incompatible October and January launch claims; it exposes the contradiction and source context.",location:"San Francisco, US",lat:37.7749,lng:-122.4194,evidence:[{source:"Orion AI Newsroom",excerpt:"Orion AI said ForgeLM 3 is scheduled for general availability in October 2026.",time:"Sep 10 · 16:00 UTC",primary:true},{source:"ModelBeat",excerpt:"People familiar with the rollout said broad ForgeLM 3 availability has moved to January 2027.",time:"Sep 11 · 13:05 UTC"}]},
  {id:"evt-quartz",time:"12:10",title:"Quartz Runtime reports 38% long-context inference throughput gain",type:"OPEN SOURCE",sourceCount:3,confidence:.88,novelty:.84,impact:.72,entities:["Quartz Runtime","Inference Efficiency"],topics:["open source","inference efficiency"],explanation:"An open-source runtime result joins multiple independent developments around inference efficiency.",evidence:[{source:"Open Source Ledger",excerpt:"Quartz Runtime contributors reported a 38% throughput gain on long-context inference workloads.",time:"12:10 UTC"}]},
  {id:"evt-nvidia-platform",time:"10:47",title:"NVIDIA introduces inference-focused accelerator platform",type:"PRODUCT",sourceCount:5,confidence:.96,novelty:.91,impact:.94,entities:["NVIDIA","Nebula Cloud"],topics:["AI chips","inference efficiency"],explanation:"Five reports converge on one underlying accelerator-platform announcement; Nebula Cloud independently confirms deployment plans.",location:"Santa Clara, US",lat:37.3541,lng:-121.9552,evidence:[{source:"ChipWire",excerpt:"NVIDIA disclosed a new accelerator platform optimized for large-scale inference deployments.",time:"09:12 UTC"},{source:"Nebula Cloud Newsroom",excerpt:"Nebula Cloud will make the new NVIDIA platform available in two regions this quarter.",time:"10:47 UTC",primary:true}]},
  {id:"evt-helix",time:"10:45",title:"Cloud operators test Helix-2 networking for dense accelerator clusters",type:"INFRASTRUCTURE",sourceCount:2,confidence:.82,novelty:.73,impact:.69,entities:["Helix-2","NVIDIA","Nebula Cloud"],topics:["networking","datacenter infrastructure"],explanation:"Infrastructure testing links networking capacity to the same accelerator expansion appearing in cloud and chip events.",location:"Frankfurt, DE",lat:50.1109,lng:8.6821,evidence:[{source:"ChipWire",excerpt:"Cloud operators are testing Helix-2 interconnects to reduce congestion in dense accelerator clusters.",time:"10:45 UTC"}]},
  {id:"evt-research",time:"08:20",title:"Adaptive sparsity research targets lower inference memory pressure",type:"RESEARCH",sourceCount:1,confidence:.9,novelty:.79,impact:.64,entities:["Inference Efficiency"],topics:["research","inference efficiency"],explanation:"A systems paper contributes a distinct mechanism to the emerging inference-efficiency cluster.",evidence:[{source:"Research Dispatch",excerpt:"A new systems paper reports reduced KV-cache pressure using adaptive sparsity during inference.",time:"08:20 UTC"}]}
];

export const signals = [
  {id:"sig-nvidia-velocity",kind:"VELOCITY",title:"NVIDIA activity velocity increased 5.7×",metric:"5.7×",severity:"HIGH",detail:"6-hour mention rate vs trailing 7-day same-hour baseline. Three event clusters account for 81% of the increase."},
  {id:"sig-efficiency-emergence",kind:"TOPIC EMERGENCE",title:"Inference efficiency emerges across three domains",metric:"3.8×",severity:"MEDIUM",detail:"Embedding cluster growth now spans hardware, systems research, and open-source runtime events."},
  {id:"sig-novel-relationship",kind:"NOVEL RELATIONSHIP",title:"New NVIDIA ↔ Nebula Cloud relationship appears",metric:"0.91",severity:"MEDIUM",detail:"No active PARTNERS_WITH edge existed before 11:35 UTC; four sources now support it."},
  {id:"sig-source-divergence",kind:"SOURCE DIVERGENCE",title:"ForgeLM 3 launch timing is materially disputed",metric:"2 claims",severity:"HIGH",detail:"Same subject and normalized property, incompatible date values. Conflict remains unresolved."}
];

export const entities = [
  {id:"ent-nvidia",name:"NVIDIA",type:"COMPANY",velocity:"5.7×",importance:.98,desc:"Semiconductor and accelerated-computing company."},
  {id:"ent-nebula",name:"Nebula Cloud",type:"COMPANY",velocity:"3.2×",importance:.79,desc:"Synthetic public-safe cloud provider used in the deterministic demo."},
  {id:"ent-orion",name:"Orion AI",type:"COMPANY",velocity:"2.6×",importance:.84,desc:"Synthetic public-safe model developer used in the deterministic demo."},
  {id:"ent-forge",name:"ForgeLM 3",type:"PRODUCT",velocity:"4.1×",importance:.74,desc:"Synthetic model release tracked by the demo workspace."},
  {id:"ent-quartz",name:"Quartz Runtime",type:"PROJECT",velocity:"3.8×",importance:.67,desc:"Synthetic open-source inference runtime."},
  {id:"ent-helix",name:"Helix-2 Interconnect",type:"TECHNOLOGY",velocity:"2.0×",importance:.61,desc:"Synthetic high-bandwidth datacenter interconnect technology."},
  {id:"ent-efficiency",name:"Inference Efficiency",type:"TOPIC",velocity:"3.8×",importance:.70,desc:"Emerging topic cluster around lower-cost, higher-throughput inference."}
];

export const graphEdges = [
  {id:"rel-nvidia-nebula",source:"ent-nvidia",target:"ent-nebula",label:"PARTNERS_WITH",newEdge:true},
  {id:"rel-nebula-helix",source:"ent-nebula",target:"ent-helix",label:"TESTS",newEdge:true},
  {id:"rel-orion-forge",source:"ent-orion",target:"ent-forge",label:"DEVELOPS"},
  {id:"rel-quartz-efficiency",source:"ent-quartz",target:"ent-efficiency",label:"ADVANCES",newEdge:true},
  {id:"rel-nvidia-helix",source:"ent-nvidia",target:"ent-helix",label:"USES_INTERCONNECT",newEdge:true}
];

export const entityById = (id:string) => entities.find(item => item.id === id);
export const eventById = (id:string) => events.find(item => item.id === id);
