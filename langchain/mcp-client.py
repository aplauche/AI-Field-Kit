from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def main():
    client = MultiServerMCPClient(
      {
        "local_server": {
          "transport": "stdio", # stdio or streamable_http depending on server
          "command": "python",
          "args": ["mcp-server.py"],
        },
        # Third party can be added as well
        "time": {
          "transport": "stdio",
          "command": "uvx",
          "args": [
            "mcp-server-time",
            "--local-timezone=America/New_York"
          ]
        },
        # example http
        "travel_server": {
          "transport": "streamable_http",
          "url": "https://mcp.kiwi.com"
        },
        # Built in filesystem
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

    # get tools
    tools = await client.get_tools()

    # get resources
    resources = await client.get_resources("local_server")

    # get prompts
    prompt = await client.get_prompt("local_server", "prompt")
    prompt = prompt[0].content

    print(tools)
    print(resources)
    print(prompt)

    # RUN YOUR ACTUAL AGENT CODE HERE

    return

if __name__ == "__main__":
    asyncio.run(main())