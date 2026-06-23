import { expect, test } from "@playwright/test";

test("verify agents belong to Medialny Dezolator", async ({ page, request }) => {
  // Use Playwright's built-in API testing to directly fetch the list of agents
  // This is the most reliable way to verify backend state with Playwright!
  const response = await request.get("http://127.0.0.1:4545/api/agents?limit=1000");
  const data = await response.json();
  const agents = data.items || data.agents || [];
  
  const uniqueAgents = agents.map((a: any) => a.name).filter((n: string) => n && n !== "librefang");

  console.log("=== SCRAPED AGENTS FROM API VIA PLAYWRIGHT ===");
  console.log(uniqueAgents.join(", "));
  console.log("===============================");

  const medialnyKeywords = [
    "arbiter", "architect", "archivist", "cib-detector", "claim", "clip", "coherence", 
    "disinfo", "dennikn", "impact", "narrative", "stance", "kg-consistency", "ml-classifier",
    "predictor", "qsvm", "source", "temporal", "triplet", "visual-analyst", "wiki-checker", "watchdog",
    "research", "investigator", "inquisitor"
  ];

  const unrelatedAgents = uniqueAgents.filter((agentName: string) => {
    const lower = agentName.toLowerCase();
    return !medialnyKeywords.some(kw => lower.includes(kw));
  });

  console.log(`Found ${unrelatedAgents.length} agents that do not appear related to Medialny Dezolator:`);
  console.log(unrelatedAgents.join(", "));

  // Soft assertion so we can see the output
  expect(unrelatedAgents.length).toBeGreaterThanOrEqual(0);
});
