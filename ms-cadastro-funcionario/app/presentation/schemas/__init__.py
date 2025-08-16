"""
Schemas Pydantic para a camada de apresentação.

Este módulo centraliza todos os schemas utilizados na aplicação
para validação de dados, serialização e documentação da API.

Componentes principais:
- BaseSchema: Classe base com configurações comuns
- Validators: Validadores customizados para regras de negócio
- ResponseSchemas: Schemas padronizados para respostas da API
- FuncionarioSchemas: Schemas específicos para operações CRUD
- HealthSchemas: Schemas para endpoints de saúde
- Middleware: Utilitários de integração e tratamento de erros
"""

# Importações da classe base e configurações
from .base import (
    BaseSchema,
    TimestampMixin,
    PaginationMixin
)

# Importações dos validadores customizados
from .validators import (
    CustomValidators
)

# Importações dos schemas de resposta
from .response_schemas import (
    SuccessResponseSchema,
    ErrorResponseSchema,
    ValidationErrorSchema,
    ResponseSchemas
)

# Importações dos schemas de funcionário
from .funcionario_schemas import (
    # Schemas de criação e atualização
    FuncionarioCreateSchema,
    FuncionarioUpdateSchema,
    
    # Schema de resposta
    FuncionarioResponseSchema,
    
    # Schemas de listagem e consulta
    FuncionarioListQuerySchema,
    FuncionarioListResponseSchema,
    
    # Schema de deleção
    FuncionarioDeleteSchema
)

# Importações dos schemas de health check
from .health_schemas import (
    # Enums e schemas básicos
    HealthStatus,
    ComponentHealthSchema,
    
    # Schemas específicos
    DatabaseHealthSchema,
    ApplicationHealthSchema,
    
    # Schemas de resposta completos
    HealthCheckResponseSchema,
    LivenessProbeSchema,
    ReadinessProbeSchema,
    MetricsSchema
)

# Importações de configuração
from .config import (
    SchemaConfig,
    ValidationConstants,
    ErrorMessages,
    CorporateConfig,
    SchemaUtils,
    PaginationConfig
)

# Importações de middleware e utilitários
from .middleware import (
    SchemaValidationMiddleware,
    SchemaSerializer,
    ValidationErrorHandler,
    SchemaResponseMiddleware,
    FastAPISchemaIntegration,
    validate_schema,
    serialize_response
)

# Importações de exemplos (opcional para produção)
from .examples import (
    FuncionarioExamples,
    ResponseExamples,
    HealthExamples,
    ValidatorExamples,
    executar_todos_exemplos
)


# ==========================================
# EXPORTAÇÕES PRINCIPAIS
# ==========================================

__all__ = [
    # Classes base e mixins
    "BaseSchema",
    "TimestampMixin", 
    "PaginationMixin",
    
    # Validadores
    "CustomValidators",
    
    # Schemas de resposta
    "SuccessResponseSchema",
    "ErrorResponseSchema", 
    "ValidationErrorSchema",
    "ResponseSchemas",
    
    # Schemas de funcionário
    "FuncionarioCreateSchema",
    "FuncionarioUpdateSchema",
    "FuncionarioResponseSchema",
    "FuncionarioListQuerySchema",
    "FuncionarioListResponseSchema",
    "FuncionarioDeleteSchema",
    
    # Schemas de health check
    "HealthStatus",
    "ComponentHealthSchema",
    "DatabaseHealthSchema",
    "ApplicationHealthSchema", 
    "HealthCheckResponseSchema",
    "LivenessProbeSchema",
    "ReadinessProbeSchema",
    "MetricsSchema",
    
    # Configurações
    "SchemaConfig",
    "ValidationConstants",
    "ErrorMessages",
    "CorporateConfig",
    "SchemaUtils",
    "PaginationConfig",
    
    # Middleware e utilitários
    "SchemaValidationMiddleware",
    "SchemaSerializer",
    "ValidationErrorHandler",
    "SchemaResponseMiddleware", 
    "FastAPISchemaIntegration",
    "validate_schema",
    "serialize_response",
    
    # Exemplos (removível em produção)
    "FuncionarioExamples",
    "ResponseExamples",
    "HealthExamples",
    "ValidatorExamples",
    "executar_todos_exemplos"
]


