from state import State
from typing import Literal
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

llm = ChatGroq(model="llama-3.3-70b-versatile")
class RouteDecision(BaseModel):
    next: Literal["researcher", "writer", "FINISH"]

async def supervisor(state: State) -> dict:
    messages = state["messages"]
    
    has_tool_result = any(isinstance(m, ToolMessage) for m in messages)
    has_ai_article = any(
        isinstance(m, AIMessage) and not m.tool_calls and m.content and len(m.content) > 100
        for m in messages
    )

    if not has_tool_result:
        return {"next": "researcher"}
    elif not has_ai_article:
        return {"next": "writer"}
    else:
        return {"next": "FINISH"}