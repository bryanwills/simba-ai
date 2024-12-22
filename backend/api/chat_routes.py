
from fastapi import APIRouter,Body
from services.classes.state_class import State
from services.flow_graph import graph
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

chat = APIRouter()    

# request input format
class Query(BaseModel):
    message: str


@chat.post("/chat")
async def invoke_graph(query: Query = Body(...)):
    """Invoke the graph workflow with a message"""

    
    config = {"configurable": {"thread_id": "2"}}
    state = State()
    state["messages"] = [("user", query.message)]
    state["question"] = query.message

    async def generate_response():
        try:
           
            
            async for event in graph.astream_events(
                state,
                version="v1",
                config=config
            ):
                
                if event["event"] == "on_chat_model_stream":
                    chunk = event["data"]["chunk"].content
                    yield chunk
           
        except Exception as e:
            yield f"Error: {str(e)}"
        finally:
            print("Done")

    return StreamingResponse(generate_response(), media_type="text/event-stream")


@chat.get("/status")
async def health():
    """Check the api is running"""
    return {"status": "🤙"}
    