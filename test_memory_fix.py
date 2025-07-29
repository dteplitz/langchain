#!/usr/bin/env python3
"""
Test script to verify memory functionality and search tool fixes.
"""

import requests
import json
import time

def test_memory():
    """Test that the system remembers the user's name across conversations."""
    
    base_url = "http://localhost:8000"
    session_id = "test_memory_damian"
    
    print("🧪 Testing Memory Functionality")
    print("=" * 50)
    
    # Test 1: First message - introduce name
    print("\n1️⃣ First message - introducing name...")
    response1 = requests.post(f"{base_url}/chat", json={
        "message": "Hi, I am Damian",
        "session_id": session_id
    })
    
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"✅ Response: {result1['response'][:100]}...")
        print(f"⏱️  Processing time: {result1['processing_time']:.2f}s")
    else:
        print(f"❌ Error: {response1.status_code} - {response1.text}")
        return False
    
    time.sleep(1)  # Small delay between requests
    
    # Test 2: Second message - ask for name
    print("\n2️⃣ Second message - asking for name...")
    response2 = requests.post(f"{base_url}/chat", json={
        "message": "What's my name?",
        "session_id": session_id
    })
    
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"✅ Response: {result2['response'][:200]}...")
        print(f"⏱️  Processing time: {result2['processing_time']:.2f}s")
        
        # Check if the response mentions "Damian"
        if "damian" in result2['response'].lower():
            print("🎉 SUCCESS: The system remembered your name!")
            return True
        else:
            print("❌ FAILED: The system did not remember your name")
            return False
    else:
        print(f"❌ Error: {response2.status_code} - {response2.text}")
        return False

def test_search_tool():
    """Test that the search tool works without errors."""
    
    base_url = "http://localhost:8000"
    session_id = "test_search_tool"
    
    print("\n🔍 Testing Search Tool Fix")
    print("=" * 50)
    
    # Test search functionality
    print("\n🔍 Testing search functionality...")
    response = requests.post(f"{base_url}/chat", json={
        "message": "What is the capital of France?",
        "session_id": session_id
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Response: {result['response'][:100]}...")
        print(f"⏱️  Processing time: {result['processing_time']:.2f}s")
        
        # Check metadata for any errors
        metadata = result.get('metadata', {})
        errors = metadata.get('errors', [])
        tools_executed = metadata.get('tools_executed', [])
        
        if errors:
            print(f"❌ Errors found: {errors}")
            return False
        else:
            print("✅ No errors in processing")
            
        if tools_executed:
            print(f"✅ Tools executed: {len(tools_executed)}")
            for tool in tools_executed:
                if tool.get('success') == False:
                    print(f"❌ Tool failed: {tool}")
                    return False
            print("✅ All tools executed successfully")
            return True
        else:
            print("ℹ️  No tools were executed")
            return True
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Memory and Search Tool Tests")
    print("=" * 60)
    
    # Test memory functionality
    memory_success = test_memory()
    
    # Test search tool
    search_success = test_search_tool()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Memory Functionality: {'✅ PASSED' if memory_success else '❌ FAILED'}")
    print(f"Search Tool Fix: {'✅ PASSED' if search_success else '❌ FAILED'}")
    
    if memory_success and search_success:
        print("\n🎉 ALL TESTS PASSED! Both issues have been fixed.")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.") 