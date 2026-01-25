from operator import add
from typing import Annotated
from typing_extensions import TypedDict

# the built in 'add' can't handle the None type, but this custom one can!
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

class DefaultState(TypedDict):
    foo: Annotated[list[int], add]

class CustomReducerState(TypedDict):
    foo: Annotated[list[int], reduce_list]



# --------------------------------------------
# We can use this with built in MessagesState
# --------------------------------------------

# MessagesState includes the reducer funtionality

from langgraph.graph import MessagesState

# Use MessagesState, which includes the messages key with add_messages reducer
class ExtendedMessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built 
    my_list: Annotated[list[int], reduce_list]