---
name: middleware-dynamic
description: "Use this when implementing dynamic prompts, dynamic tool availability, or dynamic model selection based on context in LangChain agents"
---

# Dynamic Middleware in LangChain

Adjust prompts, tools, and models at runtime based on context or state.

## Example

```python
from dataclasses import dataclass
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.middleware import wrap_model_call, ModelResponse
from typing import Callable

# --------------------------------
# Dynamic prompting
# --------------------------------

@dataclass
class LanguageContext:
    user_language: str = "English"

@dynamic_prompt
def user_language_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role."""
    user_language = request.runtime.context.user_language
    base_prompt = "You are a helpful assistant."

    if user_language != "English":
        return f"{base_prompt} only respond in {user_language}."
    elif user_language == "English":
        return base_prompt


agent = create_agent(
    model="gpt-5-nano",
    context_schema=LanguageContext,
    middleware=[user_language_prompt]
)

response = agent.invoke(
    {"message": [HumanMessage(content="Hello, how are you?")]},
    context=LanguageContext(user_language="Spanish")
)


# --------------------------------
# Dynamic tool calls
# --------------------------------

@dataclass
class UserRole:
    user_role: str = "external"

@wrap_model_call
def dynamic_tool_call(request: ModelRequest,
handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Dynamically call tools based on the runtime context"""
    user_role = request.runtime.context.user_role

    if user_role == "internal":
        pass # internal users get access to all tools
    else:
        tools = [web_search] # external users only get access to web search
        request = request.override(tools=tools)

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

from langchain.chat_models import init_chat_model

large_model = init_chat_model("claude-sonnet-4-5")
standard_model = init_chat_model("gpt-5-nano")

@wrap_model_call
def state_based_model(request: ModelRequest,
handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Select model based on State conversation length."""
    message_count = len(request.messages)

    if message_count > 10:
        model = large_model  # Long conversation - larger context
    else:
        model = standard_model  # Short conversation - efficient model

    request = request.override(model=model)
    return handler(request)


agent = create_agent(
    model="gpt-5-nano",
    middleware=[state_based_model],
    system_prompt="You are roleplaying a real life helpful office intern."
)
```

## Key Points

- `@dynamic_prompt`: Modify system prompt based on context
- `@wrap_model_call`: Intercept and modify the entire model request
- Use `request.override(tools=...)` to filter available tools
- Use `request.override(model=...)` to swap models mid-conversation
- Context is passed via `context=` parameter in invoke()
