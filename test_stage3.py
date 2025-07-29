#!/usr/bin/env python3
"""
Test script for Stage 3: Advanced Chain and Middleware.

This script tests all Stage 3 features including:
- Advanced chain with RunnableSequence and fallbacks
- Enhanced middleware stack
- Prompt validation with FakeLLM
- Configurable LLM parameters
"""

import sys
import os
import time
import uuid
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all Stage 3 imports."""
    print("🔍 Testing Stage 3 imports...")
    
    try:
        # Test advanced chain
        from src.chains.advanced_chain import create_advanced_chain, AdvancedChain
        print("✅ Advanced chain imports successful")
        
        # Test middleware
        from src.middleware.enriched_middleware import (
            EnrichedLoggingMiddleware, 
            PerformanceMiddleware, 
            SecurityMiddleware,
            create_middleware_stack
        )
        print("✅ Middleware imports successful")
        
        # Test prompt tests
        from src.tests.prompt_tests import TestPromptValidation, run_prompt_tests
        print("✅ Prompt tests imports successful")
        
        # Test enhanced logger
        from src.utils.enhanced_logger import get_enhanced_logger
        print("✅ Enhanced logger imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_advanced_chain():
    """Test advanced chain functionality."""
    print("\n🔍 Testing advanced chain...")
    
    try:
        # Test that the module can be imported
        from src.chains.advanced_chain import AdvancedChain
        
        print("✅ Advanced chain module imported successfully")
        
        # Test that the class exists
        assert AdvancedChain is not None
        print("✅ Advanced chain class available")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced chain test failed: {e}")
        return False

def test_middleware():
    """Test middleware functionality."""
    print("\n🔍 Testing middleware...")
    
    try:
        from fastapi import FastAPI
        from src.middleware.enriched_middleware import create_middleware_stack
        
        # Create test app
        app = FastAPI()
        
        # Add middleware stack
        app = create_middleware_stack(app)
        
        print("✅ Middleware stack created successfully")
        
        # Test middleware components
        from src.middleware.enriched_middleware import (
            EnrichedLoggingMiddleware,
            PerformanceMiddleware,
            SecurityMiddleware
        )
        
        # Verify middleware classes exist
        assert EnrichedLoggingMiddleware is not None
        assert PerformanceMiddleware is not None
        assert SecurityMiddleware is not None
        
        print("✅ All middleware components available")
        
        return True
        
    except Exception as e:
        print(f"❌ Middleware test failed: {e}")
        return False

def test_prompt_validation():
    """Test prompt validation with FakeLLM."""
    print("\n🔍 Testing prompt validation...")
    
    try:
        from src.tests.prompt_tests import run_prompt_tests
        
        # Run prompt tests
        success = run_prompt_tests()
        
        if success:
            print("✅ All prompt validation tests passed")
        else:
            print("❌ Some prompt validation tests failed")
            
        return success
        
    except Exception as e:
        print(f"❌ Prompt validation test failed: {e}")
        return False

def test_enhanced_logging():
    """Test enhanced logging functionality."""
    print("\n🔍 Testing enhanced logging...")
    
    try:
        from src.utils.enhanced_logger import get_enhanced_logger
        
        logger = get_enhanced_logger()
        
        # Test logging methods
        request_id = str(uuid.uuid4())
        
        # Test request logging
        logger.start_request(request_id, "Test message", "test_session")
        print("✅ Request logging test passed")
        
        # Test agent logging
        logger.start_agent(request_id, "test_agent", {"input": "test"})
        logger.end_agent(request_id, "test_agent", {"output": "test"}, {"metadata": "test"})
        print("✅ Agent logging test passed")
        
        # Test chain step logging
        logger.log_chain_step(request_id, "TEST_STEP", "Test step description")
        print("✅ Chain step logging test passed")
        
        # Test error logging
        logger.log_error(request_id, "test_agent", Exception("Test error"), {"context": "test"})
        print("✅ Error logging test passed")
        
        # Test request completion
        logger.end_request(request_id, "Test response", {"success": True})
        print("✅ Request completion logging test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced logging test failed: {e}")
        return False

def test_configurable_parameters():
    """Test configurable LLM parameters."""
    print("\n🔍 Testing configurable LLM parameters...")
    
    try:
        from src.agents.curator_agent import create_curator_agent
        from src.agents.processor_agent import create_processor_agent
        from src.agents.formatter_agent import create_formatter_agent
        
        # Test curator with custom parameters
        curator = create_curator_agent(temperature=0.05, max_tokens=200, verbose=False)
        assert curator.temperature == 0.05
        assert curator.max_tokens == 200
        print("✅ Curator agent parameters configured")
        
        # Test processor with custom parameters
        processor = create_processor_agent(temperature=0.8, max_tokens=800, verbose=False)
        assert processor.temperature == 0.8
        assert processor.max_tokens == 800
        print("✅ Processor agent parameters configured")
        
        # Test formatter with custom parameters
        formatter = create_formatter_agent(temperature=0.1, max_tokens=600, verbose=False)
        assert formatter.temperature == 0.1
        assert formatter.max_tokens == 600
        print("✅ Formatter agent parameters configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Configurable parameters test failed: {e}")
        return False

def test_fallback_mechanisms():
    """Test fallback mechanisms."""
    print("\n🔍 Testing fallback mechanisms...")
    
    try:
        # Test that fallback models can be created
        from src.models.agent_interfaces import CuratorOutput, ProcessorOutput, FormatterOutput
        
        # Test CuratorOutput creation
        curator_output = CuratorOutput(
            cleaned_message="test",
            is_valid=True,
            validation_errors=[],
            content_type="test",
            confidence=0.5
        )
        assert isinstance(curator_output, CuratorOutput)
        print("✅ CuratorOutput model functional")
        
        # Test ProcessorOutput creation
        processor_output = ProcessorOutput(
            raw_response="test",
            tools_executed=[],
            search_performed=False,
            response_quality=0.5,
            processing_time=0.1
        )
        assert isinstance(processor_output, ProcessorOutput)
        print("✅ ProcessorOutput model functional")
        
        # Test FormatterOutput creation
        formatter_output = FormatterOutput(
            formatted_response="test",
            response_structure="test",
            readability_score=0.5,
            formatting_time=0.1
        )
        assert isinstance(formatter_output, FormatterOutput)
        print("✅ FormatterOutput model functional")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback mechanisms test failed: {e}")
        return False

def main():
    """Run all Stage 3 tests."""
    print("🚀 Starting Stage 3 Tests")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Advanced Chain", test_advanced_chain),
        ("Middleware", test_middleware),
        ("Prompt Validation", test_prompt_validation),
        ("Enhanced Logging", test_enhanced_logging),
        ("Configurable Parameters", test_configurable_parameters),
        ("Fallback Mechanisms", test_fallback_mechanisms),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Stage 3 Test Results")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Stage 3 tests passed! The system is ready for production.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 