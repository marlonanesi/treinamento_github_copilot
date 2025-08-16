"""
Middleware para tratamento de exceções HTTP.

Este módulo implementa handlers customizados para diferentes tipos
de exceções, convertendo-as em respostas HTTP estruturadas.
"""

import logging
from typing import Union
from datetime import datetime

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.application.exceptions import (
    ApplicationException,
    ValidationException,
    BusinessRuleException,
    ResourceNotFoundException,
    DuplicateResourceException,
    UnauthorizedOperationException
)
from app.presentation.schemas import ErrorResponseSchema, ValidationErrorSchema


logger = logging.getLogger(__name__)


# ==========================================
# HANDLERS DE EXCEÇÕES DE DOMÍNIO
# ==========================================

async def application_exception_handler(
    request: Request, 
    exc: ApplicationException
) -> JSONResponse:
    """
    Trata exceções gerais da camada de aplicação.
    
    Args:
        request: Requisição HTTP
        exc: Exceção da aplicação
        
    Returns:
        Resposta JSON estruturada
    """
    logger.error(f"Application exception: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "exception_message": str(exc)
    })
    
    error_response = ErrorResponseSchema(
        success=False,
        message="Erro na aplicação",
        error={
            "type": "ApplicationError",
            "message": str(exc),
            "code": getattr(exc, 'error_code', 'INTERNAL_ERROR')
        },
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


async def validation_exception_handler(
    request: Request, 
    exc: ValidationException
) -> JSONResponse:
    """
    Trata exceções de validação da aplicação.
    
    Args:
        request: Requisição HTTP
        exc: Exceção de validação
        
    Returns:
        Resposta JSON com detalhes de validação
    """
    logger.warning(f"Validation exception: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "validation_errors": getattr(exc, 'errors', [])
    })
    
    validation_error = ValidationErrorSchema(
        type="ValidationError",
        message="Erro na validação dos dados fornecidos",
        details=getattr(exc, 'errors', []),
        total_errors=len(getattr(exc, 'errors', []))
    )
    
    error_response = ErrorResponseSchema(
        success=False,
        message="Dados inválidos fornecidos",
        error=validation_error,
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


async def business_rule_exception_handler(
    request: Request, 
    exc: BusinessRuleException
) -> JSONResponse:
    """
    Trata exceções de regras de negócio.
    
    Args:
        request: Requisição HTTP
        exc: Exceção de regra de negócio
        
    Returns:
        Resposta JSON com detalhes da regra violada
    """
    logger.warning(f"Business rule exception: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "business_rule": getattr(exc, 'rule', 'unknown')
    })
    
    error_response = ErrorResponseSchema(
        success=False,
        message="Regra de negócio violada",
        error={
            "type": "BusinessRuleError",
            "message": str(exc),
            "rule": getattr(exc, 'rule', 'unknown'),
            "code": getattr(exc, 'error_code', 'BUSINESS_RULE_VIOLATION')
        },
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response.model_dump()
    )


async def resource_not_found_exception_handler(
    request: Request, 
    exc: ResourceNotFoundException
) -> JSONResponse:
    """
    Trata exceções de recurso não encontrado.
    
    Args:
        request: Requisição HTTP
        exc: Exceção de recurso não encontrado
        
    Returns:
        Resposta JSON indicando recurso não encontrado
    """
    logger.info(f"Resource not found: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "resource_id": getattr(exc, 'resource_id', 'unknown')
    })
    
    error_response = ErrorResponseSchema(
        success=False,
        message="Recurso não encontrado",
        error={
            "type": "NotFoundError",
            "message": str(exc),
            "resource": getattr(exc, 'resource_type', 'unknown'),
            "resource_id": getattr(exc, 'resource_id', 'unknown'),
            "code": "RESOURCE_NOT_FOUND"
        },
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_response.model_dump()
    )


