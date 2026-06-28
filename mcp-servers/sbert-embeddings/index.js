import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const server = new Server(
  {
    name: "sbert-embeddings",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "sbert_embed_sk_cz",
        description: "Generate 768-dimensional semantic embeddings for Slovak and Czech text using gerulata/slovakbert. Useful for claim deduplication and semantic similarity searches.",
        inputSchema: {
          type: "object",
          properties: {
            text: {
              type: "string",
              description: "The Slovak or Czech text to embed.",
            },
          },
          required: ["text"],
        },
      }
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "sbert_embed_sk_cz") {
    const text = String(request.params.arguments?.text || "");
    
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn("python3", [path.join(__dirname, "embed.py")]);
      
      let outputData = "";
      let errorData = "";
      
      pythonProcess.stdout.on("data", (data) => {
        outputData += data.toString();
      });
      
      pythonProcess.stderr.on("data", (data) => {
        errorData += data.toString();
      });
      
      pythonProcess.on("close", (code) => {
        try {
          const result = JSON.parse(outputData);
          if (result.error) {
            resolve({
              content: [{ type: "text", text: `Error: ${result.error}` }],
              isError: true,
            });
          } else {
            resolve({
              content: [{ type: "text", text: JSON.stringify(result.embedding) }],
            });
          }
        } catch (e) {
          resolve({
            content: [{ type: "text", text: `Failed to parse Python output. Error: ${errorData}` }],
            isError: true,
          });
        }
      });
      
      // Write to stdin
      pythonProcess.stdin.write(JSON.stringify({ text }));
      pythonProcess.stdin.end();
    });
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("SlovakBERT Embeddings MCP server running on stdio");
}

run().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
