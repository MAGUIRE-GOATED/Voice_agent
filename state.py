from typing import TypedDict , Annotated , Sequence
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class State(TypedDict):
    messages : Annotated[Sequence[AnyMessage],add_messages]
    next: str
    

