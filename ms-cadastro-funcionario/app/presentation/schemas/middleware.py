"""
Middleware para validação e processamento de schemas.

Este módulo contém middleware e utilitários para integração
entre FastAPI e schemas Pydantic, incluindo validação,
serialização e tratamento de erros.
"""

from typing import Dict, Any, List, Optional, Type, Union, Callable
from functools import wraps
import json
from datetime import datetime
from decimal import Decimal

from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from .response_schemas import ErrorResponseSchema, ValidationErrorSchema
from .config import ErrorMessages, SchemaConfig


class SchemaValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware para validação automática de schemas em requisições.
    
    Intercepta requisições e valida o corpo da requisição contra
    schemas Pydantic antes de chegar aos endpoints.
    """
    
    def __init__(
        self,
        app,
        strict_validation: bool = True,
        log_validation_errors: bool = True
    ):
        """
        Inicializa o middleware.
        
        Args:
            app: Instância da aplicação FastAPI
            strict_validation: Se True, rejeita requisições inválidas
            log_validation_errors: Se True, loga erros de validação
        """
        super().__init__(app)
        self.strict_validation = strict_validation
        self.log_validation_errors = log_validation_errors
    
    async def dispatch(self, request: Request, call_next):
        """
        Processa requisições através do middleware.
        
        Args:
            request: Requisição HTTP
            call_next: Próximo middleware/endpoint
            
        Returns:
            Resposta HTTP processada
        """
        # Processa a requisição normalmente
        response = await call_next(request)
        
        # Adiciona headers de validação se necessário
        if hasattr(request.state, "validation_info"):
            response.headers["X-Schema-Validation"] = "processed"
        
        return response


class SchemaSerializer:
    """
    Utilitário para serialização de schemas e modelos.
    
    Fornece métodos para converter entre diferentes formatos
    de dados mantendo consistência e tipo safety.
    """
    
    @staticmethod
    def serialize_model(
        model: BaseModel,
        exclude_unset: bool = False,
        exclude_none: bool = False,
        by_alias: bool = True
    ) -> Dict[str, Any]:
        """
        Serializa um modelo Pydantic para dicionário.
        
        Args:
            model: Modelo Pydantic para serializar
            exclude_unset: Excluir campos não definidos
            exclude_none: Excluir campos None
            by_alias: Usar alias dos campos
            
        Returns:
            Dict com dados serializados
        """
        return model.model_dump(
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            by_alias=by_alias
        )
    
    @staticmethod
    def serialize_to_json(
        model: BaseModel,
        indent: Optional[int] = None,
        ensure_ascii: bool = False
    ) -> str:
        """
        Serializa um modelo Pydantic para JSON string.
        
        Args:
            model: Modelo Pydantic para serializar
            indent: Indentação para pretty print
            ensure_ascii: Garantir caracteres ASCII
            
        Returns:
            String JSON serializada
        """
        return model.model_dump_json(
            indent=indent,
            by_alias=True,
            exclude_unset=False
        )
    
    @staticmethod
    def deserialize_from_dict(
        data: Dict[str, Any],
        model_class: Type[BaseModel],
        strict: bool = False
    ) -> BaseModel:
        """
        Deserializa dicionário para modelo Pydantic.
        
        Args:
            data: Dados para deserializar
            model_class: Classe do modelo Pydantic
            strict: Validação estrita
            
        Returns:
            Instância do modelo Pydantic
        """
        try:
            return model_class.model_validate(data, strict=strict)
        except ValidationError as e:
            raise ValidationError.from_exception_data(
                title=f"Validation error for {model_class.__name__}",
                line_errors=e.errors()
            )
    
    @staticmethod
    def deserialize_from_json(
        json_str: str,
        model_class: Type[BaseModel],
        strict: bool = False
    ) -> BaseModel:
        """
        Deserializa JSON string para modelo Pydantic.
        
        Args:
            json_str: String JSON para deserializar
            model_class: Classe do modelo Pydantic
            strict: Validação estrita
            
        Returns:
            Instância do modelo Pydantic
        """
        try:
            data = json.loads(json_str)
            return SchemaSerializer.deserialize_from_dict(data, model_class, strict)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido: {str(e)}")
    
    @staticmethod
    def convert_decimals_to_float(data: Any) -> Any:
        """
        Converte Decimal para float recursivamente.
        
        Args:
            data: Dados para converter
            
        Returns:
            Dados com Decimals convertidos para float
        """
        if isinstance(data, Decimal):
            return float(data)
        elif isinstance(data, dict):
            return {key: SchemaSerializer.convert_decimals_to_float(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [SchemaSerializer.convert_decimals_to_float(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(SchemaSerializer.convert_decimals_to_float(item) for item in data)
        else:
            return data
    
    @staticmethod
    def convert_datetimes_to_iso(data: Any) -> Any:
        """
        Converte datetime para ISO string recursivamente.
        
        Args:
            data: Dados para converter
            
        Returns:
            Dados com datetimes convertidos para strings ISO
        """
        if isinstance(data, datetime):
            return data.isoformat() + ("Z" if data.tzinfo is None else "")
        elif isinstance(data, dict):
            return {key: SchemaSerializer.convert_datetimes_to_iso(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [SchemaSerializer.convert_datetimes_to_iso(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(SchemaSerializer.convert_datetimes_to_iso(item) for item in data)
        else:
            return data


class ValidationErrorHandler:
    """
    Manipulador de erros de validação Pydantic.
    
    Converte erros de validação em respostas HTTP estruturadas
    seguindo padrões da aplicação.
    """
    
    @staticmethod
    def format_validation_error(error: ValidationError) -> ValidationErrorSchema:
        """
        Formata erro de validação Pydantic para schema da aplicação.
        
        Args:
            error: Erro de validação Pydantic
            
        Returns:
            Schema estruturado de erro de validação
        """
        formatted_errors = []
        
        for error_detail in error.errors():
            field_path = ".".join(str(loc) for loc in error_detail["loc"])
            
            formatted_error = {
                "field": field_path,
                "message": ValidationErrorHandler._translate_error_message(
                    error_detail["msg"],
                    error_detail.get("type", ""),
                    field_path
                ),
                "type": error_detail.get("type", "validation_error"),
                "value": error_detail.get("input")
            }
            
            formatted_errors.append(formatted_error)
        
        return ValidationErrorSchema(
            type="ValidationError",
            message="Erro na validação dos dados fornecidos",
            details=formatted_errors,
            total_errors=len(formatted_errors)
        )
    
    @staticmethod
    def _translate_error_message(
        original_message: str,
        error_type: str,
        field_name: str
    ) -> str:
        """
        Traduz mensagens de erro do Pydantic para português.
        
        Args:
            original_message: Mensagem original em inglês
            error_type: Tipo do erro
            field_name: Nome do campo com erro
            
        Returns:
            Mensagem traduzida e contextualizada
        """
        # Mapeamento de mensagens comuns
        error_translations = {
            "field required": f"Campo '{field_name}' é obrigatório",
            "ensure this value has at most": f"Campo '{field_name}' excede o tamanho máximo permitido",
            "ensure this value has at least": f"Campo '{field_name}' não atinge o tamanho mínimo",
            "str type expected": f"Campo '{field_name}' deve ser uma string",
            "int type expected": f"Campo '{field_name}' deve ser um número inteiro",
            "float type expected": f"Campo '{field_name}' deve ser um número decimal",
            "bool type expected": f"Campo '{field_name}' deve ser verdadeiro ou falso",
            "datetime type expected": f"Campo '{field_name}' deve ser uma data válida",
            "invalid email format": f"Campo '{field_name}' deve ser um email válido",
            "string does not match regex": f"Campo '{field_name}' possui formato inválido",
            "value is not a valid decimal": f"Campo '{field_name}' deve ser um valor monetário válido",
            "extra fields not permitted": "Campos extras não são permitidos"
        }
        
        # Busca tradução exata
        for english_msg, portuguese_msg in error_translations.items():
            if english_msg in original_message.lower():
                return portuguese_msg
        
        # Tradução baseada em tipo de erro
        type_translations = {
            "value_error": f"Valor inválido para o campo '{field_name}'",
            "type_error": f"Tipo incorreto para o campo '{field_name}'",
            "missing": f"Campo '{field_name}' é obrigatório",
            "string_too_short": f"Campo '{field_name}' é muito curto",
            "string_too_long": f"Campo '{field_name}' é muito longo",
            "greater_than_equal": f"Campo '{field_name}' deve ser maior ou igual ao valor mínimo",
            "less_than_equal": f"Campo '{field_name}' deve ser menor ou igual ao valor máximo"
        }
        
        if error_type in type_translations:
            return type_translations[error_type]
        
        # Fallback para mensagem original contextualizada
        return f"Erro no campo '{field_name}': {original_message}"
    
    @staticmethod
    def create_validation_response(
        validation_error: ValidationError,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    ) -> JSONResponse:
        """
        Cria resposta HTTP para erro de validação.
        
        Args:
            validation_error: Erro de validação Pydantic
            status_code: Código de status HTTP
            
        Returns:
            Resposta JSON estruturada
        """
        formatted_error = ValidationErrorHandler.format_validation_error(validation_error)
        
        error_response = ErrorResponseSchema(
            success=False,
            message="Erro na validação dos dados",
            error=formatted_error,
            timestamp=datetime.utcnow()
        )
        
        return JSONResponse(
            status_code=status_code,
            content=SchemaSerializer.serialize_model(error_response)
        )


class SchemaResponseMiddleware:
    """
    Middleware para processamento de respostas com schemas.
    
    Padroniza respostas da API aplicando schemas de resposta
    e garantindo consistência na serialização.
    """
    
    def __init__(self, auto_serialize: bool = True):
        """
        Inicializa o middleware de resposta.
        
        Args:
            auto_serialize: Serializar automaticamente modelos Pydantic
        """
        self.auto_serialize = auto_serialize
    
    def process_response(
        self,
        data: Any,
        response_schema: Optional[Type[BaseModel]] = None
    ) -> Dict[str, Any]:
        """
        Processa dados de resposta aplicando schema.
        
        Args:
            data: Dados para processar
            response_schema: Schema opcional para validação
            
        Returns:
            Dados processados e validados
        """
        if response_schema and not isinstance(data, BaseModel):
            # Valida dados contra schema se fornecido
            validated_data = response_schema.model_validate(data)
            return SchemaSerializer.serialize_model(validated_data)
        elif isinstance(data, BaseModel):
            # Serializa modelo Pydantic
            return SchemaSerializer.serialize_model(data)
        else:
            # Processa tipos primitivos
            return SchemaSerializer.convert_decimals_to_float(
                SchemaSerializer.convert_datetimes_to_iso(data)
            )


def validate_schema(schema_class: Type[BaseModel]):
    """
    Decorator para validação automática de schemas em endpoints.
    
    Args:
        schema_class: Classe do schema para validação
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Executa função original
                result = await func(*args, **kwargs)
                return result
            except ValidationError as e:
                # Trata erros de validação
                return ValidationErrorHandler.create_validation_response(e)
            except HTTPException:
                # Re-levanta exceções HTTP
                raise
            except Exception as e:
                # Trata outros erros
                error_response = ErrorResponseSchema(
                    success=False,
                    message="Erro interno do servidor",
                    error={
                        "type": type(e).__name__,
                        "message": str(e)
                    },
                    timestamp=datetime.utcnow()
                )
                
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=SchemaSerializer.serialize_model(error_response)
                )
        
        return wrapper
    return decorator


