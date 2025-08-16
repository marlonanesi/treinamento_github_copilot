"""
Sistema de injeção de dependências para a camada de infraestrutura.
"""
import logging
from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.infrastructure.database.connection import MongoDBConnection
from app.infrastructure.database.database_manager import DatabaseManager
from app.infrastructure.repositories.funcionario_repository_impl import FuncionarioRepositoryImpl
from app.infrastructure.config.database import get_database_config
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository

logger = logging.getLogger(__name__)

# Instâncias globais (singleton)
_mongo_connection: MongoDBConnection = None
_database_manager: DatabaseManager = None


async def initialize_database() -> None:
    """
    Inicializa a conexão com o banco de dados e cria índices.
    
    Deve ser chamado na inicialização da aplicação.
    """
    global _mongo_connection, _database_manager
    
    try:
        logger.info("🔧 Inicializando infraestrutura de dados...")
        
        # Obter configurações
        config = get_database_config()
        
        # Criar conexão
        _mongo_connection = MongoDBConnection()
        await _mongo_connection.connect(
            connection_string=config["connection_string"],
            database_name=config["database_name"],
            max_pool_size=config["max_pool_size"],
            min_pool_size=config["min_pool_size"],
            max_idle_time_ms=config["max_idle_time_ms"],
            connect_timeout_ms=config["connect_timeout_ms"],
            server_selection_timeout_ms=config["server_selection_timeout_ms"]
        )
        
        # Criar gerenciador de banco
        database = _mongo_connection.get_database()
        _database_manager = DatabaseManager(database)
        
        # Inicializar índices
        await _database_manager.initialize()
        
        logger.info("✅ Infraestrutura de dados inicializada com sucesso")
        
    except Exception as e:
        logger.error(f"❌ Falha ao inicializar infraestrutura: {e}")
        raise


async def shutdown_database() -> None:
    """
    Encerra a conexão com o banco de dados.
    
    Deve ser chamado no shutdown da aplicação.
    """
    global _mongo_connection, _database_manager
    
    try:
        if _mongo_connection:
            await _mongo_connection.disconnect()
            _mongo_connection = None
            _database_manager = None
        
        logger.info("✅ Infraestrutura de dados encerrada")
        
    except Exception as e:
        logger.error(f"❌ Erro ao encerrar infraestrutura: {e}")


def get_database():
    """
    Retorna a instância do banco de dados.
    
    Returns:
        AsyncIOMotorDatabase: Instância do banco
        
    Raises:
        RuntimeError: Se não foi inicializado
    """
    if _mongo_connection is None:
        raise RuntimeError(
            "Banco de dados não foi inicializado. "
            "Execute initialize_database() primeiro."
        )
    
    return _mongo_connection.get_database()


def get_database_manager() -> DatabaseManager:
    """
    Retorna o gerenciador de banco de dados.
    
    Returns:
        DatabaseManager: Instância do gerenciador
        
    Raises:
        RuntimeError: Se não foi inicializado
    """
    if _database_manager is None:
        raise RuntimeError(
            "Database manager não foi inicializado. "
            "Execute initialize_database() primeiro."
        )
    
    return _database_manager


def get_funcionario_repository() -> AbstractFuncionarioRepository:
    """
    Factory para criar instância do repositório de funcionários.
    
    Returns:
        AbstractFuncionarioRepository: Implementação do repositório
        
    Raises:
        RuntimeError: Se banco de dados não foi inicializado
    """
    database = get_database()
    return FuncionarioRepositoryImpl(database)


# Funções para FastAPI Dependencies
async def get_database_dependency():
    """
    Dependency do FastAPI para injeção do banco de dados.
    
    Returns:
        AsyncIOMotorDatabase: Instância do banco
    """
    return get_database()


async def get_funcionario_repository_dependency() -> AbstractFuncionarioRepository:
    """
    Dependency do FastAPI para injeção do repositório de funcionários.
    
    Returns:
        AbstractFuncionarioRepository: Implementação do repositório
    """
    return get_funcionario_repository()


@lru_cache()
def get_connection_info() -> dict:
    """
    Retorna informações sobre a conexão atual.
    
    Returns:
        Dict com informações da conexão
    """
    config = get_database_config()
    
    return {
        "database_name": config["database_name"],
        "max_pool_size": config["max_pool_size"],
        "min_pool_size": config["min_pool_size"],
        "connection_configured": _mongo_connection is not None
    }


async def health_check() -> dict:
    """
    Verifica a saúde da infraestrutura de dados.
    
    Returns:
        Dict com informações de saúde
    """
    try:
        if _database_manager is None:
            return {
                "status": "unhealthy",
                "error": "Database manager não inicializado"
            }
        
        # Executar health check do database manager
        health_info = await _database_manager.health_check()
        
        # Adicionar informações de conexão
        connection_info = get_connection_info()
        health_info.update(connection_info)
        
        return health_info
        
    except Exception as e:
        logger.error(f"❌ Erro no health check da infraestrutura: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
