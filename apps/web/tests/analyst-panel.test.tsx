import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AnalystPanel } from "@/components/AnalystPanel";

afterEach(()=>vi.restoreAllMocks());

describe("AnalystPanel", () => {
  it("asks the structured analyst and labels inference", async () => {
    vi.stubGlobal("fetch",vi.fn(async()=>new Response(JSON.stringify({
      answer:"NVIDIA velocity increased 5.7×.",
      answer_type:"inference",
      tools_used:["calculate_velocity","find_related_events"],
      citations:[{kind:"signal",id:"sig-nvidia-velocity",label:"NVIDIA activity spike"}],
      uncertainty:null,
    }),{status:200,headers:{"Content-Type":"application/json"}})));
    render(<AnalystPanel />);
    expect(screen.getByLabelText("Ask PulseForge")).toHaveValue("Why is NVIDIA appearing more frequently today?");
    fireEvent.click(screen.getByRole("button",{name:"Ask"}));
    await waitFor(()=>expect(screen.getByText("INFERENCE")).toBeInTheDocument());
    expect(screen.getByText("calculate_velocity")).toBeInTheDocument();
  });
});
