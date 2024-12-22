# MigiBot Backend

This is the backend service for MigiBot, built with FastAPI and WebSocket support.

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Run the FastAPI server:
```bash
poetry run uvicorn main:app --reload
```




## API Endpoints

- 'GET /': Root endpoint, returns a hello world message
- 'GET /routes': Lists all available routes
- 'WS /ws/stream': WebSocket endpoint for real-time communication

## Development

This project uses Poetry for dependency management and requires Python >=3.11,< 3.13.

## Environment Variables

Create a '.env' file in the root directory with your configuration.

for unstructured , run the following command:

```bash
pip install unstructured
```
