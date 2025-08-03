#!/usr/bin/env python3
"""
Test script for Metadata functionality.

This script demonstrates how the metadata system works,
showing the storage and retrieval of user information and session metadata.
"""

import uuid
import json
from datetime import datetime
from src.memory.hybrid_conversation_memory import create_hybrid_memory


def test_metadata_functionality():
    """Test the metadata functionality."""
    
    # Create a unique session ID
    session_id = str(uuid.uuid4())
    print(f"🚀 Starting metadata test with session ID: {session_id}")
    print("=" * 60)
    
    # Initialize memory
    memory = create_hybrid_memory(session_id)
    
    # Test 1: Set user information
    print("\n📝 Test 1: Setting user information")
    user_info = {
        "name": "Juan Pérez",
        "age": 25,
        "language": "español",
        "preferences": {
            "learning_style": "visual",
            "difficulty_level": "intermediate",
            "topics_of_interest": ["programación", "matemáticas", "ciencia"]
        },
        "session_start": datetime.now().isoformat()
    }
    
    memory.set_user_info(user_info)
    print(f"✅ User info set: {json.dumps(user_info, indent=2, ensure_ascii=False)}")
    
    # Test 2: Set conversation objective
    print("\n📝 Test 2: Setting conversation objective")
    objective = "Ayudar al usuario a aprender programación en Python"
    memory.set_conversation_objective(objective)
    print(f"✅ Objective set: {objective}")
    
    # Test 3: Set conversation state
    print("\n📝 Test 3: Setting conversation state")
    conversation_state = {
        "current_topic": "variables en Python",
        "progress": {
            "completed_topics": ["introducción", "tipos de datos"],
            "current_lesson": "variables",
            "score": 85
        },
        "last_interaction": datetime.now().isoformat(),
        "session_duration": 1200  # seconds
    }
    
    memory.set_conversation_state(conversation_state)
    print(f"✅ Conversation state set: {json.dumps(conversation_state, indent=2, ensure_ascii=False)}")
    
    # Test 4: Set additional metadata
    print("\n📝 Test 4: Setting additional metadata")
    additional_metadata = {
        "system_info": {
            "version": "1.0.0",
            "environment": "development",
            "features_enabled": ["objectives", "user_tracking", "progress_monitoring"]
        },
        "session_config": {
            "max_tokens": 1000,
            "temperature": 0.7,
            "language": "español"
        },
        "analytics": {
            "messages_sent": 15,
            "objectives_changed": 2,
            "user_satisfaction": 4.5
        }
    }
    
    memory.set_session_metadata(additional_metadata)
    print(f"✅ Additional metadata set: {json.dumps(additional_metadata, indent=2, ensure_ascii=False)}")
    
    # Test 5: Retrieve all metadata
    print("\n📝 Test 5: Retrieving all metadata")
    all_metadata = memory.get_session_metadata()
    print(f"✅ All metadata retrieved:")
    print(json.dumps(all_metadata, indent=2, ensure_ascii=False))
    
    # Test 6: Retrieve specific values
    print("\n📝 Test 6: Retrieving specific values")
    user_name = memory.get_metadata_value("user_info.name")
    user_age = memory.get_metadata_value("user_info.age")
    current_topic = memory.get_metadata_value("conversation_state.current_topic")
    objective = memory.get_conversation_objective()
    
    print(f"✅ User name: {user_name}")
    print(f"✅ User age: {user_age}")
    print(f"✅ Current topic: {current_topic}")
    print(f"✅ Objective: {objective}")
    
    # Test 7: Update specific values
    print("\n📝 Test 7: Updating specific values")
    memory.update_conversation_state("current_topic", "funciones en Python")
    memory.update_session_metadata("analytics.messages_sent", 20)
    
    updated_topic = memory.get_metadata_value("conversation_state.current_topic")
    updated_messages = memory.get_metadata_value("analytics.messages_sent")
    
    print(f"✅ Updated topic: {updated_topic}")
    print(f"✅ Updated messages sent: {updated_messages}")
    
    # Test 8: Load memory variables
    print("\n📝 Test 8: Loading memory variables")
    memory_vars = memory.load_memory_variables({})
    
    print(f"✅ Chat history length: {len(memory_vars.get('chat_history', []))}")
    print(f"✅ Conversation objective: {memory_vars.get('conversation_objective')}")
    print(f"✅ Session metadata keys: {list(memory_vars.get('session_metadata', {}).keys())}")
    
    # Test 9: Simulate conversation with metadata context
    print("\n📝 Test 9: Simulating conversation with metadata context")
    
    # Save some conversation context
    memory.save_context(
        {"message": "¿Qué son las variables en Python?"},
        {"response": "Las variables son contenedores para almacenar datos..."}
    )
    
    memory.save_context(
        {"message": "¿Cómo se declaran?"},
        {"response": "En Python se declaran simplemente asignando un valor..."}
    )
    
    # Update progress
    memory.update_conversation_state("progress.completed_topics", 
                                   ["introducción", "tipos de datos", "variables"])
    memory.update_conversation_state("progress.current_lesson", "funciones")
    
    # Final state
    final_metadata = memory.get_session_metadata()
    print(f"✅ Final metadata state:")
    print(json.dumps(final_metadata, indent=2, ensure_ascii=False))
    
    print("\n✨ Metadata functionality test completed successfully!")


