---
name: supervisor-agent
description: "Use this when implementing multi-agent orchestration, supervisor patterns, or delegating tasks to specialized sub-agents in LangChain"
---

# Supervisor Agent Pattern

Orchestrate multiple specialized sub-agents with a supervisor that delegates tasks.

## Example

```python
from dotenv import load_dotenv
from langchain.agents import create_agent, AgentState
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

model = ChatOllama(model="qwen3:8b", temperature=0.1)
webSearchModel = ChatOllama(model="llama3.1:8b", temperature=0.1)
tavily = TavilyClient()

class WeddingState(AgentState):
  origin: str
  destination: str
  guest_count: str
  colors: str
  year: str

async def main():
  # MCP Client for external tools
  client = MultiServerMCPClient({
    "travel_server": {
      "transport": "streamable_http",
      "url": "https://mcp.kiwi.com"
    }
  })
  mcp_tools = await client.get_tools()

  @tool
  def web_search(query:str) -> Dict[str, Any]:
    """Search the web with a query for information"""
    return tavily.search(query)

  # Sub-agent: Travel
  travel_agent = create_agent(
    model=model,
    tools=mcp_tools,
    system_prompt="""
    You are a travel agent. Search for flights to the desired destination wedding location.
    Only look for one ticket, one way. Return the first flights matching criteria.
    """
  )

  # Sub-agent: Venue
  venue_agent = create_agent(
    model=webSearchModel,
    tools=[web_search],
    system_prompt="""
    You are a venue specialist. Search for venues in the desired location.
    Use web_search up to 3 times. Recommend based on price, capacity, reviews.
    """
  )

  # Sub-agent: Florist
  florist_agent = create_agent(
    model=webSearchModel,
    tools=[web_search],
    system_prompt="""
    You are a professional florist. Find 3 flower options for each color provided.
    Focus on flowers typically used for wedding ceremonies.
    """
  )

  # Tools that delegate to sub-agents
  @tool
  async def search_flights(runtime: ToolRuntime) -> str:
    """Travel agent searches for flights"""
    origin = runtime.state["origin"]
    destination = runtime.state["destination"]
    year = runtime.state["year"]
    response = await travel_agent.ainvoke({
      "messages": [HumanMessage(content=f"Find flights from {origin} to {destination} in {year}")]
    })
    return response['messages'][-1].content

  @tool
  def search_venues(runtime: ToolRuntime) -> str:
    """Chooses a venue based on location and guest capacity"""
    capacity = runtime.state["guest_count"]
    destination = runtime.state["destination"]
    response = venue_agent.invoke({
      "messages": [HumanMessage(content=f"Find venue in {destination} for {capacity} guests.")]
    })
    return response['messages'][-1].content

  @tool
  def pick_flowers(runtime: ToolRuntime) -> str:
    """Florist agent will pick flowers based on colors"""
    colors = runtime.state["colors"]
    response = florist_agent.invoke({
      "messages": [HumanMessage(content=f"Find flowers matching: {colors}")]
    })
    return response['messages'][-1].content

  @tool
  def updateState(origin: str, destination: str, guest_count: str, colors: str, year:str, runtime: ToolRuntime) -> str:
    """Update the state with wedding details"""
    return Command(update={
      "origin": origin,
      "destination": destination,
      "guest_count": guest_count,
      "colors": colors,
      "year": year,
      "messages": [ToolMessage("updated state", tool_call_id=runtime.tool_call_id)],
    })

  # Orchestrator
  orchestrator = create_agent(
    model=model,
    tools=[search_flights, search_venues, pick_flowers, updateState],
    state_schema=WeddingState,
    checkpointer=InMemorySaver(),
    system_prompt="""
    You are a wedding coordinator. Delegate tasks to specialists.
    First gather all info to update state, then delegate tasks.
    """
  )

  response = await orchestrator.ainvoke(
    {"messages": [HumanMessage(content="Wedding in Paris for 100 guests, blue and red colors")]},
    {"configurable": {"thread_id": "1"}}
  )

if __name__ == "__main__":
  asyncio.run(main())
```

## Key Points

- Create specialized sub-agents with focused system prompts
- Orchestrator has tools that invoke sub-agents
- Sub-agents access shared state via `runtime.state`
- Use `updateState` tool to collect info before delegation
- Different models for different tasks (e.g., web search vs tool calling)
- MCP integration for external service tools
