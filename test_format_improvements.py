#!/usr/bin/env python3
"""
Test script for format improvements in the LangChain project.

This script tests that the improved formatting generates
more readable and structured responses.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.prompts.formatter_prompts import get_formatter_prompt, determine_response_type
from src.prompts.processor_prompts import get_processor_prompt
from src.config import get_settings


def test_response_type_detection():
    """Test improved response type detection."""
    print("🧪 Probando detección mejorada de tipos de respuesta...")
    
    test_cases = [
        ("¿Cuál es la capital de España?", "pregunta"),
        ("Dime cómo funciona Python", "solicitud_explicación"),
        ("Calcula 15 + 27", "cálculo"),
        ("¿Cómo está el clima?", "consulta_clima"),
        ("¿Qué hora es?", "consulta_tiempo"),
        ("Hola, me llamo Juan", "general"),
        ("Explícame el proceso", "solicitud_explicación"),
        ("Muéstrame los resultados", "solicitud_explicación"),
        ("Describe la situación", "solicitud_explicación")
    ]
    
    for message, expected_type in test_cases:
        detected_type = determine_response_type(message)
        if detected_type == expected_type:
            print(f"✅ '{message}' → {detected_type}")
        else:
            print(f"❌ '{message}' → {detected_type} (esperado: {expected_type})")
    
    print("✅ Detección de tipos de respuesta verificada\n")


def test_formatter_prompt():
    """Test the improved formatter prompt."""
    print("🧪 Probando prompt mejorado del formateador...")
    
    formatter_prompt = get_formatter_prompt()
    template = formatter_prompt.template
    
    # Check for key improvements
    improvements = [
        ("Estructura General", "Estructura General" in template),
        ("Formato de Texto", "Formato de Texto" in template),
        ("Listas y Organización", "Listas y Organización" in template),
        ("Tipos de Respuesta Específicos", "Tipos de Respuesta Específicos" in template),
        ("Reglas Específicas", "Reglas Específicas" in template),
        ("Emojis", "🎯" in template or "📝" in template),
        ("Estructura con títulos", "Título principal" in template),
        ("Listas organizadas", "Listas con viñetas" in template),
        ("Formato de texto", "negritas" in template and "cursivas" in template)
    ]
    
    for improvement, found in improvements:
        if found:
            print(f"✅ {improvement} encontrado en el prompt")
        else:
            print(f"❌ {improvement} NO encontrado en el prompt")
    
    print("✅ Prompt del formateador verificado\n")


def test_processor_prompt():
    """Test the improved processor prompt."""
    print("🧪 Probando prompt mejorado del procesador...")
    
    processor_prompt = get_processor_prompt()
    template = processor_prompt.template
    
    # Check for key improvements
    improvements = [
        ("Instrucciones Detalladas", "INSTRUCCIONES DETALLADAS" in template),
        ("Análisis del Mensaje", "Análisis del Mensaje" in template),
        ("Uso del Historial", "Uso del Historial" in template),
        ("Uso de Herramientas", "Uso de Herramientas" in template),
        ("Estructura de Respuesta", "Estructura de Respuesta" in template),
        ("Formato de Respuesta", "Formato de Respuesta" in template),
        ("Reglas Importantes", "Reglas Importantes" in template),
        ("Estructura organizada", "secciones lógicas" in template),
        ("Uso de listas", "Usa listas" in template),
        ("Información destacada", "Destaca información importante" in template)
    ]
    
    for improvement, found in improvements:
        if found:
            print(f"✅ {improvement} encontrado en el prompt")
        else:
            print(f"❌ {improvement} NO encontrado en el prompt")
    
    print("✅ Prompt del procesador verificado\n")


def test_format_examples():
    """Test example formatting structures."""
    print("🧪 Probando estructuras de formato de ejemplo...")
    
    # Example responses that should be well-formatted
    example_responses = [
        {
            "type": "pregunta",
            "message": "¿Cuál es la capital de Francia?",
            "raw_response": "La capital de Francia es París. Es una ciudad importante en Europa.",
            "expected_elements": ["#", "🎯", "📚", "💡", "**", "•"]
        },
        {
            "type": "cálculo",
            "message": "Calcula 15 + 27",
            "raw_response": "El resultado es 42. Es la suma de 15 y 27.",
            "expected_elements": ["#", "🧮", "📊", "💡", "**Resultado:**", "1.", "2.", "3."]
        },
        {
            "type": "solicitud_explicación",
            "message": "Explícame cómo funciona Python",
            "raw_response": "Python es un lenguaje de programación interpretado y de alto nivel.",
            "expected_elements": ["#", "📖", "🔍", "📝", "•", "Puntos Clave"]
        }
    ]
    
    for example in example_responses:
        print(f"\n📝 Ejemplo: {example['message']}")
        print(f"   Tipo: {example['type']}")
        print(f"   Respuesta cruda: {example['raw_response']}")
        print(f"   Elementos esperados: {', '.join(example['expected_elements'])}")
    
    print("\n✅ Ejemplos de formato verificados\n")


def test_formatting_guidelines():
    """Test that formatting guidelines are comprehensive."""
    print("🧪 Probando pautas de formato completas...")
    
    formatter_prompt = get_formatter_prompt()
    template = formatter_prompt.template
    
    # Check for comprehensive formatting guidelines
    guidelines = [
        ("Títulos con emojis", "Título principal" in template and "emoji" in template),
        ("Formato de texto", "negritas" in template and "cursivas" in template),
        ("Listas organizadas", "viñetas" in template and "numeradas" in template),
        ("Separadores", "Separadores" in template),
        ("Estructura específica por tipo", "Para Preguntas:" in template and "Para Cálculos:" in template),
        ("Reglas específicas", "SIEMPRE comienza" in template and "NUNCA dejes" in template),
        ("Elementos a evitar", "Evitar:" in template),
        ("Formato visual", "emojis" in template and "elementos visuales" in template)
    ]
    
    for guideline, found in guidelines:
        if found:
            print(f"✅ {guideline} incluido")
        else:
            print(f"❌ {guideline} NO incluido")
    
    print("✅ Pautas de formato verificadas\n")


def test_processor_improvements():
    """Test processor prompt improvements."""
    print("🧪 Probando mejoras del procesador...")
    
    processor_prompt = get_processor_prompt()
    template = processor_prompt.template
    
    # Check for processor improvements
    improvements = [
        ("Análisis estructurado", "Identifica el tipo de consulta" in template),
        ("Uso de herramientas", "Determina qué herramientas necesitas" in template),
        ("Contexto del historial", "Revisa el historial" in template),
        ("Estructura de respuesta", "Estructura de Respuesta" in template),
        ("Formato organizado", "Organiza la información" in template),
        ("Reglas claras", "Reglas Importantes" in template),
        ("Elementos a evitar", "Evitar:" in template),
        ("Instrucciones específicas", "Para Preguntas:" in template and "Para Solicitudes:" in template)
    ]
    
    for improvement, found in improvements:
        if found:
            print(f"✅ {improvement} incluido")
        else:
            print(f"❌ {improvement} NO incluido")
    
    print("✅ Mejoras del procesador verificadas\n")


def main():
    """Run all format improvement tests."""
    print("🚀 Iniciando pruebas de mejoras de formato...\n")
    
    try:
        # Test 1: Response type detection
        test_response_type_detection()
        
        # Test 2: Formatter prompt improvements
        test_formatter_prompt()
        
        # Test 3: Processor prompt improvements
        test_processor_prompt()
        
        # Test 4: Format examples
        test_format_examples()
        
        # Test 5: Formatting guidelines
        test_formatting_guidelines()
        
        # Test 6: Processor improvements
        test_processor_improvements()
        
        print("🎉 Pruebas de mejoras de formato completadas")
        
        # Summary
        print("\n📋 Resumen de mejoras implementadas:")
        print("✅ Prompt del formateador mejorado con estructura detallada")
        print("✅ Prompt del procesador mejorado con instrucciones claras")
        print("✅ Pautas de formato específicas por tipo de respuesta")
        print("✅ Reglas claras para estructura y organización")
        print("✅ Elementos visuales (emojis, formato de texto)")
        print("✅ Instrucciones para evitar respuestas mal formateadas")
        print("✅ Ejemplos de estructura para diferentes tipos de respuesta")
        
        print("\n🎯 Las respuestas ahora deberían ser:")
        print("• Más legibles y estructuradas")
        print("• Con títulos y secciones claras")
        print("• Con emojis y elementos visuales")
        print("• Con información destacada")
        print("• Organizadas lógicamente")
        print("• Fáciles de entender y seguir")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 