"""
Dependências do FastAPI para injeção de dependências.

Este módulo define as dependências que serão injetadas nos endpoints
para fornecer instâncias de controllers, coordinators e validadores.
"""

from typing import Annotated
from fastapi import Depends, Path, HTTPException, status
import re

from app.application.coordinator import ApplicationCoordinator, ApplicationCoordinatorFactory
from app.infrastructure.database.connection import MongoDBConnection
from app.infrastructure.repositories.funcionario_repository_impl import FuncionarioRepositoryImpl
from app.presentation.api.controllers.funcionario_controller import FuncionarioController


# ==========================================
# VALIDADORES DE PARÂMETROS
# ==========================================

def validate_object_id(funcionario_id: str = Path(..., description="ID único do funcionário")) -> str:
    """
    Valida se o ID fornecido é um ObjectId válido do MongoDB.
    
    Args:
        funcionario_id: ID para validar
        
    Returns:
        ID validado
        
    Raises:
        HTTPException: Se o ID não for válido
    """
    # Padrão ObjectId: 24 caracteres hexadecimais
    object_id_pattern = r'^[a-f\d]{24}$'
    
    if not re.match(object_id_pattern, funcionario_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": "INVALID_ID",
                "message": "ID deve ser um ObjectId válido do MongoDB (24 caracteres hexadecimais)",
                "received_id": funcionario_id
            }
        )
    
    return funcionario_id


