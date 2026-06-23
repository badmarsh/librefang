import { expect, test } from "@playwright/test";

test.describe("Providers Configuration", () => {
  test("updates a provider API key", async ({ page }) => {
    await page.goto("/dashboard/providers");

    // The page should show providers
    await expect(page.locator("h1")).toBeVisible({ timeout: 10000 });

    // Look for a provider card/row, for example 'freellmpool' or just the first provider edit button
    const editButton = page.locator("button:has(svg.lucide-pencil)").first().or(page.locator('button[title*="Edit"]').first());
    await editButton.click();

    // Verify modal or panel opens
    await expect(page.locator('input[type="password"]').first()).toBeVisible({ timeout: 10000 });

    // Enter a dummy key
    await page.locator('input[type="password"]').first().fill("dummy-key-for-e2e");

    // Save
    await page.getByRole("button", { name: /Save|Update/i }).click();
  });
});
