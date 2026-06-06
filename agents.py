from dotenv import load_dotenv
load_dotenv()
from state import State
from typing import List , Dict , cast
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from datetime import datetime , UTC
from langchain_tavily import TavilySearch

llm = ChatGroq(model="llama-3.3-70b-versatile")
tavily = TavilySearch(max_results = 2)

async def researcher(state: State) -> Dict[str, List[AIMessage]]:
    model = llm.bind_tools([tavily])  # forces tool call
    system_prompt = """You are a Sports Researcher. 
    MANDATORY: You MUST call the tavily_search_results_json tool before responding. 
    This is not optional. Call the search tool NOW with a relevant query."""    
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_prompt}, *state["messages"]]
        ),
    )
    return {"messages": [response]}

async def writer(state:State)-> Dict[str,List[AIMessage]] :
    system_prompt = "you are a sports writer, write a clean article from the research in about 200-250 words.SYSTEM_TIME={system_time}"
    system_message = system_prompt.format(
        system_time = datetime.now(tz = UTC).isoformat()
    )
    response = cast(
        AIMessage,
        await llm.ainvoke(
            [{"role": "system", "content": system_message}, *state["messages"]]
        ),
    )
    return {"messages": [response]}









    

