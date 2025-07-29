#!/usr/bin/env python3
"""
Test script for enhanced logging system.

This script demonstrates the new human-readable logging
with colors and detailed information about the agent chain.
"""

import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_enhanced_logging():
    """Test the enhanced logging system."""
    print("🔍 Testing enhanced logging system...")
    
    try:
        from src.utils.enhanced_logger import get_enhanced_logger
        from src.chains.complete_chain import create_complete_chain
        
        # Get logger
        logger = get_enhanced_logger()
        
        # Create chain
        chain = create_complete_chain(verbose=True)
        
        # Test request
        print("\n" + "="*80)
        print("🚀 TESTING ENHANCED LOGGING WITH COMPLETE CHAIN")
        print("="*80)
        
        result = chain.invoke({
            "message": "What is the capital of France?",
            "session_id": "test_session_enhanced",
            "request_id": "test_request_enhanced",
            "debug": True
        })
        
        print("\n" + "="*80)
        print("📊 FINAL RESULT")
        print("="*80)
        print(f"Response: {result['response'][:200]}...")
        print(f"Processing Time: {result['processing_time']:.2f}s")
        print(f"Success: {result['metadata']['success']}")
        print(f"Agents Used: {result['metadata']['agents_used']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced logging test failed: {e}")
        return False

def test_logger_directly():
    """Test logger methods directly."""
    print("🔍 Testing logger methods directly...")
    
    try:
        from src.utils.enhanced_logger import get_enhanced_logger
        
        logger = get_enhanced_logger()
        
        # Test request tracking
        logger.start_request("test_123", "Hello world", "session_456")
        
        # Test agent tracking
        logger.start_agent("test_123", "curator", {"message": "test"})
        time.sleep(0.1)  # Simulate processing
        logger.end_agent("test_123", "curator", {"result": "success"}, {"confidence": 0.95})
        
        # Test tool execution
        logger.log_tool_execution("test_123", "search_web", {"query": "test"}, {"results": []}, 0.5)
        
        # Test chain step
        logger.log_chain_step("test_123", "STEP_1", "Processing curator agent")
        
        # Test error logging
        logger.log_error("test_123", "processor", Exception("Test error"), {"context": "test"})
        
        # End request
        logger.end_request("test_123", "Final response", {"success": True})
        
        print("✅ Logger methods test passed")
        return True
        
    except Exception as e:
        print(f"❌ Logger methods test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Enhanced Logging Tests...\n")
    
    tests = [
        test_logger_directly,
        test_enhanced_logging
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Enhanced logging system is working!")
        print("\n📝 Check the console output above for:")
        print("   - 🚀 Request start/end markers")
        print("   - 🤖 Agent execution details")
        print("   - 🔧 Tool execution logs")
        print("   - 🔗 Chain step information")
        print("   - ✅ Success/error indicators")
        print("   - 📊 Performance metrics")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 