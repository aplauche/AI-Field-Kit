from dataclasses import dataclass
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage

from dotenv import load_dotenv

load_dotenv()


# Custom context for the agent overall
@dataclass
class EmailContext:
  email_address: str = "test@example.com"
  password: str = "password123"

# Extend typical agent state (w/ messages) to include an auth boolean
class AuthenticatedState(AgentState):
  authenticated: bool

# Build out our tools
@tool
def check_inbox() -> str:
  """Check the user's inbox for emails"""
  # API call would go here - mocked for demo
  return """
  Hi,
  Are you free to grab a coffee next week?
  Cheers, John
  """

@tool 
def send_email(to: str, subject: str, body: str) -> str:
  """Send an email response"""
  # API call would go here - mocked for demo
  return f"Email sent to {to} \n\nwith subject: {subject} \n\nand body: {body}"

@tool
def authenticate(email: str, password: str, runtime: ToolRuntime) -> Command:
  """Authenticate the user with the given email and password"""
  if email == runtime.context.email_address and password == runtime.context.password:
    # we return the command to update with new state
    return Command(update={
      "authenticated": True,
      "messages": [ToolMessage("Authenticated!", tool_call_id=runtime.tool_call_id)]
    })
  else:
    # remember we only pass the new message to add on through the command - no mutation of state
    return Command(update={
      "authenticated": False,
      "messages": [ToolMessage("Authentication Failed!", tool_call_id=runtime.tool_call_id)]
    })


# Now we need to wrap our model call with a middleware to gate various tools
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

# This boilerplate is messy, but it is what it is...
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


# Dynamic prompt is a nice-to-have, likely would run without in this case
from langchain.agents.middleware import dynamic_prompt

@dynamic_prompt
def prompt(request: ModelRequest) -> str:
  """Generate prompt based on authenticated state"""
  authenticated = request.state.get("authenticated")

  if authenticated:
    return "You are an email assistant that helps check and respond to emails."
  else:
    return "You are an assistant that handles authentication for email users."


# Now let's spin up this agent!
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware


agent = create_agent(
  "gpt-5-nano",
  tools=[authenticate, check_inbox, send_email], # give all middleware
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
        "send_email": True,
      }
    )
  ]
)


# Test invokations:

from langchain.messages import HumanMessage

config = {"configurable": {"thread_id": "3"}}

ctx = EmailContext()

response = agent.invoke(
    {"messages": [HumanMessage(content="Hello")]},
    context=ctx,
    config=config
)

print(response['messages'][-1].content)

response = agent.invoke(
    {"messages": [HumanMessage(content="email: test@example.com, password: password123")]},
    context=ctx,
    config=config
)

print(response['messages'][-1].content)

response = agent.invoke(
    {"messages": [HumanMessage(content="Please check my email")]},
    context=ctx,
    config=config
)

print(response['messages'][-1].content)

response = agent.invoke(
    {"messages": [HumanMessage(content="Please send a response saying no")]},
    context=ctx,
    config=config
)

from pprint import pprint

pprint(response)

print(response['__interrupt__'][0].value['action_requests'][0]['args']['body'])

response = agent.invoke(
    Command( 
        resume={"decisions": [{"type": "approve"}]}  # or "reject"
    ), 
    config=config # Same thread ID to resume the paused conversation
)

print(response["messages"][-1].content)

pprint(response)