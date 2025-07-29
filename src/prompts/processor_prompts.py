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
5. **CRITICAL: Use the conversation history to maintain context and remember previous interactions**

Available Tools:
{tools_available}

Search Results (if any):
{search_results}

Previous Conversation History:
{chat_history}

User Message: {message}

Instructions:
- **CRITICAL: ALWAYS review the conversation history above first before responding**
- If the user mentioned their name, preferences, or personal information in previous messages, you MUST use that information
- If someone told you their name in a previous message, remember and use it in your response
- If the user asks "What's my name?" and you have it in the conversation history, tell them their name
- Use the search tool if the question requires current or factual information
- Provide comprehensive answers with context
- If you don't have enough information, say so clearly
- Be helpful and informative
- Structure your response logically
- **Always acknowledge previous context when relevant**
- **If the conversation history shows the user's name, always use it in your response**

Generate a detailed response that directly answers the user's question while maintaining conversation context."""
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
        # Handle both dict and SearchResult objects
        if hasattr(result, 'title'):
            # SearchResult object
            formatted.append(f"  Title: {result.title}")
            formatted.append(f"  Content: {result.content}")
            formatted.append(f"  Source: {result.source}")
            if result.url:
                formatted.append(f"  URL: {result.url}")
        elif isinstance(result, dict):
            # Dictionary object
            formatted.append(f"  Title: {result.get('title', 'N/A')}")
            formatted.append(f"  Content: {result.get('content', 'N/A')}")
            formatted.append(f"  Source: {result.get('source', 'N/A')}")
            if result.get('url'):
                formatted.append(f"  URL: {result.get('url')}")
        else:
            # Fallback
            formatted.append(f"  Content: {str(result)}")
        formatted.append("")
    
    return "\n".join(formatted) 