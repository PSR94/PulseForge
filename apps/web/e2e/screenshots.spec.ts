import fs from "node:fs";
import path from "node:path";
import { expect, test } from "@playwright/test";

const imageDir=path.resolve(process.cwd(),"../../docs/images");

test.beforeAll(()=>fs.mkdirSync(imageDir,{recursive:true}));

test("capture real PulseForge product screens", async ({ page }) => {
  await page.setViewportSize({width:1440,height:1000});

  await page.goto("/app");
  await expect(page.getByRole("heading",{name:"Intelligence overview"})).toBeVisible();
  await page.screenshot({path:path.join(imageDir,"overview.png"),fullPage:true});

  await page.goto("/app/compare");
  await expect(page.getByRole("heading",{name:"What changed?"})).toBeVisible();
  await page.screenshot({path:path.join(imageDir,"graph-diff.png"),fullPage:true});

  await page.goto("/app/events/evt-nvidia-platform");
  await expect(page.getByText("Evidence explorer")).toBeVisible();
  await page.screenshot({path:path.join(imageDir,"event-evidence.png"),fullPage:true});
});
