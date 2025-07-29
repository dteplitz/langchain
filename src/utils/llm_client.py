"""
LLM Client utility for managing Groq integration.

This module provides a centralized way to create and manage LLM clients
with proper configuration and error handling.
"""

from typing import Optional, Dict, Any
from langchain_groq import ChatGroq
from langchain.schema.language_model import BaseLanguageModel
from src.config import get_settings


def create_llm_client(
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    model_name: Optional[str] = None
) -> BaseLanguageModel:
    """
    Create a Groq LLM client with the specified configuration.
    
    Args:
        temperature: Temperature for the LLM (0.0 to 2.0)
        max_tokens: Maximum tokens for the response
        model_name: Name of the Groq model to use
        
    Returns:
        BaseLanguageModel: Configured Groq chat model
        
    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    settings = get_settings()
    
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is required")
    
    # Use provided parameters or fall back to settings
    temp = temperature if temperature is not None else settings.temperature
    tokens = max_tokens if max_tokens is not None else settings.max_tokens
    model = model_name if model_name is not None else settings.model_name
    
    return ChatGroq(
        groq_api_key=settings.groq_api_key,
        model_name=model,
        temperature=temp,
        max_tokens=tokens
    )


def get_llm_config() -> Dict[str, Any]:
    """
    Get the current LLM configuration.
    
    Returns:
        Dict[str, Any]: Current LLM configuration
    """
    settings = get_settings()
    return {
        "model_name": settings.model_name,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens
    } 