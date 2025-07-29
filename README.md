# LangChain Chat System - Stage 3 Complete

A comprehensive LangChain-based chat system with intelligent agents, advanced orchestration, and robust error handling.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LANGCHAIN CHAT SYSTEM                             │
│                              (Stage 3 Complete)                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              FASTAPI LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   /chat     │  │   /health   │  │     /       │  │   /docs     │        │
│  │   POST      │  │    GET      │  │    GET      │  │    GET      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MIDDLEWARE STACK                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Security      │  │  Performance    │  │ Enriched Logging│              │
│  │  Middleware     │  │  Middleware     │  │  Middleware     │              │
│  │                 │  │                 │  │                 │              │
│  │ • Security Headers│ │ • Slow Request │  │ • Request/Response│              │
│  │ • XSS Protection│ │   Detection     │  │   Logging       │              │
│  │ • CSP Headers   │ │ • Performance   │  │ • Error Tracking│              │
│  │                 │ │   Metrics       │  │ • Request IDs   │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ADVANCED CHAIN ORCHESTRATION                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    RunnableSequence + Fallbacks                        │ │
│  │                                                                         │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │ │
│  │  │   Curator   │───▶│  Processor  │───▶│  Formatter  │                │ │
│  │  │   Agent     │    │   Agent     │    │   Agent     │                │ │
│  │  │             │    │             │    │             │                │ │
│  │  │ • Validation│    │ • LLM Gen   │    │ • Format    │                │ │
│  │  │ • Cleaning  │    │ • Tools     │    │ • Structure │                │ │
│  │  │ • Content   │    │ • Search    │    │ • Readability│                │ │
│  │  │   Type      │    │ • Context   │    │ • Output    │                │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘                │ │
│  │         │                   │                   │                      │ │
│  │         ▼                   ▼                   ▼                      │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │ │
│  │  │   Fallback  │    │   Fallback  │    │   Fallback  │                │ │
│  │  │   Handler   │    │   Handler   │    │   Handler   │                │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘                │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              TOOLS LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Search    │  │ Calculator  │  │   Weather   │  │    Time     │        │
│  │    Tool     │  │    Tool     │  │    Tool     │  │    Tool     │        │
│  │             │  │             │  │             │  │             │        │
│  │ • Web Search│  │ • Math Ops  │  │ • Weather   │  │ • Time/Date │        │
│  │ • Knowledge │  │ • Functions │  │   Data      │  │ • Timezone  │        │
│  │   Base      │  │ • Variables │  │ • Forecast  │  │ • Schedule  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MEMORY LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    SQLite Conversation Memory                          │ │
│  │                                                                         │ │
│  │  • Session Management                                                   │ │
│  │  • Conversation History                                                 │ │
│  │  • Persistent Storage                                                   │ │
│  │  • Context Retrieval                                                    │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              LLM LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                           Groq LLM                                     │ │
│  │                                                                         │ │
│  │  • llama3-8b-8192 Model                                                │ │
│  │  • Configurable Parameters (temp, tokens, top_p)                       │ │
│  │  • Async Processing                                                     │ │
│  │  • Error Handling                                                       │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ENHANCED LOGGING                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    Structured Logging System                           │ │
│  │                                                                         │ │
│  │  • Request/Response Tracking                                           │ │
│  │  • Agent Execution Logs                                                │ │
│  │  • Tool Usage Logs                                                     │ │
│  │  • Performance Metrics                                                 │ │
│  │  • Error Context                                                       │ │
│  │  • File + Console Output                                               │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### ✅ **Stage 3 Complete Features:**

#### **Advanced Chain Orchestration:**
- **RunnableSequence**: Proper agent orchestration with sequential execution
- **RunnableWithFallbacks**: Robust error handling with fallback mechanisms
- **ConsoleCallbackHandler**: Real-time debugging and monitoring
- **Configurable LLM Parameters**: Per-agent temperature, max_tokens, top_p settings

#### **Enhanced Middleware Stack:**
- **Security Middleware**: XSS protection, CSP headers, security enhancements
- **Performance Middleware**: Slow request detection, performance metrics
- **Enriched Logging Middleware**: Detailed request/response logging with context

#### **Comprehensive Testing:**
- **FakeLLM Tests**: Prompt validation using LangChain's FakeLLM
- **Agent Integration Tests**: Complete chain flow validation
- **Error Handling Tests**: Fallback mechanism validation

#### **Production-Ready Features:**
- **Structured Logging**: Human-readable logs with colors and formatting
- **Error Tracking**: Comprehensive error context and debugging
- **Performance Monitoring**: Request timing and bottleneck detection
- **Security Headers**: Production-grade security enhancements

### ✅ **Previous Stage Features:**

#### **Intelligent Agents:**
- **Curator Agent**: Input validation, cleaning, and content type detection
- **Processor Agent**: LLM generation with tools and context
- **Formatter Agent**: Response formatting and readability optimization

#### **Tools Integration:**
- **Search Tool**: Web search and knowledge base queries
- **Calculator Tool**: Mathematical operations and functions
- **Weather Tool**: Weather data and forecasts
- **Time Tool**: Time, date, and timezone information

