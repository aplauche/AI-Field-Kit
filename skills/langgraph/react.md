---
name: langgraph-react
description: "Use this when implementing ReAct agents with LangGraph, building tool-calling graphs, or creating agents with memory using StateGraph"
---

# ReAct Pattern with LangGraph

Build a ReAct agent using LangGraph's StateGraph with tool calling and memory.

## Example

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver


# --------------------------------------------
# Setup tools and LLM
# --------------------------------------------

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)


# --------------------------------------------
# Create the assistant with state
# --------------------------------------------

sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# --------------------------------------------
# Build the Graph
# --------------------------------------------

builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message is a tool call -> route to tools
    # If the latest message is not a tool call -> route to END
    tools_condition,
)
builder.add_edge("tools", "assistant")


# --------------------------------------------
# Add Memory
# --------------------------------------------

memory = MemorySaver()
react_graph_with_memory = builder.compile(checkpointer=memory)


# --------------------------------------------
# Test it
# --------------------------------------------

config = {"configurable": {"thread_id": "1"}}

messages = [HumanMessage(content="Add 3 and 4.")]
messages = react_graph_with_memory.invoke({"messages": messages}, config)

# Memory persists - can reference previous result
messages = [HumanMessage(content="Multiply that by 2.")]
messages = react_graph_with_memory.invoke({"messages": messages}, config)
```

## Key Points

- `bind_tools(tools)`: Attach tools to LLM for function calling
- `MessagesState`: Built-in state with messages list + reducer
- `ToolNode(tools)`: Prebuilt node that executes tool calls
- `tools_condition`: Routes to tools node or END based on response
- `MemorySaver()`: In-memory checkpointer for conversation persistence
- Use `thread_id` in config to maintain separate conversations