def validate_pagination_params(
    page: int = 1,
    size: int = 20
) -> dict:
    """
    Valida e normaliza parâmetros de paginação.
    
    Args:
        page: Número da página (mínimo 1)
        size: Tamanho da página (1-100)
        
    Returns:
        Dict com parâmetros validados
        
    Raises:
        HTTPException: Se parâmetros inválidos
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": "INVALID_PAGE",
                "message": "Número da página deve ser pelo menos 1",
                "received_page": page
            }
        )
    
    if size < 1 or size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": "INVALID_PAGE_SIZE",
                "message": "Tamanho da página deve estar entre 1 e 100",
                "received_size": size
            }
        )
    
    return {
        "page": page,
        "size": size,
        "skip": (page - 1) * size
    }


# ==========================================
# DEPENDÊNCIAS DE INFRAESTRUTURA
# ==========================================

async def get_mongodb_connection():
    """
    Fornece conexão com MongoDB já inicializada.
    
    Returns:
        AsyncIOMotorDatabase: Instância do banco de dados
    """
    from app.infrastructure.dependencies import get_database_dependency
    
    return await get_database_dependency()


async def get_funcionario_repository(
    database = Depends(get_mongodb_connection)
) -> FuncionarioRepositoryImpl:
    """
    Fornece repositório de funcionário configurado.
    
    Args:
        database: Instância do banco de dados MongoDB
        
    Returns:
        Instância do repositório
    """
    return FuncionarioRepositoryImpl(database)


# ==========================================
# DEPENDÊNCIAS DE APLICAÇÃO
# ==========================================

async def get_application_coordinator(
    repository: Annotated[FuncionarioRepositoryImpl, Depends(get_funcionario_repository)]
) -> ApplicationCoordinator:
    """
    Fornece coordinator de aplicação configurado.
    
    Args:
        repository: Repositório injetado
        
    Returns:
        Instância do coordinator
    """
    factory = ApplicationCoordinatorFactory()
    coordinator = await factory.create(repository)
    return coordinator


# ==========================================
# DEPENDÊNCIAS DE APRESENTAÇÃO
# ==========================================

async def get_funcionario_controller(
    coordinator: Annotated[ApplicationCoordinator, Depends(get_application_coordinator)]
) -> FuncionarioController:
    """
    Fornece controller de funcionário configurado.
    
    Args:
        coordinator: Coordinator de aplicação injetado
        
    Returns:
        Instância do controller
    """
    return FuncionarioController(coordinator)


# ==========================================
# DEPENDÊNCIAS DE VALIDAÇÃO
# ==========================================

# Type aliases para melhor legibilidade
ValidObjectId = Annotated[str, Depends(validate_object_id)]
PaginationParams = Annotated[dict, Depends(validate_pagination_params)]
FuncionarioControllerDep = Annotated[FuncionarioController, Depends(get_funcionario_controller)]
ApplicationCoordinatorDep = Annotated[ApplicationCoordinator, Depends(get_application_coordinator)]


# ==========================================
# DEPENDÊNCIAS DE HEALTH CHECK
# ==========================================

async def get_health_dependencies() -> dict:
    """
    Fornece dependências necessárias para health check.
    
    Returns:
        Dict com informações para verificação de saúde
    """
    import psutil
    import time
    from datetime import datetime
    
    return {
        "start_time": time.time(),
        "version": "1.0.0",
        "environment": "development",  # TODO: Pegar do config
        "timestamp": datetime.utcnow(),
        "memory_usage": psutil.virtual_memory().percent,
        "cpu_usage": psutil.cpu_percent(interval=1)
    }


# ==========================================
# DEPENDÊNCIAS DE AUTENTICAÇÃO (FUTURO)
# ==========================================

async def get_current_user():
    """
    Placeholder para autenticação futura.
    
    TODO: Implementar quando houver sistema de autenticação
    """
    pass


async def require_admin_role():
    """
    Placeholder para autorização futura.
    
    TODO: Implementar quando houver sistema de autorização
    """
    pass


# ==========================================
# DEPENDÊNCIAS CUSTOMIZADAS
# ==========================================

class DependencyProvider:
    """
    Provider centralizado para dependências personalizadas.
    
    Facilita testes e configurações alternativas.
    """
    
    def __init__(self):
        self._overrides = {}
    
    def override(self, dependency_name: str, override_value):
        """
        Permite override de dependências para testes.
        
        Args:
            dependency_name: Nome da dependência
            override_value: Valor substituto
        """
        self._overrides[dependency_name] = override_value
    
    def get_override(self, dependency_name: str):
        """
        Obtém override se existir.
        
        Args:
            dependency_name: Nome da dependência
            
        Returns:
            Override ou None
        """
        return self._overrides.get(dependency_name)
    
    def clear_overrides(self):
        """Limpa todos os overrides."""
        self._overrides.clear()


# Instância global do provider
dependency_provider = DependencyProvider()


# ==========================================
# DEPENDÊNCIAS DE CONFIGURAÇÃO
# ==========================================

async def get_api_config() -> dict:
    """
    Fornece configurações da API.
    
    Returns:
        Dict com configurações
    """
    return {
        "title": "Microserviço de Cadastro de Funcionários",
        "version": "1.0.0",
        "description": "API para gerenciamento de funcionários da TechNovaMBA Solutions",
        "cors_origins": ["*"],  # TODO: Restringir em produção
        "request_timeout": 30,
        "max_request_size": 1024 * 1024,  # 1MB
        "rate_limit": {
            "requests": 100,
            "window": 60  # segundos
        }
    }


# ==========================================
# UTILITÁRIOS DE DEPENDÊNCIA
# ==========================================

def create_dependency_override(original_dependency, override_value):
    """
    Cria uma função de dependência que retorna um valor específico.
    
    Útil para testes unitários.
    
    Args:
        original_dependency: Dependência original
        override_value: Valor para override
        
    Returns:
        Função de dependência
    """
    async def override_dependency():
        return override_value
    
    return override_dependency


def validate_dependency_chain():
    """
    Valida se todas as dependências estão configuradas corretamente.
    
    Returns:
        bool: True se válidas
        
    Raises:
        ValueError: Se houver problema na configuração
    """
    try:
        # Testa criação do coordinator
        factory = ApplicationCoordinatorFactory()
        
        # TODO: Adicionar mais validações conforme necessário
        return True
        
    except Exception as e:
        raise ValueError(f"Erro na configuração de dependências: {str(e)}")


# ==========================================
# MIDDLEWARE DE DEPENDÊNCIAS
# ==========================================

class DependencyMiddleware:
    """
    Middleware para gerenciar ciclo de vida de dependências.
    
    Garante que recursos sejam adequadamente limpos.
    """
    
    def __init__(self):
        self._active_connections = []
        self._active_repositories = []
    
    async def setup_request(self):
        """Configura dependências para uma requisição."""
        pass
    
    async def cleanup_request(self):
        """Limpa recursos após uma requisição."""
        # Fechar conexões ativas
        for connection in self._active_connections:
            try:
                await connection.close()
            except Exception:
                pass  # Log error in production
        
        self._active_connections.clear()
        self._active_repositories.clear()
    
    def track_connection(self, connection):
        """Rastreia conexão para limpeza posterior."""
        self._active_connections.append(connection)
    
    def track_repository(self, repository):
        """Rastreia repositório para limpeza posterior."""
        self._active_repositories.append(repository)


# Instância global do middleware
dependency_middleware = DependencyMiddleware()


# ==========================================
# EXPORTAÇÕES PARA USO NOS ROUTERS
# ==========================================

__all__ = [
    # Validadores
    "validate_object_id",
    "validate_pagination_params",
    
    # Dependências principais
    "get_funcionario_controller",
    "get_application_coordinator", 
    "get_funcionario_repository",
    "get_mongodb_connection",
    
    # Type aliases
    "ValidObjectId",
    "PaginationParams", 
    "FuncionarioControllerDep",
    "ApplicationCoordinatorDep",
    
    # Health check
    "get_health_dependencies",
    
    # Configuração
    "get_api_config",
    
    # Utilitários
    "dependency_provider",
    "dependency_middleware",
    "create_dependency_override",
    "validate_dependency_chain"
]
