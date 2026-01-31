---
name: trim-filter
description: "Use this when implementing message filtering, trimming conversation history, or limiting context length in LangGraph agents"
---

# Message Filtering and Trimming

Multiple approaches to manage conversation length: filter nodes, slicing, and trim_messages.

## Example

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import RemoveMessage, trim_messages

llm = ChatOpenAI(model="gpt-4o")


# --------------------------------------------
# Approach 1: Filter node that modifies state
# --------------------------------------------

def filter_messages(state: MessagesState):
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    # Returns RemoveMessage items - the built-in reducer handles these
    return {"messages": delete_messages}

def chat_model_node(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("filter", filter_messages)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "filter")
builder.add_edge("filter", "chat_model")
builder.add_edge("chat_model", END)
graph = builder.compile()


# --------------------------------------------
# Approach 2: Limit messages to LLM only (preserve full state)
# --------------------------------------------

def chat_model_node(state: MessagesState):
    # Only pass the latest message to LLM, but state keeps all messages
    return {"messages": [llm.invoke(state["messages"][-1:])]}

builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)
graph = builder.compile()


# --------------------------------------------
# Approach 3: Using trim_messages utility
# --------------------------------------------

def chat_model_node(state: MessagesState):
    # Trim messages to token limit
    messages = trim_messages(
            state["messages"],
            max_tokens=100,
            strategy="last",  # Keep last messages
            token_counter=ChatOpenAI(model="gpt-4o"),
            allow_partial=False,
        )
    return {"messages": [llm.invoke(messages)]}

builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)
graph = builder.compile()
```

## Key Points

- **Filter node**: Use `RemoveMessage(id=m.id)` to delete from state
- **Slice in node**: `state["messages"][-N:]` limits LLM input only
- **trim_messages**: Token-aware trimming with strategies
- `strategy="last"`: Keep most recent messages
- `strategy="first"`: Keep oldest messages
- Filter node permanently removes; slicing preserves full history
