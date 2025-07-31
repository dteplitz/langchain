# LangChain Chat System - Stage 3 Complete

## 📋 **Resumen del Proyecto**

Este es un sistema de chat inteligente basado en **LangChain** que implementa una arquitectura de **3 agentes especializados** conectados mediante **RunnableSequence** y **RunnableWithFallbacks**. El sistema procesa mensajes del usuario a través de un pipeline inteligente que incluye validación, procesamiento con herramientas, y formateo de respuestas, todo mientras mantiene memoria persistente de las conversaciones.

### **🎯 Características Principales:**
- **3 Agentes Inteligentes**: Curator (validación), Processor (procesamiento), Formatter (formateo)
- **Herramientas Dummy**: Búsqueda web, calculadora, clima, tiempo
- **Memoria Persistente**: SQLite para historial de conversaciones
- **API REST**: FastAPI con documentación OpenAPI/Swagger
- **Logging Avanzado**: Logs estructurados y legibles
- **Manejo de Errores**: Fallbacks robustos en cada agente
- **Configuración Flexible**: Parámetros configurables por agente

---

## 🏗️ **Arquitectura del Sistema**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LANGCHAIN CHAT SYSTEM                             │
│                                                                             │
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
```

---

## 🚀 **Instalación y Configuración**

### **Prerrequisitos:**
- Python 3.8+
- Groq API Key

### **1. Clonar y Configurar:**
```bash
git clone <repository-url>
cd langchain
```

### **2. Instalar Dependencias:**
```bash
pip install -r requirements.txt
```

### **3. Configurar Variables de Entorno:**
```bash
cp env.example .env
```

Editar `.env`:
```env
GROQ_API_KEY=tu_api_key_de_groq
DATABASE_URL=sqlite:///chat_memory.db
LOG_LEVEL=INFO

# Configuración de Idioma (Español por defecto)
LANGUAGE=spanish
LOCALE=es-ES
```

### **4. Ejecutar el Servidor:**
```bash
python -m src.main
```

El servidor estará disponible en: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

### **5. Verificar Configuración en Español:**
```bash
python test_spanish_config.py
```

Este script verifica que:
- ✅ Los prompts están configurados en español
- ✅ La detección de tipos de respuesta funciona con palabras en español
- ✅ Los mensajes de error y éxito están en español
- ✅ Las variables de entorno están configuradas correctamente

### **6. Verificar Sistema de Memoria:**
```bash
# Pruebas de memoria básicas
python test_memory_fix.py

# Pruebas de integración con el servidor (requiere servidor ejecutándose)
python test_memory_integration.py
```

Estos scripts verifican que:
- ✅ La memoria SQLite funciona correctamente
- ✅ El historial de conversación se guarda y carga
- ✅ El formato del historial es correcto para los agentes
- ✅ La memoria persiste entre sesiones
- ✅ Las sesiones están correctamente separadas

---

## 🤖 **Configuración de Agentes**

### **📋 Estructura de Agentes**

El sistema utiliza una arquitectura de **3 agentes especializados** que procesan los mensajes en secuencia:

1. **Curator Agent** (`src/agents/curator_agent.py`)
2. **Processor Agent** (`src/agents/processor_agent.py`) 
3. **Formatter Agent** (`src/agents/formatter_agent.py`)

### **🔧 Configuración de Agentes Existentes**

Cada agente tiene parámetros configurables que se pueden ajustar al crear la cadena:

```python
from src.chains.advanced_chain import create_advanced_chain

# Configuración personalizada por agente
chain = create_advanced_chain(
    curator_config={
        "temperature": 0.1,      # Baja temperatura para validación consistente
        "max_tokens": 500        # Respuestas cortas para validación
    },
    processor_config={
        "temperature": 0.7,      # Temperatura media para creatividad
        "max_tokens": 1000       # Respuestas más largas
    },
    formatter_config={
        "temperature": 0.3,      # Temperatura baja para consistencia
        "max_tokens": 800        # Formateo moderado
    },
    verbose=True                 # Logs detallados
)
```

### **📝 Cómo Crear un Nuevo Agente**

#### **Paso 1: Crear el Archivo del Agente**

Crear `src/agents/nuevo_agent.py`:

```python
"""
Nuevo Agent implementation.

This agent performs [describe what it does].
"""

