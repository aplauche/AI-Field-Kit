---
name: mcp-server
description: "Use this when creating MCP (Model Context Protocol) servers, exposing tools/resources/prompts via MCP, or building reusable AI tool servers"
---

# MCP Server Implementation

Create an MCP server that exposes tools, resources, and prompts to clients.

## Example

```python
from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from typing import Dict, Any
from requests import get


# Initialize MCP server
mcp = FastMCP("sample_mcp_server")

tavily_client = TavilyClient()


# Tool: Search the web
@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    results = tavily_client.search(query)
    return results


# Resource: Provide access to external docs
@mcp.resource("https://github.com/StoutLogic/acf-builder-wiki/blob/master/Field-Types.md")
def acf_readme():
    """
    Resource for accessing ACF Field Types Readme file
    """
    url = f"https://github.com/StoutLogic/acf-builder-wiki/blob/master/Field-Types.md"
    try:
        resp = get(url)
        return resp.text
    except Exception as e:
        return f"Error: {str(e)}"


# Prompt: Define a reusable prompt template
@mcp.prompt()
def prompt():
    """Figure out and recommend field types for custom blocks or templates"""
    return """
    You are a helpful assistant that recommends ACF field types and provides the code to register them
    for WordPress developers who provide you a description of a custom block or template.

    You can use the following tools/resources to answer user questions:
    - search_web: Search the web for information
    - acf_readme: Access the Field Types guide from github repo file

    If the user asks a question that is not related to WordPress or ACF you should respond:
    "I'm sorry, I can only answer questions about ACF and WordPress."

    You may try multiple tool and resource calls to answer the user's question.
    You may also ask clarifying questions to the user to better understand their question.
    """


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Key Points

- `FastMCP(name)`: Initialize server with a name
- `@mcp.tool()`: Expose functions as callable tools
- `@mcp.resource(uri)`: Expose data sources (files, APIs, docs)
- `@mcp.prompt()`: Define reusable prompt templates
- `mcp.run(transport="stdio")`: Start server (stdio or http)
- Docstrings become tool/resource descriptions for LLMs
