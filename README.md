# Multi-Agent Deep Researcher (MCP-powered)

A multi-agent deep researcher using CrewAI for agent orchestration, LinkUp for deep web search, and the phi3 model (via Ollama) for synthesis and writing. The system produces direct, comprehensive answers with no sources/citations or agent thoughts in the output.

## Features
- Multi-agent orchestration with CrewAI (Web Searcher, Research Analyst, Technical Writer)
- Deep web search via LinkUp (using the LinkUp API)
- Synthesis and reasoning with phi3 (via Ollama)
- Exposed as an MCP server via FastAPI
- Output is a direct, clear, and comprehensive answer (no sources/citations or agent process steps)

## Setup

1. **Clone the repo**
2. **Install dependencies** (requires [Poetry](https://python-poetry.org/)):
   ```sh
   poetry install
   ```
3. **Configure environment variables**:
   - Create a `.env` file and fill in your LinkUp API key.
   - Example:
     ```
     LINKUP_API_KEY=your_linkup_api_key_here
     ```
4. **Run the MCP server**:
   ```sh
   poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/server.py
   ```

## API Usage

POST `/research`
- Body: `{ "query": "your research question" }`
- Returns: `{ "result": "direct, comprehensive answer" }`

Example:
```sh
curl -X POST http://localhost:8080/research -H "Content-Type: application/json" -d '{"query": "What is agentic AI?"}'
```

## Agentic Workflow
- The system uses CrewAI to orchestrate three agents:
  - **Web Searcher:** Uses LinkUp to find relevant information (no sources/URLs in output).
  - **Research Analyst:** Synthesizes and verifies the information, focusing on depth and clarity (no citations or agent thoughts).
  - **Technical Writer:** Produces a clear, comprehensive markdown answer (no sources/citations or agent process steps).

## MCP Server Config Example

```
{
  "mcpServers": {
    "crew_research": {
      "command": "poetry",
      "args": [
        "run",
        "python",
        "Multi-Agent-deep-researcher-mcp-windows-linux/server.py"
      ],
      "env": {
        "LINKUP_API_KEY": "your_linkup_api_key_here"
      }
    }
  }
}
```

---
