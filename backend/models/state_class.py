from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    question : str
    generation: str
    documents : list[str]
    filenames : list[str]
    llm_output : str
    suggestions: list[str]
    products:list[str]



graph_builder = StateGraph(State)