"""
Simple chain implementation for Stage 1.

This module contains a basic chain that uses only the Curator Agent
for the first stage of development.
"""

import time
import uuid
from typing import Dict, Any, Optional
from langchain.schema.runnable import Runnable
from src.agents.curator_agent import CuratorAgent, create_curator_agent
from src.memory.hybrid_conversation_memory import create_hybrid_memory
from src.memory.hybrid_conversation_memory import get_hybrid_conversation_history
from src.utils.logger import get_logger


class SimpleChain(Runnable):
    """
    Simple chain that uses only the Curator Agent.
    
    This is the basic implementation for Stage 1, which will be
    extended in later stages with additional agents.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the simple chain.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.logger = get_logger()
        
        # Initialize the curator agent
        self.curator_agent = create_curator_agent(verbose=verbose)
    
    def invoke(
        self, 
        input_data: Dict[str, Any], 
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a message through the simple chain.
        
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
        memory = create_hybrid_memory(session_id)
        
        # Get conversation history and summary
        chat_history_data = get_hybrid_conversation_history(session_id, limit=5, include_summary=True)
        chat_history = chat_history_data["recent_messages"]
        conversation_summary = chat_history_data["conversation_summary"]
        
        try:
            # Process through curator agent
            curator_result = self.curator_agent.invoke({
                "message": message,
                "chat_history": chat_history,
                "conversation_summary": conversation_summary,
                "request_id": request_id
            })
            
            # Generate response based on curator validation
            if curator_result.is_valid:
                response = f"Message validated successfully: {curator_result.cleaned_message}"
                if curator_result.content_type == "question":
                    response = f"I understand your question: {curator_result.cleaned_message}. This would be processed by the full chain in later stages."
                elif curator_result.content_type == "statement":
                    response = f"I acknowledge your statement: {curator_result.cleaned_message}"
                else:
                    response = f"Processed message: {curator_result.cleaned_message}"
            else:
                response = f"Message validation failed: {', '.join(curator_result.validation_errors)}"
            
            # Save to memory
            memory.save_context(
                {"message": message},
                {"response": response}
            )
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare response
            result = {
                "response": response,
                "session_id": session_id,
                "request_id": request_id,
                "processing_time": processing_time,
                "metadata": {
                    "agent_used": "curator",
                    "is_valid": curator_result.is_valid,
                    "confidence": curator_result.confidence,
                    "content_type": curator_result.content_type,
                    "validation_errors": curator_result.validation_errors,
                    "stage": "stage_1"
                }
            }
            
            if self.verbose:
                print(f"[SimpleChain] Input: {message}")
                print(f"[SimpleChain] Output: {result}")
                print(f"[SimpleChain] Processing time: {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            # Log error
            processing_time = time.time() - start_time
            self.logger.log_error(
                request_id=request_id,
                error=e,
                agent="simple_chain",
                context={"input": input_data}
            )
            
            # Return error response
            return {
                "response": f"Error processing message: {str(e)}",
                "session_id": session_id,
                "request_id": request_id,
                "processing_time": processing_time,
                "metadata": {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "stage": "stage_1"
                }
            }


def create_simple_chain(verbose: bool = False) -> SimpleChain:
    """
    Factory function to create a simple chain.
    
    Args:
        verbose: Enable verbose logging
        
    Returns:
        SimpleChain: Configured simple chain
    """
    return SimpleChain(verbose=verbose) 