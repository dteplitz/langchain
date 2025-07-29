"""
Curator Agent implementation.

This agent is responsible for cleaning and validating user input
before it's processed by other agents in the chain.
"""

import json
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain.schema import BaseOutputParser
from langchain.schema.runnable import Runnable
from src.utils.llm_client import create_llm_client
from src.utils.logger import get_logger
from src.prompts.curator_prompts import get_curator_prompt, format_chat_history


class CuratorOutput(BaseModel):
    """
    Output model for the Curator Agent.
    
    Attributes:
        cleaned_message: The cleaned and normalized message
        is_valid: Boolean indicating if the message is valid
        validation_errors: List of validation errors
        content_type: Type of content
        confidence: Confidence score
    """
    cleaned_message: str = Field(..., description="Cleaned and normalized message")
    is_valid: bool = Field(..., description="Whether the message is valid")
    validation_errors: list = Field(default_factory=list, description="List of validation errors")
    content_type: str = Field(..., description="Type of content (question, statement, etc.)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class CuratorOutputParser(BaseOutputParser[CuratorOutput]):
    """
    Output parser for the Curator Agent.
    
    Parses JSON responses from the LLM into structured CuratorOutput objects.
    """
    
    def parse(self, text: str) -> CuratorOutput:
        """
        Parse the LLM response into a CuratorOutput object.
        
        Args:
            text: Raw LLM response text
            
        Returns:
            CuratorOutput: Parsed output object
            
        Raises:
            ValueError: If the response cannot be parsed
        """
        try:
            # Clean the response text
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            # Parse JSON
            data = json.loads(text.strip())
            
            # Validate and create output
            return CuratorOutput(
                cleaned_message=data.get("cleaned_message", ""),
                is_valid=data.get("is_valid", False),
                validation_errors=data.get("validation_errors", []),
                content_type=data.get("content_type", "unknown"),
                confidence=data.get("confidence", 0.0)
            )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise ValueError(f"Failed to parse curator response: {e}")


class CuratorAgent(Runnable):
    """
    Curator Agent for cleaning and validating user input.
    
    This agent processes user messages to ensure they are clean,
    valid, and appropriate for further processing.
    """
    
    def __init__(
        self,
        temperature: float = 0.1,
        max_tokens: int = 500,
        verbose: bool = False
    ):
        """
        Initialize the Curator Agent.
        
        Args:
            temperature: LLM temperature for response generation
            max_tokens: Maximum tokens for response
            verbose: Enable verbose logging
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.verbose = verbose
        self.logger = get_logger()
        
        # Initialize LLM and components
        self.llm = create_llm_client(
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.prompt = get_curator_prompt()
        self.output_parser = CuratorOutputParser()
        
        # Create the runnable chain
        self.chain = self.prompt | self.llm | self.output_parser
    
    def invoke(
        self, 
        input_data: Dict[str, Any], 
        config: Optional[Dict[str, Any]] = None
    ) -> CuratorOutput:
        """
        Process a user message through the curator agent.
        
        Args:
            input_data: Input dictionary containing message and chat_history
            config: Optional configuration
            
        Returns:
            CuratorOutput: Curated and validated output
        """
        start_time = time.time()
        request_id = input_data.get("request_id", "unknown")
        message = input_data.get("message", "")
        chat_history = input_data.get("chat_history", [])
        
        # Log the request
        self.logger.log_request(
            request_id=request_id,
            message=message,
            agent="curator",
            metadata={"temperature": self.temperature, "max_tokens": self.max_tokens}
        )
        
        try:
            # Format chat history
            formatted_history = format_chat_history(chat_history)
            
            # Prepare input for the chain
            chain_input = {
                "message": message,
                "chat_history": formatted_history
            }
            
            # Run the chain
            result = self.chain.invoke(chain_input, config or {})
            
            # Log the response
            processing_time = time.time() - start_time
            self.logger.log_agent_response(
                request_id=request_id,
                agent="curator",
                response=str(result),
                processing_time=processing_time,
                metadata={"is_valid": result.is_valid, "confidence": result.confidence}
            )
            
            if self.verbose:
                print(f"[Curator] Input: {message}")
                print(f"[Curator] Output: {result}")
                print(f"[Curator] Processing time: {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            # Log the error
            processing_time = time.time() - start_time
            self.logger.log_error(
                request_id=request_id,
                error=e,
                agent="curator",
                context={"input": input_data}
            )
            
            # Return a fallback response
            return CuratorOutput(
                cleaned_message=message,
                is_valid=False,
                validation_errors=[f"Curator processing failed: {str(e)}"],
                content_type="error",
                confidence=0.0
            )
    
    def debug(self, message: str, chat_history: list = None) -> CuratorOutput:
        """
        Debug method for step-by-step inspection.
        
        Args:
            message: User message to process
            chat_history: Optional chat history
            
        Returns:
            CuratorOutput: Curated output with debug information
        """
        if chat_history is None:
            chat_history = []
        
        print(f"[DEBUG] Curator Agent Debug Mode")
        print(f"[DEBUG] Input message: {message}")
        print(f"[DEBUG] Chat history: {chat_history}")
        
        # Enable verbose mode for this call
        original_verbose = self.verbose
        self.verbose = True
        
        try:
            result = self.invoke({
                "message": message,
                "chat_history": chat_history,
                "request_id": "debug"
            })
            return result
        finally:
            self.verbose = original_verbose


def create_curator_agent(
    temperature: float = 0.1,
    max_tokens: int = 500,
    verbose: bool = False
) -> CuratorAgent:
    """
    Factory function to create a Curator Agent.
    
    Args:
        temperature: LLM temperature
        max_tokens: Maximum tokens for response
        verbose: Enable verbose logging
        
    Returns:
        CuratorAgent: Configured curator agent
    """
    return CuratorAgent(
        temperature=temperature,
        max_tokens=max_tokens,
        verbose=verbose
    ) 