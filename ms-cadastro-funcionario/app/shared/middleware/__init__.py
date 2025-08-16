"""
Middleware compartilhado para toda a aplicação.
"""

from .correlation import CorrelationMiddleware

__all__ = [
    "CorrelationMiddleware"
]
