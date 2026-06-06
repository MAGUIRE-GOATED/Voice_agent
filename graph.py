from agents import tavily
from agents import writer , researcher
from supervisor import supervisor
from langgraph.graph import StateGraph , START , END
from state import State
from typing import Literal
from langgraph.prebuilt import ToolNode 
from langgraph.checkpoint.memory import MemorySaver

builder = StateGraph(State)
builder.add_node("supervisor",supervisor)
builder.add_node("researcher",researcher)
builder.add_node("writer",writer)
builder.add_node("tools",ToolNode([tavily]))

def route_supervisor(state: State):
    return state["next"]  # returns "researcher", "writer", or "FINISH"


builder.add_conditional_edges("supervisor",route_supervisor,{"writer":"writer","researcher":"researcher","FINISH":END})

def route_researcher(state:State):
    last_message= state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "supervisor"

builder.add_conditional_edges("researcher",route_researcher,{"tools":"tools","supervisor":"supervisor"})
builder.add_edge("writer","supervisor") 
builder.add_edge("tools","researcher")
builder.add_edge(START,"supervisor")

memory = MemorySaver()
graph = builder.compile(name="Multi_agent",checkpointer=memory)