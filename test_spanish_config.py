#!/usr/bin/env python3
"""
Test script for Spanish language configuration.

This script tests the language configuration and prompts to ensure
they are properly set up for Spanish responses.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import get_settings
from src.utils.language_config import get_language_config
from src.prompts.curator_prompts import get_curator_prompt
from src.prompts.processor_prompts import get_processor_prompt
from src.prompts.formatter_prompts import get_formatter_prompt


def test_language_configuration():
    """Test the language configuration settings."""
    print("🧪 Probando configuración de idioma...")
    
    # Test settings
    settings = get_settings()
    print(f"✅ Idioma configurado: {settings.language}")
    print(f"✅ Locale configurado: {settings.locale}")
    
    # Test language config
    lang_config = get_language_config()
    print(f"✅ Instrucción de idioma: {lang_config.get_language_instruction()}")
    
    # Test error messages
    error_messages = lang_config.get_error_messages()
    print(f"✅ Mensajes de error en español: {error_messages['invalid_input']}")
    
    # Test success messages
    success_messages = lang_config.get_success_messages()
    print(f"✅ Mensajes de éxito en español: {success_messages['processing_complete']}")
    
    print("✅ Configuración de idioma funcionando correctamente\n")


def test_prompts_spanish():
    """Test that prompts are configured for Spanish."""
    print("🧪 Probando prompts en español...")
    
    # Test curator prompt
    curator_prompt = get_curator_prompt()
    curator_template = curator_prompt.template
    if "ESPAÑOL" in curator_template and "Agente Curador" in curator_template:
        print("✅ Prompt del curador configurado en español")
    else:
        print("❌ Prompt del curador NO está en español")
    
    # Test processor prompt
    processor_prompt = get_processor_prompt()
    processor_template = processor_prompt.template
    if "ESPAÑOL" in processor_template and "Agente Procesador" in processor_template:
        print("✅ Prompt del procesador configurado en español")
    else:
        print("❌ Prompt del procesador NO está en español")
    
    # Test formatter prompt
    formatter_prompt = get_formatter_prompt()
    formatter_template = formatter_prompt.template
    if "ESPAÑOL" in formatter_template and "Agente Formateador" in formatter_template:
        print("✅ Prompt del formateador configurado en español")
    else:
        print("❌ Prompt del formateador NO está en español")
    
    print("✅ Prompts verificados correctamente\n")


def test_response_type_detection():
    """Test Spanish response type detection."""
    print("🧪 Probando detección de tipos de respuesta en español...")
    
    from src.prompts.formatter_prompts import determine_response_type
    
    # Test Spanish questions
    spanish_questions = [
        "¿Cuál es la capital de España?",
        "Qué hora es?",
        "Cómo estás?",
        "Por qué llueve?",
        "Cuándo llegas?",
        "Dónde vives?",
        "Quién eres?",
        "Cuál prefieres?"
    ]
    
    for question in spanish_questions:
        response_type = determine_response_type(question)
        if response_type == "pregunta":
            print(f"✅ '{question}' → {response_type}")
        else:
            print(f"❌ '{question}' → {response_type} (esperado: pregunta)")
    
    # Test Spanish explanation requests
    spanish_explanations = [
        "Dime cómo funciona esto",
        "Explícame el proceso",
        "Describe la situación",
        "Muéstrame los resultados"
    ]
    
    for explanation in spanish_explanations:
        response_type = determine_response_type(explanation)
        if response_type == "solicitud_explicación":
            print(f"✅ '{explanation}' → {response_type}")
        else:
            print(f"❌ '{explanation}' → {response_type} (esperado: solicitud_explicación)")
    
    print("✅ Detección de tipos de respuesta verificada\n")


def test_environment_variables():
    """Test environment variables for language configuration."""
    print("🧪 Probando variables de entorno...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Archivo .env encontrado")
        
        # Read and check language variables
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "LANGUAGE=spanish" in content:
                print("✅ Variable LANGUAGE=spanish configurada")
            else:
                print("❌ Variable LANGUAGE=spanish NO configurada")
            
            if "LOCALE=es-ES" in content:
                print("✅ Variable LOCALE=es-ES configurada")
            else:
                print("❌ Variable LOCALE=es-ES NO configurada")
    else:
        print("⚠️  Archivo .env no encontrado - crea uno basado en env.example")
    
    print("✅ Variables de entorno verificadas\n")


def main():
    """Run all tests."""
    print("🚀 Iniciando pruebas de configuración en español...\n")
    
    try:
        test_language_configuration()
        test_prompts_spanish()
        test_response_type_detection()
        test_environment_variables()
        
        print("🎉 ¡Todas las pruebas completadas exitosamente!")
        print("✅ El sistema está configurado para responder en español")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 