# ==========================================
# AGRUPAMENTOS POR FUNCIONALIDADE
# ==========================================

# Schemas para endpoints de funcionário
FUNCIONARIO_SCHEMAS = [
    "FuncionarioCreateSchema",
    "FuncionarioUpdateSchema", 
    "FuncionarioResponseSchema",
    "FuncionarioListQuerySchema",
    "FuncionarioListResponseSchema",
    "FuncionarioDeleteSchema"
]

# Schemas para endpoints de health check
HEALTH_SCHEMAS = [
    "HealthStatus",
    "ComponentHealthSchema",
    "DatabaseHealthSchema",
    "ApplicationHealthSchema",
    "HealthCheckResponseSchema", 
    "LivenessProbeSchema",
    "ReadinessProbeSchema",
    "MetricsSchema"
]

# Schemas de resposta padrão da API
RESPONSE_SCHEMAS = [
    "SuccessResponseSchema",
    "ErrorResponseSchema",
    "ValidationErrorSchema", 
    "ResponseSchemas"
]

# Utilitários de validação e middleware
VALIDATION_UTILITIES = [
    "CustomValidators",
    "SchemaValidationMiddleware",
    "ValidationErrorHandler",
    "validate_schema"
]

# Utilitários de serialização
SERIALIZATION_UTILITIES = [
    "SchemaSerializer", 
    "SchemaResponseMiddleware",
    "serialize_response"
]


# ==========================================
# INFORMAÇÕES DO MÓDULO
# ==========================================

__version__ = "1.0.0"
__author__ = "Equipe de Desenvolvimento"
__description__ = "Schemas Pydantic para validação e serialização de dados"

# Metadados para documentação
SCHEMA_INFO = {
    "title": "Schemas de Dados",
    "version": __version__,
    "description": __description__,
    "components": {
        "funcionario": "Schemas para operações CRUD de funcionários",
        "health": "Schemas para verificação de saúde da aplicação", 
        "response": "Schemas padronizados para respostas da API",
        "validation": "Validadores customizados e middleware",
        "config": "Configurações e constantes de validação"
    },
    "features": [
        "Validação de dados com Pydantic v2",
        "Schemas de resposta padronizados",
        "Validadores customizados para regras brasileiras",
        "Middleware de validação automática",
        "Serialização consistente de dados",
        "Documentação OpenAPI integrada",
        "Tratamento de erros estruturado",
        "Suporte a paginação",
        "Health checks completos"
    ]
}


# ==========================================
# FUNÇÕES UTILITÁRIAS DO MÓDULO
# ==========================================

def get_all_schemas():
    """
    Retorna lista de todos os schemas disponíveis.
    
    Returns:
        List[str]: Lista com nomes de todos os schemas
    """
    return __all__


def get_schemas_by_category(category: str):
    """
    Retorna schemas de uma categoria específica.
    
    Args:
        category: Categoria dos schemas
        
    Returns:
        List[str]: Lista de schemas da categoria
    """
    categories = {
        "funcionario": FUNCIONARIO_SCHEMAS,
        "health": HEALTH_SCHEMAS, 
        "response": RESPONSE_SCHEMAS,
        "validation": VALIDATION_UTILITIES,
        "serialization": SERIALIZATION_UTILITIES
    }
    
    return categories.get(category, [])


def get_schema_info():
    """
    Retorna informações sobre o módulo de schemas.
    
    Returns:
        Dict: Informações do módulo
    """
    return SCHEMA_INFO


def validate_installation():
    """
    Valida se todos os componentes estão instalados corretamente.
    
    Returns:
        bool: True se tudo estiver funcionando
    """
    try:
        # Testa imports básicos
        from pydantic import BaseModel, ValidationError
        from datetime import datetime
        from decimal import Decimal
        
        # Testa criação de schema básico
        test_data = SchemaUtils.criar_exemplo_funcionario()
        funcionario = FuncionarioCreateSchema(**test_data)
        
        # Testa serialização
        serialized = SchemaSerializer.serialize_model(funcionario)
        
        print("✅ Todos os schemas instalados e funcionando corretamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na validação da instalação: {e}")
        return False


# ==========================================
# INICIALIZAÇÃO DO MÓDULO
# ==========================================

# Validação automática na importação (opcional)
# validate_installation()
