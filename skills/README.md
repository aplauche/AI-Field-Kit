# AI Field Kit Skills

A collection of Claude skills for building AI applications. Drop these into your project to guide Claude in implementing common AI patterns.

## Installation

Copy the `skills/` folder to your project root or to `.claude/skills/` in your home directory.

```bash
# Option 1: Copy to project
cp -r skills/ /path/to/your/project/skills/

# Option 2: Copy to global Claude config
cp -r skills/ ~/.claude/skills/
```

## Skills Index

### Basic
Foundational patterns for working with LLMs.

| Skill | Description |
|-------|-------------|
| [error-handling](basic/error-handling.md) | Error translation and retry logic for LLM APIs |
| [model-selection](basic/model-selection.md) | Dynamic model switching based on task complexity |
| [token-counting](basic/token-counting.md) | Token management and cost estimation |
| [inheritance-pattern](basic/inheritance-pattern.md) | OOP architecture for AI services |
| [template-class](basic/template-class.md) | Prompt templating system |
| [dep-injection-for-testing](basic/dep-injection-for-testing.md) | Testable AI architecture with dependency injection |
| [quick-chroma-db](basic/quick-chroma-db.md) | Quick vector database setup with ChromaDB |
| [quick-llama-docs](basic/quick-llama-docs.md) | Document indexing with LlamaIndex |

### Intermediate
Production-ready patterns for AI systems.

| Skill | Description |
|-------|-------------|
| [chunking-strategies](intermediate/chunking-strategies.md) | Document chunking approaches for RAG |
| [rag-query-rewrites](intermediate/rag-query-rewrites.md) | Query rewriting for better retrieval |
| [agent-react](intermediate/agent-react.md) | ReAct agent pattern implementation |
| [state-manager](intermediate/state-manager.md) | Conversation state and history compression |

### LangChain
LangChain-specific implementations.

| Skill | Description |
|-------|-------------|
| [agent-state](langchain/agent-state.md) | Custom agent state with tool getters/setters |
| [middleware-dynamic](langchain/middleware-dynamic.md) | Dynamic prompts, tools, and model selection |
| [middleware-hitl](langchain/middleware-hitl.md) | Human-in-the-loop approval workflows |
| [middleware-summary](langchain/middleware-summary.md) | Message history summarization |
| [supervisor-agent](langchain/supervisor-agent.md) | Multi-agent orchestration pattern |
| [email-agent-example](langchain/email-agent-example.md) | Authentication + email workflow |
| [mcp-client](langchain/mcp-client.md) | Model Context Protocol client setup |
| [mcp-server](langchain/mcp-server.md) | MCP server implementation |

### LangGraph
Graph-based workflow orchestration.

| Skill | Description |
|-------|-------------|
| [react](langgraph/react.md) | ReAct pattern with LangGraph |
| [custom-reducer](langgraph/custom-reducer.md) | Custom state reducers |
| [pydantic-state](langgraph/pydantic-state.md) | Pydantic-based state validation |
| [summary](langgraph/summary.md) | Conversation summarization workflow |
| [trim-filter](langgraph/trim-filter.md) | Message filtering and trimming |

### ML/CSS
Machine learning fundamentals.

| Skill | Description |
|-------|-------------|
| [cosine-similarity](ml-css/cosine-similarity.md) | Vector similarity for semantic search |

## Usage

These skills are automatically invoked by Claude when relevant to your task. You can also explicitly request a skill by describing the pattern you need.
