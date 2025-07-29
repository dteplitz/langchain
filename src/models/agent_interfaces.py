"""
Pydantic models for agent interfaces.

This module defines the data models used for communication
between different agents in the chain.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CuratorOutput(BaseModel):
    """
    Output from the Curator Agent.
    
    Attributes:
        cleaned_message: The cleaned and normalized message
        is_valid: Boolean indicating if the message is valid
        validation_errors: List of validation errors
        content_type: Type of content
        confidence: Confidence score
    """
    cleaned_message: str = Field(..., description="Cleaned and normalized message")
    is_valid: bool = Field(..., description="Whether the message is valid")
    validation_errors: List[str] = Field(default_factory=list, description="List of validation errors")
    content_type: str = Field(..., description="Type of content (question, statement, etc.)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class SearchResult(BaseModel):
    """
    Search result from tools.
    
    Attributes:
        title: Result title
        content: Result content
        source: Source of the information
        url: Optional URL
    """
    title: str = Field(..., description="Result title")
    content: str = Field(..., description="Result content")
    source: str = Field(..., description="Source of the information")
    url: Optional[str] = Field(None, description="Optional URL")


class ToolExecutionResult(BaseModel):
    """
    Result from tool execution.
    
    Attributes:
        tool_name: Name of the tool executed
        success: Whether the execution was successful
        result: Tool execution result
        error: Error message if failed
        execution_time: Time taken to execute
    """
    tool_name: str = Field(..., description="Name of the tool executed")
    success: bool = Field(..., description="Whether the execution was successful")
    result: Any = Field(..., description="Tool execution result")
    error: Optional[str] = Field(None, description="Error message if failed")
    execution_time: float = Field(..., description="Time taken to execute in seconds")


class ProcessorInput(BaseModel):
    """
    Input for the Processor Agent.
    
    Attributes:
        message: User message
        chat_history: Previous conversation history
        curator_output: Output from curator agent
        tools_used: List of tools that were used
        search_results: Results from search operations
    """
    message: str = Field(..., description="User message")
    chat_history: List[Dict[str, Any]] = Field(default_factory=list, description="Previous conversation history")
    curator_output: CuratorOutput = Field(..., description="Output from curator agent")
    tools_used: List[str] = Field(default_factory=list, description="List of tools that were used")
    search_results: List[SearchResult] = Field(default_factory=list, description="Results from search operations")


class ProcessorOutput(BaseModel):
    """
    Output from the Processor Agent.
    
    Attributes:
        raw_response: Raw response from the processor
        tools_executed: List of tools that were executed
        search_performed: Whether search was performed
        response_quality: Quality score of the response
        processing_time: Time taken to process
    """
    raw_response: str = Field(..., description="Raw response from the processor")
    tools_executed: List[ToolExecutionResult] = Field(default_factory=list, description="List of tools that were executed")
    search_performed: bool = Field(default=False, description="Whether search was performed")
    response_quality: float = Field(..., ge=0.0, le=1.0, description="Quality score of the response")
    processing_time: float = Field(..., description="Time taken to process in seconds")


class FormatterInput(BaseModel):
    """
    Input for the Response Formatter Agent.
    
    Attributes:
        raw_response: Raw response from processor
        user_message: Original user message
        response_type: Type of response needed
        processor_output: Output from processor agent
    """
    raw_response: str = Field(..., description="Raw response from processor")
    user_message: str = Field(..., description="Original user message")
    response_type: str = Field(..., description="Type of response needed")
    processor_output: ProcessorOutput = Field(..., description="Output from processor agent")


class FormatterOutput(BaseModel):
    """
    Output from the Response Formatter Agent.
    
    Attributes:
        formatted_response: Formatted response for user
        response_structure: Structure used for formatting
        readability_score: Readability score of the response
        formatting_time: Time taken to format
    """
    formatted_response: str = Field(..., description="Formatted response for user")
    response_structure: str = Field(..., description="Structure used for formatting")
    readability_score: float = Field(..., ge=0.0, le=1.0, description="Readability score of the response")
    formatting_time: float = Field(..., description="Time taken to format in seconds")


class ChainMetadata(BaseModel):
    """
    Metadata for the entire chain execution.
    
    Attributes:
        stage: Current stage of development
        agents_used: List of agents that were used
        total_processing_time: Total time taken
        success: Whether the chain execution was successful
        errors: List of errors encountered
    """
    stage: str = Field(..., description="Current stage of development")
    agents_used: List[str] = Field(..., description="List of agents that were used")
    total_processing_time: float = Field(..., description="Total time taken")
    success: bool = Field(..., description="Whether the chain execution was successful")
    errors: List[str] = Field(default_factory=list, description="List of errors encountered")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of execution") 