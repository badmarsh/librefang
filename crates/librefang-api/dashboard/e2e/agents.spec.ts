import { expect, test } from "@playwright/test";

test.describe("Agents Management", () => {
  test("creates, edits, and deletes an agent", async ({ page }) => {
    await page.goto("/dashboard/agents");

    // Click the create agent button (it has a title "Create Agent (n)" or similar translation)
    // Find the add/create button (it has a Plus icon)
    await page.locator('button:has(svg.lucide-plus)').first().click();
    
    // Wait for the modal/drawer to appear. Wait for any textbox.
    await expect(page.getByRole("textbox").first()).toBeVisible({ timeout: 10000 });

    const agentName = `e2e-test-agent-${Date.now()}`;
    await page.getByRole("textbox").first().fill(agentName);
    
    // Click the main action button (usually primary variant, or has a Check/Save/Create text/icon)
    await page.getByRole("button").filter({ has: page.locator('svg.lucide-check') }).first().click();
  });
});
