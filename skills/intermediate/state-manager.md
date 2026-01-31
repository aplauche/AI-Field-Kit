---
name: state-manager
description: "Use this when implementing conversation state management, message history compression, or session-based chat with token limits"
---

# Conversation State Management

Manages conversation sessions with automatic history compression when token limits are reached.

## Example

```python
class LLMStateMgmt:
  def __init__(self, storage_backend, token_limit):
    self.storage = storage_backend
    self.memory = {}
    self.token_limit = token_limit

  async def create_session(self, session_id:str) -> Dict[str, Any]:
    """New conversation"""
    session_state = {
      "id": session_id,
      "messages": [],
      "context": {},
      "meta": {
        "created_at": datetime.now(),
        "token_count": 0
      }
    }
    await self.storage.set(session_id, session_state)
    return session_state

  async def update_convo(self, session_id:str, message:Dict):
    """Adds a message and updates token counts"""
    state = await self.storage.get(session_id)
    state["messages"].append(message)

    # Check length
    total_tokens = sum(msg.get("tokens", 0) for msg in state["messages"])
    if total_tokens > self.token_limit:
      state["messages"] = self._compress(state["messages"])

    state["metadata"]["token_count"] = total_tokens
    await self.storage.set(session_id, state["messages"])

  def _compress(self, messages):
    """Compress our history to save on tokens"""
    if len(messages) < 10:
      return messages # not enough messages for compression to make sense

    # Keep the system message if present
    sys_message = messages[0] if messages[0]["role"] == "system" else None

    # Keep most recent
    recent = messages[-4:]

    # Summarize the middle
    middle = messages[1:-4] if sys_message else messages[:-4]
    summary = self._summarize_messages(middle)

    compressed = []

    if sys_message:
      compressed.append(sys_message)
    compressed.append({"role": "system", "content": f"Previous context: {summary}"})
    compressed.extend(recent)

    return compressed

  def _summarize_messages(self, messages):
    """Implement a summarizer with your favorite low cost model"""
    return "This would be a summary of passed in messages..."
```

## Key Points

- Track token counts per message for accurate limits
- Preserve system message and recent messages during compression
- Summarize middle messages to maintain context
- Use a cheap/fast model for summarization
- Storage backend is abstracted - plug in Redis, SQLite, etc.
