# LangChain Chat System - Stage 3 Complete

## 📋 **Resumen del Proyecto**

Este es un sistema de chat inteligente basado en **LangChain** que implementa una arquitectura de **3 agentes especializados** conectados mediante **RunnableSequence** y **RunnableWithFallbacks**. El sistema procesa mensajes del usuario a través de un pipeline inteligente que incluye validación, procesamiento con herramientas, y formateo de respuestas, todo mientras mantiene **memoria híbrida persistente** de las conversaciones.

### **🎯 Características Principales:**
- **3 Agentes Inteligentes**: Curator (validación), Processor (procesamiento), Formatter (formateo)
- **Herramientas Dummy**: Búsqueda web, calculadora, clima, tiempo
- **Memoria Híbrida**: Combina ConversationBufferMemory y ConversationSummaryMemory
- **API REST**: FastAPI con documentación OpenAPI/Swagger
- **Logging Avanzado**: Logs estructurados y legibles
- **Manejo de Errores**: Fallbacks robustos en cada agente
- **Configuración Flexible**: Parámetros configurables por agente
- **Gestión de Metadatos**: Sistema flexible para información de sesión

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
│  │                    Hybrid Conversation Memory                          │ │
│  │                                                                         │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │
│  │  │   Buffer Memory │  │  Summary Memory │  │  Metadata Store │        │ │
│  │  │                 │  │                 │  │                 │        │ │
│  │  │ • Recent History│  │ • Long-term     │  │ • Session Info  │        │ │
│  │  │ • Fast Access   │  │   Context       │  │ • User Data     │        │ │
│  │  │ • Token Efficient│  │ • LLM Summaries │  │ • State Mgmt    │        │ │
│  │  │ • Real-time     │  │ • Token Savings │  │ • Persistence   │        │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │
│  │                                                                         │ │
│  │  • Automatic Mode Switching (Buffer ↔ Summary)                         │ │
│  │  • SQLite Persistence                                                  │ │
│  │  • Configurable Thresholds                                             │ │
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

### **7. Verificar Mejoras de Formato:**
```bash
python test_format_improvements.py
```

Este script verifica que:
- ✅ Los prompts están mejorados para generar respuestas más legibles
- ✅ La detección de tipos de respuesta funciona correctamente
- ✅ Las pautas de formato están implementadas
- ✅ Los elementos visuales (emojis, estructura) están configurados
- ✅ Las reglas de formato están claramente definidas

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

## 🗄️ **Sistema de Gestión de Metadatos**

### **📋 Descripción General**

El sistema incluye un **sistema avanzado de gestión de metadatos** que permite almacenar y gestionar información contextual de las conversaciones de forma persistente. Los metadatos se almacenan en formato JSON en la base de datos SQLite y proporcionan un contexto rico para personalizar las respuestas de los agentes.

### **🏗️ Arquitectura de Metadatos**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           METADATA SYSTEM                                   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    SQLite Database                                      │ │
│  │                                                                         │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │
│  │  │   sessions      │  │ conversations   │  │   metadata      │        │ │
│  │  │     table       │  │     table       │  │   (JSON)        │        │ │
│  │  │                 │  │                 │  │                 │        │ │
│  │  │ • session_id    │  │ • session_id    │  │ • user_info     │        │ │
│  │  │ • metadata      │  │ • message       │  │ • objective     │        │ │
│  │  │ • created_at    │  │ • response      │  │ • state         │        │ │
│  │  │ • updated_at    │  │ • timestamp     │  │ • welcome_done  │        │ │
│  │  │                 │  │                 │  │ • reasons       │        │ │
│  │  │                 │  │                 │  │ • vars          │        │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MEMORY INTERFACE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Direct        │  │   Generic       │  │   Utility       │              │
│  │   Methods       │  │   Access        │  │   Methods       │              │ │
│  │                 │  │                 │  │                 │              │ │
│  │ • set_user_info │  │ • get_metadata_ │  │ • is_loan_info_ │              │ │
│  │ • get_user_info │  │   value()       │  │   complete()    │              │ │
│  │ • set_objective │  │ • update_session│  │ • reset_loan_   │              │ │
│  │ • get_objective │  │   _metadata()   │  │   variables()   │              │ │
│  │ • set_reasons   │  │ • set_session_  │  │ • add_reason()  │              │ │
│  │ • get_reasons   │  │   metadata()    │  │ • remove_reason │              │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📊 Tipos de Metadatos**

