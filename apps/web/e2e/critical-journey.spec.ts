import fs from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

test("end-to-end intelligence journey", async ({ page, request }) => {
  const workspace = await request.post("http://127.0.0.1:8000/api/v1/workspaces", {
    data: { name: "Playwright Intelligence", description: "Isolation smoke test" },
  });
  expect(workspace.status()).toBe(201);
  expect((await workspace.json()).id).toContain("playwright-intelligence");

  await page.goto("/");
  await page.getByRole("link", { name: /Open demo workspace/i }).first().click();
  await expect(page.getByRole("heading", { name: "Intelligence overview" })).toBeVisible();

  const fixture = path.join(process.cwd(), "e2e/fixtures/intelligence-note.md");
  const upload = await request.post("http://127.0.0.1:8000/api/v1/documents/upload", {
    multipart: {
      title: "NVIDIA and OpenAI announce joint inference research program",
      file: {
        name: "intelligence-note.md",
        mimeType: "text/markdown",
        buffer: fs.readFileSync(fixture),
      },
    },
  });
  expect(upload.ok()).toBeTruthy();
  const uploadBody = await upload.json();
  expect(uploadBody.event_ids.length).toBeGreaterThan(0);

  await page.goto("/app/feed");
  await expect(page.getByText("NVIDIA and OpenAI announce joint inference research program")).toBeVisible();

  await page.goto(`/app/events/${uploadBody.event_ids[0]}`);
  await expect(page.getByRole("heading", { name: /NVIDIA and OpenAI announce joint inference research program/ })).toBeVisible();
  await expect(page.getByText("Evidence explorer")).toBeVisible();
  await expect(page.getByText(/deterministic Playwright fixture/)).toBeVisible();

  await page.goto("/app/entities/ent-nvidia");
  await expect(page.getByRole("heading", { name: "NVIDIA" })).toBeVisible();

  await page.goto("/app/graph");
  await expect(page.getByText("Temporal Graph Diff")).toBeVisible();

  await page.goto("/app#analyst");
  await page.getByRole("button", { name: "Ask" }).click();
  await expect(page.getByText("INFERENCE")).toBeVisible();
  await expect(page.getByText("calculate_velocity")).toBeVisible();

  await page.goto("/app/briefings");
  await expect(page.getByRole("heading", { name: "Evidence-linked briefings" })).toBeVisible();
  await expect(page.getByRole("link", { name: "PDF" })).toBeVisible();

  await page.goto("/app/watchlists");
  await page.getByLabel("Entity or topic").fill("NVIDIA");
  await page.getByRole("button", { name: "Create watchlist" }).click();
  await expect(page.getByText(/Created watch-/)).toBeVisible();
});
