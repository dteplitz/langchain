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
    template="""Eres un Agente Formateador de Respuestas responsable de formatear y estructurar la respuesta final a los usuarios.

Tu rol es:
1. Tomar la respuesta cruda del agente procesador
2. Formatearla de manera clara, estructurada y fácil de usar
3. Asegurar que la respuesta sea concisa pero completa
4. Agregar formato y estructura apropiados

**IMPORTANTE: SIEMPRE responde en ESPAÑOL**

Mensaje Original del Usuario: {user_message}
Tipo de Respuesta: {response_type}
Respuesta Cruda del Procesador: {raw_response}

Pautas de Formato:
- Haz la respuesta clara y fácil de leer
- Usa viñetas o listas numeradas cuando sea apropiado
- Destaca información clave
- Mantén la respuesta concisa pero informativa
- Mantén un tono útil y profesional
- Si es una pregunta, proporciona una respuesta directa primero, luego contexto
- Si es una declaración, reconoce y proporciona información relevante
- **Responde SIEMPRE en ESPAÑOL**

Formatea la respuesta para que sea fácil de usar y bien estructurada."""
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
        str: Response type (pregunta, declaración, comando, etc.)
    """
    message_lower = user_message.lower()
    
    # Check for explanation requests first (to avoid conflicts with questions)
    if any(word in message_lower for word in ['dime', 'explícame', 'describe', 'muéstrame', 'muestrame']):
        return "solicitud_explicación"
    # Then check for questions
    elif any(word in message_lower for word in ['qué', 'que', 'cual', 'cuál', 'como', 'cómo', 'por qué', 'porque', 'cuando', 'cuándo', 'donde', 'dónde', 'quien', 'quién']):
        return "pregunta"
    elif any(word in message_lower for word in ['calcula', 'calcula', 'resuelve', 'resuelve']):
        return "cálculo"
    elif any(word in message_lower for word in ['clima', 'temperatura', 'pronóstico', 'pronostico']):
        return "consulta_clima"
    elif any(word in message_lower for word in ['hora', 'fecha', 'programa', 'agenda']):
        return "consulta_tiempo"
    else:
        return "general" 