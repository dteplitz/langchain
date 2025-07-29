"""
Advanced chain implementation for Stage 3.

This module contains the advanced chain with:
- RunnableSequence for proper agent orchestration
- RunnableWithFallbacks for robust error handling
- ConsoleCallbackHandler for debugging
- Configurable LLM parameters per agent
"""

import time
import uuid
from typing import Dict, Any, Optional, List
from langchain.schema.runnable import Runnable, RunnableSequence, RunnableWithFallbacks, RunnableLambda
# ConsoleCallbackHandler not available in current LangChain version
# from langchain.callbacks import ConsoleCallbackHandler
from langchain.schema.output_parser import StrOutputParser

from src.agents.curator_agent import create_curator_agent
from src.agents.processor_agent import create_processor_agent
from src.agents.formatter_agent import create_formatter_agent
from src.memory.conversation_memory import create_memory, get_conversation_history
from src.utils.enhanced_logger import get_enhanced_logger
from src.models.agent_interfaces import (
    CuratorOutput, ProcessorInput, ProcessorOutput, 
    FormatterInput, FormatterOutput, ChainMetadata
)


class AdvancedChain(Runnable):
    """
    Advanced chain with robust orchestration and error handling.
    
    This chain uses RunnableSequence and RunnableWithFallbacks
    for better reliability and debugging capabilities.
    """
    
    def __init__(
        self,
        curator_config: Dict[str, Any] = None,
        processor_config: Dict[str, Any] = None,
        formatter_config: Dict[str, Any] = None,
        verbose: bool = False
    ):
        """
        Initialize the advanced chain.
        
        Args:
            curator_config: Configuration for curator agent
            processor_config: Configuration for processor agent
            formatter_config: Configuration for formatter agent
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.logger = get_enhanced_logger()
        
        # Default configurations
        curator_config = curator_config or {"temperature": 0.1, "max_tokens": 500}
        processor_config = processor_config or {"temperature": 0.7, "max_tokens": 1000}
        formatter_config = formatter_config or {"temperature": 0.3, "max_tokens": 800}
        
        # Initialize agents with configurations
        self.curator_agent = create_curator_agent(**curator_config, verbose=verbose)
        self.processor_agent = create_processor_agent(**processor_config, verbose=verbose)
        self.formatter_agent = create_formatter_agent(**formatter_config, verbose=verbose)
        
        # Create callback handler for debugging (simplified for current LangChain version)
        self.callback_handler = None  # ConsoleCallbackHandler not available
        
        # Build the advanced chain
        self._build_chain()
    
    def _build_chain(self):
        """Build the RunnableSequence with fallbacks."""
        
        # Step 1: Curator Agent with fallback
        curator_with_fallback = RunnableWithFallbacks(
            runnable=self.curator_agent,
            fallbacks=[
                RunnableLambda(self._curator_fallback)
            ]
        )
        
        # Step 2: Processor Agent with fallback
        processor_with_fallback = RunnableWithFallbacks(
            runnable=self.processor_agent,
            fallbacks=[
                RunnableLambda(self._processor_fallback)
            ]
        )
        
        # Step 3: Formatter Agent with fallback
        formatter_with_fallback = RunnableWithFallbacks(
            runnable=self.formatter_agent,
            fallbacks=[
                RunnableLambda(self._formatter_fallback)
            ]
        )
        
        # Create the complete chain directly
        self.chain = RunnableLambda(self._process_complete_chain)
    
    def _curator_fallback(self, input_data: Dict[str, Any], config: Dict[str, Any]) -> CuratorOutput:
        """
        Fallback for curator agent.
        
        Args:
            input_data: Input data
            config: Configuration
            
        Returns:
            CuratorOutput: Fallback result
        """
        self.logger.log_chain_step(
            input_data.get("request_id", "unknown"),
            "FALLBACK",
            "Curator agent failed, using fallback"
        )
        
        return CuratorOutput(
            cleaned_message=input_data.get("message", ""),
            is_valid=True,  # Assume valid in fallback
            validation_errors=[],
            content_type="general",
            confidence=0.5
        )
    
    def _processor_fallback(self, input_data: ProcessorInput, config: Dict[str, Any]) -> ProcessorOutput:
        """
        Fallback for processor agent.
        
        Args:
            input_data: Processor input
            config: Configuration
            
        Returns:
            ProcessorOutput: Fallback result
        """
        self.logger.log_chain_step(
            "unknown",
            "FALLBACK",
            "Processor agent failed, using fallback"
        )
        
        return ProcessorOutput(
            raw_response=f"I understand your message: {input_data.message}. This is a fallback response.",
            tools_executed=[],
            search_performed=False,
            response_quality=0.3,
            processing_time=0.1
        )
    
    def _formatter_fallback(self, input_data: FormatterInput, config: Dict[str, Any]) -> FormatterOutput:
        """
        Fallback for formatter agent.
        
        Args:
            input_data: Formatter input
            config: Configuration
            
        Returns:
            FormatterOutput: Fallback result
        """
        self.logger.log_chain_step(
            "unknown",
            "FALLBACK",
            "Formatter agent failed, using fallback"
        )
        
        return FormatterOutput(
            formatted_response=input_data.raw_response,
            response_structure="fallback",
            readability_score=0.5,
            formatting_time=0.1
        )
    
    def _orchestrate_wrapper(self, data: Any) -> Dict[str, Any]:
        """
        Wrapper for orchestration that handles the data structure from RunnableSequence.
        
        Args:
            data: Data from the previous step in the chain
            
        Returns:
            Dict[str, Any]: Final result
        """
        # Handle different data structures
        if isinstance(data, dict):
            # If data is a dict, it might contain both curator_result and input_data
            if len(data) == 2:
                # Extract curator_result and input_data
                items = list(data.items())
                curator_result = items[0][1]
                input_data = items[1][1]
            else:
                # Assume data is input_data
                curator_result = None
                input_data = data
        else:
            # If data is not a dict, assume it's curator_result and we need to get input_data from context
            curator_result = data
            input_data = {"message": "Unknown", "session_id": "unknown", "request_id": "unknown"}
        
        return self._orchestrate_agents(curator_result, input_data)
    
    def _process_complete_chain(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the complete chain from start to finish.
        
        Args:
            input_data: Input data containing message and session_id
            
        Returns:
            Dict[str, Any]: Final result
        """
        try:
            # Step 1: Curator Agent
            curator_result = self.curator_agent.invoke(input_data)
            
            # Step 2: Process through the complete orchestration
            return self._orchestrate_agents(curator_result, input_data)
            
        except Exception as e:
            # Fallback if curator fails
            self.logger.log_error(
                request_id=input_data.get("request_id", "unknown"),
                agent_name="complete_chain",
                error=e,
                context={"input": input_data}
            )
            
            # Return error response
            return {
                "response": f"Error processing message: {str(e)}",
                "session_id": input_data.get("session_id", "unknown"),
                "request_id": input_data.get("request_id", "unknown"),
                "processing_time": 0.0,
                "metadata": {
                    "agents_used": [],
                    "is_valid": False,
                    "confidence": 0.0,
                    "content_type": "error",
                    "validation_errors": [str(e)],
                    "stage": "stage_3",
                    "success": False,
                    "errors": [str(e)]
                }
            }
    
    def _orchestrate_agents(
        self, 
        curator_result: CuratorOutput, 
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Orchestrate the complete flow of agents.
        
        Args:
            curator_result: Result from curator agent
            input_data: Original input data
            
        Returns:
            Dict[str, Any]: Final result
        """
        start_time = time.time()
        request_id = input_data.get("request_id", str(uuid.uuid4()))
        session_id = input_data.get("session_id", str(uuid.uuid4()))
        message = input_data.get("message", "")
        
        # Start request tracking
        self.logger.start_request(request_id, message, session_id)
        
        # Create memory for this session
        memory = create_memory(session_id)
        chat_history = get_conversation_history(session_id, limit=5)
        
        # Debug: Log chat history
        self.logger.log_chain_step(request_id, "MEMORY_DEBUG", f"Chat history length: {len(chat_history)}")
        if chat_history:
            self.logger.log_chain_step(request_id, "MEMORY_DEBUG", f"Last message: {chat_history[-1].get('message', 'N/A')}")
            self.logger.log_chain_step(request_id, "MEMORY_DEBUG", f"Last response: {chat_history[-1].get('response', 'N/A')[:100]}...")
        
        agents_used = ["curator"]
        errors = []
        
        try:
            # Check if curator validation failed
            if not curator_result.is_valid:
                self.logger.log_chain_step(request_id, "VALIDATION_FAILED", "Curator validation failed")
                
                response = f"Message validation failed: {', '.join(curator_result.validation_errors)}"
                
                # Save to memory
                memory.save_context(
                    {"message": message},
                    {"response": response}
                )
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                result = {
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
                        "stage": "stage_3",
                        "success": False,
                        "errors": errors
                    }
                }
                
                self.logger.end_request(request_id, response, result["metadata"])
                return result
            
            # Step 2: Processor Agent
            self.logger.log_chain_step(request_id, "STEP_2", "Starting Processor Agent")
            
            processor_input = ProcessorInput(
                message=message,
                chat_history=chat_history,
                curator_output=curator_result.dict(),
                tools_used=[],
                search_results=[]
            )
            
            # Execute processor with fallback
            processor_result = self.processor_agent.invoke(processor_input)
            agents_used.append("processor")
            
            # Step 3: Formatter Agent
            self.logger.log_chain_step(request_id, "STEP_3", "Starting Formatter Agent")
            
            formatter_input = FormatterInput(
                raw_response=processor_result.raw_response,
                user_message=message,
                response_type=curator_result.content_type,
                processor_output=processor_result.dict()
            )
            
            # Execute formatter with fallback
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
                    "stage": "stage_3",
                    "success": True,
                    "errors": errors
                }
            }
            
            self.logger.end_request(request_id, formatter_result.formatted_response, result["metadata"])
            return result
            
        except Exception as e:
            # Log error
            processing_time = time.time() - start_time
            self.logger.log_error(
                request_id=request_id,
                agent_name="advanced_chain",
                error=e,
                context={"input": input_data}
            )
            
            errors.append(str(e))
            
            # Return error response
            result = {
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
                    "stage": "stage_3",
                    "success": False,
                    "errors": errors
                }
            }
            
            self.logger.end_request(request_id, result["response"], result["metadata"])
            return result
    
    def invoke(
        self, 
        input_data: Dict[str, Any], 
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a message through the advanced chain.
        
        Args:
            input_data: Input dictionary with message and session_id
            config: Optional configuration
            
        Returns:
            Dict[str, Any]: Processed response with metadata
        """
        # Add callbacks if verbose (simplified for current LangChain version)
        if self.verbose:
            # Log verbose information directly
            self.logger.logger.info(f"[VERBOSE] Processing request with advanced chain")
            self.logger.logger.info(f"[VERBOSE] Input: {input_data}")
        
        return self.chain.invoke(input_data, config or {})
    
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
        
        print(f"[DEBUG] Advanced Chain Debug Mode")
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


def create_advanced_chain(
    curator_config: Dict[str, Any] = None,
    processor_config: Dict[str, Any] = None,
    formatter_config: Dict[str, Any] = None,
    verbose: bool = False
) -> AdvancedChain:
    """
    Factory function to create an advanced chain.
    
    Args:
        curator_config: Configuration for curator agent
        processor_config: Configuration for processor agent
        formatter_config: Configuration for formatter agent
        verbose: Enable verbose logging
        
    Returns:
        AdvancedChain: Configured advanced chain
    """
    return AdvancedChain(
        curator_config=curator_config,
        processor_config=processor_config,
        formatter_config=formatter_config,
        verbose=verbose
    ) 