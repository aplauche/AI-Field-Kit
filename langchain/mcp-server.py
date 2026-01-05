# Sample MCP Server

from dotenv import load_dotenv

load_dotenv()

from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from typing import Dict, Any
from requests import get


# MCP allows for tools, prompts, and resources

mcp = FastMCP("sample_mcp_server") # Name your MCP server

tavily_client = TavilyClient()


# Tool for searching the web
@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
    """Search the web for information"""

    results = tavily_client.search(query)

    return results


# Resources - provide access to langchain-ai repo files
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


# Prompt template
@mcp.prompt()
def prompt():
    """Figure out and reccommend field types for custom blocks or templates"""
    return """
    You are a helpful assistant that recommends ACF field types and provides the code to register them
    for WordPress developers who provide you a description of a custom block or template. 

    You can use the following tools/resources to answer user questions:
    - search_web: Search the web for information
    - acf_readme: Access the Field Types guide from github repo file

    If the user asks a question that is not related to WordPress or ACF you should respond: "I'm sorry, I can only answer questions about ACF and WordPress."

    You may try multiple tool and resource calls to answer the user's question.

    You may also ask clarifying questions to the user to better understand their question.
    """

if __name__ == "__main__":
    mcp.run(transport="stdio")