#### **1. Metadatos Básicos**
- **`user_info`**: Información del usuario (nombre, edad, preferencias, etc.)
- **`conversation_objective`**: Objetivo principal de la conversación
- **`conversation_state`**: Estado actual de la conversación (tópico, progreso, etc.)

#### **2. Metadatos Extendidos**
- **`welcome_done`**: Control del flujo de bienvenida (boolean)
- **`reasons`**: Lista de motivos/razones de la conversación (array de strings)
- **`reasons_confirmed`**: Confirmación de los motivos (boolean)
- **`vars_info_given`**: Estado de información de variables (boolean)
- **`vars`**: Variables específicas (monthly, duration, rate para préstamos)

### **🔧 Métodos de Gestión de Metadatos**

#### **Gestión de Información del Usuario**
```python
from src.memory.conversation_memory import create_memory

memory = create_memory("session_123")

# Establecer información del usuario
user_info = {
    "name": "Juan Pérez",
    "age": 25,
    "language": "español",
    "preferences": {
        "learning_style": "visual",
        "difficulty_level": "intermediate",
        "topics_of_interest": ["programación", "matemáticas"]
    }
}
memory.set_user_info(user_info)

# Obtener información del usuario
user_data = memory.get_user_info()
print(f"Usuario: {user_data['name']}")
```

#### **Gestión de Objetivo de Conversación**
```python
# Establecer objetivo
memory.set_conversation_objective("Ayudar al usuario a aprender Python")

# Obtener objetivo
objective = memory.get_conversation_objective()
print(f"Objetivo: {objective}")

# Actualizar objetivo
memory.update_conversation_objective("Ayudar con programación web")

# Limpiar objetivo
memory.clear_objective()
```

#### **Gestión de Estado de Conversación**
```python
# Establecer estado
conversation_state = {
    "current_topic": "variables en Python",
    "progress": {
        "completed_topics": ["introducción", "tipos de datos"],
        "current_lesson": "variables",
        "score": 85
    }
}
memory.set_conversation_state(conversation_state)

# Obtener estado
state = memory.get_conversation_state()
print(f"Tópico actual: {state['current_topic']}")

# Actualizar elemento específico
memory.update_conversation_state("progress.score", 90)
```

#### **Gestión de Flujo de Bienvenida**
```python
# Verificar si se mostró la bienvenida
if not memory.get_welcome_status():
    # Mostrar mensaje de bienvenida
    print("¡Bienvenido al sistema!")
    memory.set_welcome_status(True)
else:
    print("¡Hola de nuevo!")
```

#### **Gestión de Motivos**
```python
# Agregar motivos
memory.add_reason("Necesito ayuda con programación")
memory.add_reason("Quiero aprender Python")
memory.add_reason("Tengo un proyecto en mente")

# Obtener todos los motivos
reasons = memory.get_reasons()
print(f"Motivos: {reasons}")

# Confirmar motivos
memory.set_reasons_confirmed(True)

# Verificar confirmación
if memory.get_reasons_confirmed():
    print("Motivos confirmados, procediendo...")

# Remover motivo específico
memory.remove_reason("Tengo un proyecto en mente")
```

#### **Gestión de Variables Específicas**
```python
# Establecer variables de préstamo
memory.set_loan_variables(
    monthly=1500.0,
    duration=36,
    rate=5.5
)

# Obtener variables
vars_data = memory.get_vars()
print(f"Pago mensual: ${vars_data['monthly']}")

# Actualizar variable específica
memory.update_var("monthly", 2000.0)

# Obtener variable específica
monthly = memory.get_var("monthly")
print(f"Nuevo pago mensual: ${monthly}")

# Verificar si la información está completa
if memory.is_loan_info_complete():
    print("Información de préstamo completa")
else:
    print("Falta información del préstamo")

# Marcar que se proporcionó información
memory.set_vars_info_given(True)

# Resetear variables
memory.reset_loan_variables()
```

