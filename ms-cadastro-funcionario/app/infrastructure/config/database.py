"""
Configurações específicas para MongoDB.
"""
import os
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient


def get_database_config() -> Dict[str, Any]:
    """
    Retorna configurações do banco de dados baseadas em variáveis de ambiente.
    
    Returns:
        Dict com configurações do MongoDB
    """
    return {
        "connection_string": os.getenv(
            "MONGODB_URL", 
            "mongodb://app_user:app_password123@localhost:27017/funcionarios_db?authSource=funcionarios_db"
        ),
        "database_name": os.getenv(
            "DATABASE_NAME", 
            "funcionarios_db"
        ),
        "max_pool_size": int(os.getenv("MONGODB_MAX_POOL_SIZE", "10")),
        "min_pool_size": int(os.getenv("MONGODB_MIN_POOL_SIZE", "1")),
        "max_idle_time_ms": int(os.getenv("MONGODB_MAX_IDLE_TIME_MS", "30000")),
        "connect_timeout_ms": int(os.getenv("MONGODB_CONNECT_TIMEOUT_MS", "5000")),
        "server_selection_timeout_ms": int(os.getenv("MONGODB_SERVER_SELECTION_TIMEOUT_MS", "5000"))
    }


def get_mongo_client(connection_string: str = None, **kwargs):
    """
    Factory para criar cliente Motor com configurações otimizadas.
    
    Args:
        connection_string: URL de conexão (usa padrão se None)
        **kwargs: Configurações adicionais
        
    Returns:
        AsyncIOMotorClient configurado
    """
    if connection_string is None:
        config = get_database_config()
        connection_string = config["connection_string"]
    
    # Configurações padrão
    default_config = {
        "maxPoolSize": int(os.getenv("MONGODB_MAX_POOL_SIZE", "10")),
        "minPoolSize": int(os.getenv("MONGODB_MIN_POOL_SIZE", "1")),
        "maxIdleTimeMS": int(os.getenv("MONGODB_MAX_IDLE_TIME_MS", "30000")),
        "connectTimeoutMS": int(os.getenv("MONGODB_CONNECT_TIMEOUT_MS", "5000")),
        "serverSelectionTimeoutMS": int(os.getenv("MONGODB_SERVER_SELECTION_TIMEOUT_MS", "5000")),
        "retryWrites": True,
        "w": "majority"
    }
    
    # Mesclar com configurações personalizadas
    default_config.update(kwargs)
    
    return AsyncIOMotorClient(connection_string, **default_config)


def get_test_database_config() -> Dict[str, Any]:
    """
    Configurações específicas para ambiente de teste.
    
    Returns:
        Dict com configurações para testes
    """
    return {
        "connection_string": os.getenv(
            "TEST_MONGODB_URL", 
            "mongodb://app_user:app_password123@localhost:27017/test_funcionarios_db?authSource=funcionarios_db"
        ),
        "database_name": f"test_{os.getenv('DATABASE_NAME', 'funcionarios_db')}",
        "max_pool_size": 5,
        "min_pool_size": 1,
        "max_idle_time_ms": 10000,
        "connect_timeout_ms": 3000,
        "server_selection_timeout_ms": 3000
    }
