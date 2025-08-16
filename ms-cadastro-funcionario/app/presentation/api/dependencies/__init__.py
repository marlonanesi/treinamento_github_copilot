"""
Dependências FastAPI para injeção de dependências.

Este módulo centraliza todas as dependências utilizadas nos endpoints
da API para injeção automática pelo FastAPI.
"""

from .dependencies import (
    # Validadores de parâmetros
    validate_object_id,
    validate_pagination_params,
    
    # Dependências principais
    get_funcionario_controller,
    get_application_coordinator,
    get_funcionario_repository,
    get_mongodb_connection,
    
    # Type aliases para facilitar uso
    ValidObjectId,
    PaginationParams,
    FuncionarioControllerDep,
    ApplicationCoordinatorDep,
    
    # Health check dependencies
    get_health_dependencies,
    
    # Configurações
    get_api_config,
    
    # Utilitários
    dependency_provider,
    dependency_middleware,
    create_dependency_override,
    validate_dependency_chain
)

__all__ = [
    "validate_object_id",
    "validate_pagination_params", 
    "get_funcionario_controller",
    "get_application_coordinator",
    "get_funcionario_repository",
    "get_mongodb_connection",
    "ValidObjectId",
    "PaginationParams",
    "FuncionarioControllerDep", 
    "ApplicationCoordinatorDep",
    "get_health_dependencies",
    "get_api_config",
    "dependency_provider",
    "dependency_middleware",
    "create_dependency_override",
    "validate_dependency_chain"
]
