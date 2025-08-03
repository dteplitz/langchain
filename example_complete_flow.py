#!/usr/bin/env python3
"""
Complete Flow Example with Extended Metadata.

This script demonstrates a complete conversation flow using all
the extended metadata features for a loan calculation scenario.
"""

import uuid
import json
from datetime import datetime
from src.memory.hybrid_conversation_memory import create_hybrid_memory


class LoanAssistant:
    """Simulated loan assistant that uses extended metadata."""
    
    def __init__(self, session_id: str):
        self.memory = create_hybrid_memory(session_id)
        self.session_id = session_id
    
    def start_conversation(self) -> str:
        """Start the conversation and show welcome message."""
        if not self.memory.get_welcome_status():
            self.memory.set_welcome_status(True)
            return """¡Hola! Soy tu asistente de préstamos. 

Te ayudo a calcular y comparar opciones de financiamiento. 

Para empezar, ¿podrías decirme por qué necesitas un préstamo?"""
        else:
            return "¡Hola de nuevo! ¿En qué puedo ayudarte hoy?"
    
    def process_reason(self, user_message: str) -> str:
        """Process user's reason for needing a loan."""
        # Add the reason to the list
        self.memory.add_reason(user_message)
        
        reasons = self.memory.get_reasons()
        
        if len(reasons) == 1:
            return f"Entiendo, necesitas un préstamo para: {user_message}\n\n¿Hay alguna otra razón o motivo adicional?"
        else:
            return f"Perfecto, he registrado tus motivos:\n" + "\n".join([f"• {reason}" for reason in reasons]) + "\n\n¿Estás de acuerdo con estos motivos?"
    
    def confirm_reasons(self, user_response: str) -> str:
        """Confirm the reasons with the user."""
        if any(word in user_response.lower() for word in ["sí", "si", "correcto", "ok", "vale"]):
            self.memory.set_reasons_confirmed(True)
            return """Excelente. Ahora necesito algunos datos para calcular tu préstamo:

1. ¿Cuál es el monto mensual que puedes pagar?
2. ¿Por cuántos meses quieres el préstamo?
3. ¿Qué tasa de interés te han ofrecido?

Puedes darme estos datos uno por uno o todos juntos."""
        else:
            return "Entiendo. ¿Podrías aclarar o modificar alguno de los motivos?"
    
    def collect_variables(self, user_message: str) -> str:
        """Collect loan variables from user."""
        # Simple parsing (in a real scenario, you'd use NLP)
        words = user_message.lower().split()
        
        monthly = None
        duration = None
        rate = None
        
        # Try to extract numbers and context
        for i, word in enumerate(words):
            try:
                value = float(word.replace(',', '').replace('$', ''))
                
                # Context-based assignment
                if i > 0 and any(month_word in words[i-1] for month_word in ["mensual", "mes", "pago"]):
                    monthly = value
                elif i > 0 and any(duration_word in words[i-1] for duration_word in ["meses", "años", "duración"]):
                    duration = int(value)
                elif i > 0 and any(rate_word in words[i-1] for rate_word in ["tasa", "interés", "%"]):
                    rate = value
                elif "%" in word:
                    rate = value
                elif value > 1000:  # Likely monthly payment
                    monthly = value
                elif value < 100:  # Likely rate
                    rate = value
                elif 12 <= value <= 360:  # Likely duration
                    duration = int(value)
                    
            except ValueError:
                continue
        
        # Update variables
        if monthly is not None:
            self.memory.update_var("monthly", monthly)
        if duration is not None:
            self.memory.update_var("duration", duration)
        if rate is not None:
            self.memory.update_var("rate", rate)
        
        current_vars = self.memory.get_vars()
        missing_vars = []
        
        if current_vars["monthly"] is None:
            missing_vars.append("monto mensual")
        if current_vars["duration"] is None:
            missing_vars.append("duración en meses")
        if current_vars["rate"] is None:
            missing_vars.append("tasa de interés")
        
        if missing_vars:
            return f"Gracias. Aún necesito: {', '.join(missing_vars)}.\n\n¿Podrías proporcionarme esta información?"
        else:
            self.memory.set_vars_info_given(True)
            return self.calculate_loan()
    
    def calculate_loan(self) -> str:
        """Calculate loan based on collected variables."""
        vars_data = self.memory.get_vars()
        monthly = vars_data["monthly"]
        duration = vars_data["duration"]
        rate = vars_data["rate"]
        
        # Simple loan calculation
        monthly_rate = rate / 100 / 12
        total_payments = monthly * duration
        principal = monthly * ((1 - (1 + monthly_rate) ** -duration) / monthly_rate)
        total_interest = total_payments - principal
        
        return f"""📊 **Cálculo de tu préstamo:**

💰 **Detalles del préstamo:**
• Pago mensual: ${monthly:,.2f}
• Duración: {duration} meses
• Tasa de interés: {rate}% anual

📈 **Resultados:**
• Monto del préstamo: ${principal:,.2f}
• Total a pagar: ${total_payments:,.2f}
• Intereses totales: ${total_interest:,.2f}

¿Te parece bien esta opción o quieres ajustar algún parámetro?"""
    
    def get_conversation_summary(self) -> dict:
        """Get a summary of the conversation state."""
        return {
            "session_id": self.session_id,
            "welcome_done": self.memory.get_welcome_status(),
            "reasons": self.memory.get_reasons(),
            "reasons_confirmed": self.memory.get_reasons_confirmed(),
            "vars_info_given": self.memory.get_vars_info_given(),
            "loan_variables": self.memory.get_vars(),
            "is_complete": self.memory.is_loan_info_complete(),
            "all_metadata": self.memory.get_session_metadata()
        }


