#!/usr/bin/env python3
"""
Integration test for memory functionality with the server.

This script tests that the memory system works correctly
when processing messages through the actual API.
"""

import requests
import json
import time
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import get_settings


def test_memory_with_server():
    """Test memory functionality with the running server."""
    
    base_url = "http://localhost:8000"
    session_id = "test_memory_integration"
    
    print("🧪 Probando memoria con el servidor...")
    print("=" * 60)
    
    try:
        # Test 1: First message - introduce name
        print("\n1️⃣ Primer mensaje - presentando nombre...")
        response1 = requests.post(f"{base_url}/chat", json={
            "message": "Hola, me llamo Carlos",
            "session_id": session_id
        }, timeout=30)
        
        if response1.status_code == 200:
            result1 = response1.json()
            print(f"✅ Respuesta: {result1['response'][:100]}...")
            print(f"⏱️  Tiempo de procesamiento: {result1['processing_time']:.2f}s")
        else:
            print(f"❌ Error: {response1.status_code} - {response1.text}")
            return False
        
        time.sleep(1)  # Pequeña pausa entre requests
        
        # Test 2: Second message - ask for name
        print("\n2️⃣ Segundo mensaje - preguntando por el nombre...")
        response2 = requests.post(f"{base_url}/chat", json={
            "message": "¿Cuál es mi nombre?",
            "session_id": session_id
        }, timeout=30)
        
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"✅ Respuesta: {result2['response'][:200]}...")
            print(f"⏱️  Tiempo de procesamiento: {result2['processing_time']:.2f}s")
            
            # Verificar si la respuesta menciona "Carlos"
            if "carlos" in result2['response'].lower():
                print("🎉 ¡ÉXITO: El sistema recordó tu nombre!")
            else:
                print("❌ FALLO: El sistema NO recordó tu nombre")
                print(f"Respuesta completa: {result2['response']}")
                return False
        else:
            print(f"❌ Error: {response2.status_code} - {response2.text}")
            return False
        
        time.sleep(1)
        
        # Test 3: Third message - ask about previous conversation
        print("\n3️⃣ Tercer mensaje - preguntando sobre conversación anterior...")
        response3 = requests.post(f"{base_url}/chat", json={
            "message": "¿Recuerdas qué te dije antes?",
            "session_id": session_id
        }, timeout=30)
        
        if response3.status_code == 200:
            result3 = response3.json()
            print(f"✅ Respuesta: {result3['response'][:200]}...")
            print(f"⏱️  Tiempo de procesamiento: {result3['processing_time']:.2f}s")
            
            # Verificar si la respuesta menciona algo de la conversación anterior
            if any(word in result3['response'].lower() for word in ["carlos", "nombre", "dijiste", "antes"]):
                print("🎉 ¡ÉXITO: El sistema recordó la conversación anterior!")
            else:
                print("⚠️  El sistema no parece recordar la conversación anterior claramente")
        else:
            print(f"❌ Error: {response3.status_code} - {response3.text}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. Asegúrate de que esté ejecutándose en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def test_memory_persistence():
    """Test that memory persists across different requests."""
    
    base_url = "http://localhost:8000"
    session_id = "test_persistence_123"
    
    print("\n🧪 Probando persistencia de memoria...")
    print("=" * 60)
    
    try:
        # Test 1: First session
        print("\n1️⃣ Primera sesión...")
        response1 = requests.post(f"{base_url}/chat", json={
            "message": "Mi color favorito es el azul",
            "session_id": session_id
        }, timeout=30)
        
        if response1.status_code != 200:
            print(f"❌ Error en primera sesión: {response1.status_code}")
            return False
        
        print("✅ Primera sesión completada")
        
        # Simulate some time passing
        time.sleep(2)
        
        # Test 2: Second session (same session_id)
        print("\n2️⃣ Segunda sesión (misma sesión)...")
        response2 = requests.post(f"{base_url}/chat", json={
            "message": "¿Cuál es mi color favorito?",
            "session_id": session_id
        }, timeout=30)
        
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"✅ Respuesta: {result2['response'][:200]}...")
            
            if "azul" in result2['response'].lower():
                print("🎉 ¡ÉXITO: La memoria persistió entre sesiones!")
                return True
            else:
                print("❌ FALLO: La memoria no persistió entre sesiones")
                return False
        else:
            print(f"❌ Error en segunda sesión: {response2.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de persistencia: {e}")
        return False


