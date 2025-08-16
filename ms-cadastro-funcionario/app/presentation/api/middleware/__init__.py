"""
Middleware para FastAPI.

Este módulo centraliza todos os middlewares utilizados pela aplicação
incluindo tratamento de exceções, logging e métricas.
"""

from .exception_handler import (
    # Exception handlers
    application_exception_handler,
    validation_exception_handler,
    business_rule_exception_handler,
    resource_not_found_exception_handler,
    duplicate_resource_exception_handler,
    unauthorized_operation_exception_handler,
    http_exception_handler,
    pydantic_validation_exception_handler,
    mongodb_exception_handler,
    generic_exception_handler,
    
    # Utilities
    get_exception_handlers,
    setup_exception_logging,
    log_exception_context,
    ExceptionHandlingMiddleware
)

from .logging_middleware import (
    # Middleware classes
    LoggingMiddleware,
    PerformanceLoggingMiddleware,
    MetricsMiddleware,
    
    # Configuration
    setup_logging_middleware,
    create_logging_middleware
)

__all__ = [
    # Exception handlers
    "application_exception_handler",
    "validation_exception_handler",
    "business_rule_exception_handler", 
    "resource_not_found_exception_handler",
    "duplicate_resource_exception_handler",
    "unauthorized_operation_exception_handler",
    "http_exception_handler",
    "pydantic_validation_exception_handler",
    "mongodb_exception_handler",
    "generic_exception_handler",
    "get_exception_handlers",
    "setup_exception_logging",
    "log_exception_context",
    "ExceptionHandlingMiddleware",
    
    # Logging middleware
    "LoggingMiddleware",
    "PerformanceLoggingMiddleware", 
    "MetricsMiddleware",
    "setup_logging_middleware",
    "create_logging_middleware"
]