#### **Acceso Genérico a Metadatos**
```python
# Acceso con notación de punto para estructuras anidadas
user_name = memory.get_metadata_value("user_info.name")
learning_style = memory.get_metadata_value("user_info.preferences.learning_style")
current_topic = memory.get_metadata_value("conversation_state.current_topic")

# Con valores por defecto
non_existent = memory.get_metadata_value("non.existent.key", "valor_por_defecto")

# Actualizar metadatos específicos
memory.update_session_metadata("user_info.age", 26)

# Establecer metadatos completos
all_metadata = {
    "user_info": {"name": "María", "age": 30},
    "conversation_objective": "Aprender JavaScript",
    "welcome_done": True,
    "reasons": ["Desarrollo web", "Carrera profesional"]
}
memory.set_session_metadata(all_metadata)
```

### **🎯 Casos de Uso Prácticos**

#### **1. Asistente de Préstamos**
```python
class LoanAssistant:
    def __init__(self, session_id: str):
        self.memory = create_memory(session_id)
    
    def start_conversation(self) -> str:
        if not self.memory.get_welcome_status():
            self.memory.set_welcome_status(True)
            return "¡Hola! Soy tu asistente de préstamos. ¿Por qué necesitas un préstamo?"
        return "¡Hola de nuevo! ¿En qué puedo ayudarte?"
    
    def process_reason(self, user_message: str) -> str:
        self.memory.add_reason(user_message)
        reasons = self.memory.get_reasons()
        
        if len(reasons) == 1:
            return f"Entiendo, necesitas un préstamo para: {user_message}\n¿Hay otra razón?"
        else:
            return f"Perfecto, tus motivos son:\n" + "\n".join([f"• {r}" for r in reasons])
    
    def collect_variables(self, user_message: str) -> str:
        # Parsear mensaje para extraer variables
        # ... lógica de parsing ...
        
        self.memory.set_loan_variables(monthly=1500, duration=36, rate=5.5)
        
        if self.memory.is_loan_info_complete():
            return self.calculate_loan()
        else:
            return "Aún necesito más información..."
```

#### **2. Asistente Educativo Personalizado**
```python
class EducationalAssistant:
    def __init__(self, session_id: str):
        self.memory = create_memory(session_id)
    
    def personalize_response(self, message: str) -> str:
        user_info = self.memory.get_user_info()
        objective = self.memory.get_conversation_objective()
        state = self.memory.get_conversation_state()
        
        # Personalizar respuesta basada en metadatos
        if user_info.get("preferences", {}).get("learning_style") == "visual":
            return f"Te ayudo con {message} usando ejemplos visuales..."
        elif user_info.get("preferences", {}).get("learning_style") == "practical":
            return f"Te ayudo con {message} con ejercicios prácticos..."
        else:
            return f"Te ayudo con {message} de forma general..."
    
    def update_progress(self, topic: str, score: int):
        self.memory.update_conversation_state("current_topic", topic)
        self.memory.update_conversation_state("progress.score", score)
```

### **🔍 Monitoreo y Debugging**

#### **Verificar Estado de Metadatos**
```python
# Obtener todos los metadatos
all_metadata = memory.get_session_metadata()
print(json.dumps(all_metadata, indent=2, ensure_ascii=False))

# Verificar variables específicas
print(f"Welcome done: {memory.get_welcome_status()}")
print(f"Reasons confirmed: {memory.get_reasons_confirmed()}")
print(f"Vars info given: {memory.get_vars_info_given()}")
print(f"Loan complete: {memory.is_loan_info_complete()}")
```

