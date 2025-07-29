"""
Prompt templates for the Processor Agent.

This module contains all prompt templates used by the Processor agent
for generating responses using LLM and tools.
"""

from langchain.prompts import PromptTemplate
from typing import Dict, Any


# Complete prompt template for the processor agent
PROCESSOR_PROMPT = PromptTemplate(
    input_variables=["message", "chat_history", "search_results", "tools_available"],
    template="""You are a Processor Agent responsible for generating comprehensive responses using available tools and knowledge.

Your role is to:
1. Analyze the user's question or request
2. Use available tools to gather information
3. Generate a detailed and accurate response
4. Provide context and explanations when appropriate

Available Tools:
{tools_available}

Search Results (if any):
{search_results}

Previous Conversation History:
{chat_history}

User Message: {message}

Instructions:
- Use the search tool if the question requires current or factual information
- Provide comprehensive answers with context
- If you don't have enough information, say so clearly
- Be helpful and informative
- Structure your response logically

Generate a detailed response that directly answers the user's question."""
)


def get_processor_prompt() -> PromptTemplate:
    """
    Get the processor prompt template.
    
    Returns:
        PromptTemplate: The processor prompt template
    """
    return PROCESSOR_PROMPT


def format_tools_available() -> str:
    """
    Format available tools for prompt inclusion.
    
    Returns:
        str: Formatted tools description
    """
    return """- search_web: Search for current information on the web
- search_knowledge_base: Search internal knowledge base
- calculate: Perform mathematical calculations
- get_weather: Get current weather information
- get_time: Get current time and date"""


def format_search_results(search_results: list) -> str:
    """
    Format search results for prompt inclusion.
    
    Args:
        search_results: List of search results
        
    Returns:
        str: Formatted search results string
    """
    if not search_results:
        return "No search results available."
    
    formatted = []
    for i, result in enumerate(search_results, 1):
        formatted.append(f"Result {i}:")
        formatted.append(f"  Title: {result.get('title', 'N/A')}")
        formatted.append(f"  Content: {result.get('content', 'N/A')}")
        formatted.append(f"  Source: {result.get('source', 'N/A')}")
        formatted.append("")
    
    return "\n".join(formatted) 