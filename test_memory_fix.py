#!/usr/bin/env python3
"""
Test script for memory issues in the LangChain project.

This script tests the conversation memory system to identify
and fix issues with chat history formatting and persistence.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.memory.conversation_memory import create_memory, get_conversation_history
from src.prompts.curator_prompts import format_chat_history
from src.config import get_settings


def test_memory_creation():
    """Test memory creation and database initialization."""
    print("🧪 Probando creación de memoria...")
    
    try:
        # Create memory for test session
        session_id = "test_session_123"
        memory = create_memory(session_id)
        
        print(f"✅ Memoria creada para sesión: {session_id}")
        print(f"✅ Ruta de base de datos: {memory.db_path}")
        
        # Test database initialization
        import sqlite3
        with sqlite3.connect(memory.db_path) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
            if cursor.fetchone():
                print("✅ Tabla 'conversations' existe")
            else:
                print("❌ Tabla 'conversations' NO existe")
        
        return memory
        
    except Exception as e:
        print(f"❌ Error creando memoria: {e}")
        return None


def test_memory_save_and_load():
    """Test saving and loading conversation data."""
    print("\n🧪 Probando guardado y carga de conversación...")
    
    try:
        session_id = "test_session_456"
        memory = create_memory(session_id)
        
        # Test data
        test_message = "Hola, ¿cómo estás?"
        test_response = "¡Hola! Estoy muy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?"
        
        # Save conversation
        memory.save_context(
            {"message": test_message},
            {"response": test_response}
        )
        print("✅ Conversación guardada")
        
        # Load conversation history
        history = get_conversation_history(session_id, limit=5)
        print(f"✅ Historial cargado: {len(history)} mensajes")
        
        if history:
            last_message = history[-1]
            print(f"✅ Último mensaje: {last_message.get('message', 'N/A')}")
            print(f"✅ Última respuesta: {last_message.get('response', 'N/A')[:50]}...")
        
        return history
        
    except Exception as e:
        print(f"❌ Error en guardado/carga: {e}")
        return []


def test_chat_history_format():
    """Test chat history formatting for agents."""
    print("\n🧪 Probando formato de historial de chat...")
    
    try:
        # Create test history in the format returned by get_conversation_history
        test_history = [
            {
                "message": "Hola, me llamo Juan",
                "response": "¡Hola Juan! Es un placer conocerte. ¿En qué puedo ayudarte?",
                "timestamp": "2024-01-01 10:00:00"
            },
            {
                "message": "¿Cuál es mi nombre?",
                "response": "Tu nombre es Juan, como me dijiste anteriormente.",
                "timestamp": "2024-01-01 10:01:00"
            }
        ]
        
        print("📝 Historial de prueba:")
        for i, entry in enumerate(test_history, 1):
            print(f"  {i}. Usuario: {entry['message']}")
            print(f"     Asistente: {entry['response'][:50]}...")
        
        # Test formatting
        formatted = format_chat_history(test_history)
        print(f"\n📝 Historial formateado:")
        print(formatted)
        
        # Check if format is correct for agents
        if "Usuario:" in formatted and "Asistente:" in formatted:
            print("✅ Formato correcto para agentes")
        else:
            print("❌ Formato incorrecto para agentes")
        
        return formatted
        
    except Exception as e:
        print(f"❌ Error en formato: {e}")
        return ""


def test_memory_integration():
    """Test memory integration with agents."""
    print("\n🧪 Probando integración de memoria con agentes...")
    
    try:
        session_id = "test_integration_789"
        memory = create_memory(session_id)
        
        # Simulate a conversation
        conversations = [
            ("Hola, me llamo María", "¡Hola María! Es un placer conocerte."),
            ("¿Recuerdas mi nombre?", "Sí, tu nombre es María."),
            ("¿Cuál es mi nombre?", "Tu nombre es María, como me dijiste anteriormente.")
        ]
        
        # Save conversations
        for message, response in conversations:
            memory.save_context(
                {"message": message},
                {"response": response}
            )
        
        print(f"✅ {len(conversations)} conversaciones guardadas")
        
        # Load history
        history = get_conversation_history(session_id, limit=10)
        print(f"✅ Historial cargado: {len(history)} mensajes")
        
        # Format for agents
        formatted_history = format_chat_history(history)
        print(f"\n📝 Historial formateado para agentes:")
        print(formatted_history)
        
        # Check if name is preserved
        if "María" in formatted_history:
            print("✅ Nombre del usuario preservado en el historial")
        else:
            print("❌ Nombre del usuario NO preservado")
        
        return history
        
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        return []


def test_database_operations():
    """Test database operations and error handling."""
    print("\n🧪 Probando operaciones de base de datos...")
    
    try:
        settings = get_settings()
        db_path = settings.database_url.replace("sqlite:///", "")
        
        print(f"📁 Ruta de base de datos: {db_path}")
        
        # Check if database file exists
        if os.path.exists(db_path):
            print("✅ Archivo de base de datos existe")
            
            # Check file size
            size = os.path.getsize(db_path)
            print(f"📊 Tamaño de archivo: {size} bytes")
        else:
            print("⚠️  Archivo de base de datos NO existe")
        
        # Test database connection
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            # Check table structure
            cursor = conn.execute("PRAGMA table_info(conversations)")
            columns = cursor.fetchall()
            print(f"📋 Columnas en tabla 'conversations': {len(columns)}")
            
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Check record count
            cursor = conn.execute("SELECT COUNT(*) FROM conversations")
            count = cursor.fetchone()[0]
            print(f"📊 Total de registros: {count}")
            
            # Check recent records
            cursor = conn.execute("""
                SELECT session_id, message, response, timestamp 
                FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT 3
            """)
            
            recent = cursor.fetchall()
            print(f"📝 Registros recientes: {len(recent)}")
            
            for record in recent:
                print(f"  - Sesión: {record[0]}")
                print(f"    Mensaje: {record[1][:30]}...")
                print(f"    Respuesta: {record[2][:30]}...")
                print(f"    Timestamp: {record[3]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en operaciones de base de datos: {e}")
        return False


def main():
    """Run all memory tests."""
    print("🚀 Iniciando pruebas de memoria...\n")
    
    try:
        # Test 1: Memory creation
        memory = test_memory_creation()
        if not memory:
            print("❌ No se pudo crear memoria - abortando pruebas")
            return
        
        # Test 2: Save and load
        history = test_memory_save_and_load()
        
        # Test 3: Format testing
        formatted = test_chat_history_format()
        
        # Test 4: Integration testing
        integration_history = test_memory_integration()
        
        # Test 5: Database operations
        db_ok = test_database_operations()
        
        print("\n🎉 Pruebas de memoria completadas")
        
        # Summary
        print("\n📋 Resumen:")
        print(f"✅ Creación de memoria: {'OK' if memory else 'FAIL'}")
        print(f"✅ Guardado/Carga: {'OK' if history else 'FAIL'}")
        print(f"✅ Formato: {'OK' if formatted else 'FAIL'}")
        print(f"✅ Integración: {'OK' if integration_history else 'FAIL'}")
        print(f"✅ Base de datos: {'OK' if db_ok else 'FAIL'}")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 