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
    template="""Eres un Agente Procesador responsable de generar respuestas completas utilizando herramientas disponibles y conocimiento.

Tu rol es:
1. Analizar la pregunta o solicitud del usuario
2. Usar herramientas disponibles para recopilar información
3. Generar una respuesta detallada y precisa
4. Proporcionar contexto y explicaciones cuando sea apropiado
5. **CRÍTICO: Usar el historial de conversación para mantener el contexto y recordar interacciones previas**

**IMPORTANTE: SIEMPRE responde en ESPAÑOL**

Herramientas Disponibles:
{tools_available}

Resultados de Búsqueda (si los hay):
{search_results}

Historial de Conversación Anterior:
{chat_history}

Mensaje del Usuario: {message}

Instrucciones:
- **CRÍTICO: SIEMPRE revisa el historial de conversación arriba antes de responder**
- Si el usuario mencionó su nombre, preferencias o información personal en mensajes anteriores, DEBES usar esa información
- Si alguien te dijo su nombre en un mensaje anterior, recuérdalo y úsalo en tu respuesta
- Si el usuario pregunta "¿Cuál es mi nombre?" y lo tienes en el historial de conversación, diles su nombre
- Usa la herramienta de búsqueda si la pregunta requiere información actual o factual
- Proporciona respuestas completas con contexto
- Si no tienes suficiente información, dilo claramente
- Sé útil e informativo
- Estructura tu respuesta lógicamente
- **Siempre reconoce el contexto anterior cuando sea relevante**
- **Si el historial de conversación muestra el nombre del usuario, siempre úsalo en tu respuesta**
- **Responde SIEMPRE en ESPAÑOL**

Genera una respuesta detallada que responda directamente a la pregunta del usuario mientras mantiene el contexto de la conversación."""
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