#### **Persistencia de Metadatos**
```python
# Los metadatos persisten entre instancias de memoria
memory1 = create_memory("session_123")
memory1.set_user_info({"name": "Juan"})

memory2 = create_memory("session_123")  # Misma sesión
user_info = memory2.get_user_info()
print(f"Usuario: {user_info['name']}")  # Imprime: "Usuario: Juan"
```

### **🧪 Testing de Metadatos**

#### **Ejecutar Tests Completos**
```bash
# Test de funcionalidad básica
python test_metadata_functionality.py

# Test de metadatos extendidos
python test_extended_metadata.py

# Ejemplo de flujo completo
python example_complete_flow.py
```

#### **Test de Persistencia**
```python
import uuid
from src.memory.conversation_memory import create_memory

# Crear memoria y establecer datos
session_id = str(uuid.uuid4())
memory1 = create_memory(session_id)
memory1.set_welcome_status(True)
memory1.add_reason("Test reason")
memory1.set_loan_variables(monthly=1000, duration=24, rate=3.5)

# Crear nueva instancia con misma sesión
memory2 = create_memory(session_id)

# Verificar persistencia
assert memory2.get_welcome_status() == True
assert "Test reason" in memory2.get_reasons()
assert memory2.get_var("monthly") == 1000
print("✅ Persistencia verificada")
```

### **📈 Beneficios del Sistema de Metadatos**

1. **Contexto Rico**: Los agentes tienen acceso a información detallada del usuario y la conversación
2. **Personalización**: Respuestas adaptadas al perfil y preferencias del usuario
3. **Control de Flujo**: Gestión de estados de conversación y progreso
4. **Persistencia**: Información que sobrevive entre sesiones
5. **Flexibilidad**: Estructura JSON permite cualquier tipo de metadatos
6. **Escalabilidad**: Fácil agregar nuevos tipos de metadatos
7. **Debugging**: Fácil monitoreo y verificación del estado del sistema

### **🔗 Integración con Agentes**

Los agentes pueden acceder a los metadatos a través de la memoria:

```python
def process_with_context(self, message: str, memory):
    # Obtener contexto
    user_info = memory.get_user_info()
    objective = memory.get_conversation_objective()
    state = memory.get_conversation_state()
    
    # Personalizar procesamiento
    if user_info.get("preferences", {}).get("learning_style") == "visual":
        # Usar prompts con ejemplos visuales
        pass
    elif objective == "préstamo":
        # Usar lógica específica para préstamos
        pass
    
    # Actualizar estado
    memory.update_conversation_state("last_interaction", datetime.now().isoformat())
```

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

### **🎨 Mejoras de Formato y Legibilidad:**

El sistema ahora genera respuestas **mucho más legibles y estructuradas**:

#### **📝 Estructura Mejorada:**
- **Títulos principales** con emojis descriptivos
- **Secciones organizadas** con subtítulos claros
- **Listas con viñetas** para enumeraciones simples
- **Listas numeradas** para pasos o secuencias
- **Separadores visuales** entre secciones importantes

#### **🔤 Formato de Texto:**
- **Negritas** para conceptos importantes
- *Cursivas* para énfasis
- `Código` para términos técnicos
- **Emojis** para hacer las respuestas más amigables

#### **🎯 Tipos de Respuesta Específicos:**

**Para Preguntas:**
```
# 🎯 Respuesta Directa
[Respuesta clara y concisa]

## 📚 Explicación Detallada
[Información adicional organizada]

## 💡 Información Adicional
[Contexto, ejemplos, etc.]
```

**Para Cálculos:**
```
# 🧮 Resultado del Cálculo
**Resultado:** [número/valor]

## 📊 Proceso Detallado
1. Paso 1
2. Paso 2
3. Paso 3

## 💡 Explicación
[Contexto del resultado]
```

