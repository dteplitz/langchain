#!/usr/bin/env python3
"""
Test script for Stage 1 implementation.

This script validates that all components are working correctly
before running the FastAPI server.
"""

import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from src.config import get_settings
        from src.utils.llm_client import create_llm_client
        from src.utils.logger import get_logger
        from src.memory.hybrid_conversation_memory import create_hybrid_memory
        from src.agents.curator_agent import create_curator_agent
        from src.chains.simple_chain import create_simple_chain
        from src.models import ChatRequest, ChatResponse
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("🔍 Testing configuration...")
    
    try:
        from src.config import get_settings
        
        # Test with environment variable
        os.environ["GROQ_API_KEY"] = "test_key"
        settings = get_settings()
        
        assert settings.groq_api_key == "test_key"
        assert settings.model_name == "llama3-8b-8192"
        assert settings.temperature == 0.7
        
        print("✅ Configuration test passed")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_logger():
    """Test logging functionality."""
    print("🔍 Testing logger...")
    
    try:
        from src.utils.logger import get_logger
        
        logger = get_logger()
        logger.log_request("test_id", "test message", "test_agent")
        
        print("✅ Logger test passed")
        return True
    except Exception as e:
        print(f"❌ Logger test failed: {e}")
        return False

def test_memory():
    """Test memory functionality."""
    print("🔍 Testing memory...")
    
    try:
        from src.memory.hybrid_conversation_memory import create_hybrid_memory, get_hybrid_conversation_history
        
        # Create memory
        memory = create_hybrid_memory("test_session")
        
        # Save context
        memory.save_context(
            {"message": "Hello"},
            {"response": "Hi there!"}
        )
        
        # Load history
        history = get_hybrid_conversation_history("test_session")
        assert len(history["recent_messages"]) > 0
        
        print("✅ Memory test passed")
        return True
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        return False

def test_curator_agent():
    """Test curator agent (without LLM)."""
    print("🔍 Testing curator agent...")
    
    try:
        from src.agents.curator_agent import create_curator_agent
        
        # Create agent
        agent = create_curator_agent(verbose=True)
        
        # Test debug method
        result = agent.debug("Hello, how are you?")
        
        print("✅ Curator agent test passed")
        return True
    except Exception as e:
        print(f"❌ Curator agent test failed: {e}")
        return False

def test_simple_chain():
    """Test simple chain (without LLM)."""
    print("🔍 Testing simple chain...")
    
    try:
        from src.chains.simple_chain import create_simple_chain
        
        # Create chain
        chain = create_simple_chain(verbose=True)
        
        # Test with mock data
        result = chain.invoke({
            "message": "Test message",
            "session_id": "test_session",
            "request_id": "test_request"
        })
        
        assert "response" in result
        assert "session_id" in result
        assert "processing_time" in result
        
        # Check if we got an error response (expected without valid API key)
        if "error" in result.get("metadata", {}):
            print("⚠️  Simple chain test passed with expected API error")
        else:
            print("✅ Simple chain test passed")
        
        return True
    except Exception as e:
        print(f"❌ Simple chain test failed: {e}")
        return False

def test_models():
    """Test Pydantic models."""
    print("🔍 Testing Pydantic models...")
    
    try:
        from src.models import ChatRequest, ChatResponse, HealthResponse
        
        # Test ChatRequest
        request = ChatRequest(
            message="Test message",
            session_id="test_session",
            debug=False
        )
        assert request.message == "Test message"
        
        # Test ChatResponse
        response = ChatResponse(
            response="Test response",
            session_id="test_session",
            request_id="test_request",
            processing_time=1.0
        )
        assert response.response == "Test response"
        
        # Test HealthResponse
        health = HealthResponse(status="healthy", version="1.0.0")
        assert health.status == "healthy"
        
        print("✅ Models test passed")
        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Stage 1 validation tests...\n")
    
    tests = [
        test_imports,
        test_config,
        test_logger,
        test_memory,
        test_curator_agent,
        test_simple_chain,
        test_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Stage 1 is ready to run.")
        print("\n📝 Next steps:")
        print("1. Set your GROQ_API_KEY in .env file")
        print("2. Run: python -m src.main")
        print("3. Visit: http://localhost:8000/docs")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 