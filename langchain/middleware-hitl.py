from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command
from langchain.messages import HumanMessage


# HUMAN IN THE LOOP

# Use for sensitive actions, missing context, debugging

@tool
def read_email(runtime: ToolRuntime) -> str:
    """Read an email from the given address."""
    # take email from state
    return runtime.state["email"]

@tool
def send_email(body: str) -> str:
    """Send an email to the given address with the given subject and body."""
    # fake email sending
    return f"Email sent"


# Custom State with email key
class EmailState(AgentState):
    email: str

# Built in middleware for interupts 
agent = create_agent(
    model="gpt-5-nano",
    tools=[read_email, send_email],
    state_schema=EmailState,
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "read_email": False,
                "send_email": True,
            },
            description_prefix="Tool execution requires approval",
        ),
    ],
)


# Pretend run:

config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {
        "messages": [HumanMessage(content="Please read my email and send a response.")],
        "email": "Hi, I can't make the meeting tomorrow. Can we reschedule? Best, John."
    },
    config=config
)


print(response['__interrupt__'])

# Isolating the actual potential email 
print(response['__interrupt__'][0].value['action_requests'][0]['args']['body']) # body arg comes from our tool

# How to approve interupts:
response = agent.invoke(
    Command( 
        resume={"decisions": [{"type": "approve"}]}
    ), 
    config=config # Same thread ID to resume the paused conversation
)

pprint(response) # tool call proceeds and agent summarizes what happened.


# How to reject:
# This will result in another interupt with edits based on your explanation request
response = agent.invoke(
    Command(        
        resume={
            "decisions": [
                {
                    "type": "reject",
                    # An explanation of why the request was rejected
                    "message": "Tell John I will call him shortly."
                }
            ]
        }
    ), 
    config=config # Same thread ID to resume the paused conversation
    )   

pprint(response) # A new interupt will come back with the edits in place for approval - generally would be in a while loop.


# How to manually edit at the interupt point - this could in theory trigger calls to subagents as well
# Edit call immediatly proceeds with the new edited value - no extra interupt for approval
response = agent.invoke(
    Command(        
        resume={
            "decisions": [
                {
                    "type": "edit",
                    # Edited action with tool name and args
                    "edited_action": {
                        # Tool name to call.
                        # Will usually be the same as the original action.
                        "name": "send_email",
                        # Arguments to pass to the tool.
                        "args": {"body": "Impossible! I am leaving on a plane tomorrow."},
                    }
                }
            ]
        }
    ), 
    config=config # Same thread ID to resume the paused conversation
    )   

pprint(response)