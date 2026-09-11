import { describe, expect, it } from "vitest";
import { events, graphEdges, signals } from "@/lib/demo";

describe("deterministic intelligence fixture", () => {
  it("contains the signature demo states", () => {
    expect(events.find(event => event.id === "evt-nvidia-platform")?.sourceCount).toBe(5);
    expect(signals.some(signal => signal.id === "sig-nvidia-velocity" && signal.metric === "5.7×")).toBe(true);
    expect(signals.some(signal => signal.id === "sig-source-divergence")).toBe(true);
    expect(graphEdges.some(edge => edge.id === "rel-nvidia-nebula" && edge.newEdge)).toBe(true);
  });
});
