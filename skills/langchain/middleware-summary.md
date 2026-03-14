---
name: middleware-summary
description: "Use this when implementing message history summarization, trimming conversation history, or managing context length in LangChain agents"
---

# Message History Management

Built-in summarization and custom trimming strategies for managing conversation length.

## Example

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from langchain.messages import RemoveMessage
from typing import Any

from langchain.agents.middleware import before_agent


# Built in summary
agent = create_agent(
  model="gpt-5-nano",
  checkpointer=InMemorySaver(),
  middleware=[
    SummarizationMiddleware(
      model="gpt-4o-mini", # Use lightweight model for summary
      trigger=("tokens", 100), # at 100 tokens, run the summarizer
      keep=("messages", 1), # Only keep 1 message after summary runs
    )
  ]
)


# Custom trim strategy
@before_agent
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Remove all the tool messages from the state"""
    messages = state["messages"]

    # filter tool messages
    tool_messages = [m for m in messages if isinstance(m, ToolMessage)]

    # Return value should be instructions for HOW to mutate state, not directly mutated state
    # This returns essentially an array of command objects to run against the state graph
    return {"messages": [RemoveMessage(id=m.id) for m in tool_messages]}

agent = create_agent(
    model="gpt-5-nano",
    checkpointer=InMemorySaver(),
    middleware=[trim_messages],
)
```

## Key Points

- `SummarizationMiddleware`: Auto-summarize when token limit reached
- `trigger`: When to summarize - `("tokens", N)` or `("messages", N)`
- `keep`: How many messages to retain after summarization
- Use lightweight model for summarization to save costs
- `@before_agent`: Custom middleware runs before each agent call
- `RemoveMessage(id=m.id)`: Delete specific messages from state
