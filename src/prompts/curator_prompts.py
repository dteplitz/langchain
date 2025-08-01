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
    template="""Eres un Agente Curador responsable de limpiar y validar la entrada del usuario.

Tu rol es:
1. Limpiar y normalizar el mensaje del usuario
2. Detectar contenido inválido o solicitudes fuera del dominio
3. Asegurar que el mensaje sea apropiado para el procesamiento
4. Proporcionar una respuesta estructurada con los resultados de validación

**IMPORTANTE: SIEMPRE responde en ESPAÑOL**

Debes responder con un objeto JSON válido que contenga:
- cleaned_message: El mensaje limpio y normalizado
- is_valid: Booleano que indica si el mensaje es válido
- validation_errors: Lista de errores de validación (vacía si es válido)
- content_type: Tipo de contenido (pregunta, declaración, comando, etc.)
- confidence: Puntuación de confianza (0.0 a 1.0)

Ejemplo de respuesta válida:
{{
    "cleaned_message": "¿Cuál es la capital de Francia?",
    "is_valid": true,
    "validation_errors": [],
    "content_type": "pregunta",
    "confidence": 0.95
}}

Ejemplo de respuesta inválida:
{{
    "cleaned_message": "",
    "is_valid": false,
    "validation_errors": ["El mensaje contiene contenido inapropiado"],
    "content_type": "inválido",
    "confidence": 0.0
}}

Mensaje del Usuario: {message}

Historial de Conversación Anterior:
{chat_history}

Por favor, analiza y valida este mensaje según tu rol como Agente Curador.

Responde ÚNICAMENTE con un objeto JSON válido."""
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
        chat_history: List of chat messages from memory (with 'message' and 'response' keys)
        
    Returns:
        str: Formatted chat history string
    """
    if not chat_history:
        return "No hay historial de conversación previo."
    
    formatted_history = []
    for i, entry in enumerate(chat_history[-5:], 1):  # Last 5 messages
        # Handle both memory format (message/response) and agent format (role/content)
        if "message" in entry and "response" in entry:
            # Memory format from SQLite
            user_message = entry.get("message", "")
            assistant_response = entry.get("response", "")
            formatted_history.append(f"{i}. Usuario: {user_message}")
            formatted_history.append(f"{i}. Asistente: {assistant_response}")
        elif "role" in entry and "content" in entry:
            # Agent format
            role = "Usuario" if entry.get("role") == "user" else "Asistente"
            content = entry.get("content", "")
            formatted_history.append(f"{i}. {role}: {content}")
        else:
            # Fallback for unknown format
            formatted_history.append(f"{i}. Mensaje: {str(entry)}")
    
    return "\n".join(formatted_history) 