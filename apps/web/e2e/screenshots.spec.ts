import { test } from "@playwright/test";
import { resolve } from "node:path";

const output = resolve(process.cwd(), "../../docs/assets");

for (const [name, path] of [["workspace", "/app"], ["graph", "/app/graph"], ["event", "/app/events/evt-forgelm-schedule"]] as const) {
  test(`capture ${name} screenshot`, async ({ page }) => {
    await page.goto(path);
    await page.setViewportSize({ width: 1600, height: 1000 });
    await page.screenshot({ path: resolve(output, `${name}.png`), fullPage: true });
  });
}
