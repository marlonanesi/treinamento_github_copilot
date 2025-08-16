"""
Configurações Gerais

Contém classes de configuração, settings e variáveis de ambiente.
"""

from app.infrastructure.config.database import (
    get_database_config,
    get_mongo_client,
    get_test_database_config
)

__all__ = [
    "get_database_config",
    "get_mongo_client",
    "get_test_database_config"
]
