---
name: middleware-hitl
description: "Use this when implementing human-in-the-loop approval workflows, tool call interrupts, or user confirmation for sensitive actions in LangChain"
---

# Human-in-the-Loop Middleware

Interrupt agent execution for human approval on sensitive tool calls.

## Example

```python
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command
from langchain.messages import HumanMessage


@tool
def read_email(runtime: ToolRuntime) -> str:
    """Read an email from the given address."""
    return runtime.state["email"]

@tool
def send_email(body: str) -> str:
    """Send an email to the given address with the given subject and body."""
    return f"Email sent"


class EmailState(AgentState):
    email: str

# Built in middleware for interrupts
agent = create_agent(
    model="gpt-5-nano",
    tools=[read_email, send_email],
    state_schema=EmailState,
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "read_email": False,
                "send_email": True,  # Interrupt before sending
            },
            description_prefix="Tool execution requires approval",
        ),
    ],
)

config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {
        "messages": [HumanMessage(content="Please read my email and send a response.")],
        "email": "Hi, I can't make the meeting tomorrow. Can we reschedule? Best, John."
    },
    config=config
)

# Check for interrupt
print(response['__interrupt__'])
print(response['__interrupt__'][0].value['action_requests'][0]['args']['body'])

# How to APPROVE:
response = agent.invoke(
    Command(
        resume={"decisions": [{"type": "approve"}]}
    ),
    config=config
)

# How to REJECT with feedback:
response = agent.invoke(
    Command(
        resume={
            "decisions": [
                {
                    "type": "reject",
                    "message": "Tell John I will call him shortly."
                }
            ]
        }
    ),
    config=config
)

# How to EDIT the action directly:
response = agent.invoke(
    Command(
        resume={
            "decisions": [
                {
                    "type": "edit",
                    "edited_action": {
                        "name": "send_email",
                        "args": {"body": "Impossible! I am leaving on a plane tomorrow."},
                    }
                }
            ]
        }
    ),
    config=config
)
```

## Key Points

- `interrupt_on`: Dict mapping tool names to boolean (True = require approval)
- Interrupt response contains `__interrupt__` with pending action details
- Resume with `approve`, `reject` (with message), or `edit` (with new args)
- Use same `thread_id` to resume paused conversations
- Rejection triggers agent to retry with your feedback