def test_different_sessions():
    """Test that different sessions have separate memory."""
    
    base_url = "http://localhost:8000"
    session1 = "test_session_A"
    session2 = "test_session_B"
    
    print("\n🧪 Probando sesiones separadas...")
    print("=" * 60)
    
    try:
        # Test 1: Session A
        print("\n1️⃣ Sesión A...")
        response1 = requests.post(f"{base_url}/chat", json={
            "message": "Me llamo Ana",
            "session_id": session1
        }, timeout=30)
        
        if response1.status_code != 200:
            print(f"❌ Error en sesión A: {response1.status_code}")
            return False
        
        # Test 2: Session B
        print("\n2️⃣ Sesión B...")
        response2 = requests.post(f"{base_url}/chat", json={
            "message": "Me llamo Bob",
            "session_id": session2
        }, timeout=30)
        
        if response2.status_code != 200:
            print(f"❌ Error en sesión B: {response2.status_code}")
            return False
        
        # Test 3: Ask for name in Session A
        print("\n3️⃣ Preguntando nombre en Sesión A...")
        response3 = requests.post(f"{base_url}/chat", json={
            "message": "¿Cuál es mi nombre?",
            "session_id": session1
        }, timeout=30)
        
        if response3.status_code == 200:
            result3 = response3.json()
            print(f"✅ Respuesta Sesión A: {result3['response'][:100]}...")
            
            if "ana" in result3['response'].lower():
                print("✅ Sesión A recordó el nombre correcto (Ana)")
            else:
                print("❌ Sesión A no recordó el nombre correcto")
                return False
        else:
            print(f"❌ Error preguntando en sesión A: {response3.status_code}")
            return False
        
        # Test 4: Ask for name in Session B
        print("\n4️⃣ Preguntando nombre en Sesión B...")
        response4 = requests.post(f"{base_url}/chat", json={
            "message": "¿Cuál es mi nombre?",
            "session_id": session2
        }, timeout=30)
        
        if response4.status_code == 200:
            result4 = response4.json()
            print(f"✅ Respuesta Sesión B: {result4['response'][:100]}...")
            
            if "bob" in result4['response'].lower():
                print("✅ Sesión B recordó el nombre correcto (Bob)")
                print("🎉 ¡ÉXITO: Las sesiones están correctamente separadas!")
                return True
            else:
                print("❌ Sesión B no recordó el nombre correcto")
                return False
        else:
            print(f"❌ Error preguntando en sesión B: {response4.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de sesiones separadas: {e}")
        return False


def main():
    """Run all memory integration tests."""
    print("🚀 Iniciando pruebas de integración de memoria...")
    print("=" * 80)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ El servidor no está respondiendo correctamente")
            print("Asegúrate de ejecutar: python -m src.main")
            return
    except:
        print("❌ No se puede conectar al servidor")
        print("Asegúrate de ejecutar: python -m src.main")
        return
    
    print("✅ Servidor está ejecutándose")
    
    # Run tests
    test_results = []
    
    # Test 1: Basic memory functionality
    print("\n" + "="*80)
    print("PRUEBA 1: Funcionalidad básica de memoria")
    print("="*80)
    test1_result = test_memory_with_server()
    test_results.append(("Funcionalidad básica", test1_result))
    
    # Test 2: Memory persistence
    print("\n" + "="*80)
    print("PRUEBA 2: Persistencia de memoria")
    print("="*80)
    test2_result = test_memory_persistence()
    test_results.append(("Persistencia", test2_result))
    
    # Test 3: Different sessions
    print("\n" + "="*80)
    print("PRUEBA 3: Sesiones separadas")
    print("="*80)
    test3_result = test_different_sessions()
    test_results.append(("Sesiones separadas", test3_result))
    
    # Summary
    print("\n" + "="*80)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*80)
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(test_results)} pruebas pasaron")
    
    if passed == len(test_results):
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! El sistema de memoria funciona correctamente.")
    else:
        print(f"\n⚠️  {len(test_results) - passed} prueba(s) fallaron. Revisa los detalles arriba.")


if __name__ == "__main__":
    main() 