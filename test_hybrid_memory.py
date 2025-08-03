"""
Test script for Hybrid Conversation Memory.

This script demonstrates the hybrid memory functionality:
- Buffer mode for short conversations
- Summary mode for long conversations
- Metadata management
- Automatic switching between modes
"""

import uuid
import time
from src.memory.hybrid_conversation_memory import create_hybrid_memory, get_hybrid_conversation_history


def test_hybrid_memory_basic():
    """Test basic hybrid memory functionality."""
    print("🧪 Testing Basic Hybrid Memory Functionality")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id, verbose=True)
    
    print(f"📋 Session ID: {session_id}")
    print(f"📊 Initial stats: {memory.get_memory_stats()}")
    
    # Test metadata functionality
    print("\n🔧 Testing Metadata Functionality:")
    memory.set_welcome_status(True)
    memory.add_reason("Testing hybrid memory")
    memory.set_loan_variables(monthly=1000, duration=12, rate=5.5)
    
    print(f"✅ Welcome status: {memory.get_welcome_status()}")
    print(f"✅ Reasons: {memory.get_reasons()}")
    print(f"✅ Loan variables: {memory.get_loan_variables()}")
    print(f"✅ Loan complete: {memory.is_loan_info_complete()}")


def test_buffer_mode():
    """Test buffer mode for short conversations."""
    print("\n\n🧪 Testing Buffer Mode (Short Conversations)")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id, summary_threshold=5, verbose=True)
    
    # Simulate short conversation (buffer mode)
    messages = [
        ("Hola, ¿cómo estás?", "¡Hola! Estoy muy bien, gracias por preguntar."),
        ("¿Qué puedes hacer?", "Puedo ayudarte con muchas cosas, como cálculos, búsquedas y conversaciones."),
        ("¿Puedes calcular 2+2?", "Por supuesto, 2 + 2 = 4."),
        ("Gracias", "¡De nada! Estoy aquí para ayudarte.")
    ]
    
    for i, (user_msg, ai_response) in enumerate(messages, 1):
        print(f"\n💬 Message {i}:")
        print(f"   User: {user_msg}")
        print(f"   AI: {ai_response}")
        
        # Save to memory
        memory.save_context(
            {"message": user_msg},
            {"response": ai_response}
        )
        
        # Load memory variables
        vars = memory.load_memory_variables({})
        print(f"   📊 Memory mode: {'Summary' if memory._should_use_summary() else 'Buffer'}")
        print(f"   📝 Recent history length: {len(vars.get('recent_history', []))}")
        print(f"   📋 Summary: {vars.get('conversation_summary', 'N/A')[:50]}...")


def test_summary_mode():
    """Test summary mode for long conversations."""
    print("\n\n🧪 Testing Summary Mode (Long Conversations)")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id, summary_threshold=3, verbose=True)
    
    # Simulate long conversation (will trigger summary mode)
    long_conversation = [
        ("Hola, necesito ayuda con un préstamo", "¡Hola! Te ayudo con tu préstamo. ¿Qué información necesitas?"),
        ("Quiero comprar una casa", "Excelente decisión. Para ayudarte mejor, necesito saber el precio de la casa."),
        ("La casa cuesta $200,000", "Perfecto. ¿Tienes un enganche o pagarás el 100% con préstamo?"),
        ("Tengo $40,000 de enganche", "Muy bien. Entonces necesitarás un préstamo de $160,000."),
        ("¿Cuál sería mi pago mensual?", "Para calcular tu pago mensual, necesito saber la tasa de interés y el plazo."),
        ("Tasa del 5% por 30 años", "Con esos datos, tu pago mensual sería aproximadamente $859."),
        ("¿Puedes explicarme cómo se calcula?", "Claro. El pago se calcula usando la fórmula de amortización."),
        ("¿Qué otros costos debo considerar?", "Además del pago principal, debes considerar impuestos, seguro y mantenimiento."),
        ("¿Cuánto son los impuestos?", "Los impuestos varían por ubicación, pero típicamente son 1-2% del valor de la casa."),
        ("¿Y el seguro?", "El seguro de hogar típicamente cuesta $800-$1,200 por año."),
        ("¿Cuándo puedo aplicar?", "Puedes aplicar en cualquier momento. Te recomiendo comparar varias opciones."),
        ("¿Qué documentos necesito?", "Necesitarás comprobantes de ingresos, historial crediticio y documentación de la propiedad.")
    ]
    
    for i, (user_msg, ai_response) in enumerate(long_conversation, 1):
        print(f"\n💬 Message {i}:")
        print(f"   User: {user_msg}")
        print(f"   AI: {ai_response}")
        
        # Save to memory
        memory.save_context(
            {"message": user_msg},
            {"response": ai_response}
        )
        
        # Load memory variables
        vars = memory.load_memory_variables({})
        print(f"   📊 Memory mode: {'Summary' if memory._should_use_summary() else 'Buffer'}")
        print(f"   📝 Recent history length: {len(vars.get('recent_history', []))}")
        
        summary = vars.get('conversation_summary', '')
        if summary:
            print(f"   📋 Summary: {summary[:100]}...")
        
        # Show stats every few messages
        if i % 4 == 0:
            stats = memory.get_memory_stats()
            print(f"   📈 Stats: {stats}")


