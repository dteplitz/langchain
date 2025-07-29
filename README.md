# LangChain Chat System - Stage 1

A LangChain-based chat system with intelligent agents, built with FastAPI and modern Python practices.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│  Simple Chain   │───▶│ Curator Agent   │
│                 │    │                 │    │                 │
│ • /chat         │    │ • Memory Mgmt   │    │ • Input Clean   │
│ • /health       │    │ • Error Handling│    │ • Validation    │
│ • CORS          │    │ • Logging       │    │ • JSON Output   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SQLite DB     │    │   Groq LLM      │    │   Logging       │
│                 │    │                 │    │                 │
│ • Chat History  │    │ • llama3-8b     │    │ • Structured    │
│ • Session Mgmt  │    │ • Fast Response │    │ • Request IDs   │
│ • Persistence   │    │ • Configurable  │    │ • Performance   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Features (Stage 1)

- **Curator Agent**: Cleans and validates user input
- **FastAPI Integration**: RESTful API with OpenAPI documentation
- **SQLite Memory**: Persistent conversation history
- **Structured Logging**: Request tracking and performance metrics
- **Error Handling**: Comprehensive error management
- **CORS Support**: Cross-origin resource sharing
- **Type Safety**: Full type hints and Pydantic validation

## 📋 Prerequisites

- Python 3.8+
- Groq API key (get one at [groq.com](https://groq.com))

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd langchain
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your Groq API key
   ```

4. **Set your Groq API key**
   ```bash
   # Edit .env file
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
python -m src.main
```

### Production Mode
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### With Debug Logging
```bash
DEBUG=true python -m src.main
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔧 API Usage

### Chat Endpoint

**POST** `/chat`

```json
{
  "message": "What is the capital of France?",
  "session_id": "user_123",
  "debug": false
}
```

**Response:**
```json
{
  "response": "I understand your question: What is the capital of France?. This would be processed by the full chain in later stages.",
  "session_id": "user_123",
  "request_id": "req_456",
  "processing_time": 1.23,
  "metadata": {
    "agent_used": "curator",
    "is_valid": true,
    "confidence": 0.95,
    "content_type": "question",
    "validation_errors": [],
    "stage": "stage_1"
  }
}
```

## 🏗️ Project Structure

```
langchain/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── models.py              # Pydantic models
│   ├── agents/
│   │   ├── __init__.py
│   │   └── curator_agent.py   # Curator agent implementation
│   ├── chains/
│   │   ├── __init__.py
│   │   └── simple_chain.py    # Simple chain for Stage 1
│   ├── memory/
│   │   ├── __init__.py
│   │   └── conversation_memory.py  # SQLite memory management
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── curator_prompts.py # Curator agent prompts
│   └── utils/
│       ├── __init__.py
│       ├── llm_client.py      # Groq LLM client
│       └── logger.py          # Structured logging
├── requirements.txt           # Python dependencies
├── env.example               # Environment variables template
├── chat_memory.db            # SQLite database (created automatically)
└── README.md                 # This file
```

## 🔍 Testing the System

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Simple Chat
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "session_id": "test_user"
  }'
```

### 3. Debug Mode
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Python?",
    "session_id": "debug_user",
    "debug": true
  }'
```

## 🧪 Validation Examples

The Curator Agent will validate different types of input:

- **Valid Questions**: "What is the capital of France?"
- **Valid Statements**: "I like programming"
- **Invalid Content**: Messages with inappropriate content
- **Empty Messages**: Will be flagged as invalid

## 📊 Monitoring

The system provides comprehensive logging:

- **Request Tracking**: Each request gets a unique ID
- **Performance Metrics**: Processing time for each agent
- **Error Logging**: Detailed error information with context
- **Agent Responses**: Logged with metadata and confidence scores

## 🔧 Configuration

Key configuration options in `.env`:

```bash
# LLM Settings
MODEL_NAME=llama3-8b-8192    # Groq model to use
TEMPERATURE=0.7              # Response creativity (0.0-2.0)
MAX_TOKENS=1000              # Maximum response length

# Logging
LOG_LEVEL=INFO               # Logging level
DEBUG=false                  # Debug mode

# Database
DATABASE_URL=sqlite:///./chat_memory.db
```

## 🚧 Stage 1 Limitations

This is the first stage of development. Current limitations:

- Only the Curator Agent is implemented
- No actual response generation (placeholder responses)
- Basic chain orchestration
- No tools or external APIs

## 🔮 Next Stages

**Stage 2**: Add Processor and Response agents with tools
**Stage 3**: Complete RunnableSequence with fallbacks and callbacks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Ensure your Groq API key is valid
4. Verify all dependencies are installed 