**Para Explicaciones:**
```
# 📖 [Tema Principal]
[Explicación estructurada]

## 🔍 Puntos Clave
• Punto 1
• Punto 2
• Punto 3

## 🧠 **Sistema de Memoria Híbrida**

### **📋 Descripción General**

El sistema implementa una **memoria híbrida inteligente** que combina las mejores características de `ConversationBufferMemory` y `ConversationSummaryMemory` de LangChain, junto con un sistema de metadatos personalizado para máxima flexibilidad y eficiencia.

### **🏗️ Arquitectura de la Memoria Híbrida**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        HYBRID CONVERSATION MEMORY                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Buffer Memory │  │  Summary Memory │  │  Metadata Store │              │
│  │                 │  │                 │  │                 │              │
│  │ • Recent History│  │ • Long-term     │  │ • Session Info  │              │
│  │ • Fast Access   │  │   Context       │  │ • User Data     │              │
│  │ • Token Efficient│  │ • LLM Summaries │  │ • State Mgmt    │              │
│  │ • Real-time     │  │ • Token Savings │  │ • Persistence   │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    Automatic Mode Switching                            │ │
│  │                                                                         │ │
│  │  Short Conversations (< threshold) → Buffer Mode                       │ │
│  │  Long Conversations (≥ threshold) → Summary Mode                       │ │
│  │                                                                         │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **🎯 Características Principales**

#### **1. Modo Buffer (Conversaciones Cortas)**
- **Acceso rápido** a historial reciente
- **Bajo uso de tokens** para conversaciones cortas
- **Respuesta en tiempo real** sin procesamiento adicional
- **Ideal para**: Preguntas simples, cálculos rápidos, interacciones breves

#### **2. Modo Summary (Conversaciones Largas)**
- **Resúmenes automáticos** generados por LLM
- **Reducción significativa** de tokens (50-80%)
- **Contexto preservado** en conversaciones largas
- **Ideal para**: Conversaciones complejas, consultas detalladas, sesiones largas

#### **3. Metadatos Flexibles**
- **Información de sesión** personalizable
- **Estado de conversación** persistente
- **Datos de usuario** estructurados
- **Compatibilidad total** con el sistema existente

### **⚙️ Configuración y Uso**

#### **Creación de Memoria Híbrida**
```python
from src.memory.hybrid_conversation_memory import create_hybrid_memory

# Configuración básica
memory = create_hybrid_memory(
    session_id="user_123",
    buffer_window=10,        # Mensajes recientes a mantener
    summary_threshold=15,    # Umbral para cambiar a summary
    verbose=True             # Logging detallado
)
```

#### **Configuración Avanzada**
```python
# Configuración personalizada
memory = create_hybrid_memory(
    session_id="user_123",
    buffer_window=5,         # Buffer más pequeño
    summary_threshold=8,     # Cambio más temprano a summary
    verbose=True
)

# Configuración para conversaciones largas
memory = create_hybrid_memory(
    session_id="user_123",
    buffer_window=20,        # Buffer más grande
    summary_threshold=25,    # Cambio más tardío
    verbose=False
)
```

### **🔄 Funcionamiento Automático**

#### **Carga de Variables de Memoria**
```python
# El sistema decide automáticamente qué modo usar
vars = memory.load_memory_variables({})

if memory._should_use_summary():
    # Modo Summary: resumen + historial reciente
    recent_history = vars.get('recent_history', [])
    conversation_summary = vars.get('conversation_summary', '')
    session_metadata = vars.get('session_metadata', {})
else:
    # Modo Buffer: solo historial reciente
    recent_history = vars.get('recent_history', [])
    conversation_summary = ''
    session_metadata = vars.get('session_metadata', {})
```

#### **Guardado de Contexto**
```python
# Guarda automáticamente en ambos sistemas
memory.save_context(
    {"message": "Hola, ¿cómo estás?"},
    {"response": "¡Hola! Estoy muy bien, gracias."}
)

# Actualiza contador de conversación
# Decide si usar summary basado en threshold
# Persiste en SQLite
```

### **📊 Monitoreo y Estadísticas**

#### **Estadísticas de Memoria**
```python
stats = memory.get_memory_stats()
print(f"Session ID: {stats['session_id']}")
print(f"Conversation Length: {stats['conversation_length']}")
print(f"Using Summary: {stats['using_summary']}")
print(f"Buffer Window: {stats['buffer_window']}")
print(f"Summary Threshold: {stats['summary_threshold']}")
```

#### **Historial de Conversación**
```python
from src.memory.hybrid_conversation_memory import get_hybrid_conversation_history