def test_metadata_persistence():
    """Test that metadata persists across memory instances."""
    print("\n" + "=" * 60)
    print("🔄 Testing Metadata Persistence")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    
    # Create first memory instance and set data
    memory1 = create_hybrid_memory(session_id)
    memory1.set_user_info({"name": "María García", "age": 30})
    memory1.set_conversation_objective("Aprender JavaScript")
    memory1.set_conversation_state({"current_topic": "DOM manipulation"})
    
    print(f"✅ Data set in memory1")
    
    # Create second memory instance with same session_id
    memory2 = create_hybrid_memory(session_id)
    
    # Retrieve data from second instance
    user_info = memory2.get_user_info()
    objective = memory2.get_conversation_objective()
    state = memory2.get_conversation_state()
    
    print(f"✅ Retrieved from memory2:")
    print(f"   User info: {user_info}")
    print(f"   Objective: {objective}")
    print(f"   State: {state}")
    
    # Verify persistence
    assert user_info.get("name") == "María García"
    assert objective == "Aprender JavaScript"
    assert state.get("current_topic") == "DOM manipulation"
    
    print("✅ Metadata persistence test passed!")


def test_metadata_utilities():
    """Test metadata utility functions."""
    print("\n" + "=" * 60)
    print("🛠️ Testing Metadata Utilities")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id)
    
    # Test nested key access
    memory.set_session_metadata({
        "user": {
            "profile": {
                "name": "Carlos",
                "preferences": {
                    "theme": "dark",
                    "notifications": True
                }
            }
        }
    })
    
    # Test get_metadata_value with nested keys
    name = memory.get_metadata_value("user.profile.name")
    theme = memory.get_metadata_value("user.profile.preferences.theme")
    notifications = memory.get_metadata_value("user.profile.preferences.notifications")
    
    print(f"✅ Nested key access:")
    print(f"   Name: {name}")
    print(f"   Theme: {theme}")
    print(f"   Notifications: {notifications}")
    
    # Test default values
    non_existent = memory.get_metadata_value("non.existent.key", "default_value")
    print(f"✅ Default value for non-existent key: {non_existent}")
    
    # Test metadata merging
    memory.set_session_metadata({"new_key": "new_value"})
    all_metadata = memory.get_session_metadata()
    print(f"✅ Metadata after merging: {json.dumps(all_metadata, indent=2, ensure_ascii=False)}")
    
    print("✅ Metadata utilities test completed!")


if __name__ == "__main__":
    print("🧪 Metadata System Test")
    print("=" * 60)
    
    try:
        # Run all tests
        test_metadata_functionality()
        test_metadata_persistence()
        test_metadata_utilities()
        
        print("\n🎉 All metadata tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 