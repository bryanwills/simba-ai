
# MigiBot

A Role-Based Retrieval Augmented Generation (RAG) System for Enterprise Information Management

## Overview
Mig iBot is a RAG system that retrieves information based on user roles and policies, ensuring secure and contextual access to enterprise knowledge.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # FastAPI endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Environment and app configuration
│   │   └── logger.py          # Logging configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py        # API request schemas
│   │   └── responses.py       # API response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py     # LLM integration (OpenAI, etc.)
│   │   ├── agent_service.py   # LangChain agents and tools
│   │   └── db_service.py      # Database operations
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py         # Utility functions
│   └── tests/
│       ├── test_api.py        # API endpoint tests
│       └── test_agents.py     # Agent logic tests
```

## Architecture Components

- Core Components
  - API Layer (api/): REST endpoints handling HTTP requests and responses
  - Service Layer (services/): Core business logic implementation
  - Models (models/): Data validation and schema definitions
  - Core (core/): System-wide configurations and utilities
- Key Services
  - LLM Service: Manages direct interactions with Language Models
  - Agent Service: Orchestrates LangChain agents and tools
  - Database Service: Handles data persistence and retrieval

## Testing

- Comprehensive test suite covering:
  - API endpoint functionality
  - Agent behavior and interactions
  - Integration testing

## Getting Started

1. Clone the repository
2. Install dependencies
3. Run the application

