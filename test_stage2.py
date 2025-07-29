#!/usr/bin/env python3
"""
Test script for Stage 2 implementation.

This script validates that all components are working correctly
with the complete chain of 3 agents.
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
        from src.utils.tools import get_available_tools, execute_tool
        from src.memory.conversation_memory import create_memory
        from src.agents.curator_agent import create_curator_agent
        from src.agents.processor_agent import create_processor_agent
        from src.agents.formatter_agent import create_formatter_agent
        from src.chains.complete_chain import create_complete_chain
        from src.models.agent_interfaces import CuratorOutput, ProcessorInput, ProcessorOutput, FormatterInput, FormatterOutput
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_tools():
    """Test dummy tools functionality."""
    print("🔍 Testing tools...")
    
    try:
        from src.utils.tools import get_available_tools, execute_tool
        
        # Test search tool
        search_results = execute_tool("search_web", query="capital of france")
        assert isinstance(search_results, list)
        assert len(search_results) > 0
        
        # Test calculator tool
        calc_result = execute_tool("calculate", expression="2+2")
        assert calc_result["success"] == True
        assert calc_result["result"] == 4
        
        # Test time tool
        time_result = execute_tool("get_time")
        assert "current_time" in time_result
        
        print("✅ Tools test passed")
        return True
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

def test_processor_agent():
    """Test processor agent (without LLM)."""
    print("🔍 Testing processor agent...")
    
    try:
        from src.agents.processor_agent import create_processor_agent
        from src.models.agent_interfaces import CuratorOutput, ProcessorInput
        
        # Create agent
        agent = create_processor_agent(verbose=True)
        
        # Create mock curator output
        curator_output = CuratorOutput(
            cleaned_message="What is the capital of France?",
            is_valid=True,
            validation_errors=[],
            content_type="question",
            confidence=0.95
        )
        
        # Test debug method
        result = agent.debug("What is the capital of France?", curator_output)
        
        print("✅ Processor agent test passed")
        return True
    except Exception as e:
        print(f"❌ Processor agent test failed: {e}")
        return False

def test_formatter_agent():
    """Test formatter agent (without LLM)."""
    print("🔍 Testing formatter agent...")
    
    try:
        from src.agents.formatter_agent import create_formatter_agent
        from src.models.agent_interfaces import ProcessorOutput, FormatterInput
        
        # Create agent
        agent = create_formatter_agent(verbose=True)
        
        # Create mock processor output
        processor_output = ProcessorOutput(
            raw_response="Paris is the capital of France.",
            tools_executed=[],
            search_performed=True,
            response_quality=0.9,
            processing_time=1.0
        )
        
        # Test debug method
        result = agent.debug("Paris is the capital of France.", "What is the capital of France?", processor_output)
        
        print("✅ Formatter agent test passed")
        return True
    except Exception as e:
        print(f"❌ Formatter agent test failed: {e}")
        return False

def test_complete_chain():
    """Test complete chain (without LLM)."""
    print("🔍 Testing complete chain...")
    
    try:
        from src.chains.complete_chain import create_complete_chain
        
        # Create chain
        chain = create_complete_chain(verbose=True)
        
        # Test with mock data
        result = chain.invoke({
            "message": "What is the capital of France?",
            "session_id": "test_session",
            "request_id": "test_request"
        })
        
        assert "response" in result
        assert "session_id" in result
        assert "processing_time" in result
        assert "metadata" in result
        assert "agents_used" in result["metadata"]
        
        # Check if we got an error response (expected without valid API key)
        if "error" in result.get("metadata", {}).get("errors", []):
            print("⚠️  Complete chain test passed with expected API error")
        else:
            print("✅ Complete chain test passed")
        
        return True
    except Exception as e:
        print(f"❌ Complete chain test failed: {e}")
        return False

def test_agent_interfaces():
    """Test Pydantic agent interfaces."""
    print("🔍 Testing agent interfaces...")
    
    try:
        from src.models.agent_interfaces import (
            CuratorOutput, ProcessorInput, ProcessorOutput, 
            FormatterInput, FormatterOutput, SearchResult, ToolExecutionResult
        )
        
        # Test CuratorOutput
        curator_output = CuratorOutput(
            cleaned_message="Test message",
            is_valid=True,
            validation_errors=[],
            content_type="question",
            confidence=0.95
        )
        assert curator_output.is_valid == True
        
        # Test SearchResult
        search_result = SearchResult(
            title="Test Title",
            content="Test Content",
            source="Test Source"
        )
        assert search_result.title == "Test Title"
        
        # Test ToolExecutionResult
        tool_result = ToolExecutionResult(
            tool_name="test_tool",
            success=True,
            result={"test": "data"},
            execution_time=1.0
        )
        assert tool_result.success == True
        
        print("✅ Agent interfaces test passed")
        return True
    except Exception as e:
        print(f"❌ Agent interfaces test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Stage 2 validation tests...\n")
    
    tests = [
        test_imports,
        test_tools,
        test_processor_agent,
        test_formatter_agent,
        test_complete_chain,
        test_agent_interfaces
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Stage 2 is ready to run.")
        print("\n📝 Next steps:")
        print("1. Set your GROQ_API_KEY in .env file")
        print("2. Run: python -m src.main")
        print("3. Visit: http://localhost:8000/docs")
        print("4. Test with: What is the capital of France?")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 