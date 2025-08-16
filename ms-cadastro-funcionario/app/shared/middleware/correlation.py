"""
Middleware de correlação para rastreamento de requisições.

Adiciona IDs únicos para cada requisição facilitando
o debugging e observabilidade da aplicação.
"""

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared.logging import get_logger

logger = get_logger(__name__)


class CorrelationMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar correlation ID às requisições.
    
    Gera ou propaga correlation ID através das chamadas,
    facilitando o rastreamento de requisições distribuídas.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processa requisição adicionando correlation ID.
        
        Args:
            request: Requisição HTTP
            call_next: Próximo handler da cadeia
            
        Returns:
            Response: Resposta com headers de correlação
        """
        # Obter ou gerar correlation ID
        correlation_id = request.headers.get(
            'X-Correlation-ID',
            str(uuid.uuid4())
        )
        
        # Gerar request ID único
        request_id = str(uuid.uuid4())
        
        # Adicionar ao state da requisição
        request.state.correlation_id = correlation_id
        request.state.request_id = request_id
        
        # Log início da requisição
        logger.info(
            f"Iniciando requisição {request.method} {request.url.path}",
            extra={
                'correlation_id': correlation_id,
                'request_id': request_id,
                'method': request.method,
                'endpoint': request.url.path,
                'query_params': str(request.query_params),
                'user_agent': request.headers.get('User-Agent', 'Unknown')
            }
        )
        
        # Processar requisição
        response = await call_next(request)
        
        # Adicionar headers de correlação na resposta
        response.headers['X-Correlation-ID'] = correlation_id
        response.headers['X-Request-ID'] = request_id
        
        # Log fim da requisição
        logger.info(
            f"Requisição finalizada com status {response.status_code}",
            extra={
                'correlation_id': correlation_id,
                'request_id': request_id,
                'method': request.method,
                'endpoint': request.url.path,
                'status_code': response.status_code
            }
        )
        
        return response