import time
from typing import Dict, Any, Optional
from langchain.schema.runnable import Runnable
from langchain.schema.output_parser import StrOutputParser

from src.utils.llm_client import get_llm_client
from src.utils.enhanced_logger import get_enhanced_logger
from src.prompts.nuevo_prompts import get_nuevo_prompt
from src.models.agent_interfaces import NuevoInput, NuevoOutput


class NuevoAgent(Runnable):
    """
    Nuevo Agent for [specific functionality].
    
    This agent is responsible for [detailed description].
    """
    
    def __init__(
        self,
        temperature: float = 0.5,
        max_tokens: int = 600,
        verbose: bool = False
    ):
        """
        Initialize the nuevo agent.
        
        Args:
            temperature: LLM temperature (0.0 to 1.0)
            max_tokens: Maximum tokens for response
            verbose: Enable verbose logging
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.verbose = verbose
        self.logger = get_enhanced_logger()
        
        # Initialize LLM client
        self.llm = get_llm_client(temperature=temperature, max_tokens=max_tokens)
        
        # Create the chain
        self.chain = get_nuevo_prompt() | self.llm | StrOutputParser()
    
    def invoke(
        self, 
        input_data: NuevoInput, 
        config: Optional[Dict[str, Any]] = None
    ) -> NuevoOutput:
        """
        Process input through the nuevo agent.
        
        Args:
            input_data: NuevoInput containing required data
            config: Optional configuration
            
        Returns:
            NuevoOutput: Processed result
        """
        start_time = time.time()
        request_id = input_data.request_id or "unknown"
        
        # Log the request
        self.logger.start_agent(request_id, "nuevo", {
            "input_data": input_data.dict(),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        })
        
        try:
            # Process the input
            result = self.chain.invoke(input_data.dict(), config or {})
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create output
            output = NuevoOutput(
                processed_data=result,
                processing_time=processing_time,
                success=True
            )
            
            # Log the response
            self.logger.end_agent(request_id, "nuevo", output, {
                "processing_time": processing_time,
                "success": True
            })
            
            return output
            
        except Exception as e:
            # Log error
            processing_time = time.time() - start_time
            self.logger.log_error(
                request_id=request_id,
                agent_name="nuevo",
                error=e,
                context={"input": input_data.dict()}
            )
            
            # Return error response
            return NuevoOutput(
                processed_data=f"Error: {str(e)}",
                processing_time=processing_time,
                success=False
            )


def create_nuevo_agent(
    temperature: float = 0.5,
    max_tokens: int = 600,
    verbose: bool = False
) -> NuevoAgent:
    """
    Create a new nuevo agent instance.
    
    Args:
        temperature: LLM temperature
        max_tokens: Maximum tokens
        verbose: Enable verbose logging
        
    Returns:
        NuevoAgent: Configured agent instance
    """
    return NuevoAgent(
        temperature=temperature,
        max_tokens=max_tokens,
        verbose=verbose
    )
```

#### **Paso 2: Crear los Prompts**

Crear `src/prompts/nuevo_prompts.py`:

```python
"""
Prompt templates for the Nuevo Agent.

This module contains all prompt templates used by the Nuevo agent.
"""

from langchain.prompts import PromptTemplate
from typing import Dict, Any


# Prompt template for the nuevo agent
NUEVO_PROMPT = PromptTemplate(
    input_variables=["input_data", "context"],
    template="""You are a Nuevo Agent responsible for [specific task].

Your role is to:
1. [Task 1]
2. [Task 2]
3. [Task 3]

Input Data: {input_data}
Context: {context}

Instructions:
- [Specific instruction 1]
- [Specific instruction 2]
- [Specific instruction 3]