async def duplicate_resource_exception_handler(
    request: Request, 
    exc: DuplicateResourceException
) -> JSONResponse:
    """
    Trata exceções de recurso duplicado.
    
    Args:
        request: Requisição HTTP
        exc: Exceção de recurso duplicado
        
    Returns:
        Resposta JSON indicando conflito de recurso
    """
    logger.warning(f"Duplicate resource: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "duplicate_field": getattr(exc, 'field', 'unknown'),
        "duplicate_value": getattr(exc, 'value', 'unknown')
    })
    
    error_response = ErrorResponseSchema(
        success=False,
        message="Recurso já existe",
        error={
            "type": "ConflictError",
            "message": str(exc),
            "field": getattr(exc, 'field', 'unknown'),
            "value": getattr(exc, 'value', 'unknown'),
            "code": "DUPLICATE_RESOURCE"
        },
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_response.model_dump()
    )


async def unauthorized_operation_exception_handler(
    request: Request, 
    exc: UnauthorizedOperationException
) -> JSONResponse:
    """
    Trata exceções de operação não autorizada.
    
    Args:
        request: Requisição HTTP
        exc: Exceção de operação não autorizada
        
    Returns:
        Resposta JSON indicando operação não autorizada
    """
    logger.warning(f"Unauthorized operation: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "operation": getattr(exc, 'operation', 'unknown')
    })
    
    error_response = ErrorResponseSchema(
        success=False,
        message="Operação não autorizada",
        error={
            "type": "UnauthorizedError",
            "message": str(exc),
            "operation": getattr(exc, 'operation', 'unknown'),
            "code": "UNAUTHORIZED_OPERATION"
        },
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=error_response.model_dump()
    )


# ==========================================
# HANDLERS DE EXCEÇÕES HTTP
# ==========================================

