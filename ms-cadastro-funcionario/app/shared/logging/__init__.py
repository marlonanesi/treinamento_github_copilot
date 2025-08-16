"""
Sistema de logging compartilhado.

Exporta funcionalidades de logging estruturado para uso
em toda a aplicação.
"""

from .logger import (
    setup_logging,
    get_logger,
    create_request_logger,
    LoggerAdapter,
    JSONFormatter,
    StructuredFormatter
)

__all__ = [
    "setup_logging",
    "get_logger", 
    "create_request_logger",
    "LoggerAdapter",
    "JSONFormatter",
    "StructuredFormatter"
]