def simulate_complete_conversation():
    """Simulate a complete loan conversation flow."""
    print("🏦 Simulando Conversación Completa de Préstamo")
    print("=" * 60)
    
    # Create assistant
    session_id = str(uuid.uuid4())
    assistant = LoanAssistant(session_id)
    
    # Simulate conversation steps
    conversation_steps = [
        ("", "start"),  # Initial greeting
        ("Necesito dinero para comprar un auto", "reason"),
        ("También para hacer algunas mejoras en mi casa", "reason"),
        ("Sí, esos son los motivos", "confirm"),
        ("Puedo pagar $1500 mensuales por 36 meses con 5.5% de interés", "variables"),
    ]
    
    print(f"🆔 Session ID: {session_id}")
    print()
    
    for i, (user_message, step_type) in enumerate(conversation_steps, 1):
        print(f"💬 Paso {i}: {step_type.upper()}")
        if user_message:
            print(f"   Usuario: {user_message}")
        
        # Process based on step type
        if step_type == "start":
            response = assistant.start_conversation()
        elif step_type == "reason":
            response = assistant.process_reason(user_message)
        elif step_type == "confirm":
            response = assistant.confirm_reasons(user_message)
        elif step_type == "variables":
            response = assistant.collect_variables(user_message)
        
        print(f"   Asistente: {response}")
        print()
        
        # Show current state
        summary = assistant.get_conversation_summary()
        print(f"📊 Estado actual:")
        print(f"   - Welcome done: {summary['welcome_done']}")
        print(f"   - Reasons: {len(summary['reasons'])} motivos")
        print(f"   - Reasons confirmed: {summary['reasons_confirmed']}")
        print(f"   - Vars info given: {summary['vars_info_given']}")
        print(f"   - Loan complete: {summary['is_complete']}")
        print("-" * 40)
    
    # Show final summary
    print("\n🎯 RESUMEN FINAL:")
    final_summary = assistant.get_conversation_summary()
    print(json.dumps(final_summary, indent=2, ensure_ascii=False))


def demonstrate_metadata_access():
    """Demonstrate how to access and use the extended metadata."""
    print("\n🔍 Demostrando Acceso a Metadatos Extendidos")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id)
    
    # Set up some metadata
    memory.set_welcome_status(True)
    memory.add_reason("Compra de vehículo")
    memory.add_reason("Mejoras en casa")
    memory.set_reasons_confirmed(True)
    memory.set_loan_variables(monthly=2000.0, duration=48, rate=4.8)
    memory.set_vars_info_given(True)
    
    print("📋 Métodos de acceso a metadatos:")
    print()
    
    # Direct methods
    print("🔧 Métodos directos:")
    print(f"   - get_welcome_status(): {memory.get_welcome_status()}")
    print(f"   - get_reasons(): {memory.get_reasons()}")
    print(f"   - get_reasons_confirmed(): {memory.get_reasons_confirmed()}")
    print(f"   - get_vars_info_given(): {memory.get_vars_info_given()}")
    print(f"   - get_vars(): {memory.get_vars()}")
    print(f"   - is_loan_info_complete(): {memory.is_loan_info_complete()}")
    print()
    
    # Generic metadata access
    print("🔧 Acceso genérico:")
    print(f"   - get_metadata_value('welcome_done'): {memory.get_metadata_value('welcome_done')}")
    print(f"   - get_metadata_value('reasons'): {memory.get_metadata_value('reasons')}")
    print(f"   - get_metadata_value('vars.monthly'): {memory.get_metadata_value('vars.monthly')}")
    print(f"   - get_metadata_value('vars.duration'): {memory.get_metadata_value('vars.duration')}")
    print(f"   - get_metadata_value('vars.rate'): {memory.get_metadata_value('vars.rate')}")
    print()
    
    # All metadata
    print("📊 Todos los metadatos:")
    all_metadata = memory.get_session_metadata()
    print(json.dumps(all_metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print("🎯 Ejemplo de Flujo Completo con Metadatos Extendidos")
    print("=" * 60)
    
    # Run demonstrations
    simulate_complete_conversation()
    demonstrate_metadata_access()
    
    print("\n✨ Ejemplo completado!") 