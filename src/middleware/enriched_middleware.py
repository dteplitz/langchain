"""
Enriched middleware for enhanced logging and error handling.

This module provides middleware that enriches requests with
detailed logging and comprehensive error handling.
"""

import time
import uuid
import json
from typing import Dict, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import JSONResponse

from src.utils.enhanced_logger import get_enhanced_logger
from src.models.api_models import ErrorResponse


class EnrichedLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for enriched request/response logging.
    
    This middleware provides detailed logging of all requests
    and responses with performance metrics and error tracking.
    """
    
    def __init__(self, app, log_requests: bool = True, log_responses: bool = True):
        """
        Initialize the enriched logging middleware.
        
        Args:
            app: FastAPI application
            log_requests: Whether to log requests
            log_responses: Whether to log responses
        """
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.logger = get_enhanced_logger()
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Process the request through the middleware.
        
        Args:
            request: Incoming request
            call_next: Next middleware/endpoint
            
        Returns:
            Response: Processed response
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Add request ID to request state
        request.state.request_id = request_id
        request.state.start_time = start_time
        
        # Log request
        if self.log_requests:
            await self._log_request(request, request_id)
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Processing-Time"] = str(processing_time)
            
            # Log response
            if self.log_responses:
                await self._log_response(request, response, request_id, processing_time)
            
            return response
            
        except Exception as e:
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Log error
            await self._log_error(request, e, request_id, processing_time)
            
            # Return error response
            error_response = ErrorResponse(
                error="Internal Server Error",
                message=str(e),
                request_id=request_id,
                processing_time=processing_time
            )
            
            return JSONResponse(
                status_code=500,
                content=error_response.dict(),
                headers={"X-Request-ID": request_id, "X-Processing-Time": str(processing_time)}
            )
    
    async def _log_request(self, request: Request, request_id: str):
        """Log incoming request details."""
        # Extract request information
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Log request details
        self.logger.logger.info(f"[MIDDLEWARE] Request started: {method} {url}")
        self.logger.logger.info(f"[MIDDLEWARE] Request ID: {request_id}")
        self.logger.logger.info(f"[MIDDLEWARE] Client IP: {client_ip}")
        self.logger.logger.info(f"[MIDDLEWARE] User Agent: {user_agent[:100]}...")
        
        # Log headers (excluding sensitive ones)
        safe_headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in ['authorization', 'cookie', 'x-api-key']
        }
        self.logger.logger.debug(f"[MIDDLEWARE] Headers: {json.dumps(dict(safe_headers), indent=2)}")
    
    async def _log_response(self, request: Request, response: Response, request_id: str, processing_time: float):
        """Log response details."""
        method = request.method
        url = str(request.url)
        status_code = response.status_code
        
        # Log response details
        self.logger.logger.info(f"[MIDDLEWARE] Response completed: {method} {url} -> {status_code}")
        self.logger.logger.info(f"[MIDDLEWARE] Request ID: {request_id}")
        self.logger.logger.info(f"[MIDDLEWARE] Processing time: {processing_time:.3f}s")
        
        # Log response headers
        response_headers = dict(response.headers)
        self.logger.logger.debug(f"[MIDDLEWARE] Response headers: {json.dumps(response_headers, indent=2)}")
        
        # Log response body for chat endpoint
        if "/chat" in url and status_code == 200:
            try:
                # Try to get response body (this might not work for streaming responses)
                if hasattr(response, 'body'):
                    body = response.body.decode('utf-8')
                    if len(body) < 1000:  # Only log if not too long
                        self.logger.logger.debug(f"[MIDDLEWARE] Response body: {body}")
            except Exception:
                pass  # Ignore if we can't read the body
    
    async def _log_error(self, request: Request, error: Exception, request_id: str, processing_time: float):
        """Log error details."""
        method = request.method
        url = str(request.url)
        error_type = type(error).__name__
        error_message = str(error)
        
        # Log error details
        self.logger.logger.error(f"[MIDDLEWARE] Error occurred: {method} {url}")
        self.logger.logger.error(f"[MIDDLEWARE] Request ID: {request_id}")
        self.logger.logger.error(f"[MIDDLEWARE] Error type: {error_type}")
        self.logger.logger.error(f"[MIDDLEWARE] Error message: {error_message}")
        self.logger.logger.error(f"[MIDDLEWARE] Processing time: {processing_time:.3f}s")
        
        # Log request context
        self.logger.logger.error(f"[MIDDLEWARE] Request context: {json.dumps({
            'method': method,
            'url': url,
            'client_ip': request.client.host if request.client else "unknown",
            'user_agent': request.headers.get("user-agent", "unknown")
        }, indent=2)}")


class PerformanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware for performance monitoring.
    
    This middleware tracks performance metrics and provides
    alerts for slow requests.
    """
    
    def __init__(self, app, slow_request_threshold: float = 5.0):
        """
        Initialize the performance middleware.
        
        Args:
            app: FastAPI application
            slow_request_threshold: Threshold for slow requests (seconds)
        """
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
        self.logger = get_enhanced_logger()
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Process the request through the performance middleware.
        
        Args:
            request: Incoming request
            call_next: Next middleware/endpoint
            
        Returns:
            Response: Processed response
        """
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Check for slow requests
        if processing_time > self.slow_request_threshold:
            self.logger.logger.warning(
                f"[PERFORMANCE] Slow request detected: {request.method} {request.url} "
                f"took {processing_time:.3f}s (threshold: {self.slow_request_threshold}s)"
            )
        
        # Add performance headers
        response.headers["X-Processing-Time"] = str(processing_time)
        response.headers["X-Performance-Warning"] = "slow" if processing_time > self.slow_request_threshold else "normal"
        
        return response


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware for security enhancements.
    
    This middleware adds security headers and validates requests.
    """
    
    def __init__(self, app):
        """
        Initialize the security middleware.
        
        Args:
            app: FastAPI application
        """
        super().__init__(app)
        self.logger = get_enhanced_logger()
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Process the request through the security middleware.
        
        Args:
            request: Incoming request
            call_next: Next middleware/endpoint
            
        Returns:
            Response: Processed response
        """
        # Add security headers
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Content Security Policy - Allow Swagger resources
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'"
        )
        response.headers["Content-Security-Policy"] = csp_policy
        
        return response


def create_middleware_stack(app):
    """
    Create the complete middleware stack.
    
    Args:
        app: FastAPI application
        
    Returns:
        FastAPI: Application with middleware stack
    """
    # Add middleware in order (last added is executed first)
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(PerformanceMiddleware, slow_request_threshold=5.0)
    app.add_middleware(EnrichedLoggingMiddleware, log_requests=True, log_responses=True)
    
    return app 