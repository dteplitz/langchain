"""
Main FastAPI application for the LangChain project.

This module contains the FastAPI app with endpoints, middleware,
and error handling for the chat system.
"""

import uuid
import time
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.models import ChatRequest, ChatResponse, ErrorResponse, HealthResponse
from src.chains.complete_chain import create_complete_chain
from src.config import get_settings
from src.utils.logger import get_logger


# Global variables
chain = None
logger = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the FastAPI application.
    """
    # Startup
    global chain, logger
    logger = get_logger()
    chain = create_complete_chain(verbose=get_settings().debug)
    logger.logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.logger.info("Application shutting down")


# Create FastAPI app
app = FastAPI(
    title="LangChain Chat API",
    description="A LangChain-based chat system with intelligent agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add processing time header and request logging.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint function
        
    Returns:
        Response: FastAPI response with processing time header
    """
    start_time = time.time()
    
    # Generate request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Log request
    logger.log_request(
        request_id=request_id,
        message=f"{request.method} {request.url.path}",
        agent="api",
        metadata={
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )
    
    # Process request
    response = await call_next(request)
    
    # Add processing time header
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: FastAPI request object
        exc: Exception that occurred
        
    Returns:
        JSONResponse: Error response with details
    """
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    # Log the error
    logger.log_error(
        request_id=request_id,
        error=exc,
        agent="api",
        context={
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )
    
    # Return error response
    error_response = ErrorResponse(
        error=str(exc),
        error_type=type(exc).__name__,
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


@app.get("/", response_model=HealthResponse)
async def root():
    """
    Root endpoint with health check information.
    
    Returns:
        HealthResponse: Health status and version information
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Health status and version information
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for processing user messages.
    
    This endpoint processes user messages through the LangChain system
    and returns a response with metadata.
    
    Args:
        request: ChatRequest containing the user message and options
        
    Returns:
        ChatResponse: Processed response with metadata
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Prepare input for the chain
        chain_input = {
            "message": request.message,
            "session_id": request.session_id or str(uuid.uuid4()),
            "request_id": request_id,
            "debug": request.debug
        }
        
        # Process through the chain
        result = chain.invoke(chain_input)
        
        # Create response
        response = ChatResponse(
            response=result["response"],
            session_id=result["session_id"],
            request_id=result["request_id"],
            processing_time=result["processing_time"],
            metadata=result["metadata"]
        )
        
        return response
        
    except Exception as e:
        # Log error
        logger.log_error(
            request_id=request_id,
            error=e,
            agent="chat_endpoint",
            context={"request": request.dict()}
        )
        
        # Raise HTTP exception
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 