#### **Memory Management:**
- **SQLite Persistence**: Conversation history and session management
- **Context Retrieval**: Intelligent conversation context loading
- **Session Isolation**: Multi-user session support

## 📦 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd langchain
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp env.example .env
# Edit .env with your GROQ_API_KEY
```

4. **Run the application:**
```bash
python -m src.main
```

## 🔧 Configuration

### **Environment Variables:**
```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./chat_memory.db

# Logging Configuration
LOG_LEVEL=INFO
DEBUG=false

# LLM Configuration
MODEL_NAME=llama3-8b-8192
TEMPERATURE=0.7
MAX_TOKENS=1000
```

### **Agent Configuration:**
```python
# Curator Agent
curator_config = {
    "temperature": 0.1,    # Low temperature for consistent validation
    "max_tokens": 500      # Short responses for validation
}

# Processor Agent
processor_config = {
    "temperature": 0.7,    # Balanced creativity and consistency
    "max_tokens": 1000     # Longer responses for detailed answers
}

# Formatter Agent
formatter_config = {
    "temperature": 0.3,    # Low temperature for consistent formatting
    "max_tokens": 800      # Medium length for formatted responses
}
```

## 🧪 Testing

### **Run All Tests:**
```bash
# Stage 1 tests
python test_stage1.py

# Stage 2 tests
python test_stage2.py

# Enhanced logging tests
python test_enhanced_logging.py

# Prompt validation tests
python src/tests/prompt_tests.py
```

### **Test Individual Components:**
```bash
# Test specific agents
python -c "from src.agents.curator_agent import create_curator_agent; agent = create_curator_agent(); print('Curator agent created successfully')"

# Test tools
python -c "from src.utils.tools import execute_tool; result = execute_tool('search_web', query='test'); print(result)"

# Test memory
python -c "from src.memory.conversation_memory import create_memory; memory = create_memory('test'); print('Memory created successfully')"
```

## 📡 API Usage

### **Chat Endpoint:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What is the capital of France?",
       "session_id": "user_123",
       "debug": false
     }'
```

### **Response Format:**
```json
{
  "response": "**Answer:** Paris is the capital of France.\n\n**Details:** Paris is known as the 'City of Light'...",
  "session_id": "user_123",
  "request_id": "81f8060d-90e7-492e-88a3-5020aa8b39c3",
  "processing_time": 4.36,
  "metadata": {
    "agents_used": ["curator", "processor", "formatter"],
    "is_valid": true,
    "confidence": 0.95,
    "content_type": "question",
    "tools_executed": [...],
    "search_performed": true,
    "response_quality": 0.8,
    "readability_score": 0.55,
    "response_structure": "paragraph",
    "stage": "stage_3",
    "success": true,
    "errors": []
  }
}
```

## 📊 Monitoring & Logging

### **Log Files:**
- **Console Output**: Real-time colored logs with emojis and formatting
- **File Logs**: `logs/langchain_YYYYMMDD.log` for detailed analysis
- **Request Tracking**: Complete request/response lifecycle logging

### **Performance Metrics:**
- **Processing Time**: Per-request and per-agent timing
- **Slow Request Detection**: Automatic alerts for requests > 5s
- **Agent Performance**: Individual agent execution times
- **Tool Usage**: Tool execution frequency and success rates

### **Error Tracking:**
- **Detailed Error Context**: Full error stack traces with request context
- **Fallback Handling**: Automatic fallback when agents fail
- **Error Classification**: Categorized error types for analysis

## 🔍 Debugging

### **Enhanced Logging:**
```bash
# Enable verbose mode
export DEBUG=true

# View detailed logs
tail -f logs/langchain_$(date +%Y%m%d).log
```

### **Agent Debugging:**
```python
# Debug individual agents
agent = create_curator_agent(verbose=True)
result = agent.debug("Test message")

# Debug complete chain
chain = create_advanced_chain(verbose=True)
result = chain.debug("Test message")
```

### **Middleware Debugging:**
- **Request IDs**: Track requests across the entire system
- **Performance Headers**: Monitor processing times
- **Security Headers**: Verify security configurations

## 🏗️ Architecture Benefits

### **Stage 3 Improvements:**
1. **Robust Error Handling**: Fallbacks ensure system reliability
2. **Production Monitoring**: Comprehensive logging and metrics
3. **Security Enhancements**: Production-grade security headers
4. **Performance Optimization**: Slow request detection and optimization
5. **Testing Coverage**: FakeLLM tests ensure prompt quality

### **Scalability Features:**
- **Modular Design**: Easy to add new agents or tools
- **Configurable Parameters**: Fine-tune performance per use case
- **Session Management**: Support for multiple concurrent users
- **Memory Optimization**: Efficient conversation history management

## 🚀 Next Steps

The system is now **production-ready** with:
- ✅ Complete agent orchestration
- ✅ Robust error handling
- ✅ Comprehensive logging
- ✅ Security enhancements
- ✅ Performance monitoring
- ✅ Testing coverage

**Ready for deployment and scaling!** 🎉

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 