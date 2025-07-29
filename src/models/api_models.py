"""
Pydantic models for FastAPI request and response schemas.

This module defines the data models used in the API endpoints
with proper validation and documentation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request model for the chat endpoint.
    
    Attributes:
        message: User message to process
        session_id: Optional session identifier for conversation continuity
        debug: Enable debug mode for step-by-step inspection
    """
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=2000,
        description="User message to process"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session identifier for conversation continuity"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode for step-by-step inspection"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is the capital of France?",
                "session_id": "user_123",
                "debug": False
            }
        }


class ChatResponse(BaseModel):
    """
    Response model for the chat endpoint.
    
    Attributes:
        response: Processed response from the system
        session_id: Session identifier used
        request_id: Unique request identifier
        processing_time: Time taken to process the request
        metadata: Additional metadata about the processing
    """
    response: str = Field(..., description="Processed response from the system")
    session_id: str = Field(..., description="Session identifier used")
    request_id: str = Field(..., description="Unique request identifier")
    processing_time: float = Field(..., description="Time taken to process in seconds")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the processing"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "The capital of France is Paris.",
                "session_id": "user_123",
                "request_id": "req_456",
                "processing_time": 1.23,
                "metadata": {
                    "agent_used": "curator",
                    "confidence": 0.95
                }
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response model for API errors.
    
    Attributes:
        error: Error message
        error_type: Type of error
        request_id: Request identifier where error occurred
        timestamp: When the error occurred
    """
    error: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Type of error")
    request_id: str = Field(..., description="Request identifier where error occurred")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the error occurred")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid input message",
                "error_type": "ValidationError",
                "request_id": "req_456",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class HealthResponse(BaseModel):
    """
    Health check response model.
    
    Attributes:
        status: Service status
        timestamp: Current timestamp
        version: API version
    """
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Current timestamp")
    version: str = Field(..., description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T12:00:00Z",
                "version": "1.0.0"
            }
        } 