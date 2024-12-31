from functools import lru_cache
from langchain_openai import ChatOpenAI
from core.config import settings, LLMConfig, VectorStoreConfig
from typing import Optional



@lru_cache()
def get_llm (LLMConfig: Optional[LLMConfig] = None):
    """
    Get a Language Learning Model (LLM) instance based on the configured provider.

    Args:
        LLMConfig: Configuration object containing provider, model name, API key and other settings

    Returns:
        A LangChain chat model instance (ChatOpenAI, ChatAnthropic etc.) configured with the specified settings

    Raises:
        ValueError: If an unsupported LLM provider is specified in the config

    Example:
        llm = get_llm(LLMConfig(
            provider="openai",
            model_name="gpt-4",
            api_key="...",
            temperature=0.7
        ))
    """
    if LLMConfig is not None:
        return ChatOpenAI(
            model_name=LLMConfig.model_name,
            temperature=LLMConfig.temperature,
            api_key=LLMConfig.api_key,
            streaming=LLMConfig.streaming
        )
    else:
        if settings.LLM.provider == "openai":
            try:
                return ChatOpenAI(
                    model_name=settings.LLM.model_name,
                    temperature=settings.LLM.temperature,
                    api_key=settings.LLM.api_key,
                    streaming=settings.LLM.streaming
                )
            except Exception as e:
                print(f"Error initializing LLM: {e}, openai is not supported")
                raise e
    
        elif settings.LLM.provider == "anthropic":
            return """ChatAnthropic(
                model=settings.LLM.model_name,
                temperature=settings.LLM.temperature,
                api_key=settings.LLM.api_key,
                streaming=settings.LLM.streaming
            )"""
    
    raise ValueError(f"Unsupported LLM provider: {settings.LLM.provider}")
