---
name: rag-query-rewrites
description: "Use this when implementing RAG with query rewriting, conversation-aware retrieval, or optimizing semantic search queries"
---

# RAG with Query Rewriting

Rewrite user queries to improve retrieval quality, especially in multi-turn conversations.

## Example

```python
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

CHROMA_PATH = "chroma"
MODEL = "qwen2:7b"

RAG_PROMPT = """
You are a helpful assistant. Use the retrieved context and prior conversation
to answer the user's latest question. Be concise and cite sources if relevant.

Context:
{context}

Conversation so far:
{history}

User's question:
{question}

Answer:
"""

REWRITE_PROMPT = """
You are a query rewriter. Your job is to rewrite ONLY the user's *latest question*
into a standalone, fully self-contained query that can be used for document retrieval.

Use prior questions *only as background context*, but always make sure the
rewritten query reflects the LATEST user question — not earlier ones.

Prior questions (for background only):
{history}

LATEST user question: {question}

FOR EXAMPLE:
Conversation:
User: Who wrote The Hobbit?
Assistant: J.R.R. Tolkien.
Latest question: When was it published?
Rewritten query: When was The Hobbit published?

Rewritten standalone query:
"""


def build_prompt(history, context, question):
    history_str = "\n".join([f"User: {h['question']}\nAssistant: {h['answer']}" for h in history])
    prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT)
    return prompt_template.format(context=context, history=history_str, question=question)


def rewrite_query(llm, history, question):
    # Only use the last few user questions to alter query
    short_history = history[-2:]
    history_str = "\n".join([f"User: {h['question']}" for h in short_history])
    prompt_template = ChatPromptTemplate.from_template(REWRITE_PROMPT)
    prompt = prompt_template.format(history=history_str, question=question)

    return llm.invoke(prompt).strip()


def run_chat():
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    llm = OllamaLLM(model=MODEL)

    history = []

    while True:
        query_text = input("You: ").strip()

        if query_text.lower() in ["exit", "quit", "q"]:
            break

        # Step 1: Rewrite query for retrieval
        retrieval_query = rewrite_query(llm, history, query_text)

        # Step 2: Retrieve context with rewritten query
        results = db.similarity_search_with_score(retrieval_query, k=5)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
        sources = [doc.metadata.get("id", None) for doc, _ in results]

        # Step 3: Build final answer prompt
        prompt = build_prompt(history, context_text, query_text)

        # Step 4: Model generates answer
        response_text = llm.invoke(prompt)

        # Step 5: Save turn
        history.append({"question": query_text, "answer": response_text})

        print(f"\n{response_text}\n")
        print(f"Sources: {sources}")
```

## Key Points

- Rewrite queries to be standalone (resolve pronouns like "it", "they")
- Use a small/fast model for rewriting, larger model for answering
- Only include recent history (2-3 turns) for rewriting context
- Track sources for citation and debugging
