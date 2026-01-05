## HOW TO SETUP TRACING AND STUDIO

Tracing is the simplest to setup. All you need is to add env variables:

```
# Langsmith keys
LANGSMITH_API_KEY = '****'
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=sample-project
```

To use langgraph studio requires a bit more setup:

First, install langgraph-cli and api

`uv pip install langgraph-api`

Then create a langgraph.json file:

```
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:agent"
  },
  "env": "./.env"
}
```

The agent should just be a pure declaration without checkpointers or prompts since langgraph studio handles all of this.

Run `uv run langraph dev` to start up the server.