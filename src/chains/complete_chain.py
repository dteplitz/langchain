"""
Complete chain implementation for Stage 2.

This module contains the complete chain that connects all three agents:
1. Curator Agent - Validates and cleans input
2. Processor Agent - Generates responses using tools
3. Formatter Agent - Formats the final response
"""

import time
import uuid
from typing import Dict, Any, Optional
from langchain.schema.runnable import Runnable
from src.agents.curator_agent import CuratorAgent, create_curator_agent
from src.agents.processor_agent import ProcessorAgent, create_processor_agent
from src.agents.formatter_agent import FormatterAgent, create_formatter_agent
from src.memory.conversation_memory import create_memory, get_conversation_history
from src.utils.logger import get_logger
from src.models.agent_interfaces import (
    CuratorOutput, ProcessorInput, ProcessorOutput, 
    FormatterInput, FormatterOutput, ChainMetadata
)


class CompleteChain(Runnable):
    """
    Complete chain that orchestrates all three agents.
    
    This chain processes user messages through:
    1. Curator Agent: Validates and cleans input
    2. Processor Agent: Generates responses using tools
    3. Formatter Agent: Formats the final response
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the complete chain.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.logger = get_logger()
        
        # Initialize all agents
        self.curator_agent = create_curator_agent(verbose=verbose)
        self.processor_agent = create_processor_agent(verbose=verbose)
        self.formatter_agent = create_formatter_agent(verbose=verbose)
    
    def invoke(
        self, 
        input_data: Dict[str, Any], 
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a message through the complete chain.
        
        Args:
            input_data: Input dictionary with message and session_id
            config: Optional configuration
            
        Returns:
            Dict[str, Any]: Processed response with metadata
        """
        start_time = time.time()
        
        # Extract input data
        message = input_data.get("message", "")
        session_id = input_data.get("session_id", str(uuid.uuid4()))
        request_id = input_data.get("request_id", str(uuid.uuid4()))
        debug = input_data.get("debug", False)
        
        # Create memory for this session
        memory = create_memory(session_id)
        
        # Get conversation history
        chat_history = get_conversation_history(session_id, limit=5)
        
        # Track agents used and errors
        agents_used = []
        errors = []
        
        try:
            # Step 1: Curator Agent
            if self.verbose:
                print(f"[CompleteChain] Step 1: Curator Agent")
            
            curator_result = self.curator_agent.invoke({
                "message": message,
                "chat_history": chat_history,
                "request_id": request_id
            })
            
            agents_used.append("curator")
            
            # Check if curator validation failed
            if not curator_result.is_valid:
                response = f"Message validation failed: {', '.join(curator_result.validation_errors)}"
                
                # Save to memory
                memory.save_context(
                    {"message": message},
                    {"response": response}
                )
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                return {
                    "response": response,
                    "session_id": session_id,
                    "request_id": request_id,
                    "processing_time": processing_time,
                    "metadata": {
                        "agents_used": agents_used,
                        "is_valid": False,
                        "confidence": curator_result.confidence,
                        "content_type": curator_result.content_type,
                        "validation_errors": curator_result.validation_errors,
                        "stage": "stage_2",
                        "success": False,
                        "errors": errors
                    }
                }
            
            # Step 2: Processor Agent
            if self.verbose:
                print(f"[CompleteChain] Step 2: Processor Agent")
            
            processor_input = ProcessorInput(
                message=message,
                chat_history=chat_history,
                curator_output=curator_result.dict(),
                tools_used=[],
                search_results=[]
            )
            
            processor_result = self.processor_agent.invoke(processor_input)
            agents_used.append("processor")
            
            # Step 3: Formatter Agent
            if self.verbose:
                print(f"[CompleteChain] Step 3: Formatter Agent")
            
            formatter_input = FormatterInput(
                raw_response=processor_result.raw_response,
                user_message=message,
                response_type=curator_result.content_type,
                processor_output=processor_result.dict()
            )
            
            formatter_result = self.formatter_agent.invoke(formatter_input)
            agents_used.append("formatter")
            
            # Save to memory
            memory.save_context(
                {"message": message},
                {"response": formatter_result.formatted_response}
            )
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare response
            result = {
                "response": formatter_result.formatted_response,
                "session_id": session_id,
                "request_id": request_id,
                "processing_time": processing_time,
                "metadata": {
                    "agents_used": agents_used,
                    "is_valid": curator_result.is_valid,
                    "confidence": curator_result.confidence,
                    "content_type": curator_result.content_type,
                    "validation_errors": curator_result.validation_errors,
                    "tools_executed": [tool.dict() for tool in processor_result.tools_executed],
                    "search_performed": processor_result.search_performed,
                    "response_quality": processor_result.response_quality,
                    "readability_score": formatter_result.readability_score,
                    "response_structure": formatter_result.response_structure,
                    "stage": "stage_2",
                    "success": True,
                    "errors": errors
                }
            }
            
            if self.verbose:
                print(f"[CompleteChain] Input: {message}")
                print(f"[CompleteChain] Output: {result}")
                print(f"[CompleteChain] Processing time: {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            # Log error
            processing_time = time.time() - start_time
            self.logger.log_error(
                request_id=request_id,
                error=e,
                agent="complete_chain",
                context={"input": input_data}
            )
            
            errors.append(str(e))
            
            # Return error response
            return {
                "response": f"Error processing message: {str(e)}",
                "session_id": session_id,
                "request_id": request_id,
                "processing_time": processing_time,
                "metadata": {
                    "agents_used": agents_used,
                    "is_valid": False,
                    "confidence": 0.0,
                    "content_type": "error",
                    "validation_errors": [],
                    "stage": "stage_2",
                    "success": False,
                    "errors": errors
                }
            }
    
    def debug(self, message: str, session_id: str = None) -> Dict[str, Any]:
        """
        Debug method for step-by-step inspection.
        
        Args:
            message: User message to process
            session_id: Optional session identifier
            
        Returns:
            Dict[str, Any]: Processed output with debug information
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        print(f"[DEBUG] Complete Chain Debug Mode")
        print(f"[DEBUG] Input message: {message}")
        print(f"[DEBUG] Session ID: {session_id}")
        
        # Enable verbose mode for this call
        original_verbose = self.verbose
        self.verbose = True
        
        try:
            result = self.invoke({
                "message": message,
                "session_id": session_id,
                "request_id": "debug",
                "debug": True
            })
            return result
        finally:
            self.verbose = original_verbose


def create_complete_chain(verbose: bool = False) -> CompleteChain:
    """
    Factory function to create a complete chain.
    
    Args:
        verbose: Enable verbose logging
        
    Returns:
        CompleteChain: Configured complete chain
    """
    return CompleteChain(verbose=verbose) 