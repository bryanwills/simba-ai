from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
import uvicorn
from services.classes.state_class import State
from services.flow_graph import graph



app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# request input format
class Query(BaseModel):
    message: str


@app.post("/chat")
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
                    token = event["data"]["chunk"].content
                    yield token
           
        except Exception as e:
            yield f"Error: {str(e)}"
        finally:
            print("Done")

    return StreamingResponse(generate_response(), media_type="text/event-stream")


@app.get("/health")
async def health():
    """Check the api is running"""
    return {"status": "🤙"}
    

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="localhost",
        port=8000,
        reload=True
    )