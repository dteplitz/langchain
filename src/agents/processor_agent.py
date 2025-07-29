"""
Processor Agent implementation.

This agent is responsible for generating comprehensive responses
using available tools and the LLM.
"""

import time
import re
from typing import Dict, Any, Optional, List
from langchain.schema.runnable import Runnable
from src.utils.llm_client import create_llm_client
from src.utils.enhanced_logger import get_enhanced_logger
from src.utils.tools import execute_tool, get_available_tools
from src.prompts.processor_prompts import get_processor_prompt, format_tools_available, format_search_results
from src.prompts.curator_prompts import format_chat_history
from src.models.agent_interfaces import ProcessorInput, ProcessorOutput, CuratorOutput, ToolExecutionResult, SearchResult


class ProcessorAgent(Runnable):
    """
    Processor Agent for generating comprehensive responses using tools.
    
    This agent processes user messages by using available tools
    and generating detailed responses with the LLM.
    """
    
    def __init__(
        self,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        verbose: bool = False
    ):
        """
        Initialize the Processor Agent.
        
        Args:
            temperature: LLM temperature for response generation
            max_tokens: Maximum tokens for response
            verbose: Enable verbose logging
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.verbose = verbose
        self.logger = get_enhanced_logger()
        
        # Initialize LLM and components
        self.llm = create_llm_client(
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.prompt = get_processor_prompt()
        
        # Create the runnable chain
        self.chain = self.prompt | self.llm
    
    def _determine_tools_needed(self, message: str, curator_output: Dict[str, Any]) -> List[str]:
        """
        Determine which tools are needed based on the message.
        
        Args:
            message: User message
            curator_output: Output from curator agent
            
        Returns:
            List[str]: List of tool names needed
        """
        message_lower = message.lower()
        tools_needed = []
        
        # Check for search needs
        if any(word in message_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'tell me', 'explain']):
            tools_needed.append('search_web')
        
        # Check for calculation needs
        if any(word in message_lower for word in ['calculate', 'compute', 'solve', 'math', '+', '-', '*', '/', '=']):
            tools_needed.append('calculate')
        
        # Check for weather needs
        if any(word in message_lower for word in ['weather', 'temperature', 'forecast', 'climate']):
            tools_needed.append('get_weather')
        
        # Check for time needs
        if any(word in message_lower for word in ['time', 'date', 'schedule', 'when']):
            tools_needed.append('get_time')
        
        return tools_needed
    
    def _execute_tools(self, tools_needed: List[str], message: str, request_id: str = "unknown") -> List[ToolExecutionResult]:
        """
        Execute the needed tools.
        
        Args:
            tools_needed: List of tools to execute
            message: User message for context
            request_id: Request identifier for logging
            
        Returns:
            List[ToolExecutionResult]: Results from tool executions
        """
        results = []
        
        for tool_name in tools_needed:
            start_time = time.time()
            
            try:
                # Prepare input parameters
                if tool_name == 'search_web':
                    input_params = {"query": message}
                    result = execute_tool(tool_name, query=message)
                elif tool_name == 'calculate':
                    # Extract mathematical expression from message
                    math_pattern = r'(\d+[\+\-\*\/\^]\d+|\d+\s*[\+\-\*\/\^]\s*\d+)'
                    math_match = re.search(math_pattern, message)
                    if math_match:
                        expression = math_match.group(1)
                        input_params = {"expression": expression}
                        result = execute_tool(tool_name, expression=expression)
                    else:
                        input_params = {"expression": "none"}
                        result = {"error": "No mathematical expression found", "success": False}
                elif tool_name == 'get_weather':
                    # Extract location from message (simplified)
                    location = "Paris"  # Default location
                    input_params = {"location": location}
                    result = execute_tool(tool_name, location=location)
                elif tool_name == 'get_time':
                    input_params = {}
                    result = execute_tool(tool_name)
                else:
                    input_params = {"tool": tool_name}
                    result = {"error": f"Unknown tool: {tool_name}", "success": False}
                
                execution_time = time.time() - start_time
                
                # Log tool execution
                self.logger.log_tool_execution(request_id, tool_name, input_params, result, execution_time)
                
                tool_result = ToolExecutionResult(
                    tool_name=tool_name,
                    success=result.get("success", True),
                    result=result,
                    error=result.get("error"),
                    execution_time=execution_time
                )
                
                results.append(tool_result)
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Log tool error
                self.logger.log_error(request_id, f"tool_{tool_name}", e, {
                    "tool_name": tool_name,
                    "input_params": input_params if 'input_params' in locals() else {}
                })
                
                tool_result = ToolExecutionResult(
                    tool_name=tool_name,
                    success=False,
                    result={},
                    error=str(e),
                    execution_time=execution_time
                )
                results.append(tool_result)
        
        return results
    
    def _extract_search_results(self, tool_results: List[ToolExecutionResult]) -> List[SearchResult]:
        """
        Extract search results from tool executions.
        
        Args:
            tool_results: Results from tool executions
            
        Returns:
            List[SearchResult]: Extracted search results
        """
        search_results = []
        
        for tool_result in tool_results:
            if tool_result.tool_name == 'search_web' and tool_result.success:
                if isinstance(tool_result.result, list):
                    for result in tool_result.result:
                        if isinstance(result, dict):
                            search_result = SearchResult(
                                title=result.get('title', ''),
                                content=result.get('content', ''),
                                source=result.get('source', ''),
                                url=result.get('url')
                            )
                            search_results.append(search_result)
        
        return search_results
    
    def invoke(
        self, 
        input_data: ProcessorInput, 
        config: Optional[Dict[str, Any]] = None
    ) -> ProcessorOutput:
        """
        Process a message through the processor agent.
        
        Args:
            input_data: ProcessorInput containing message and curator output
            config: Optional configuration
            
        Returns:
            ProcessorOutput: Processed response with tool results
        """
        start_time = time.time()
        request_id = input_data.chat_history[0].get("request_id", "unknown") if input_data.chat_history else "unknown"
        
        # Log the request (using enhanced logger)
        self.logger.start_agent(request_id, "processor", {
            "message": input_data.message,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        })
        
        try:
            # Determine which tools are needed
            tools_needed = self._determine_tools_needed(input_data.message, input_data.curator_output)
            
            # Execute tools
            tool_results = self._execute_tools(tools_needed, input_data.message, request_id)
            
            # Extract search results
            search_results = self._extract_search_results(tool_results)
            
            # Format inputs for the LLM
            formatted_history = format_chat_history(input_data.chat_history)
            tools_available = format_tools_available()
            search_results_text = format_search_results(search_results)
            
            # Prepare input for the chain
            chain_input = {
                "message": input_data.message,
                "chat_history": formatted_history,
                "search_results": search_results_text,
                "tools_available": tools_available
            }
            
            # Run the chain
            llm_response = self.chain.invoke(chain_input, config or {})
            raw_response = llm_response.content if hasattr(llm_response, 'content') else str(llm_response)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Calculate response quality (simplified)
            response_quality = 0.8 if tool_results else 0.6
            
            # Create output
            result = ProcessorOutput(
                raw_response=raw_response,
                tools_executed=tool_results,
                search_performed=len(search_results) > 0,
                response_quality=response_quality,
                processing_time=processing_time
            )
            
            # Log the response (using enhanced logger)
            self.logger.end_agent(request_id, "processor", result, {
                "tools_used": tools_needed,
                "search_performed": len(search_results) > 0,
                "response_quality": response_quality,
                "processing_time": processing_time
            })
            
            if self.verbose:
                print(f"[Processor] Input: {input_data.message}")
                print(f"[Processor] Tools used: {tools_needed}")
                print(f"[Processor] Output: {result}")
                print(f"[Processor] Processing time: {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            # Log error (using enhanced logger)
            processing_time = time.time() - start_time
            self.logger.log_error(
                request_id=request_id,
                agent_name="processor",
                error=e,
                context={"input": input_data.dict()}
            )
            
            # Return error response
            return ProcessorOutput(
                raw_response=f"Error processing message: {str(e)}",
                tools_executed=[],
                search_performed=False,
                response_quality=0.0,
                processing_time=processing_time
            )
    
    def debug(self, message: str, curator_output: CuratorOutput, chat_history: list = None) -> ProcessorOutput:
        """
        Debug method for step-by-step inspection.
        
        Args:
            message: User message to process
            curator_output: Output from curator agent
            chat_history: Optional chat history
            
        Returns:
            ProcessorOutput: Processed output with debug information
        """
        if chat_history is None:
            chat_history = []
        
        print(f"[DEBUG] Processor Agent Debug Mode")
        print(f"[DEBUG] Input message: {message}")
        print(f"[DEBUG] Curator output: {curator_output}")
        print(f"[DEBUG] Chat history: {chat_history}")
        
        # Enable verbose mode for this call
        original_verbose = self.verbose
        self.verbose = True
        
        try:
            input_data = ProcessorInput(
                message=message,
                chat_history=chat_history,
                curator_output=curator_output,
                tools_used=[],
                search_results=[]
            )
            
            result = self.invoke(input_data)
            return result
        finally:
            self.verbose = original_verbose


def create_processor_agent(
    temperature: float = 0.7,
    max_tokens: int = 1000,
    verbose: bool = False
) -> ProcessorAgent:
    """
    Factory function to create a Processor Agent.
    
    Args:
        temperature: LLM temperature
        max_tokens: Maximum tokens for response
        verbose: Enable verbose logging
        
    Returns:
        ProcessorAgent: Configured processor agent
    """
    return ProcessorAgent(
        temperature=temperature,
        max_tokens=max_tokens,
        verbose=verbose
    ) 