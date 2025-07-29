"""
Response Formatter Agent implementation.

This agent is responsible for formatting and structuring
the final response to users.
"""

import time
from typing import Dict, Any, Optional
from langchain.schema.runnable import Runnable
from src.utils.llm_client import create_llm_client
from src.utils.logger import get_logger
from src.prompts.formatter_prompts import get_formatter_prompt, determine_response_type
from src.models.agent_interfaces import FormatterInput, FormatterOutput, ProcessorOutput


class FormatterAgent(Runnable):
    """
    Response Formatter Agent for formatting final responses.
    
    This agent takes the raw response from the processor agent
    and formats it in a clear, structured, and user-friendly way.
    """
    
    def __init__(
        self,
        temperature: float = 0.3,
        max_tokens: int = 800,
        verbose: bool = False
    ):
        """
        Initialize the Response Formatter Agent.
        
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
        self.prompt = get_formatter_prompt()
        
        # Create the runnable chain
        self.chain = self.prompt | self.llm
    
    def _calculate_readability_score(self, text: str) -> float:
        """
        Calculate a simple readability score for the text.
        
        Args:
            text: Text to analyze
            
        Returns:
            float: Readability score (0.0 to 1.0)
        """
        if not text:
            return 0.0
        
        # Simple readability metrics
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        characters = len(text)
        
        if sentences == 0 or words == 0:
            return 0.5
        
        # Average words per sentence (lower is better for readability)
        avg_words_per_sentence = words / sentences
        
        # Average word length (shorter words are more readable)
        avg_word_length = characters / words
        
        # Calculate score (simplified)
        sentence_score = max(0, 1 - (avg_words_per_sentence - 15) / 10)  # Penalize very long sentences
        word_score = max(0, 1 - (avg_word_length - 4) / 2)  # Penalize very long words
        
        readability_score = (sentence_score + word_score) / 2
        return max(0.0, min(1.0, readability_score))
    
    def _determine_response_structure(self, response_type: str, raw_response: str) -> str:
        """
        Determine the structure used for formatting.
        
        Args:
            response_type: Type of response
            raw_response: Raw response text
            
        Returns:
            str: Structure description
        """
        if response_type == "question":
            if "•" in raw_response or "-" in raw_response:
                return "bullet_points"
            elif any(str(i) + "." in raw_response for i in range(1, 10)):
                return "numbered_list"
            else:
                return "paragraph"
        elif response_type == "explanation_request":
            return "structured_explanation"
        elif response_type == "calculation":
            return "calculation_result"
        else:
            return "general_format"
    
    def invoke(
        self, 
        input_data: FormatterInput, 
        config: Optional[Dict[str, Any]] = None
    ) -> FormatterOutput:
        """
        Format a response through the formatter agent.
        
        Args:
            input_data: FormatterInput containing raw response and context
            config: Optional configuration
            
        Returns:
            FormatterOutput: Formatted response
        """
        start_time = time.time()
        request_id = "unknown"  # Will be extracted from processor output if available
        
        # Log the request
        self.logger.log_request(
            request_id=request_id,
            message=f"Formatting response for: {input_data.user_message}",
            agent="formatter",
            metadata={"temperature": self.temperature, "max_tokens": self.max_tokens}
        )
        
        try:
            # Prepare input for the chain
            chain_input = {
                "raw_response": input_data.raw_response,
                "user_message": input_data.user_message,
                "response_type": input_data.response_type
            }
            
            # Run the chain
            llm_response = self.chain.invoke(chain_input, config or {})
            formatted_response = llm_response.content if hasattr(llm_response, 'content') else str(llm_response)
            
            # Calculate formatting time
            formatting_time = time.time() - start_time
            
            # Calculate readability score
            readability_score = self._calculate_readability_score(formatted_response)
            
            # Determine response structure
            response_structure = self._determine_response_structure(
                input_data.response_type, 
                formatted_response
            )
            
            # Create output
            result = FormatterOutput(
                formatted_response=formatted_response,
                response_structure=response_structure,
                readability_score=readability_score,
                formatting_time=formatting_time
            )
            
            # Log the response
            self.logger.log_agent_response(
                request_id=request_id,
                agent="formatter",
                response=formatted_response,
                processing_time=formatting_time,
                metadata={
                    "response_type": input_data.response_type,
                    "response_structure": response_structure,
                    "readability_score": readability_score
                }
            )
            
            if self.verbose:
                print(f"[Formatter] Input: {input_data.user_message}")
                print(f"[Formatter] Raw response: {input_data.raw_response[:100]}...")
                print(f"[Formatter] Output: {formatted_response}")
                print(f"[Formatter] Formatting time: {formatting_time:.2f}s")
                print(f"[Formatter] Readability score: {readability_score:.2f}")
            
            return result
            
        except Exception as e:
            # Log error
            formatting_time = time.time() - start_time
            self.logger.log_error(
                request_id=request_id,
                error=e,
                agent="formatter",
                context={"input": input_data.dict()}
            )
            
            # Return error response
            return FormatterOutput(
                formatted_response=f"Error formatting response: {str(e)}",
                response_structure="error",
                readability_score=0.0,
                formatting_time=formatting_time
            )
    
    def debug(self, raw_response: str, user_message: str, processor_output: ProcessorOutput) -> FormatterOutput:
        """
        Debug method for step-by-step inspection.
        
        Args:
            raw_response: Raw response from processor
            user_message: Original user message
            processor_output: Output from processor agent
            
        Returns:
            FormatterOutput: Formatted output with debug information
        """
        print(f"[DEBUG] Formatter Agent Debug Mode")
        print(f"[DEBUG] User message: {user_message}")
        print(f"[DEBUG] Raw response: {raw_response}")
        print(f"[DEBUG] Processor output: {processor_output}")
        
        # Enable verbose mode for this call
        original_verbose = self.verbose
        self.verbose = True
        
        try:
            response_type = determine_response_type(user_message)
            
            input_data = FormatterInput(
                raw_response=raw_response,
                user_message=user_message,
                response_type=response_type,
                processor_output=processor_output
            )
            
            result = self.invoke(input_data)
            return result
        finally:
            self.verbose = original_verbose


def create_formatter_agent(
    temperature: float = 0.3,
    max_tokens: int = 800,
    verbose: bool = False
) -> FormatterAgent:
    """
    Factory function to create a Response Formatter Agent.
    
    Args:
        temperature: LLM temperature
        max_tokens: Maximum tokens for response
        verbose: Enable verbose logging
        
    Returns:
        FormatterAgent: Configured formatter agent
    """
    return FormatterAgent(
        temperature=temperature,
        max_tokens=max_tokens,
        verbose=verbose
    ) 