async def http_exception_handler(
    request: Request, 
    exc: HTTPException
) -> JSONResponse:
    """
    Trata exceções HTTP do FastAPI.
    
    Args:
        request: Requisição HTTP
        exc: Exceção HTTP
        
    Returns:
        Resposta JSON estruturada
    """
    logger.info(f"HTTP exception: {exc.status_code} - {exc.detail}", extra={
        "status_code": exc.status_code,
        "path": request.url.path,
        "method": request.method,
        "detail": exc.detail
    })
    
    # Se o detalhe já é um dict estruturado, usar como está
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    
    # Caso contrário, estruturar a resposta
    error_response = ErrorResponseSchema(
        success=False,
        message="Erro HTTP",
        error={
            "type": "HTTPError",
            "message": str(exc.detail),
            "status_code": exc.status_code,
            "code": f"HTTP_{exc.status_code}"
        },
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


# ==========================================
# HANDLERS DE EXCEÇÕES PYDANTIC
# ==========================================

async def pydantic_validation_exception_handler(
    request: Request, 
    exc: ValidationError
) -> JSONResponse:
    """
    Trata erros de validação do Pydantic.
    
    Args:
        request: Requisição HTTP
        exc: Erro de validação do Pydantic
        
    Returns:
        Resposta JSON com detalhes de validação
    """
    logger.warning(f"Pydantic validation error: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "validation_errors": exc.errors()
    })
    
    # Converter erros do Pydantic para formato da aplicação
    formatted_errors = []
    for error in exc.errors():
        field_path = ".".join(str(loc) for loc in error["loc"])
        formatted_errors.append({
            "field": field_path,
            "message": error["msg"],
            "type": error["type"],
            "value": error.get("input")
        })
    
    validation_error = ValidationErrorSchema(
        type="ValidationError",
        message="Erro na validação dos dados da requisição",
        details=formatted_errors,
        total_errors=len(formatted_errors)
    )
    
    error_response = ErrorResponseSchema(
        success=False,
        message="Dados da requisição inválidos",
        error=validation_error,
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


# ==========================================
# HANDLERS DE EXCEÇÕES DE BANCO
# ==========================================

async def mongodb_exception_handler(
    request: Request, 
    exc: Exception
) -> JSONResponse:
    """
    Trata exceções específicas do MongoDB.
    
    Args:
        request: Requisição HTTP
        exc: Exceção do MongoDB
        
    Returns:
        Resposta JSON indicando erro de banco
    """
    logger.error(f"MongoDB exception: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "mongodb_error": str(exc)
    })
    
    # Mapear tipos específicos de erro do MongoDB
    error_message = "Erro no banco de dados"
    error_code = "DATABASE_ERROR"
    
    if "duplicate key" in str(exc).lower():
        error_message = "Dados duplicados - registro já existe"
        error_code = "DUPLICATE_KEY"
    elif "connection" in str(exc).lower():
        error_message = "Erro de conexão com o banco de dados"
        error_code = "CONNECTION_ERROR"
    elif "timeout" in str(exc).lower():
        error_message = "Timeout na operação do banco de dados"
        error_code = "TIMEOUT_ERROR"
    
    error_response = ErrorResponseSchema(
        success=False,
        message=error_message,
        error={
            "type": "DatabaseError",
            "message": error_message,
            "code": error_code,
            "database": "MongoDB"
        },
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


# ==========================================
# HANDLER GENÉRICO
# ==========================================

async def generic_exception_handler(
    request: Request, 
    exc: Exception
) -> JSONResponse:
    """
    Handler genérico para exceções não tratadas.
    
    Args:
        request: Requisição HTTP
        exc: Exceção não tratada
        
    Returns:
        Resposta JSON genérica de erro interno
    """
    logger.error(f"Unhandled exception: {str(exc)}", extra={
        "exception_type": type(exc).__name__,
        "path": request.url.path,
        "method": request.method,
        "exception_message": str(exc)
    }, exc_info=True)
    
    error_response = ErrorResponseSchema(
        success=False,
        message="Erro interno do servidor",
        error={
            "type": "InternalServerError",
            "message": "Ocorreu um erro inesperado. Tente novamente mais tarde.",
            "code": "INTERNAL_SERVER_ERROR"
        },
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


# ==========================================
# MAPEAMENTO DE EXCEÇÕES
# ==========================================

def get_exception_handlers():
    """
    Retorna mapeamento de exceções para handlers.
    
    Returns:
        Dict com mapeamento de exceções
    """
    return {
        # Exceções de domínio/aplicação
        ApplicationException: application_exception_handler,
        ValidationException: validation_exception_handler,
        BusinessRuleException: business_rule_exception_handler,
        ResourceNotFoundException: resource_not_found_exception_handler,
        DuplicateResourceException: duplicate_resource_exception_handler,
        UnauthorizedOperationException: unauthorized_operation_exception_handler,
        
        # Exceções HTTP
        HTTPException: http_exception_handler,
        
        # Exceções Pydantic
        ValidationError: pydantic_validation_exception_handler,
        
        # Handler genérico (deve ser o último)
        Exception: generic_exception_handler
    }


# ==========================================
# UTILITÁRIOS DE LOGGING
# ==========================================

def setup_exception_logging():
    """
    Configura logging específico para exceções.
    """
    # Configurar logger específico para exceções
    exception_logger = logging.getLogger("app.exceptions")
    exception_logger.setLevel(logging.INFO)
    
    # TODO: Adicionar handlers específicos se necessário
    
    return exception_logger


def log_exception_context(
    request: Request,
    exc: Exception,
    additional_context: dict = None
):
    """
    Loga contexto detalhado da exceção.
    
    Args:
        request: Requisição HTTP
        exc: Exceção ocorrida
        additional_context: Contexto adicional
    """
    context = {
        "path": request.url.path,
        "method": request.method,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if additional_context:
        context.update(additional_context)
    
    logger.error("Exception context", extra=context, exc_info=True)


# ==========================================
# MIDDLEWARE DE EXCEÇÕES
# ==========================================

class ExceptionHandlingMiddleware:
    """
    Middleware para captura e processamento de exceções.
    
    Captura exceções não tratadas e garante resposta estruturada.
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        """
        Processa requisição através do middleware.
        
        Args:
            scope: Escopo ASGI
            receive: Callable para receber mensagens
            send: Callable para enviar mensagens
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            # Log da exceção não tratada
            logger.error(f"Unhandled exception in middleware: {str(exc)}", exc_info=True)
            
            # Enviar resposta de erro
            error_response = ErrorResponseSchema(
                success=False,
                message="Erro interno do servidor",
                error={
                    "type": "InternalServerError",
                    "message": "Erro inesperado no processamento da requisição",
                    "code": "MIDDLEWARE_ERROR"
                },
                timestamp=datetime.utcnow()
            )
            
            response_body = error_response.model_dump_json().encode()
            
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [
                    [b"content-type", b"application/json"],
                    [b"content-length", str(len(response_body)).encode()]
                ]
            })
            
            await send({
                "type": "http.response.body",
                "body": response_body
            })
