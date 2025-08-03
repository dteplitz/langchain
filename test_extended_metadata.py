#!/usr/bin/env python3
"""
Test script for Extended Metadata functionality.

This script demonstrates the new metadata features:
- welcome_done: Whether welcome message has been shown
- reasons: List of reason strings
- reasons_confirmed: Whether reasons have been confirmed
- vars_info_given: Whether variable information has been provided
- vars: Dictionary with monthly, duration, rate variables
"""

import uuid
import json
from datetime import datetime
from src.memory.hybrid_conversation_memory import create_hybrid_memory


def test_welcome_flow():
    """Test the welcome flow functionality."""
    print("🎉 Testing Welcome Flow")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id)
    
    # Test initial welcome status
    print(f"✅ Initial welcome status: {memory.get_welcome_status()}")
    
    # Set welcome as done
    memory.set_welcome_status(True)
    print(f"✅ Welcome status after setting: {memory.get_welcome_status()}")
    
    # Reset welcome status
    memory.set_welcome_status(False)
    print(f"✅ Welcome status after reset: {memory.get_welcome_status()}")


def test_reasons_management():
    """Test the reasons management functionality."""
    print("\n📝 Testing Reasons Management")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id)
    
    # Test initial reasons
    initial_reasons = memory.get_reasons()
    print(f"✅ Initial reasons: {initial_reasons}")
    
    # Add reasons
    reasons_to_add = [
        "Necesito ayuda con programación",
        "Quiero aprender Python",
        "Tengo un proyecto en mente"
    ]
    
    for reason in reasons_to_add:
        memory.add_reason(reason)
        print(f"✅ Added reason: {reason}")
    
    # Get all reasons
    all_reasons = memory.get_reasons()
    print(f"✅ All reasons: {all_reasons}")
    
    # Test adding duplicate
    memory.add_reason("Necesito ayuda con programación")
    print(f"✅ Reasons after adding duplicate: {memory.get_reasons()}")
    
    # Remove a reason
    memory.remove_reason("Quiero aprender Python")
    print(f"✅ Reasons after removal: {memory.get_reasons()}")
    
    # Test reasons confirmation
    print(f"✅ Initial reasons confirmed: {memory.get_reasons_confirmed()}")
    memory.set_reasons_confirmed(True)
    print(f"✅ Reasons confirmed after setting: {memory.get_reasons_confirmed()}")


def test_variables_management():
    """Test the variables management functionality."""
    print("\n🔢 Testing Variables Management")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id)
    
    # Test initial variables
    initial_vars = memory.get_vars()
    print(f"✅ Initial variables: {initial_vars}")
    
    # Test vars_info_given status
    print(f"✅ Initial vars_info_given: {memory.get_vars_info_given()}")
    
    # Set individual variables
    memory.update_var("monthly", 1500.0)
    memory.update_var("duration", 36)
    memory.update_var("rate", 5.5)
    
    print(f"✅ Variables after individual updates: {memory.get_vars()}")
    
    # Test getting specific variables
    monthly = memory.get_var("monthly")
    duration = memory.get_var("duration")
    rate = memory.get_var("rate")
    
    print(f"✅ Monthly: {monthly}")
    print(f"✅ Duration: {duration}")
    print(f"✅ Rate: {rate}")
    
    # Test loan variables methods
    memory.set_loan_variables(monthly=2000.0, duration=48, rate=4.2)
    print(f"✅ Loan variables after set_loan_variables: {memory.get_loan_variables()}")
    
    # Test if loan info is complete
    is_complete = memory.is_loan_info_complete()
    print(f"✅ Is loan info complete: {is_complete}")
    
    # Reset variables
    memory.reset_loan_variables()
    print(f"✅ Variables after reset: {memory.get_vars()}")
    print(f"✅ Vars info given after reset: {memory.get_vars_info_given()}")


