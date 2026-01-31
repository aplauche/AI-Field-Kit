---
name: email-agent-example
description: "Use this when implementing authentication-gated tools, tool access control, or building an email agent with human approval in LangChain"
---

# Email Agent with Authentication

Full example combining auth state, tool gating, dynamic prompts, and human-in-the-loop.

## Example

```python
from dataclasses import dataclass
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage, HumanMessage
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.agents.middleware import dynamic_prompt, HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from typing import Callable


# Context for credentials
@dataclass
class EmailContext:
  email_address: str = "test@example.com"
  password: str = "password123"

# State tracks auth status
class AuthenticatedState(AgentState):
  authenticated: bool

# Tools
@tool
def check_inbox() -> str:
  """Check the user's inbox for emails"""
  return """
  Hi,
  Are you free to grab a coffee next week?
  Cheers, John
  """

@tool
def send_email(to: str, subject: str, body: str) -> str:
  """Send an email response"""
  return f"Email sent to {to} with subject: {subject}"

@tool
def authenticate(email: str, password: str, runtime: ToolRuntime) -> Command:
  """Authenticate the user with the given email and password"""
  if email == runtime.context.email_address and password == runtime.context.password:
    return Command(update={
      "authenticated": True,
      "messages": [ToolMessage("Authenticated!", tool_call_id=runtime.tool_call_id)]
    })
  else:
    return Command(update={
      "authenticated": False,
      "messages": [ToolMessage("Authentication Failed!", tool_call_id=runtime.tool_call_id)]
    })


# Middleware: Gate tools based on auth
@wrap_model_call
def gated_tool_call(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
  """Only allow read/write if the user is authenticated"""
  authenticated = request.state.get("authenticated")

  if authenticated:
    tools = [check_inbox, send_email]
  else:
    tools = [authenticate]

  request = request.override(tools=tools)
  return handler(request)


# Middleware: Dynamic prompt based on auth
@dynamic_prompt
def prompt(request: ModelRequest) -> str:
  """Generate prompt based on authenticated state"""
  authenticated = request.state.get("authenticated")

  if authenticated:
    return "You are an email assistant that helps check and respond to emails."
  else:
    return "You are an assistant that handles authentication for email users."


# Create agent with all middleware
agent = create_agent(
  "gpt-5-nano",
  tools=[authenticate, check_inbox, send_email],
  checkpointer=InMemorySaver(),
  state_schema=AuthenticatedState,
  context_schema=EmailContext,
  middleware=[
    prompt,
    gated_tool_call,
    HumanInTheLoopMiddleware(
      interrupt_on={
        "authenticate": False,
        "check_inbox": False,
        "send_email": True,  # Require approval to send
      }
    )
  ]
)


# Usage flow
config = {"configurable": {"thread_id": "3"}}
ctx = EmailContext()

# 1. Initial greeting - agent asks for auth
response = agent.invoke(
    {"messages": [HumanMessage(content="Hello")]},
    context=ctx, config=config
)

# 2. Provide credentials
response = agent.invoke(
    {"messages": [HumanMessage(content="email: test@example.com, password: password123")]},
    context=ctx, config=config
)

# 3. Check inbox (now authenticated)
response = agent.invoke(
    {"messages": [HumanMessage(content="Please check my email")]},
    context=ctx, config=config
)

# 4. Send response - triggers interrupt
response = agent.invoke(
    {"messages": [HumanMessage(content="Please send a response saying no")]},
    context=ctx, config=config
)

# 5. Approve the send
response = agent.invoke(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config
)
```

## Key Points

- Combine multiple middleware: prompts, tool gating, HITL
- Context holds credentials, state holds auth status
- Tool gating changes available tools based on state
- Dynamic prompts adjust behavior pre/post authentication
- HITL on send_email prevents accidental sends
