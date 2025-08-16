"""
Schemas para respostas padronizadas da API.

Este módulo define os schemas que padronizam as respostas da API,
incluindo respostas de sucesso, erro e validação.
"""

from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from datetime import datetime
from pydantic import Field

from .base import BaseSchema

# Type variable para tornar SuccessResponseSchema genérico
T = TypeVar('T')


class SuccessResponseSchema(BaseSchema, Generic[T]):
    """
    Schema para respostas de sucesso da API.
    
    Padroniza o formato de retorno para operações bem-sucedidas.
    """
    
    success: bool = Field(
        True, 
        description="Indica se a operação foi bem-sucedida",
        example=True
    )
    
    message: str = Field(
        ..., 
        description="Mensagem descritiva da operação realizada",
        example="Operação realizada com sucesso"
    )
    
    data: Optional[T] = Field(
        None, 
        description="Dados retornados pela operação",
        example={"id": "123", "nome": "João Silva"}
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da resposta",
        example="2024-01-15T10:30:00Z"
    )
    
    class Config:
        """Configuração do schema com exemplos para documentação."""
        json_schema_extra = {
            "examples": [
                {
                    "success": True,
                    "message": "Funcionário criado com sucesso",
                    "data": {
                        "id": "60d5ecb74b24c3b3d8f8e1a2",
                        "nome_completo": "João Silva Santos",
                        "email": "joao.santos@company.com",
                        "cargo": "Desenvolvedor Senior"
                    },
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            ]
        }


class ErrorResponseSchema(BaseSchema):
    """
    Schema para respostas de erro da API.
    
    Padroniza o formato de retorno para operações que resultaram em erro.
    """
    
    success: bool = Field(
        False, 
        description="Indica se a operação foi bem-sucedida",
        example=False
    )
    
    error: str = Field(
        ..., 
        description="Tipo ou código do erro ocorrido",
        example="VALIDATION_ERROR"
    )
    
    message: str = Field(
        ..., 
        description="Mensagem descritiva do erro",
        example="Os dados fornecidos são inválidos"
    )
    
    details: Optional[Dict[str, Any]] = Field(
        None, 
        description="Detalhes adicionais sobre o erro",
        example={"field": "email", "reason": "Email já existe no sistema"}
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do erro",
        example="2024-01-15T10:30:00Z"
    )
    
    path: Optional[str] = Field(
        None,
        description="Caminho da API onde o erro ocorreu",
        example="/api/v1/funcionarios"
    )
    
    class Config:
        """Configuração do schema com exemplos para documentação."""
        json_schema_extra = {
            "examples": [
                {
                    "success": False,
                    "error": "DUPLICATE_EMAIL",
                    "message": "Email já existe no sistema",
                    "details": {
                        "email": "joao.silva@company.com",
                        "field": "email"
                    },
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/v1/funcionarios"
                }
            ]
        }


class ValidationErrorDetailSchema(BaseSchema):
    """
    Schema para detalhes de erro de validação individual.
    """
    
    field: str = Field(
        ..., 
        description="Campo que contém o erro de validação",
        example="email"
    )
    
    message: str = Field(
        ..., 
        description="Mensagem específica do erro de validação",
        example="Email deve ter formato válido"
    )
    
    value: Optional[Any] = Field(
        None, 
        description="Valor que causou o erro (pode ser omitido por segurança)",
        example="invalid-email"
    )
    
    code: Optional[str] = Field(
        None,
        description="Código específico do erro de validação",
        example="INVALID_FORMAT"
    )


class ValidationErrorSchema(BaseSchema):
    """
    Schema para respostas de erro de validação.
    
    Especialização do ErrorResponseSchema para erros de validação,
    fornecendo detalhes específicos sobre cada campo com erro.
    """
    
    success: bool = Field(
        False, 
        description="Indica se a operação foi bem-sucedida",
        example=False
    )
    
    error: str = Field(
        "VALIDATION_ERROR", 
        description="Tipo do erro (sempre VALIDATION_ERROR para este schema)",
        example="VALIDATION_ERROR"
    )
    
    message: str = Field(
        ..., 
        description="Mensagem geral sobre os erros de validação",
        example="Foram encontrados erros de validação nos dados fornecidos"
    )
    
    errors: List[ValidationErrorDetailSchema] = Field(
        ..., 
        description="Lista detalhada de erros de validação por campo",
        example=[
            {
                "field": "email",
                "message": "Email deve ter formato válido",
                "value": "invalid-email",
                "code": "INVALID_FORMAT"
            }
        ]
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do erro",
        example="2024-01-15T10:30:00Z"
    )
    
    path: Optional[str] = Field(
        None,
        description="Caminho da API onde o erro ocorreu",
        example="/api/v1/funcionarios"
    )
    
    class Config:
        """Configuração do schema com exemplos para documentação."""
        json_schema_extra = {
            "examples": [
                {
                    "success": False,
                    "error": "VALIDATION_ERROR",
                    "message": "Foram encontrados erros de validação nos dados fornecidos",
                    "errors": [
                        {
                            "field": "email",
                            "message": "Email deve ter formato válido",
                            "value": "invalid-email",
                            "code": "INVALID_FORMAT"
                        },
                        {
                            "field": "nome_completo",
                            "message": "Nome deve conter pelo menos 2 palavras",
                            "code": "INVALID_LENGTH"
                        }
                    ],
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/v1/funcionarios"
                }
            ]
        }


class NotFoundErrorSchema(BaseSchema):
    """
    Schema específico para erros 404 - Recurso não encontrado.
    """
    
    success: bool = Field(
        False, 
        description="Indica se a operação foi bem-sucedida",
        example=False
    )
    
    error: str = Field(
        "NOT_FOUND", 
        description="Tipo do erro (sempre NOT_FOUND para este schema)",
        example="NOT_FOUND"
    )
    
    message: str = Field(
        ..., 
        description="Mensagem descritiva do recurso não encontrado",
        example="Funcionário não encontrado"
    )
    
    resource: str = Field(
        ...,
        description="Tipo do recurso que não foi encontrado",
        example="funcionario"
    )
    
    identifier: Optional[str] = Field(
        None,
        description="Identificador do recurso que não foi encontrado",
        example="60d5ecb74b24c3b3d8f8e1a2"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do erro",
        example="2024-01-15T10:30:00Z"
    )
    
    class Config:
        """Configuração do schema com exemplos para documentação."""
        json_schema_extra = {
            "examples": [
                {
                    "success": False,
                    "error": "NOT_FOUND",
                    "message": "Funcionário não encontrado",
                    "resource": "funcionario",
                    "identifier": "60d5ecb74b24c3b3d8f8e1a2",
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            ]
        }


class ConflictErrorSchema(BaseSchema):
    """
    Schema específico para erros 409 - Conflito (ex: email duplicado).
    """
    
    success: bool = Field(
        False, 
        description="Indica se a operação foi bem-sucedida",
        example=False
    )
    
    error: str = Field(
        "CONFLICT", 
        description="Tipo do erro (sempre CONFLICT para este schema)",
        example="CONFLICT"
    )
    
    message: str = Field(
        ..., 
        description="Mensagem descritiva do conflito",
        example="Email já existe no sistema"
    )
    
    conflict_field: str = Field(
        ...,
        description="Campo que causou o conflito",
        example="email"
    )
    
    conflict_value: Optional[str] = Field(
        None,
        description="Valor que causou o conflito",
        example="joao.silva@company.com"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do erro",
        example="2024-01-15T10:30:00Z"
    )
    
    class Config:
        """Configuração do schema com exemplos para documentação."""
        json_schema_extra = {
            "examples": [
                {
                    "success": False,
                    "error": "CONFLICT",
                    "message": "Email já existe no sistema",
                    "conflict_field": "email",
                    "conflict_value": "joao.silva@company.com",
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            ]
        }


# Schemas de resposta para diferentes códigos HTTP
class ResponseSchemas:
    """
    Classe com mapeamentos de schemas para diferentes códigos de status HTTP.
    
    Facilita a documentação da API indicando qual schema usar para cada status.
    """
    
    # Respostas de sucesso
    SUCCESS = SuccessResponseSchema
    
    # Respostas de erro cliente (4xx)
    BAD_REQUEST = ValidationErrorSchema
    NOT_FOUND = NotFoundErrorSchema
    CONFLICT = ConflictErrorSchema
    VALIDATION_ERROR = ValidationErrorSchema
    
    # Respostas de erro servidor (5xx)
    INTERNAL_ERROR = ErrorResponseSchema
    
    @classmethod
    def get_responses_dict(cls, success_schema: Any = None) -> Dict[Union[int, str], Dict[str, Any]]:
        """
        Retorna dicionário de respostas para usar na documentação do FastAPI.
        
        Args:
            success_schema: Schema específico para resposta de sucesso (200)
            
        Returns:
            Dicionário com códigos de status e seus schemas correspondentes
        """
        responses = {
            200: {
                "model": success_schema or cls.SUCCESS,
                "description": "Operação realizada com sucesso"
            },
            400: {
                "model": cls.BAD_REQUEST,
                "description": "Dados de entrada inválidos"
            },
            404: {
                "model": cls.NOT_FOUND,
                "description": "Recurso não encontrado"
            },
            409: {
                "model": cls.CONFLICT,
                "description": "Conflito - recurso já existe"
            },
            422: {
                "model": cls.VALIDATION_ERROR,
                "description": "Erro de validação"
            },
            500: {
                "model": cls.INTERNAL_ERROR,
                "description": "Erro interno do servidor"
            }
        }
        
        return responses