Generate a response that [describe expected output]."""
)


def get_nuevo_prompt() -> PromptTemplate:
    """
    Get the nuevo prompt template.
    
    Returns:
        PromptTemplate: The nuevo prompt template
    """
    return NUEVO_PROMPT
```

#### **Paso 3: Definir las Interfaces**

Agregar a `src/models/agent_interfaces.py`:

```python
class NuevoInput(BaseModel):
    """Input model for Nuevo Agent."""
    input_data: str
    context: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


class NuevoOutput(BaseModel):
    """Output model for Nuevo Agent."""
    processed_data: str
    processing_time: float
    success: bool
    metadata: Optional[Dict[str, Any]] = None
```

#### **Paso 4: Integrar en la Cadena**

Modificar `src/chains/advanced_chain.py`:

```python
# Importar el nuevo agente
from src.agents.nuevo_agent import create_nuevo_agent
from src.models.agent_interfaces import NuevoInput, NuevoOutput

class AdvancedChain(Runnable):
    def __init__(self, ...):
        # ... existing code ...
        
        # Agregar el nuevo agente
        self.nuevo_agent = create_nuevo_agent(**nuevo_config, verbose=verbose)
    
    def _orchestrate_agents(self, ...):
        # ... existing code ...
        
        # Agregar el nuevo agente al flujo
        nuevo_input = NuevoInput(
            input_data=processor_result.raw_response,
            context={"user_message": message},
            request_id=request_id
        )
        
        nuevo_result = self.nuevo_agent.invoke(nuevo_input)
        agents_used.append("nuevo")
        
        # Continuar con el formatter usando el resultado del nuevo agente
        formatter_input = FormatterInput(
            raw_response=nuevo_result.processed_data,
            user_message=message,
            response_type=curator_result.content_type,
            processor_output=processor_result.dict()
        )
```

### **🔄 Flujo de Agentes**

```
User Message
     │
     ▼
┌─────────────┐
│   Curator   │ ← Validación y limpieza
│   Agent     │
└─────────────┘
     │
     ▼
┌─────────────┐
│  Processor  │ ← Procesamiento con herramientas
│   Agent     │
└─────────────┘
     │
     ▼
┌─────────────┐
│  Formatter  │ ← Formateo de respuesta
│   Agent     │
└─────────────┘
     │
     ▼
   Response
```

---

## 🛠️ **Sistema de Herramientas (Tools)**

### **📋 Herramientas Disponibles**

El sistema incluye **4 herramientas dummy** que simulan funcionalidades reales:

#### **1. Search Tool (`search_web`)**
- **Propósito**: Búsqueda web simulada
- **Funcionalidad**: Busca información en una base de conocimiento interna
- **Uso**: Cuando el usuario pregunta por información factual
- **Ejemplo**: "¿Cuál es la capital de Francia?"

```python
# Ejecución manual
from src.utils.tools import execute_tool
result = execute_tool("search_web", query="Python programming")
```

#### **2. Calculator Tool (`calculate`)**
- **Propósito**: Operaciones matemáticas
- **Funcionalidad**: Evalúa expresiones matemáticas
- **Uso**: Cuando el usuario incluye cálculos
- **Ejemplo**: "¿Cuánto es 15 + 27?"

```python
result = execute_tool("calculate", expression="15 + 27")
```

#### **3. Weather Tool (`get_weather`)**
- **Propósito**: Información meteorológica
- **Funcionalidad**: Proporciona datos climáticos simulados
- **Uso**: Cuando el usuario pregunta por el clima
- **Ejemplo**: "¿Cómo está el clima en París?"

```python
result = execute_tool("get_weather", location="Paris")
```

#### **4. Time Tool (`get_time`)**
- **Propósito**: Información de tiempo y fecha
- **Funcionalidad**: Proporciona hora y fecha actual
- **Uso**: Cuando el usuario pregunta por tiempo/fecha
- **Ejemplo**: "¿Qué hora es?"

```python
result = execute_tool("get_time", timezone="UTC")
```

### **🔧 Cómo Funcionan las Herramientas**

#### **Detección Automática**
El **Processor Agent** detecta automáticamente qué herramientas necesita basándose en el contenido del mensaje:

```python
def _determine_tools_needed(self, message: str, curator_output: Dict[str, Any]) -> List[str]:
    """Determine which tools are needed based on message content."""
    message_lower = message.lower()
    tools_needed = []
    
    # Check for search needs
    if any(word in message_lower for word in ['what', 'how', 'when', 'where', 'why', 'who']):
        tools_needed.append('search_web')
    
    # Check for calculation needs
    if any(char in message for char in ['+', '-', '*', '/', '=']):
        tools_needed.append('calculate')
    
    # Check for weather needs
    if any(word in message_lower for word in ['weather', 'temperature', 'forecast']):
        tools_needed.append('get_weather')
    
    # Check for time needs
    if any(word in message_lower for word in ['time', 'date', 'schedule']):
        tools_needed.append('get_time')
    
    return tools_needed
```

#### **Ejecución Secuencial**
Las herramientas se ejecutan en paralelo y los resultados se combinan:

```python
def _execute_tools(self, tools_needed: List[str], message: str, request_id: str) -> List[ToolExecutionResult]:
    """Execute the needed tools."""
    results = []
    
    for tool_name in tools_needed:
        try:
            # Execute tool with appropriate parameters
            if tool_name == 'search_web':
                result = execute_tool(tool_name, query=message)
            elif tool_name == 'calculate':
                result = execute_tool(tool_name, expression=extract_math_expression(message))
            # ... other tools
            
            # Log execution
            self.logger.log_tool_execution(request_id, tool_name, input_params, result, execution_time)
            
            results.append(ToolExecutionResult(
                tool_name=tool_name,
                success=True,
                result=result,
                execution_time=execution_time
            ))
            
        except Exception as e:
            # Handle tool errors
            results.append(ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                error=str(e),
                execution_time=execution_time
            ))
    
    return results
```

### **📝 Cómo Crear una Nueva Herramienta**

#### **Paso 1: Crear la Clase de Herramienta**

```python
class DummyNewTool:
    """Dummy new tool for [specific functionality]."""
    
    def new_function(self, param1: str, param2: int = 10) -> Dict[str, Any]:
        """
        Perform new functionality.
        
        Args:
            param1: First parameter
            param2: Second parameter (default: 10)
            
        Returns:
            Dict[str, Any]: Tool result
        """
        # Simulate processing delay
        time.sleep(random.uniform(0.1, 0.3))
        
        # Generate dummy result
        return {
            "param1": param1,
            "param2": param2,
            "result": f"Processed {param1} with value {param2}",
            "timestamp": datetime.now().isoformat(),
            "source": "Dummy New Tool"
        }
```

#### **Paso 2: Registrar la Herramienta**

En `src/utils/tools.py`:

```python
# Global tool instances
new_tool = DummyNewTool()

def get_available_tools() -> Dict[str, Any]:
    """Get all available tools."""
    return {
        "search_web": search_tool.search_web,
        "calculate": calculator_tool.calculate,
        "get_weather": weather_tool.get_weather,
        "get_time": time_tool.get_time,
        "new_function": new_tool.new_function  # ← Nueva herramienta
    }
```

#### **Paso 3: Actualizar la Detección**

En `src/agents/processor_agent.py`:

```python
def _determine_tools_needed(self, message: str, curator_output: Dict[str, Any]) -> List[str]:
    """Determine which tools are needed based on message content."""
    message_lower = message.lower()
    tools_needed = []
    
    # ... existing tool detection ...
    
    # Check for new tool needs
    if any(word in message_lower for word in ['new', 'function', 'specific']):
        tools_needed.append('new_function')
    
    return tools_needed
```

#### **Paso 4: Manejar la Ejecución**

```python
def _execute_tools(self, tools_needed: List[str], message: str, request_id: str) -> List[ToolExecutionResult]:
    """Execute the needed tools."""
    for tool_name in tools_needed:
        if tool_name == 'new_function':
            # Extract parameters from message
            param1 = extract_param1_from_message(message)
            param2 = extract_param2_from_message(message)
            
            result = execute_tool(tool_name, param1=param1, param2=param2)
        # ... other tools
```

### **🔍 Monitoreo de Herramientas**

Cada ejecución de herramienta se registra con:

- **Tiempo de ejecución**
- **Parámetros de entrada**
- **Resultados o errores**
- **Estado de éxito/fallo**

```python
# Ejemplo de log de herramienta
13:25:05 - langchain_debug - INFO - [TOOL] search_web
13:25:05 - langchain_debug - INFO - [TOOL] Input: {"query": "What's my name?"}
13:25:05 - langchain_debug - INFO - [TOOL] Result: List with 2 items
13:25:05 - langchain_debug - INFO - [TOOL] Time: 0.15s
```

---

## 📡 **API Endpoints**

### **POST /chat**
Endpoint principal para procesar mensajes.

**Request:**
```json
{
  "message": "¿Cuál es la capital de Francia?",
  "session_id": "user_123",
  "debug": false
}
```

**Response:**
```json
{
  "response": "La capital de Francia es París...",
  "session_id": "user_123",
  "request_id": "uuid-here",
  "processing_time": 2.5,
  "metadata": {
    "agents_used": ["curator", "processor", "formatter"],
    "is_valid": true,
    "confidence": 0.95,
    "tools_executed": [...],
    "stage": "stage_3"
  }
}
```

### **GET /health**
Verificación de estado del sistema.

### **GET /docs**
Documentación interactiva de la API (Swagger UI).

---

## 🧪 **Testing**

### **Ejecutar Tests de Etapas:**
```bash
# Test Etapa 1
python test_stage1.py

# Test Etapa 2  
python test_stage2.py

# Test Etapa 3
python test_stage3.py

# Test de Logging
python test_enhanced_logging.py
```

### **Test de Prompts:**
```bash
python -c "from src.tests.prompt_tests import TestPromptValidation; TestPromptValidation().run_all_tests()"
```

---

## 📊 **Logging y Monitoreo**

### **Tipos de Logs:**
- **Request/Response**: Cada petición HTTP
- **Agent Execution**: Procesamiento de cada agente
- **Tool Execution**: Ejecución de herramientas
- **Error Tracking**: Errores y fallbacks
- **Performance**: Tiempos de procesamiento

### **Ejemplo de Log:**
```
13:25:29 - langchain_debug - INFO - [AGENT] [CURATOR] Starting...
13:25:30 - langchain_debug - INFO - [AGENT] [CURATOR] Completed in 1.05s
13:25:30 - langchain_debug - INFO - [CHAIN] STEP_2: Starting Processor Agent
13:25:31 - langchain_debug - INFO - [TOOL] search_web executed successfully
13:25:31 - langchain_debug - INFO - [AGENT] [FORMATTER] Starting...
```

---

## 🔧 **Configuración Avanzada**

### **Variables de Entorno:**
```env
GROQ_API_KEY=tu_api_key
DATABASE_URL=sqlite:///chat_memory.db
LOG_LEVEL=INFO
DEBUG_MODE=false

# Configuración de Idioma
LANGUAGE=spanish
LOCALE=es-ES
```

### **Configuración de Idioma:**

El sistema está configurado por defecto para responder en **español**. Puedes cambiar el idioma modificando las variables de entorno:

```env
# Para español (por defecto)
LANGUAGE=spanish
LOCALE=es-ES

# Para inglés
LANGUAGE=english
LOCALE=en-US

# Para otros idiomas
LANGUAGE=french
LOCALE=fr-FR
```

**Características del idioma español:**
- ✅ Prompts configurados en español
- ✅ Detección de preguntas en español (¿qué?, ¿cómo?, ¿por qué?, etc.)
- ✅ Mensajes de error y éxito en español
- ✅ Formato de fecha español (DD/MM/YYYY)
- ✅ Separador decimal español (coma)
- ✅ Puntuación española (¿, ¡, etc.)

### **Parámetros de Agentes:**
```python
# Configuración personalizada
agent_configs = {
    "curator": {"temperature": 0.1, "max_tokens": 500},
    "processor": {"temperature": 0.7, "max_tokens": 1000},
    "formatter": {"temperature": 0.3, "max_tokens": 800}
}
```

---

## 🚨 **Solución de Problemas**

### **Error: "GROQ_API_KEY not found"**
```bash
# Verificar variable de entorno
echo $GROQ_API_KEY
# O agregar al .env
GROQ_API_KEY=tu_api_key_aqui
```

### **Error: "Port 8000 already in use"**
```bash
# En Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# En Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### **Error: "Database locked"**
```bash
# Reiniciar el servidor
# O eliminar el archivo de base de datos
rm chat_memory.db
```

### **Error: "Memory not working"**
```bash
# Verificar que la base de datos existe
ls -la chat_memory.db

# Ejecutar pruebas de memoria
python test_memory_fix.py

# Si hay problemas, recrear la base de datos
rm chat_memory.db
python test_memory_fix.py
```

### **Error: "System doesn't remember conversations"**
```bash
# Verificar formato del historial
python test_memory_fix.py

# Verificar integración con el servidor
python test_memory_integration.py

# Asegurarse de usar el mismo session_id en conversaciones relacionadas
```

---

## 📚 **Referencias**

- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Groq API Documentation](https://console.groq.com/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)

---

## 🤝 **Contribución**

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 