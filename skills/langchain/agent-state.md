---
name: agent-state
description: "Use this when implementing custom agent state in LangChain, creating state getters/setters as tools, or managing persistent agent context"
---

# Custom Agent State with LangChain

Extend AgentState to add custom fields and create tools for reading/writing state.

## Example

```python
from langchain.agents import AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama


# Extend AgentState and define your state schema for langchain to understand
class CustomState(AgentState):
    favourite_colour: str

# Create tools for getters / setters
# ToolRuntime is passed automatically to tool calls and contains tool_call_id and additional metadata

# Setter
@tool
def update_favourite_colour(favourite_colour: str, runtime: ToolRuntime) -> Command:
  """Update the favourite colour of the user in the state once they've revealed it."""
  return Command(update={
    "favourite_colour": favourite_colour,
    "messages": [ToolMessage("Successfully updated favourite colour", tool_call_id=runtime.tool_call_id)]}
  )

# Getter
@tool
def read_favourite_colour(runtime: ToolRuntime) -> str:
  """Read the favourite colour of the user from the state."""
  try:
    return runtime.state["favourite_colour"]
  except KeyError:
    return "No favourite colour found in state"


# Now set up our agent with access to getters / setters
model = ChatOllama(model="llama3.1:8b", temperature=0)

agent = create_agent(
    model=model,
    tools=[update_favourite_colour, read_favourite_colour],
    checkpointer=InMemorySaver(),
    state_schema=CustomState
)

# Will run the setter to update state
response1 = agent.invoke(
    { "messages": [HumanMessage(content="My favourite colour is green")]},
    {"configurable": {"thread_id": "1"}}
)

# Will run the getter to access context for the question
response2 = agent.invoke(
    { "messages": [HumanMessage(content="What's my favourite colour?")]},
    {"configurable": {"thread_id": "1"}}
)
```

## Key Points

- Extend `AgentState` to define custom state fields
- `ToolRuntime` provides access to state and tool_call_id
- Setters return `Command(update={...})` to modify state
- Getters access `runtime.state["field_name"]`
- Use `InMemorySaver` checkpointer for thread persistence
