"""
Enhanced logger for human-readable debugging.

This module provides structured logging that's easy to read and understand
for debugging the agent chain without LangSmith.
"""

import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
import sys


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for better readability."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


class EnhancedLogger:
    """
    Enhanced logger for human-readable debugging.
    
    Provides structured logging with colors, timing, and detailed
    information about agent operations.
    """
    
    def __init__(self, name: str = "langchain_debug"):
        """
        Initialize the enhanced logger.
        
        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
        
        # Track request flow
        self.request_timers = {}
        self.agent_timers = {}
    
    def _setup_handlers(self):
        """Setup console and file handlers."""
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        colored_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(colored_formatter)
        
        # File handler for detailed logs
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"langchain_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def start_request(self, request_id: str, message: str, session_id: str = None):
        """
        Start tracking a new request.
        
        Args:
            request_id: Unique request identifier
            message: User message
            session_id: Session identifier
        """
        self.request_timers[request_id] = time.time()
        
        self.logger.info("="*60)
        self.logger.info(f"[START] NEW REQUEST STARTED")
        self.logger.info(f"[START] Request ID: {request_id}")
        self.logger.info(f"[START] Session ID: {session_id or 'N/A'}")
        self.logger.info(f"[START] Message: {message[:100]}{'...' if len(message) > 100 else ''}")
        self.logger.info("="*60)
    
    def end_request(self, request_id: str, response: str, metadata: Dict[str, Any]):
        """
        End request tracking and log summary.
        
        Args:
            request_id: Request identifier
            response: Final response
            metadata: Response metadata
        """
        if request_id in self.request_timers:
            total_time = time.time() - self.request_timers[request_id]
            
            self.logger.info("="*60)
            self.logger.info(f"[END] REQUEST COMPLETED")
            self.logger.info(f"[END] Request ID: {request_id}")
            self.logger.info(f"[END] Total Time: {total_time:.2f}s")
            self.logger.info(f"[END] Agents Used: {', '.join(metadata.get('agents_used', []))}")
            self.logger.info(f"[END] Success: {metadata.get('success', False)}")
            self.logger.info(f"[END] Response Length: {len(response)} chars")
            self.logger.info(f"[END] Response Preview: {response[:100]}{'...' if len(response) > 100 else ''}")
            self.logger.info("="*60)
            
            del self.request_timers[request_id]
    
    def start_agent(self, request_id: str, agent_name: str, input_data: Dict[str, Any]):
        """
        Start tracking an agent execution.
        
        Args:
            request_id: Request identifier
            agent_name: Name of the agent
            input_data: Input data for the agent
        """
        agent_key = f"{request_id}_{agent_name}"
        self.agent_timers[agent_key] = time.time()
        
        self.logger.info(f"[AGENT] [{agent_name.upper()}] Starting...")
        self.logger.info(f"[AGENT] [{agent_name.upper()}] Input: {self._format_input(input_data)}")
    
    def end_agent(self, request_id: str, agent_name: str, output: Any, metadata: Dict[str, Any] = None):
        """
        End agent tracking and log results.
        
        Args:
            request_id: Request identifier
            agent_name: Name of the agent
            output: Agent output
            metadata: Additional metadata
        """
        agent_key = f"{request_id}_{agent_name}"
        
        if agent_key in self.agent_timers:
            execution_time = time.time() - self.agent_timers[agent_key]
            
            self.logger.info(f"[AGENT] [{agent_name.upper()}] Completed in {execution_time:.2f}s")
            self.logger.info(f"[AGENT] [{agent_name.upper()}] Output: {self._format_output(output)}")
            
            if metadata:
                self.logger.info(f"[AGENT] [{agent_name.upper()}] Metadata: {json.dumps(metadata, indent=2)}")
            
            del self.agent_timers[agent_key]
    
    def log_tool_execution(self, request_id: str, tool_name: str, input_params: Dict[str, Any], result: Any, execution_time: float):
        """
        Log tool execution details.
        
        Args:
            request_id: Request identifier
            tool_name: Name of the tool
            input_params: Input parameters
            result: Tool result
            execution_time: Time taken
        """
        self.logger.info(f"[TOOL] {tool_name}")
        self.logger.info(f"[TOOL] Input: {json.dumps(input_params, indent=2)}")
        self.logger.info(f"[TOOL] Result: {self._format_tool_result(result)}")
        self.logger.info(f"[TOOL] Time: {execution_time:.2f}s")
    
    def log_error(self, request_id: str, agent_name: str, error: Exception, context: Dict[str, Any] = None):
        """
        Log error with context.
        
        Args:
            request_id: Request identifier
            agent_name: Name of the agent where error occurred
            error: Exception that occurred
            context: Additional context
        """
        self.logger.error(f"[ERROR] [{agent_name.upper()}] ERROR: {type(error).__name__}: {str(error)}")
        
        if context:
            self.logger.error(f"[ERROR] [{agent_name.upper()}] Context: {json.dumps(context, indent=2)}")
    
    def log_chain_step(self, request_id: str, step_name: str, description: str, data: Any = None):
        """
        Log a step in the chain execution.
        
        Args:
            request_id: Request identifier
            step_name: Name of the step
            description: Description of what's happening
            data: Optional data for the step
        """
        self.logger.info(f"[CHAIN] {step_name}: {description}")
        
        if data:
            self.logger.debug(f"[CHAIN] {step_name} Data: {self._format_data(data)}")
    
    def _format_input(self, input_data: Dict[str, Any]) -> str:
        """Format input data for logging."""
        if isinstance(input_data, dict):
            # Truncate long values
            formatted = {}
            for key, value in input_data.items():
                if isinstance(value, str) and len(value) > 100:
                    formatted[key] = value[:100] + "..."
                else:
                    formatted[key] = value
            return json.dumps(formatted, indent=2)
        return str(input_data)
    
    def _format_output(self, output: Any) -> str:
        """Format output data for logging."""
        if hasattr(output, 'dict'):
            return json.dumps(output.dict(), indent=2)
        elif isinstance(output, dict):
            return json.dumps(output, indent=2)
        else:
            return str(output)[:200] + "..." if len(str(output)) > 200 else str(output)
    
    def _format_tool_result(self, result: Any) -> str:
        """Format tool result for logging."""
        if isinstance(result, list):
            return f"List with {len(result)} items"
        elif isinstance(result, dict):
            return json.dumps(result, indent=2)
        else:
            return str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
    
    def _format_data(self, data: Any) -> str:
        """Format general data for logging."""
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=2)
        else:
            return str(data)


# Global logger instance
_enhanced_logger = None

def get_enhanced_logger() -> EnhancedLogger:
    """
    Get the global enhanced logger instance.
    
    Returns:
        EnhancedLogger: The global logger instance
    """
    global _enhanced_logger
    if _enhanced_logger is None:
        _enhanced_logger = EnhancedLogger()
    return _enhanced_logger 