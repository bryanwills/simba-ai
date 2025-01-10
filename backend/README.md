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

#TODO:
Add libheif to docker 


## API Endpoints

- 'GET /': Root endpoint, returns a hello world message
- 'GET /routes': Lists all available routes
- 'WS /ws/stream': WebSocket endpoint for real-time communication

## Development

This project uses Poetry for dependency management and requires Python >=3.11,< 3.13.

## Environment Variables

Create a '.env' file in the root directory with your configuration.

for unstructured , run the following command:

for windows install pyenv 
```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
the python version is located in the .python-version file

```bash
pyenv install 
```

**only for windows**
Install poetry
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

```

exectue poetry for the first time
```bash
poetry install
poetry shell
```



