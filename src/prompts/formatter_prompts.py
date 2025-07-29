"""
Prompt templates for the Response Formatter Agent.

This module contains all prompt templates used by the Response Formatter agent
for formatting and structuring the final response.
"""

from langchain.prompts import PromptTemplate
from typing import Dict, Any


# Complete prompt template for the formatter agent
FORMATTER_PROMPT = PromptTemplate(
    input_variables=["raw_response", "user_message", "response_type"],
    template="""You are a Response Formatter Agent responsible for formatting and structuring the final response to users.

Your role is to:
1. Take the raw response from the processor agent
2. Format it in a clear, structured, and user-friendly way
3. Ensure the response is concise but comprehensive
4. Add appropriate formatting and structure

User's Original Message: {user_message}
Response Type: {response_type}
Raw Response from Processor: {raw_response}

Formatting Guidelines:
- Make the response clear and easy to read
- Use bullet points or numbered lists when appropriate
- Highlight key information
- Keep the response concise but informative
- Maintain a helpful and professional tone
- If it's a question, provide a direct answer first, then context
- If it's a statement, acknowledge and provide relevant information

Format the response to be user-friendly and well-structured."""
)


def get_formatter_prompt() -> PromptTemplate:
    """
    Get the formatter prompt template.
    
    Returns:
        PromptTemplate: The formatter prompt template
    """
    return FORMATTER_PROMPT


def determine_response_type(user_message: str) -> str:
    """
    Determine the type of response needed based on user message.
    
    Args:
        user_message: The user's message
        
    Returns:
        str: Response type (question, statement, command, etc.)
    """
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which']):
        return "question"
    elif any(word in message_lower for word in ['tell me', 'explain', 'describe', 'show me']):
        return "explanation_request"
    elif any(word in message_lower for word in ['calculate', 'compute', 'solve']):
        return "calculation"
    elif any(word in message_lower for word in ['weather', 'temperature', 'forecast']):
        return "weather_inquiry"
    elif any(word in message_lower for word in ['time', 'date', 'schedule']):
        return "time_inquiry"
    else:
        return "general" 