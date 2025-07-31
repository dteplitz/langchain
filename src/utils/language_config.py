"""
Language configuration utilities for the LangChain project.

This module handles language-specific configurations, translations,
and locale settings for the application.
"""

from typing import Dict, Any, Optional
from src.config import get_settings


class LanguageConfig:
    """
    Language configuration manager for the application.
    
    Handles language-specific settings, translations, and locale configurations.
    """
    
    def __init__(self):
        """Initialize the language configuration."""
        self.settings = get_settings()
        self.language = self.settings.language.lower()
        self.locale = self.settings.locale
        
    def get_language_instruction(self) -> str:
        """
        Get the language instruction for prompts.
        
        Returns:
            str: Language instruction string
        """
        if self.language == "spanish":
            return "**IMPORTANTE: SIEMPRE responde en ESPAÑOL**"
        elif self.language == "english":
            return "**IMPORTANT: ALWAYS respond in ENGLISH**"
        else:
            return f"**IMPORTANT: ALWAYS respond in {self.language.upper()}**"
    
    def get_system_language_context(self) -> str:
        """
        Get system language context for prompts.
        
        Returns:
            str: System language context
        """
        if self.language == "spanish":
            return """
            Configuración de Idioma:
            - Idioma principal: Español
            - Locale: es-ES
            - Formato de fecha: DD/MM/YYYY
            - Separador decimal: coma (,)
            - Moneda: Euro (€)
            
            Instrucciones de Idioma:
            - Responde SIEMPRE en español
            - Usa términos y expresiones apropiados para el español
            - Mantén un tono formal pero amigable
            - Usa la puntuación correcta del español (¿, ¡, etc.)
            """
        else:
            return f"""
            Language Configuration:
            - Primary language: {self.language.title()}
            - Locale: {self.locale}
            
            Language Instructions:
            - Always respond in {self.language}
            - Use appropriate terms and expressions for {self.language}
            - Maintain a formal but friendly tone
            """
    
    def get_error_messages(self) -> Dict[str, str]:
        """
        Get error messages in the configured language.
        
        Returns:
            Dict[str, str]: Dictionary of error messages
        """
        if self.language == "spanish":
            return {
                "invalid_input": "Entrada inválida",
                "processing_error": "Error durante el procesamiento",
                "tool_error": "Error en la herramienta",
                "memory_error": "Error en la memoria de conversación",
                "api_error": "Error en la API",
                "timeout_error": "Tiempo de espera agotado",
                "validation_error": "Error de validación",
                "not_found": "No encontrado",
                "unauthorized": "No autorizado",
                "server_error": "Error del servidor"
            }
        else:
            return {
                "invalid_input": "Invalid input",
                "processing_error": "Processing error",
                "tool_error": "Tool error",
                "memory_error": "Conversation memory error",
                "api_error": "API error",
                "timeout_error": "Timeout error",
                "validation_error": "Validation error",
                "not_found": "Not found",
                "unauthorized": "Unauthorized",
                "server_error": "Server error"
            }
    
    def get_success_messages(self) -> Dict[str, str]:
        """
        Get success messages in the configured language.
        
        Returns:
            Dict[str, str]: Dictionary of success messages
        """
        if self.language == "spanish":
            return {
                "processing_complete": "Procesamiento completado",
                "response_generated": "Respuesta generada exitosamente",
                "tool_executed": "Herramienta ejecutada correctamente",
                "memory_updated": "Memoria actualizada",
                "validation_passed": "Validación exitosa"
            }
        else:
            return {
                "processing_complete": "Processing complete",
                "response_generated": "Response generated successfully",
                "tool_executed": "Tool executed successfully",
                "memory_updated": "Memory updated",
                "validation_passed": "Validation passed"
            }
    
    def format_date(self, date_obj: Any) -> str:
        """
        Format date according to locale settings.
        
        Args:
            date_obj: Date object to format
            
        Returns:
            str: Formatted date string
        """
        if self.language == "spanish":
            # Spanish date format: DD/MM/YYYY
            return date_obj.strftime("%d/%m/%Y")
        else:
            # Default format: YYYY-MM-DD
            return date_obj.strftime("%Y-%m-%d")
    
    def format_number(self, number: float) -> str:
        """
        Format number according to locale settings.
        
        Args:
            number: Number to format
            
        Returns:
            str: Formatted number string
        """
        if self.language == "spanish":
            # Spanish format: comma as decimal separator
            return f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            # Default format: period as decimal separator
            return f"{number:,.2f}"


# Global language config instance
_language_config = None


def get_language_config() -> LanguageConfig:
    """
    Get the global language configuration instance.
    
    Returns:
        LanguageConfig: The language configuration instance
    """
    global _language_config
    if _language_config is None:
        _language_config = LanguageConfig()
    return _language_config 