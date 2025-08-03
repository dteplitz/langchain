#!/usr/bin/env python3
"""
Example of how agents can use metadata for personalized responses.

This script demonstrates how the metadata system can be integrated
with agents to provide personalized and contextual responses.
"""

import uuid
from datetime import datetime
from src.memory.hybrid_conversation_memory import create_hybrid_memory
from src.agents.curator_agent import create_curator_agent


def setup_user_session():
    """Set up a user session with metadata."""
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id)
    
    # Set user information
    user_info = {
        "name": "Ana Rodríguez",
        "age": 28,
        "language": "español",
        "preferences": {
            "learning_style": "practical",
            "difficulty_level": "beginner",
            "topics_of_interest": ["programación", "diseño web", "inteligencia artificial"]
        },
        "session_start": datetime.now().isoformat()
    }
    memory.set_user_info(user_info)
    
    # Set conversation objective
    objective = "Ayudar a Ana a aprender programación web desde cero"
    memory.set_conversation_objective(objective)
    
    # Set conversation state
    conversation_state = {
        "current_topic": "introducción a HTML",
        "progress": {
            "completed_topics": [],
            "current_lesson": "estructura básica HTML",
            "score": 0
        },
        "last_interaction": datetime.now().isoformat(),
        "session_duration": 0
    }
    memory.set_conversation_state(conversation_state)
    
    return memory


def create_personalized_curator(memory):
    """Create a curator agent that uses metadata for personalization."""
    
    def personalized_curator_prompt(message: str, chat_history: list) -> str:
        """Create a personalized prompt based on user metadata."""
        
        # Get user information
        user_info = memory.get_user_info()
        conversation_state = memory.get_conversation_state()
        objective = memory.get_conversation_objective()
        
        # Create personalized context
        personalization = f"""
**INFORMACIÓN DEL USUARIO:**
- Nombre: {user_info.get('name', 'Usuario')}
- Edad: {user_info.get('age', 'No especificada')}
- Estilo de aprendizaje: {user_info.get('preferences', {}).get('learning_style', 'general')}
- Nivel de dificultad: {user_info.get('preferences', {}).get('difficulty_level', 'intermedio')}
- Tópicos de interés: {', '.join(user_info.get('preferences', {}).get('topics_of_interest', []))}

**ESTADO DE LA CONVERSACIÓN:**
- Objetivo: {objective}
- Tópico actual: {conversation_state.get('current_topic', 'No especificado')}
- Progreso: {conversation_state.get('progress', {}).get('current_lesson', 'No especificado')}
- Puntuación: {conversation_state.get('progress', {}).get('score', 0)}/100

**MENSAJE DEL USUARIO:**
{message}

**HISTORIAL DE CONVERSACIÓN:**
{format_chat_history(chat_history)}

Por favor, analiza este mensaje considerando el perfil del usuario y el contexto de la conversación.
        """
        
        return personalization
    
    return personalized_curator_prompt


def format_chat_history(chat_history: list) -> str:
    """Format chat history for display."""
    if not chat_history:
        return "No hay historial de conversación previo."
    
    formatted = []
    for i, entry in enumerate(chat_history[-3:], 1):
        if "message" in entry and "response" in entry:
            formatted.append(f"{i}. Usuario: {entry['message']}")
            formatted.append(f"{i}. Asistente: {entry['response']}")
    
    return "\n".join(formatted)


