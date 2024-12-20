from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.stream_service import stream_graph_updates_sync
from fastapi.responses import JSONResponse

router = APIRouter()

@router.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    greeting = {"greeting": "Bienvenue à MigiBot 👩‍🏭"}
    await websocket.send_json(greeting)
    closed = False
    try:
        while True:
            user_input = await websocket.receive_text()
            for response in stream_graph_updates_sync(user_input):
                await websocket.send_json(response)
    except WebSocketDisconnect:
        print("Client disconnected")
        closed = True
    # ... rest of your websocket handling code ...

@router.get("/")
async def root():
    return {"message": "Hello World 2 "}

@router.get("/routes")
async def get_routes():
    routes = [{"path": route.path, "name": route.name} for route in router.routes]
    return JSONResponse(routes)