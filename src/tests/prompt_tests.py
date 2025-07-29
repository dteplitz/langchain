"""
Prompt tests using FakeLLM.

This module contains tests for validating all agent prompts
using LangChain's FakeLLM for consistent testing.
"""

# import pytest  # Not required for basic testing
from typing import Dict, Any, List
from langchain_community.llms import FakeListLLM
from langchain.schema.runnable import Runnable

from src.agents.curator_agent import create_curator_agent
from src.agents.processor_agent import create_processor_agent
from src.agents.formatter_agent import create_formatter_agent
from src.models.agent_interfaces import CuratorOutput, ProcessorInput, FormatterInput


class TestPromptValidation:
    """Test class for prompt validation using FakeLLM."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Create fake LLM responses for testing
        self.curator_responses = [
            '{"cleaned_message": "What is the capital of France?", "is_valid": true, "validation_errors": [], "content_type": "question", "confidence": 0.95}',
            '{"cleaned_message": "Hello how are you", "is_valid": true, "validation_errors": [], "content_type": "statement", "confidence": 0.8}',
            '{"cleaned_message": "", "is_valid": false, "validation_errors": ["Message is empty"], "content_type": "invalid", "confidence": 0.0}'
        ]
        
        self.processor_responses = [
            "Paris is the capital of France. It is known as the 'City of Light' and is famous for its art, fashion, and culture.",
            "I'm doing well, thank you for asking! How are you today?",
            "I understand your question. Let me provide you with a comprehensive answer."
        ]
        
        self.formatter_responses = [
            "**Answer:** Paris is the capital of France.\n\n**Details:** Paris is known as the 'City of Light' and is famous for its art, fashion, and culture.",
            "Hello! I'm doing well, thank you for asking. How are you today?",
            "I understand your question. Here's a comprehensive answer for you."
        ]
    
    def test_curator_agent_prompt(self):
        """Test curator agent prompt with FakeLLM."""
        # Create fake LLM
        fake_llm = FakeListLLM(responses=self.curator_responses)
        
        # Create curator agent with fake LLM
        agent = create_curator_agent(verbose=False)
        agent.llm = fake_llm  # Replace with fake LLM
        
        # Test cases
        test_cases = [
            {
                "message": "What is the capital of France?",
                "expected_type": "question",
                "expected_valid": True
            },
            {
                "message": "Hello, how are you?",
                "expected_type": "statement",
                "expected_valid": True
            },
            {
                "message": "",
                "expected_type": "invalid",
                "expected_valid": False
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            result = agent.invoke({
                "message": test_case["message"],
                "chat_history": [],
                "request_id": f"test_{i}"
            })
            
            assert isinstance(result, CuratorOutput)
            assert result.content_type == test_case["expected_type"]
            assert result.is_valid == test_case["expected_valid"]
            assert result.confidence >= 0.0 and result.confidence <= 1.0
    
    def test_processor_agent_prompt(self):
        """Test processor agent prompt with FakeLLM."""
        # Create fake LLM
        fake_llm = FakeListLLM(responses=self.processor_responses)
        
        # Create processor agent with fake LLM
        agent = create_processor_agent(verbose=False)
        agent.llm = fake_llm  # Replace with fake LLM
        
        # Test cases
        test_cases = [
            {
                "message": "What is the capital of France?",
                "expected_quality": 0.8
            },
            {
                "message": "Hello, how are you?",
                "expected_quality": 0.6
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            curator_output = CuratorOutput(
                cleaned_message=test_case["message"],
                is_valid=True,
                validation_errors=[],
                content_type="question",
                confidence=0.9
            )
            
            processor_input = ProcessorInput(
                message=test_case["message"],
                chat_history=[],
                curator_output=curator_output.dict(),
                tools_used=[],
                search_results=[]
            )
            
            result = agent.invoke(processor_input)
            
            assert isinstance(result, ProcessorOutput)
            assert result.response_quality >= 0.0 and result.response_quality <= 1.0
            assert len(result.raw_response) > 0
    
    def test_formatter_agent_prompt(self):
        """Test formatter agent prompt with FakeLLM."""
        # Create fake LLM
        fake_llm = FakeListLLM(responses=self.formatter_responses)
        
        # Create formatter agent with fake LLM
        agent = create_formatter_agent(verbose=False)
        agent.llm = fake_llm  # Replace with fake LLM
        
        # Test cases
        test_cases = [
            {
                "raw_response": "Paris is the capital of France.",
                "user_message": "What is the capital of France?",
                "response_type": "question",
                "expected_structure": "paragraph"
            },
            {
                "raw_response": "I'm doing well, thank you!",
                "user_message": "Hello, how are you?",
                "response_type": "statement",
                "expected_structure": "paragraph"
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            processor_output = ProcessorOutput(
                raw_response=test_case["raw_response"],
                tools_executed=[],
                search_performed=False,
                response_quality=0.8,
                processing_time=1.0
            )
            
            formatter_input = FormatterInput(
                raw_response=test_case["raw_response"],
                user_message=test_case["user_message"],
                response_type=test_case["response_type"],
                processor_output=processor_output.dict()
            )
            
            result = agent.invoke(formatter_input)
            
            assert isinstance(result, FormatterOutput)
            assert result.readability_score >= 0.0 and result.readability_score <= 1.0
            assert len(result.formatted_response) > 0
            assert result.response_structure in ["paragraph", "bullet_points", "numbered_list", "structured_explanation"]
    
    def test_chain_integration(self):
        """Test complete chain integration with FakeLLM."""
        # Create fake LLM responses for the complete flow
        fake_responses = [
            # Curator responses
            '{"cleaned_message": "What is the capital of France?", "is_valid": true, "validation_errors": [], "content_type": "question", "confidence": 0.95}',
            # Processor responses
            "Paris is the capital of France. It is known as the 'City of Light'.",
            # Formatter responses
            "**Answer:** Paris is the capital of France.\n\n**Details:** Paris is known as the 'City of Light'."
        ]
        
        fake_llm = FakeListLLM(responses=fake_responses)
        
        # Create agents with fake LLM
        curator = create_curator_agent(verbose=False)
        curator.llm = fake_llm
        
        processor = create_processor_agent(verbose=False)
        processor.llm = fake_llm
        
        formatter = create_formatter_agent(verbose=False)
        formatter.llm = fake_llm
        
        # Test complete flow
        message = "What is the capital of France?"
        
        # Step 1: Curator
        curator_result = curator.invoke({
            "message": message,
            "chat_history": [],
            "request_id": "test_chain"
        })
        
        assert curator_result.is_valid
        assert curator_result.content_type == "question"
        
        # Step 2: Processor
        processor_input = ProcessorInput(
            message=message,
            chat_history=[],
            curator_output=curator_result.dict(),
            tools_used=[],
            search_results=[]
        )
        
        processor_result = processor.invoke(processor_input)
        assert len(processor_result.raw_response) > 0
        
        # Step 3: Formatter
        formatter_input = FormatterInput(
            raw_response=processor_result.raw_response,
            user_message=message,
            response_type=curator_result.content_type,
            processor_output=processor_result.dict()
        )
        
        formatter_result = formatter.invoke(formatter_input)
        assert len(formatter_result.formatted_response) > 0
        assert "**Answer:**" in formatter_result.formatted_response


def run_prompt_tests():
    """Run all prompt tests."""
    print("🧪 Running prompt validation tests...")
    
    test_instance = TestPromptValidation()
    test_instance.setup_method()
    
    # Run tests
    try:
        test_instance.test_curator_agent_prompt()
        print("✅ Curator agent prompt test passed")
        
        test_instance.test_processor_agent_prompt()
        print("✅ Processor agent prompt test passed")
        
        test_instance.test_formatter_agent_prompt()
        print("✅ Formatter agent prompt test passed")
        
        test_instance.test_chain_integration()
        print("✅ Chain integration test passed")
        
        print("🎉 All prompt tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Prompt test failed: {e}")
        return False


if __name__ == "__main__":
    run_prompt_tests() 