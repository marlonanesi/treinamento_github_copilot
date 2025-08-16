"""
Configurações de Banco de Dados

Contém configurações e conexões com MongoDB.
"""

from app.infrastructure.database.connection import MongoDBConnection
from app.infrastructure.database.database_manager import DatabaseManager
from app.infrastructure.database.models import FuncionarioModel

__all__ = [
    "MongoDBConnection",
    "DatabaseManager", 
    "FuncionarioModel"
]
