# Fully Local Supervisor Agent With Web Search
# CREDIT: Example was adapted from Langchain Foundations Course 

from dotenv import load_dotenv
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware.tool_call_limit import ToolCallLimitMiddleware
from langchain.tools import tool, ToolRuntime
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from tavily import TavilyClient
from typing import Dict, Any
import asyncio
from langgraph.types import Command


load_dotenv()

# This model is better at delegating tool calls
model = ChatOllama(
  model="qwen3:8b", temperature=0.1
)

# This model works better for web search
webSearchModel = ChatOllama(
  model="llama3.1:8b", temperature=0.1
)

tavily = TavilyClient()

class WeddingState(AgentState):
  origin: str
  destination: str
  guest_count: str
  colors: str
  year: str

async def main():

  # MCP Client
  client = MultiServerMCPClient(
    {
      "travel_server": {
        "transport": "streamable_http",
        "url": "https://mcp.kiwi.com"
      }
    }
  )

  mcp_tools = await client.get_tools()

  # Tool Declarations

  @tool
  def web_search(query:str) -> Dict[str, Any]:
    """Search the web with a query for information"""
    return tavily.search(query)
  
  # Enforce web_search limit programmatically for venue agent
  # venue_web_search_limiter = ToolCallLimitMiddleware(
  #   tool_name="web_search",      # Limit only web_search tool
  #   run_limit=3,                  # Max 3 calls per agent invocation
  #   exit_behavior="end"           # Stop immediately when limit reached
  # )

  # Sub Agent Declarations

  travel_agent = create_agent(
    model=model,
    tools=mcp_tools,
    system_prompt="""
    You are a travel agent. Search for flights to the desired destination wedding location.
    You are not allowed to ask any more follow up questions, you must find the best flight options based on the following criteria:
    - Price (lowest, economy class)
    - Duration (shortest)
    - Date (time of year which you believe is best for a wedding at this location)
    To make things easy, only look for one ticket, one way.
    Don't search extensively, just return the first flights you find matching the criteria.
    You will be given no extra information, only the origin and destination. It is your job to think critically about the best options.
    Once you have found the best options, let the user know your shortlist of options.
    """
  )

  # Venue - web search

  venue_agent = create_agent(
    model=webSearchModel,
    tools=[web_search],
    system_prompt="""
    You are a venue specialist. Search for venues in the desired location, and with the desired capacity.

    Search Strategy:
    1. Use web_search up to 3 times 
    2. Refine your queries if needed across your 3 searches
    3. After gathering results, analyze and recommend the best options

    Recommendation Criteria:
    - Price (lowest)
    - Capacity (at least as much as requested)
    - Reviews (highest)

    Provide your final venue recommendations based on the search results you obtain.
    """,
    # Option to limit depth of searches
    # middleware=[venue_web_search_limiter]
  )

  # Flowers - web search - based on colors

  florist_agent = create_agent(
    model=webSearchModel,
    tools=[web_search],
    system_prompt="""
    You are a professional florist. You take colors given to you and search the web to identify flowers that match each color. You should find 3 options of flower
    for each color provided. No follow up questions are allowed. Focus on flowers that are typically used for wedding ceremonies. Flowers do not need to match every color, just one.
    """
  )

  # Orchestrator Agent

  # First, create tooling for our subagents
  @tool
  async def search_flights(runtime: ToolRuntime) -> str:
    """Travel agent searches from flights from origin to desired wedding location"""
    origin = runtime.state["origin"]
    destination = runtime.state["destination"]
    year = runtime.state["year"]
    response = await travel_agent.ainvoke({"messages": [HumanMessage(content=f"Find flights from {origin} to {destination} in the year {year}")]})
    return response['messages'][-1].content
  
  @tool
  def search_venues(runtime: ToolRuntime) -> str:
    """Chooses a venue based on location and guest capacity"""
    capacity = runtime.state["guest_count"]
    destination = runtime.state["destination"]
    response = venue_agent.invoke({"messages": [HumanMessage(content=f"Find a wedding venue in {destination} with capacity for {capacity} guests.")]})
    return response['messages'][-1].content
  
  @tool
  def pick_flowers(runtime: ToolRuntime) -> str:
    """Florist agent will pick flowers based on colors"""
    colors = runtime.state["colors"]
    response = florist_agent.invoke({"messages": [HumanMessage(content=f"Find flowers that match the following colors: {colors}")]})
    return response['messages'][-1].content

  @tool
  def updateState(origin: str, destination: str, guest_count: str, colors: str, year:str, runtime: ToolRuntime) -> str:
    """Update the state when you have identified all of the following values: origin, destination, colors, year, guest_count"""
    return Command(update={
      "origin": origin,
      "destination": destination,
      "guest_count": guest_count,
      "colors": colors,
      "year": year,
      "messages": [ToolMessage("updated state", tool_call_id=runtime.tool_call_id)],
    })


  orchestrator = create_agent(
    model=model,
    tools=[search_flights, search_venues, pick_flowers, updateState],
    state_schema=WeddingState,
    checkpointer=InMemorySaver(),
    system_prompt="""
    You are a wedding coordinator. Delegate tasks to your specialists for flights, venues, and flowers.
    First find all the information you need to update the state. Once that is done you can delegate the tasks.
    Once you have received their answers, Show me all the details for the wedding.
    """
  )



# Workflow Runner
  response = await orchestrator.ainvoke(
    {"messages": [HumanMessage(content="I'm from London and I'd like a wedding in Paris for 100 guests in 2026, with blue and red as the color palette")]},
    {"configurable": {"thread_id": "1"}}
  )


  print(response)
  print()
  print("----------------------")
  print()
  print(response["messages"][-1].content)

if __name__ == "__main__":
  asyncio.run(main())