history = get_hybrid_conversation_history(
    session_id="user_123",
    limit=10,
    include_summary=True
)

print(f"Recent Messages: {len(history['recent_messages'])}")
print(f"Summary: {history['conversation_summary']}")
print(f"Total Messages: {history['total_messages']}")
```

### **🧪 Pruebas y Validación**

#### **Pruebas Básicas**
```bash
# Probar funcionalidad básica
python test_hybrid_memory.py

# Probar integración con cadenas
python example_hybrid_chain_integration.py
```

#### **Pruebas Específicas**
```python
# Probar modo buffer
def test_buffer_mode():
    memory = create_hybrid_memory(session_id="test", summary_threshold=5)
    # Agregar < 5 mensajes
    # Verificar que usa buffer mode

# Probar modo summary
def test_summary_mode():
    memory = create_hybrid_memory(session_id="test", summary_threshold=3)
    # Agregar ≥ 3 mensajes
    # Verificar que usa summary mode
```

### **📈 Beneficios y Ventajas**

#### **Eficiencia de Tokens**
- **Conversaciones cortas**: Sin overhead de resúmenes
- **Conversaciones largas**: Reducción de 50-80% en tokens
- **Escalabilidad**: Manejo eficiente de sesiones largas

#### **Rendimiento**
- **Respuestas más rápidas** en conversaciones cortas
- **Contexto preservado** en conversaciones largas
- **Uso optimizado** de recursos del LLM

#### **Flexibilidad**
- **Configuración adaptable** según necesidades
- **Compatibilidad total** con sistema existente
- **Metadatos personalizables** para casos específicos

#### **Persistencia**
- **Datos persistentes** en SQLite
- **Recuperación de sesiones** entre reinicios
- **Backup y restauración** simplificados

### **🔧 Integración con Cadenas Existentes**

#### **Uso en CompleteChain**
```python
from src.chains.complete_chain import create_complete_chain
from src.memory.hybrid_conversation_memory import create_hybrid_memory

# Crear cadena con memoria híbrida
chain = create_complete_chain(verbose=True)
memory = create_hybrid_memory(session_id="user_123", verbose=True)

# Procesar mensaje
input_data = {
    "message": "Hola, necesito ayuda",
    "session_id": "user_123",
    "request_id": str(uuid.uuid4())
}

result = chain.invoke(input_data)
```

#### **Compatibilidad con Agentes**
```python
# Los agentes pueden acceder a memoria híbrida
curator_input = {
    "message": message,
    "chat_history": memory.load_memory_variables({}),
    "request_id": request_id
}

curator_result = curator_agent.invoke(curator_input)
```

### **🚀 Casos de Uso Prácticos**

#### **1. Asistente de Préstamos**
```python
# Configuración para conversaciones largas
memory = create_hybrid_memory(
    session_id="loan_user_123",
    buffer_window=10,
    summary_threshold=8,
    verbose=True
)

# Metadatos específicos del dominio
memory.set_welcome_status(True)
memory.add_reason("Solicitud de préstamo hipotecario")
memory.set_loan_variables(monthly=1500, duration=30, rate=4.5)
```

#### **2. Asistente Educativo**
```python
# Configuración para sesiones de estudio
memory = create_hybrid_memory(
    session_id="student_456",
    buffer_window=15,
    summary_threshold=12,
    verbose=False
)

# Metadatos educativos
memory.update_session_metadata("subject", "mathematics")
memory.update_session_metadata("difficulty", "intermediate")
memory.update_session_metadata("session_type", "tutoring")
```

### **📝 Resumen**
```

#### **✅ Beneficios de las Mejoras:**
- **Más fácil de leer** y entender
- **Información mejor organizada** y estructurada
- **Elementos visuales** que facilitan la comprensión
- **Información destacada** cuando es importante
- **Estructura lógica** que sigue un flujo natural
- **Respuestas profesionales** pero amigables

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