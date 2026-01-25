# --------------------------------------------
# How to manage long convos
# --------------------------------------------

# --------------------------------------------
# Filtering state with a custom filter node
# --------------------------------------------
from langchain_openai import ChatOpenAI

from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import RemoveMessage

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")

# Nodes
def filter_messages(state: MessagesState):
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    # returns an array of RemoveMessage items - The built-in reducer knows how to handle these
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
# Limit messages to LLM, preserving state
# --------------------------------------------

# Node
def chat_model_node(state: MessagesState):
    # No modification of state, this just only passes through the latest message to LLM
    return {"messages": [llm.invoke(state["messages"][-1:])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)
graph = builder.compile()


# --------------------------------------------
# Using LangGraph Trim Options
# --------------------------------------------

from langchain_core.messages import trim_messages

# Node
def chat_model_node(state: MessagesState):
    # Call trim messages passing in state and params
    messages = trim_messages(
            state["messages"],
            max_tokens=100,
            strategy="last",
            token_counter=ChatOpenAI(model="gpt-4o"),
            allow_partial=False,
        )
    return {"messages": [llm.invoke(messages)]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)
graph = builder.compile()