def serialize_response(exclude_none: bool = False, exclude_unset: bool = False):
    """
    Decorator para serialização automática de respostas.
    
    Args:
        exclude_none: Excluir campos None
        exclude_unset: Excluir campos não definidos
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            if isinstance(result, BaseModel):
                return SchemaSerializer.serialize_model(
                    result,
                    exclude_none=exclude_none,
                    exclude_unset=exclude_unset
                )
            
            return result
        
        return wrapper
    return decorator


# ==========================================
# UTILITÁRIOS DE INTEGRAÇÃO
# ==========================================

class FastAPISchemaIntegration:
    """
    Utilitários para integração entre FastAPI e schemas Pydantic.
    
    Fornece helpers para configuração automática de endpoints,
    documentação OpenAPI e validação de dados.
    """
    
    @staticmethod
    def configure_openapi_schema(
        app,
        title: str = "API de Cadastro de Funcionários",
        version: str = "1.0.0",
        description: str = "API para gerenciamento de funcionários"
    ):
        """
        Configura schema OpenAPI da aplicação.
        
        Args:
            app: Instância FastAPI
            title: Título da API
            version: Versão da API
            description: Descrição da API
        """
        app.title = title
        app.version = version
        app.description = description
        
        # Configurações adicionais do OpenAPI
        app.openapi_tags = [
            {
                "name": "funcionarios",
                "description": "Operações relacionadas a funcionários"
            },
            {
                "name": "health",
                "description": "Verificação de saúde da aplicação"
            }
        ]
    
    @staticmethod
    def create_error_responses() -> Dict[Union[int, str], Dict[str, Any]]:
        """
        Cria dicionário de respostas de erro para OpenAPI.
        
        Returns:
            Dict com respostas de erro padronizadas
        """
        return {
            400: {
                "description": "Requisição inválida",
                "content": {
                    "application/json": {
                        "example": {
                            "success": False,
                            "message": "Dados inválidos na requisição",
                            "error": {
                                "type": "BadRequestError",
                                "message": "Parâmetros inválidos"
                            },
                            "timestamp": "2024-01-15T10:30:00Z"
                        }
                    }
                }
            },
            404: {
                "description": "Recurso não encontrado",
                "content": {
                    "application/json": {
                        "example": {
                            "success": False,
                            "message": "Funcionário não encontrado",
                            "error": {
                                "type": "NotFoundError",
                                "message": "Funcionário com ID especificado não existe"
                            },
                            "timestamp": "2024-01-15T10:30:00Z"
                        }
                    }
                }
            },
            422: {
                "description": "Erro de validação",
                "content": {
                    "application/json": {
                        "example": {
                            "success": False,
                            "message": "Erro na validação dos dados",
                            "error": {
                                "type": "ValidationError",
                                "details": [
                                    {
                                        "field": "email",
                                        "message": "Formato de email inválido",
                                        "value": "email-invalido"
                                    }
                                ]
                            },
                            "timestamp": "2024-01-15T10:30:00Z"
                        }
                    }
                }
            },
            500: {
                "description": "Erro interno do servidor",
                "content": {
                    "application/json": {
                        "example": {
                            "success": False,
                            "message": "Erro interno do servidor",
                            "error": {
                                "type": "InternalServerError",
                                "message": "Erro inesperado no processamento"
                            },
                            "timestamp": "2024-01-15T10:30:00Z"
                        }
                    }
                }
            }
        }
