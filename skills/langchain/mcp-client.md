---
name: mcp-client
description: "Use this when setting up MCP (Model Context Protocol) clients, connecting to MCP servers, or integrating external tools via MCP in LangChain"
---

# MCP Client Setup

Connect to multiple MCP servers (local and remote) to access tools, resources, and prompts.

## Example

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def main():
    client = MultiServerMCPClient(
      {
        # Local server via stdio
        "local_server": {
          "transport": "stdio",
          "command": "python",
          "args": ["mcp-server.py"],
        },
        # Third party MCP server
        "time": {
          "transport": "stdio",
          "command": "uvx",
          "args": [
            "mcp-server-time",
            "--local-timezone=America/New_York"
          ]
        },
        # HTTP-based MCP server
        "travel_server": {
          "transport": "streamable_http",
          "url": "https://mcp.kiwi.com"
        },
        # Built-in filesystem server
        "filesystem": {
          "command": "npx",
          "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/Users/username/Desktop",
            "/path/to/other/allowed/dir"
          ]
        }
      }
    )

    # Get all tools from all servers
    tools = await client.get_tools()

    # Get resources from specific server
    resources = await client.get_resources("local_server")

    # Get prompts from specific server
    prompt = await client.get_prompt("local_server", "prompt")
    prompt = prompt[0].content

    print(tools)
    print(resources)
    print(prompt)

    # Use tools with your agent
    # agent = create_agent(model=model, tools=tools)

if __name__ == "__main__":
    asyncio.run(main())
```

## Key Points

- `MultiServerMCPClient`: Connect to multiple MCP servers at once
- Transport types: `stdio` (local process) or `streamable_http` (remote)
- `get_tools()`: Retrieves all available tools from all servers
- `get_resources(server_name)`: Get resources from specific server
- `get_prompt(server_name, prompt_name)`: Get prompt templates
- Tools can be passed directly to `create_agent(tools=tools)`