def test_complete_metadata_flow():
    """Test a complete metadata flow simulation."""
    print("\n🔄 Testing Complete Metadata Flow")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id)
    
    print("🚀 Starting complete flow simulation...")
    
    # Step 1: Welcome flow
    print("\n1️⃣ Welcome Flow:")
    memory.set_welcome_status(True)
    print(f"   Welcome shown: {memory.get_welcome_status()}")
    
    # Step 2: Collect reasons
    print("\n2️⃣ Collecting Reasons:")
    user_reasons = [
        "Necesito calcular un préstamo",
        "Quiero comparar opciones de financiamiento",
        "Necesito entender los términos del préstamo"
    ]
    
    for reason in user_reasons:
        memory.add_reason(reason)
        print(f"   Added: {reason}")
    
    print(f"   Total reasons: {memory.get_reasons()}")
    
    # Step 3: Confirm reasons
    print("\n3️⃣ Confirming Reasons:")
    memory.set_reasons_confirmed(True)
    print(f"   Reasons confirmed: {memory.get_reasons_confirmed()}")
    
    # Step 4: Collect variables
    print("\n4️⃣ Collecting Variables:")
    memory.set_vars_info_given(True)
    memory.set_loan_variables(
        monthly=2500.0,
        duration=60,
        rate=6.8
    )
    
    print(f"   Vars info given: {memory.get_vars_info_given()}")
    print(f"   Loan variables: {memory.get_loan_variables()}")
    print(f"   Info complete: {memory.is_loan_info_complete()}")
    
    # Step 5: Show final metadata state
    print("\n5️⃣ Final Metadata State:")
    final_metadata = memory.get_session_metadata()
    print(json.dumps(final_metadata, indent=2, ensure_ascii=False))


def test_metadata_persistence_extended():
    """Test that extended metadata persists across memory instances."""
    print("\n💾 Testing Extended Metadata Persistence")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    
    # Create first memory instance and set extended data
    memory1 = create_hybrid_memory(session_id)
    memory1.set_welcome_status(True)
    memory1.add_reason("Test reason 1")
    memory1.add_reason("Test reason 2")
    memory1.set_reasons_confirmed(True)
    memory1.set_vars_info_given(True)
    memory1.set_loan_variables(monthly=1000.0, duration=24, rate=3.5)
    
    print(f"✅ Extended data set in memory1")
    
    # Create second memory instance with same session_id
    memory2 = create_hybrid_memory(session_id)
    
    # Retrieve extended data from second instance
    welcome_done = memory2.get_welcome_status()
    reasons = memory2.get_reasons()
    reasons_confirmed = memory2.get_reasons_confirmed()
    vars_info_given = memory2.get_vars_info_given()
    vars = memory2.get_vars()
    
    print(f"✅ Retrieved from memory2:")
    print(f"   Welcome done: {welcome_done}")
    print(f"   Reasons: {reasons}")
    print(f"   Reasons confirmed: {reasons_confirmed}")
    print(f"   Vars info given: {vars_info_given}")
    print(f"   Variables: {vars}")
    
    # Verify persistence
    assert welcome_done == True
    assert len(reasons) == 2
    assert reasons_confirmed == True
    assert vars_info_given == True
    assert vars["monthly"] == 1000.0
    
    print("✅ Extended metadata persistence test passed!")


def test_metadata_utilities_extended():
    """Test extended metadata utility functions."""
    print("\n🛠️ Testing Extended Metadata Utilities")
    print("=" * 60)
    
    session_id = str(uuid.uuid4())
    memory = create_hybrid_memory(session_id)
    
    # Test nested access to extended metadata
    memory.set_session_metadata({
        "welcome_done": True,
        "reasons": ["reason1", "reason2"],
        "reasons_confirmed": True,
        "vars_info_given": True,
        "vars": {
            "monthly": 1500.0,
            "duration": 36,
            "rate": 5.5
        }
    })
    
    # Test get_metadata_value with extended keys
    welcome_done = memory.get_metadata_value("welcome_done")
    reasons = memory.get_metadata_value("reasons")
    monthly = memory.get_metadata_value("vars.monthly")
    
    print(f"✅ Extended metadata access:")
    print(f"   Welcome done: {welcome_done}")
    print(f"   Reasons: {reasons}")
    print(f"   Monthly payment: {monthly}")
    
    # Test default values for extended metadata
    non_existent_reason = memory.get_metadata_value("non_existent_reason", "default")
    print(f"✅ Default value for non-existent reason: {non_existent_reason}")
    
    print("✅ Extended metadata utilities test completed!")


if __name__ == "__main__":
    print("🧪 Extended Metadata System Test")
    print("=" * 60)
    
    try:
        # Run all extended tests
        test_welcome_flow()
        test_reasons_management()
        test_variables_management()
        test_complete_metadata_flow()
        test_metadata_persistence_extended()
        test_metadata_utilities_extended()
        
        print("\n🎉 All extended metadata tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 