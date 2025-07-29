"""
Dummy tools for the Processor Agent.

This module contains dummy implementations of various tools
that the processor agent can use to gather information.
"""

import time
import random
from typing import List, Dict, Any
from datetime import datetime
import math


class DummySearchTool:
    """Dummy search tool that returns fake search results."""
    
    def __init__(self):
        self.knowledge_base = {
            "capital of france": {
                "title": "Capital of France",
                "content": "Paris is the capital and largest city of France. It is known as the 'City of Light' and is famous for its art, fashion, gastronomy, and culture.",
                "source": "Encyclopedia Britannica"
            },
            "python programming": {
                "title": "Python Programming Language",
                "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data science, AI, and automation.",
                "source": "Python.org"
            },
            "machine learning": {
                "title": "Machine Learning",
                "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed.",
                "source": "Stanford University"
            },
            "langchain": {
                "title": "LangChain Framework",
                "content": "LangChain is a framework for developing applications powered by language models. It provides tools for building LLM applications with memory, tools, and chains.",
                "source": "LangChain Documentation"
            },
            "fastapi": {
                "title": "FastAPI Framework",
                "content": "FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints. It's designed to be easy to use and fast to develop.",
                "source": "FastAPI Documentation"
            }
        }
    
    def search_web(self, query: str) -> List[Dict[str, str]]:
        """
        Simulate web search with dummy results.
        
        Args:
            query: Search query
            
        Returns:
            List[Dict[str, str]]: Search results
        """
        query_lower = query.lower()
        results = []
        
        # Check knowledge base first
        for key, data in self.knowledge_base.items():
            if key in query_lower or any(word in query_lower for word in key.split()):
                results.append(data)
        
        # If no exact matches, generate generic results
        if not results:
            results = [
                {
                    "title": f"Search Results for: {query}",
                    "content": f"This is a dummy search result for '{query}'. In a real implementation, this would contain actual search results from the web.",
                    "source": "Dummy Search Engine"
                },
                {
                    "title": f"Additional Information about {query}",
                    "content": f"More dummy information about '{query}'. This simulates additional search results that would be found online.",
                    "source": "Dummy Database"
                }
            ]
        
        # Add some delay to simulate real search
        time.sleep(random.uniform(0.1, 0.3))
        
        return results[:3]  # Return max 3 results
    
    def search_knowledge_base(self, query: str) -> List[Dict[str, str]]:
        """
        Search internal knowledge base.
        
        Args:
            query: Search query
            
        Returns:
            List[Dict[str, str]]: Knowledge base results
        """
        return self.search_web(query)


class DummyCalculatorTool:
    """Dummy calculator tool for mathematical operations."""
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Perform mathematical calculations.
        
        Args:
            expression: Mathematical expression
            
        Returns:
            Dict[str, Any]: Calculation result
        """
        try:
            # Basic mathematical operations
            expression = expression.lower().replace(' ', '')
            
            # Handle common mathematical functions
            if 'sqrt' in expression:
                expression = expression.replace('sqrt', 'math.sqrt')
            if 'sin' in expression:
                expression = expression.replace('sin', 'math.sin')
            if 'cos' in expression:
                expression = expression.replace('cos', 'math.cos')
            if 'log' in expression:
                expression = expression.replace('log', 'math.log10')
            
            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            
            return {
                "expression": expression,
                "result": result,
                "success": True
            }
        except Exception as e:
            return {
                "expression": expression,
                "result": None,
                "error": str(e),
                "success": False
            }


class DummyWeatherTool:
    """Dummy weather tool for weather information."""
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Get weather information for a location.
        
        Args:
            location: City or location name
            
        Returns:
            Dict[str, Any]: Weather information
        """
        # Simulate API delay
        time.sleep(random.uniform(0.2, 0.5))
        
        # Generate dummy weather data
        temperatures = random.randint(10, 30)
        conditions = random.choice(['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Clear'])
        humidity = random.randint(30, 80)
        
        return {
            "location": location,
            "temperature": f"{temperatures}°C",
            "condition": conditions,
            "humidity": f"{humidity}%",
            "timestamp": datetime.now().isoformat(),
            "source": "Dummy Weather API"
        }


class DummyTimeTool:
    """Dummy time tool for time and date information."""
    
    def get_time(self, timezone: str = "UTC") -> Dict[str, Any]:
        """
        Get current time and date information.
        
        Args:
            timezone: Timezone (default: UTC)
            
        Returns:
            Dict[str, Any]: Time information
        """
        now = datetime.now()
        
        return {
            "timezone": timezone,
            "current_time": now.strftime("%H:%M:%S"),
            "current_date": now.strftime("%Y-%m-%d"),
            "day_of_week": now.strftime("%A"),
            "timestamp": now.isoformat(),
            "source": "System Clock"
        }


# Global tool instances
search_tool = DummySearchTool()
calculator_tool = DummyCalculatorTool()
weather_tool = DummyWeatherTool()
time_tool = DummyTimeTool()


def get_available_tools() -> Dict[str, Any]:
    """
    Get all available tools.
    
    Returns:
        Dict[str, Any]: Dictionary of available tools
    """
    return {
        "search_web": search_tool.search_web,
        "search_knowledge_base": search_tool.search_knowledge_base,
        "calculate": calculator_tool.calculate,
        "get_weather": weather_tool.get_weather,
        "get_time": time_tool.get_time
    }


def execute_tool(tool_name: str, **kwargs) -> Any:
    """
    Execute a specific tool.
    
    Args:
        tool_name: Name of the tool to execute
        **kwargs: Tool-specific arguments
        
    Returns:
        Any: Tool execution result
    """
    tools = get_available_tools()
    
    if tool_name not in tools:
        raise ValueError(f"Tool '{tool_name}' not found")
    
    return tools[tool_name](**kwargs) 