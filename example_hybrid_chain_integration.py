"""
Example of integrating Hybrid Memory with existing chains.

This example demonstrates how to use the hybrid memory system
with the existing chain architecture, showing the benefits of
automatic buffer/summary switching.
"""

import uuid
import time
from typing import Dict, Any
from src.memory.hybrid_conversation_memory import create_hybrid_memory
from src.chains.complete_chain import create_complete_chain
from src.utils.enhanced_logger import get_enhanced_logger


class HybridChainExample:
    """
    Example class demonstrating hybrid memory integration.
    
    This class shows how to use the hybrid memory system
    with the existing chain architecture.
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the hybrid chain example.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.logger = get_enhanced_logger()
        self.chain = create_complete_chain(verbose=verbose)
    
    def simulate_conversation(self, session_id: str, messages: list) -> Dict[str, Any]:
        """
        Simulate a conversation using hybrid memory.
        
        Args:
            session_id: Session identifier
            messages: List of user messages
            
        Returns:
            Dict[str, Any]: Conversation results
        """
        print(f"\n🚀 Starting conversation simulation for session: {session_id}")
        print("=" * 60)
        
        # Create hybrid memory
        memory = create_hybrid_memory(
            session_id=session_id,
            buffer_window=5,
            summary_threshold=8,
            verbose=self.verbose
        )
        
        results = []
        
        for i, user_message in enumerate(messages, 1):
            print(f"\n💬 Message {i}: {user_message}")
            
            # Prepare input for chain
            input_data = {
                "message": user_message,
                "session_id": session_id,
                "request_id": str(uuid.uuid4()),
                "debug": self.verbose
            }
            
            # Process through chain
            start_time = time.time()
            result = self.chain.invoke(input_data)
            processing_time = time.time() - start_time
            
            # Get memory stats
            memory_stats = memory.get_memory_stats()
            
            print(f"   🤖 Response: {result['response'][:100]}...")
            print(f"   ⏱️  Processing time: {processing_time:.2f}s")
            print(f"   📊 Memory mode: {'Summary' if memory_stats['using_summary'] else 'Buffer'}")
            print(f"   📝 Conversation length: {memory_stats['conversation_length']}")
            
            # Show memory variables
            if self.verbose:
                vars = memory.load_memory_variables({})
                recent_count = len(vars.get('recent_history', []))
                summary_length = len(vars.get('conversation_summary', ''))
                print(f"   📋 Recent history: {recent_count} messages")
                print(f"   📄 Summary length: {summary_length} chars")
            
            results.append({
                "message": user_message,
                "response": result['response'],
                "processing_time": processing_time,
                "memory_stats": memory_stats
            })
        
        return {
            "session_id": session_id,
            "total_messages": len(messages),
            "results": results,
            "final_memory_stats": memory.get_memory_stats()
        }
    
    def demonstrate_buffer_mode(self):
        """Demonstrate buffer mode with short conversation."""
        print("\n🧪 Demonstrating Buffer Mode (Short Conversation)")
        print("=" * 60)
        
        session_id = str(uuid.uuid4())
        messages = [
            "Hola, ¿cómo estás?",
            "¿Puedes ayudarme con una pregunta simple?",
            "¿Cuál es la capital de Francia?",
            "Gracias por la información",
            "¿Puedes calcular 15 * 23?",
            "Perfecto, eso es todo"
        ]
        
        result = self.simulate_conversation(session_id, messages)
        
        print(f"\n📊 Buffer Mode Results:")
        print(f"   Total messages: {result['total_messages']}")
        print(f"   Final memory mode: {'Summary' if result['final_memory_stats']['using_summary'] else 'Buffer'}")
        print(f"   Final conversation length: {result['final_memory_stats']['conversation_length']}")
    
    def demonstrate_summary_mode(self):
        """Demonstrate summary mode with long conversation."""
        print("\n🧪 Demonstrating Summary Mode (Long Conversation)")
        print("=" * 60)
        
        session_id = str(uuid.uuid4())
        messages = [
            "Hola, necesito ayuda con un proyecto de programación",
            "Estoy trabajando con Python y LangChain",
            "Quiero crear un sistema de memoria híbrida",
            "¿Puedes explicarme cómo funciona ConversationSummaryMemory?",
            "¿Cuáles son las ventajas de usar resúmenes?",
            "¿Cómo se compara con ConversationBufferMemory?",
            "¿Puedes darme un ejemplo de implementación?",
            "¿Qué parámetros debo configurar?",
            "¿Cómo manejo la persistencia de datos?",
            "¿Puedo combinar diferentes tipos de memoria?",
            "¿Cuál es la mejor estrategia para conversaciones largas?",
            "¿Cómo optimizo el uso de tokens?",
            "¿Puedes mostrarme cómo integrar con FastAPI?",
            "¿Qué consideraciones debo tener en cuenta?",
            "Gracias por toda la información"
        ]
        
        result = self.simulate_conversation(session_id, messages)
        
        print(f"\n📊 Summary Mode Results:")
        print(f"   Total messages: {result['total_messages']}")
        print(f"   Final memory mode: {'Summary' if result['final_memory_stats']['using_summary'] else 'Buffer'}")
        print(f"   Final conversation length: {result['final_memory_stats']['conversation_length']}")
    
    def demonstrate_metadata_integration(self):
        """Demonstrate metadata integration with hybrid memory."""
        print("\n🧪 Demonstrating Metadata Integration")
        print("=" * 60)
        
        session_id = str(uuid.uuid4())
        memory = create_hybrid_memory(session_id, verbose=True)
        
        # Set up metadata
        print("🔧 Setting up metadata...")
        memory.set_welcome_status(True)
        memory.add_reason("Testing hybrid memory integration")
        memory.add_reason("Demonstrating metadata capabilities")
        memory.set_loan_variables(monthly=1500, duration=24, rate=4.5)
        
        print(f"   ✅ Welcome status: {memory.get_welcome_status()}")
        print(f"   ✅ Reasons: {memory.get_reasons()}")
        print(f"   ✅ Loan variables: {memory.get_loan_variables()}")
        print(f"   ✅ Loan complete: {memory.is_loan_info_complete()}")
        
        # Simulate conversation with metadata context
        messages = [
            "Hola, ¿ya me diste la bienvenida?",
            "¿Cuáles son las razones de esta conversación?",
            "¿Tienes información sobre mi préstamo?",
            "¿Puedes calcular mi pago mensual?",
            "Gracias por recordar toda la información"
        ]
        
        result = self.simulate_conversation(session_id, messages)
        
        # Check metadata persistence
        final_memory = create_hybrid_memory(session_id, verbose=False)
        print(f"\n📊 Metadata Persistence Check:")
        print(f"   ✅ Welcome status: {final_memory.get_welcome_status()}")
        print(f"   ✅ Reasons: {final_memory.get_reasons()}")
        print(f"   ✅ Loan variables: {final_memory.get_loan_variables()}")
    
    def compare_performance(self):
        """Compare performance between buffer and summary modes."""
        print("\n🧪 Comparing Performance: Buffer vs Summary")
        print("=" * 60)
        
        # Test buffer mode
        print("\n📋 Testing Buffer Mode Performance:")
        buffer_session = str(uuid.uuid4())
        buffer_messages = ["Test message"] * 5
        
        buffer_start = time.time()
        buffer_result = self.simulate_conversation(buffer_session, buffer_messages)
        buffer_time = time.time() - buffer_start
        
        # Test summary mode
        print("\n📝 Testing Summary Mode Performance:")
        summary_session = str(uuid.uuid4())
        summary_messages = ["Test message"] * 15
        
        summary_start = time.time()
        summary_result = self.simulate_conversation(summary_session, summary_messages)
        summary_time = time.time() - summary_start
        
        # Compare results
        print(f"\n📊 Performance Comparison:")
        print(f"   Buffer Mode:")
        print(f"     Messages: {buffer_result['total_messages']}")
        print(f"     Total time: {buffer_time:.2f}s")
        print(f"     Avg time per message: {buffer_time/buffer_result['total_messages']:.2f}s")
        print(f"     Memory mode: {'Summary' if buffer_result['final_memory_stats']['using_summary'] else 'Buffer'}")
        
        print(f"   Summary Mode:")
        print(f"     Messages: {summary_result['total_messages']}")
        print(f"     Total time: {summary_time:.2f}s")
        print(f"     Avg time per message: {summary_time/summary_result['total_messages']:.2f}s")
        print(f"     Memory mode: {'Summary' if summary_result['final_memory_stats']['using_summary'] else 'Buffer'}")
        
        # Calculate efficiency
        buffer_avg = buffer_time / buffer_result['total_messages']
        summary_avg = summary_time / summary_result['total_messages']
        efficiency = ((buffer_avg - summary_avg) / buffer_avg) * 100
        
        print(f"\n🎯 Efficiency Analysis:")
        print(f"   Summary mode is {efficiency:.1f}% {'slower' if efficiency < 0 else 'faster'} per message")
        print(f"   Summary mode handles {summary_result['total_messages']/buffer_result['total_messages']:.1f}x more messages")


def main():
    """Run the hybrid chain integration example."""
    print("🚀 Hybrid Memory Chain Integration Example")
    print("=" * 80)
    
    try:
        example = HybridChainExample(verbose=True)
        
        # Run demonstrations
        example.demonstrate_buffer_mode()
        example.demonstrate_summary_mode()
        example.demonstrate_metadata_integration()
        example.compare_performance()
        
        print("\n\n✅ All demonstrations completed successfully!")
        print("🎉 Hybrid memory integration is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 