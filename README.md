# migibot

we develop a RAG for our customers that is responsible of retreiving information based on roles and policies 

## Architecture 

backend/
    app/
        __init__.py
        main.py
        api/
            __init__.py
            routes.py      # Defines FastAPI endpoints
        core/
            __init__.py
            config.py       # Configuration handling (env variables, settings)
            logger.py       # Logging setup
        models/
            __init__.py
            requests.py     # Pydantic models for API request bodies
            responses.py    # Pydantic models for API responses
        services/
            __init__.py
            llm_service.py  # Interacting directly with the LLM (OpenAI, etc.)
            agent_service.py # Encapsulate agent logic (LangChain chains, tools)
            db_service.py   # Database-related functions (if applicable)
        utils/
            __init__.py
            helpers.py      # Helper functions not tied to business logic
        tests/
            test_api.py
            test_agents.py
            
## Summary of the Backend/App Architecture

- main.py: Entry point, sets up the FastAPI instance and includes routers.
- api/: Defines the HTTP endpoints; minimal logic, mostly request/response handling.
- core/: Holds configuration, logging, and other cross-cutting concerns.
- models/: Defines Pydantic models for data validation and schemas.
- services/: Where domain logic resides.
- llm_service.py: Direct interaction with the LLM.
-agent_service.py: Agent and chain logic using LangChain, orchestrating LLM calls and tools.
-utils/: Miscellaneous helper functions.
-tests/: Testing your application at various levels (unit, integration).
