import { expect, test } from "@playwright/test";

test.describe("Chat Sessions", () => {
  test("creates a session and sends a mock message", async ({ page }) => {
    // Intercept the chat stream API to avoid hitting real LLMs
    await page.route("**/api/agents/*/stream", async (route) => {
      // Return a simulated chunked SSE response
      const mockResponse = `data: {"type":"AgentMessage","content":"Hello from E2E test!","timestamp":"${new Date().toISOString()}"}\n\n`;
      await route.fulfill({
        status: 200,
        contentType: "text/event-stream",
        body: mockResponse,
      });
    });

    await page.goto("/dashboard/agents");

    // Click on the first link that might be a chat link (has "chat" or "session" in href)
    const chatLink = page.locator('a[href*="/chat"], a[href*="/session"]').first();
    if (await chatLink.isVisible()) {
        await chatLink.click();

        // Wait for the main text area or input.
        const input = page.locator('textarea, input[type="text"]').last();
        await expect(input).toBeVisible({ timeout: 10000 });

        // Send a message
        await input.fill("Test message");
        await page.keyboard.press("Enter");

        // Verify our mock response appears
        await expect(page.getByText("Hello from E2E test!")).toBeVisible({ timeout: 10000 });
    }
  });
});