def test_memory_comparison():
    """Compare buffer vs summary memory usage."""
    print("\n\n🧪 Testing Memory Usage Comparison")
    print("=" * 50)
    
    # Test with different thresholds
    thresholds = [3, 5, 10]
    
    for threshold in thresholds:
        print(f"\n📊 Testing with threshold = {threshold}")
        
        session_id = str(uuid.uuid4())
        memory = create_hybrid_memory(session_id, summary_threshold=threshold, verbose=False)
        
        # Add some messages
        for i in range(threshold + 2):
            user_msg = f"Message {i+1}"
            ai_response = f"Response {i+1}"
            
            memory.save_context(
                {"message": user_msg},
                {"response": ai_response}
            )
        
        # Check final state
        vars = memory.load_memory_variables({})
        stats = memory.get_memory_stats()
        
        print(f"   📝 Final length: {stats['conversation_length']}")
        print(f"   🔄 Using summary: {stats['using_summary']}")
        print(f"   📋 Recent history: {len(vars.get('recent_history', []))} messages")
        print(f"   📄 Summary length: {len(vars.get('conversation_summary', ''))} chars")


def test_conversation_history():
    """Test conversation history retrieval."""
    print("\n\n🧪 Testing Conversation History Retrieval")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id, summary_threshold=3, verbose=False)
    
    # Add some messages
    messages = [
        ("Hello", "Hi there!"),
        ("How are you?", "I'm doing great, thanks!"),
        ("What's the weather?", "I can't check the weather right now, but I can help with other things."),
        ("Tell me a joke", "Why don't scientists trust atoms? Because they make up everything!"),
        ("That's funny", "I'm glad you liked it! 😄")
    ]
    
    for user_msg, ai_response in messages:
        memory.save_context(
            {"message": user_msg},
            {"response": ai_response}
        )
    
    # Get conversation history
    history = get_hybrid_conversation_history(session_id, limit=10, include_summary=True)
    
    print(f"📋 Recent messages: {len(history['recent_messages'])}")
    print(f"📄 Summary: {history['conversation_summary'][:100]}...")
    print(f"📊 Total messages: {history['total_messages']}")
    
    # Show recent messages
    print("\n💬 Recent Messages:")
    for msg in history['recent_messages']:
        print(f"   User: {msg['message']}")
        print(f"   AI: {msg['response']}")
        print(f"   Time: {msg['timestamp']}")
        print()


def test_memory_persistence():
    """Test memory persistence across instances."""
    print("\n\n🧪 Testing Memory Persistence")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    
    # First instance
    print("📝 Creating first memory instance...")
    memory1 = create_hybrid_memory(session_id, verbose=False)
    memory1.set_welcome_status(True)
    memory1.add_reason("Testing persistence")
    memory1.save_context(
        {"message": "Hello"},
        {"response": "Hi there!"}
    )
    
    stats1 = memory1.get_memory_stats()
    print(f"   📊 First instance stats: {stats1}")
    
    # Second instance (should load existing data)
    print("\n📝 Creating second memory instance...")
    memory2 = create_hybrid_memory(session_id, verbose=False)
    
    stats2 = memory2.get_memory_stats()
    print(f"   📊 Second instance stats: {stats2}")
    
    # Verify data persistence
    print(f"   ✅ Welcome status persisted: {memory2.get_welcome_status()}")
    print(f"   ✅ Reasons persisted: {memory2.get_reasons()}")
    print(f"   ✅ Conversation length persisted: {memory2._conversation_length}")


def main():
    """Run all tests."""
    print("🚀 Starting Hybrid Memory Tests")
    print("=" * 60)
    
    try:
        # Run all tests
        test_hybrid_memory_basic()
        test_buffer_mode()
        test_summary_mode()
        test_memory_comparison()
        test_conversation_history()
        test_memory_persistence()
        
        print("\n\n✅ All tests completed successfully!")
        print("🎉 Hybrid memory is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 