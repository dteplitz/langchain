"""
Configuration module for the LangChain project.

This module handles all configuration settings including environment variables,
API keys, and application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        groq_api_key: API key for Groq LLM service
        database_url: SQLite database URL for memory storage
        log_level: Logging level for the application
        debug: Debug mode flag
    """
    
    groq_api_key: str = Field(..., env="GROQ_API_KEY", description="Groq API key")
    database_url: str = Field(
        default="sqlite:///./chat_memory.db", 
        env="DATABASE_URL", 
        description="SQLite database URL"
    )
    log_level: str = Field(default="INFO", env="LOG_LEVEL", description="Logging level")
    debug: bool = Field(default=False, env="DEBUG", description="Debug mode")
    
    # LLM Configuration
    model_name: str = Field(
        default="llama3-8b-8192", 
        env="MODEL_NAME", 
        description="Groq model name"
    )
    temperature: float = Field(
        default=0.7, 
        env="TEMPERATURE", 
        description="LLM temperature"
    )
    max_tokens: int = Field(
        default=1000, 
        env="MAX_TOKENS", 
        description="Maximum tokens for LLM response"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
_settings = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings: The application settings
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 