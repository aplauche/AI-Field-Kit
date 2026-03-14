---
name: custom-reducer
description: "Use this when implementing custom state reducers in LangGraph, handling None values in state, or extending MessagesState with custom fields"
---

# Custom State Reducers

Define custom reducer functions to control how state fields are merged/updated.

## Example

```python
from operator import add
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import MessagesState


# The built-in 'add' can't handle None, but this custom one can!
def reduce_list(left: list | None, right: list | None) -> list:
    """Safely combine two lists, handling cases where either or both inputs might be None.

    Args:
        left (list | None): The first list to combine, or None.
        right (list | None): The second list to combine, or None.

    Returns:
        list: A new list containing all elements from both input lists.
               If an input is None, it's treated as an empty list.
    """
    if not left:
        left = []
    if not right:
        right = []
    return left + right


# Default state uses built-in add (fails on None)
class DefaultState(TypedDict):
    foo: Annotated[list[int], add]

# Custom reducer handles None gracefully
class CustomReducerState(TypedDict):
    foo: Annotated[list[int], reduce_list]


# --------------------------------------------
# Extend MessagesState with custom fields
# --------------------------------------------

# MessagesState already includes messages with add_messages reducer
class ExtendedMessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built
    my_list: Annotated[list[int], reduce_list]
```

## Key Points

- `Annotated[Type, reducer_fn]`: Attach reducer to state field
- Reducers receive `(left, right)` - current state and new value
- Handle `None` explicitly for optional fields
- `MessagesState` has built-in `add_messages` reducer for messages
- Extend `MessagesState` to add custom fields alongside messages
- Reducer return value becomes the new state value
