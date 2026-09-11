import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AnalystPanel } from "@/components/AnalystPanel";

describe("AnalystPanel", () => {
  it("labels generated synthesis as inference and exposes structured tools", () => {
    render(<AnalystPanel />);
    expect(screen.getByText("INFERENCE")).toBeInTheDocument();
    expect(screen.getByText("calculate_velocity")).toBeInTheDocument();
    expect(screen.getByLabelText("Ask PulseForge")).toHaveValue(
      "Why is NVIDIA appearing more frequently today?",
    );
  });
});
