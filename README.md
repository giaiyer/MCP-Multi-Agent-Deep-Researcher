# MCP Multi-Agent Deep Researcher 

A multi-agent research system built on the Model Context Protocol (MCP), using CrewAI for agent orchestration, LinkUp for deep web search, and the phi3 model (via Ollama) for synthesis and writing. Exposed as an MCP-compliant server, it delivers direct, comprehensive answers.

## Features
- MCP-Compliant Server for seamless integration into any agent ecosystem
- CrewAI Agent Orchestration (Web Searcher → Analyst → Technical Writer)
- LinkUp API for deep web search
- Local phi3 Model (Ollama) for writing, synthesis, and reasoning
- Returns clear, structured answers

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
  - **Web Searcher:** Uses LinkUp to find relevant information.
  - **Research Analyst:** Synthesizes and verifies the information, focusing on depth and clarity.
  - **Technical Writer:** Produces a clear, comprehensive markdown answer.

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
