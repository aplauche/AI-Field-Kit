


# Rather than before/after model mods - this middleware actually adjust the model and model request itself

from dataclasses import dataclass
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.middleware import wrap_model_call, ModelResponse
from typing import Callable

# --------------------------------
# Dynamic prompting
# --------------------------------

# Create some context to draw from
@dataclass
class LanguageContext:
    user_language: str = "English"

# We can use dynamic prompt to magically adjust system prompt based on context
@dynamic_prompt
def user_language_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role."""
    user_language = request.runtime.context.user_language
    base_prompt = "You are a helpful assistant."

    if user_language != "English":
        return f"{base_prompt} only respond in {user_language}."
    elif user_language == "English":
        return base_prompt



# Create the agent with our custom context and middlware
agent = create_agent(
    model="gpt-5-nano",
    context_schema=LanguageContext,
    middleware=[user_language_prompt]
)

# Example run - modifying context:
response = agent.invoke(
    {"message": [HumanMessage(content="Hello, how are you?")]},
    context=LanguageContext(user_language="Spanish")
)

print(response["messages"][-1].content)



# --------------------------------
# Dynamic tool calls
# --------------------------------

@dataclass
class UserRole:
    user_role: str = "external"

tavily_client = TavilyClient()

db = SQLDatabase.from_uri("sqlite:///resources/Chinook.db")

# Here are our standard tools:

@tool
def web_search(query: str) -> Dict[str, Any]:

    """Search the web for information"""

    return tavily_client.search(query)

@tool
def sql_query(query: str) -> str:

    """Obtain information from the database using SQL queries"""

    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"

@wrap_model_call
def dynamic_tool_call(request: ModelRequest, 
handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    # All these args are automatically provided at run time

    """Dynamically call tools based on the runtime context"""
    # Pull out context from request runtime
    user_role = request.runtime.context.user_role
    
    if user_role == "internal":
        pass # internal users get access to all tools
    else:
        tools = [web_search] # external users only get access to web search
        request = request.override(tools=tools) # override the tools on the request

    # return and call the handler with the new request
    return handler(request)



agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search, sql_query],
    middleware=[dynamic_tool_call],
    context_schema=UserRole
)



# --------------------------------
# Dynamic Model Swapping
# --------------------------------

from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model
from typing import Callable

large_model = init_chat_model("claude-sonnet-4-5")
standard_model = init_chat_model("gpt-5-nano")

# Same deal - wrap_model_call auto-passes in reques and handler callable - looks more complicated than it is
@wrap_model_call
def state_based_model(request: ModelRequest, 
handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Select model based on State conversation length."""
    # request.messages is a shortcut for request.state["messages"]
    message_count = len(request.messages)  

    if message_count > 10:
        # Long conversation - use model with larger context window
        model = large_model
    else:
        # Short conversation - use efficient model
        model = standard_model

    request = request.override(model=model)  

    return handler(request)

# Example call
agent = create_agent(
    model="gpt-5-nano",
    middleware=[state_based_model],
    system_prompt="You are roleplaying a real life helpful office intern."
)

# intern will upgrade to larger model when conversation continues for too long to stay helpful