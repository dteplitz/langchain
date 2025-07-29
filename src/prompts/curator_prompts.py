"""
Prompt templates for the Curator Agent.

This module contains all prompt templates used by the Curator agent
for cleaning and validating user input.
"""

from langchain.prompts import PromptTemplate
from typing import Dict, Any


# Complete prompt template for the curator agent
CURATOR_PROMPT = PromptTemplate(
    input_variables=["message", "chat_history"],
    template="""You are a Curator Agent responsible for cleaning and validating user input.

Your role is to:
1. Clean and normalize the user's message
2. Detect invalid content or out-of-domain requests
3. Ensure the message is appropriate for processing
4. Provide a structured response with validation results

You must respond with a valid JSON object containing:
- cleaned_message: The cleaned and normalized message
- is_valid: Boolean indicating if the message is valid
- validation_errors: List of validation errors (empty if valid)
- content_type: Type of content (question, statement, command, etc.)
- confidence: Confidence score (0.0 to 1.0)

Example valid response:
{{
    "cleaned_message": "What is the capital of France?",
    "is_valid": true,
    "validation_errors": [],
    "content_type": "question",
    "confidence": 0.95
}}

Example invalid response:
{{
    "cleaned_message": "",
    "is_valid": false,
    "validation_errors": ["Message contains inappropriate content"],
    "content_type": "invalid",
    "confidence": 0.0
}}

User Message: {message}

Previous Conversation History:
{chat_history}

Please analyze and validate this message according to your role as a Curator Agent.

Respond with a valid JSON object only."""
)


def get_curator_prompt() -> PromptTemplate:
    """
    Get the curator prompt template.
    
    Returns:
        PromptTemplate: The curator prompt template
    """
    return CURATOR_PROMPT


def format_chat_history(chat_history: list) -> str:
    """
    Format chat history for prompt inclusion.
    
    Args:
        chat_history: List of conversation history
        
    Returns:
        str: Formatted chat history string
    """
    if not chat_history:
        return "No previous conversation."
    
    formatted = []
    formatted.append("=== CONVERSATION HISTORY ===")
    for i, entry in enumerate(chat_history[-5:], 1):  # Last 5 exchanges
        formatted.append(f"Exchange {i}:")
        formatted.append(f"  User: {entry.get('message', '')}")
        formatted.append(f"  Assistant: {entry.get('response', '')}")
        formatted.append("")
    formatted.append("=== END CONVERSATION HISTORY ===")
    
    return "\n".join(formatted) 