def simulate_personalized_conversation():
    """Simulate a personalized conversation using metadata."""
    
    print("🎭 Simulando conversación personalizada con metainformación")
    print("=" * 60)
    
    # Set up user session
    memory = setup_user_session()
    
    # Get user info for display
    user_info = memory.get_user_info()
    print(f"👤 Usuario: {user_info['name']} ({user_info['age']} años)")
    print(f"🎯 Objetivo: {memory.get_conversation_objective()}")
    print(f"📚 Estilo de aprendizaje: {user_info['preferences']['learning_style']}")
    print(f"📊 Nivel: {user_info['preferences']['difficulty_level']}")
    print()
    
    # Simulate conversation messages
    messages = [
        "Hola, ¿qué es HTML?",
        "¿Puedes mostrarme un ejemplo básico?",
        "¿Qué significa la etiqueta <div>?",
        "¿Cómo puedo hacer que mi página se vea mejor?"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"💬 Mensaje {i}: {message}")
        
        # Get current metadata for context
        current_state = memory.get_conversation_state()
        user_preferences = memory.get_user_info()['preferences']
        
        # Simulate agent processing with metadata context
        print(f"🔍 Contexto del agente:")
        print(f"   - Usuario: {user_info['name']}")
        print(f"   - Tópico actual: {current_state['current_topic']}")
        print(f"   - Estilo de aprendizaje: {user_preferences['learning_style']}")
        print(f"   - Nivel: {user_preferences['difficulty_level']}")
        
        # Simulate response based on user profile
        if user_preferences['learning_style'] == 'practical':
            print(f"🤖 Respuesta (estilo práctico): Te voy a mostrar ejemplos concretos y ejercicios prácticos...")
        else:
            print(f"🤖 Respuesta (estilo teórico): Te explico los conceptos fundamentales...")
        
        # Update conversation state
        if i == 1:
            memory.update_conversation_state("current_topic", "conceptos básicos de HTML")
        elif i == 2:
            memory.update_conversation_state("current_topic", "estructura HTML básica")
        elif i == 3:
            memory.update_conversation_state("current_topic", "etiquetas HTML comunes")
        elif i == 4:
            memory.update_conversation_state("current_topic", "CSS básico")
        
        # Update progress
        memory.update_conversation_state("progress.score", i * 25)
        memory.update_conversation_state("progress.completed_topics", 
                                       ["introducción", "ejemplos básicos", "etiquetas comunes"][:i])
        
        print(f"📊 Progreso actualizado: {i * 25}/100")
        print("-" * 40)
    
    # Show final metadata state
    print("\n📋 Estado final de la metainformación:")
    final_metadata = memory.get_session_metadata()
    import json
    print(json.dumps(final_metadata, indent=2, ensure_ascii=False))


def demonstrate_metadata_integration():
    """Demonstrate how metadata can be integrated with existing agents."""
    
    print("\n🔧 Demostrando integración con agentes existentes")
    print("=" * 60)
    
    # Create memory with metadata
    memory = setup_user_session()
    
    # Create curator agent
    curator = create_curator_agent(verbose=True)
    
    # Simulate processing a message with metadata context
    message = "¿Cómo puedo empezar a programar?"
    
    print(f"💬 Mensaje: {message}")
    
    # Get metadata for context
    user_info = memory.get_user_info()
    objective = memory.get_conversation_objective()
    
    print(f"🔍 Contexto disponible:")
    print(f"   - Usuario: {user_info['name']}")
    print(f"   - Objetivo: {objective}")
    print(f"   - Intereses: {user_info['preferences']['topics_of_interest']}")
    
    # Process with curator (this would normally use the metadata)
    try:
        result = curator.invoke({
            "message": message,
            "chat_history": [],
            "request_id": "metadata_demo"
        })
        
        print(f"✅ Resultado del curator:")
        print(f"   - Mensaje limpio: {result.cleaned_message}")
        print(f"   - Válido: {result.is_valid}")
        print(f"   - Tipo: {result.content_type}")
        print(f"   - Confianza: {result.confidence}")
        
    except Exception as e:
        print(f"❌ Error en el procesamiento: {e}")


if __name__ == "__main__":
    print("🎯 Ejemplo de uso de metainformación en agentes")
    print("=" * 60)
    
    # Run demonstrations
    simulate_personalized_conversation()
    demonstrate_metadata_integration()
    
    print("\n✨ Ejemplo completado!") 