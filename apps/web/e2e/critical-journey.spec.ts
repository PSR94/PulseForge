import { expect, test } from "@playwright/test";

test("intelligence vertical slice: source → event → entity → graph → evidence → analyst → briefing", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: /Open demo workspace/i }).first().click();
  await expect(page.getByRole("heading", { name: "Intelligence overview" })).toBeVisible();

  await page.goto("/app/sources");
  await page.getByLabel("Source name").fill("PulseForge Test Feed");
  await page.getByLabel("Source URL").fill("https://example.com/feed.xml");
  await page.getByRole("button", { name: "Add source" }).click();
  await expect(page.getByText(/Registered PulseForge Test Feed/)).toBeVisible();

  await page.goto("/app/events/evt-nvidia-platform");
  await expect(page.getByRole("heading", { name: /NVIDIA introduces inference-focused accelerator platform/ })).toBeVisible();
  await expect(page.getByText("Evidence explorer")).toBeVisible();
  await expect(page.getByText(/NVIDIA disclosed a new accelerator platform/)).toBeVisible();

  await page.goto("/app/entities/ent-nvidia");
  await expect(page.getByRole("heading", { name: "NVIDIA" })).toBeVisible();
  await expect(page.getByText("5.7×")).toBeVisible();

  await page.goto("/app/graph");
  await expect(page.getByText("Temporal Graph Diff")).toBeVisible();
  await expect(page.getByText("NVIDIA PARTNERS_WITH Nebula Cloud")).toBeVisible();

  await page.goto("/app#analyst");
  await page.getByRole("button", { name: "Ask" }).click();
  await expect(page.getByText(/NVIDIA mention velocity is 5.7×/)).toBeVisible();

  await page.goto("/app/briefings");
  await expect(page.getByRole("heading", { name: "Intelligence briefings" })).toBeVisible();
  await expect(page.getByText(/ForgeLM 3: October 2026 vs January 2027/)).toBeVisible();
});
