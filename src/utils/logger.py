"""
Logging utility for the LangChain project.

This module provides structured logging with metadata for each agent
and request tracking.
"""

import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime
from src.config import get_settings


class StructuredLogger:
    """
    Structured logger for the LangChain project.
    
    Provides logging with metadata and request tracking capabilities.
    """
    
    def __init__(self, name: str = "langchain_project"):
        """
        Initialize the structured logger.
        
        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self.settings = get_settings()
        
        # Configure logging level
        level = getattr(logging, self.settings.log_level.upper())
        self.logger.setLevel(level)
        
        # Add handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_request(
        self, 
        request_id: str, 
        message: str, 
        agent: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log a request with structured metadata.
        
        Args:
            request_id: Unique request identifier
            message: User message
            agent: Agent name
            metadata: Additional metadata
        """
        log_data = {
            "request_id": request_id,
            "agent": agent,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        self.logger.info(f"Request processed: {json.dumps(log_data)}")
    
    def log_error(
        self, 
        request_id: str, 
        error: Exception, 
        agent: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an error with structured metadata.
        
        Args:
            request_id: Unique request identifier
            error: Exception that occurred
            agent: Agent name where error occurred
            context: Additional context
        """
        log_data = {
            "request_id": request_id,
            "agent": agent,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {}
        }
        
        self.logger.error(f"Error occurred: {json.dumps(log_data)}")
    
    def log_agent_response(
        self, 
        request_id: str, 
        agent: str, 
        response: str,
        processing_time: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an agent response with performance metrics.
        
        Args:
            request_id: Unique request identifier
            agent: Agent name
            response: Agent response
            processing_time: Time taken to process in seconds
            metadata: Additional metadata
        """
        log_data = {
            "request_id": request_id,
            "agent": agent,
            "response_length": len(response),
            "processing_time_seconds": processing_time,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        self.logger.info(f"Agent response: {json.dumps(log_data)}")


# Global logger instance
_logger = None


def get_logger() -> StructuredLogger:
    """
    Get the global logger instance.
    
    Returns:
        StructuredLogger: The global logger
    """
    global _logger
    if _logger is None:
        _logger = StructuredLogger()
    return _logger 