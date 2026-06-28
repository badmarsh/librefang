import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import neo4j from "neo4j-driver";

const server = new Server(
  {
    name: "temporal-kg",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Connect to Memgraph using Bolt protocol
const driver = neo4j.driver(
  process.env.MEMGRAPH_URI || "bolt://localhost:7687",
  neo4j.auth.basic(
    process.env.MEMGRAPH_USER || "",
    process.env.MEMGRAPH_PASSWORD || ""
  )
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "query_temporal_graph",
        description: "Execute a read-only Cypher query against the temporal graph database to analyze narratives and claims.",
        inputSchema: {
          type: "object",
          properties: {
            cypher: {
              type: "string",
              description: "The Cypher query to execute. MUST be read-only.",
            },
            parameters: {
              type: "object",
              description: "Query parameters",
              additionalProperties: true,
            },
          },
          required: ["cypher"],
        },
      },
      {
        name: "store_narrative_cluster",
        description: "Store a new narrative cluster and its associated claims into the temporal graph database.",
        inputSchema: {
          type: "object",
          properties: {
            cluster_id: { type: "string" },
            claim_ids: {
              type: "array",
              items: { type: "string" }
            },
            narrative: { type: "string" },
            timestamp: { type: "string" }
          },
          required: ["cluster_id", "claim_ids", "narrative"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "query_temporal_graph") {
    const session = driver.session();
    try {
      const cypher = String(request.params.arguments?.cypher || "");
      if (cypher.toLowerCase().includes("delete") || cypher.toLowerCase().includes("remove") || cypher.toLowerCase().includes("detach")) {
         throw new Error("Read-only queries only.");
      }
      const params = request.params.arguments?.parameters || {};
      const result = await session.readTransaction(tx => tx.run(cypher, params));
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result.records.map(r => r.toObject()), null, 2),
          },
        ],
      };
    } catch (e) {
      return {
        content: [{ type: "text", text: `Error: ${e.message}` }],
        isError: true,
      };
    } finally {
      await session.close();
    }
  } else if (request.params.name === "store_narrative_cluster") {
    const session = driver.session();
    try {
      const args = request.params.arguments || {};
      const { cluster_id, claim_ids, narrative, timestamp } = args;
      
      const cypher = `
        MERGE (n:NarrativeCluster {id: $cluster_id})
        SET n.narrative = $narrative, n.timestamp = $timestamp
        WITH n
        UNWIND $claim_ids AS claim_id
        MERGE (c:Claim {id: claim_id})
        MERGE (c)-[:BELONGS_TO]->(n)
        RETURN n.id AS clusterId, count(c) AS claimsLinked
      `;
      const result = await session.writeTransaction(tx => tx.run(cypher, { 
         cluster_id, claim_ids, narrative, timestamp: timestamp || new Date().toISOString() 
      }));
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result.records.map(r => r.toObject()), null, 2),
          },
        ],
      };
    } catch (e) {
      return {
        content: [{ type: "text", text: `Error: ${e.message}` }],
        isError: true,
      };
    } finally {
      await session.close();
    }
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Temporal KG MCP server running on stdio");
}

run().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
