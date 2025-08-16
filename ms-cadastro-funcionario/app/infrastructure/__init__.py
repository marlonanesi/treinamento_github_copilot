"""
Infrastructure Layer - Camada de Infraestrutura

Contém implementações concretas de repositórios, configurações de banco de dados
e outras dependências externas.
"""

from app.infrastructure.dependencies import (
    initialize_database,
    shutdown_database,
    get_funcionario_repository,
    get_database_dependency,
    get_funcionario_repository_dependency,
    health_check
)

from app.infrastructure.repositories.funcionario_repository_impl import FuncionarioRepositoryImpl
from app.infrastructure.database.connection import MongoDBConnection
from app.infrastructure.database.database_manager import DatabaseManager

__all__ = [
    # Funções de inicialização
    "initialize_database",
    "shutdown_database",
    
    # Factories
    "get_funcionario_repository",
    
    # Dependencies para FastAPI
    "get_database_dependency", 
    "get_funcionario_repository_dependency",
    
    # Health check
    "health_check",
    
    # Classes principais
    "FuncionarioRepositoryImpl",
    "MongoDBConnection",
    "DatabaseManager"
]
