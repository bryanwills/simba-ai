from ..models.state_class import State
from ..core.flow_graph import graph

def stream_graph_updates_sync(user_input: str):
    config = {"configurable": {"thread_id": "2"}}
    state = State()
    state["messages"] = [("user", user_input)]
    state["question"] = user_input
    
    for output in graph.stream(state, config):
        for key, value in output.items():
            if key == "retrieve":
                response_data = {}
            elif key == "generate":
                response_data = {
                    "generation": value.get("generation"),
                }
            elif key == "transform_query":
                response_data = {
                    "suggestions": value.get("suggestions"),
                }
            else:
                response_data = {}
            
            yield response_data