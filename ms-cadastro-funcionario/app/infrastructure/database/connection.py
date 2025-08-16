"""
Configuração de conexão assíncrona com MongoDB usando Motor.
"""
import logging
from typing import Optional, TYPE_CHECKING
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


class MongoDBConnection:
    """
    Singleton pattern para conexão única com MongoDB.
    Gerencia pool de conexões e configurações otimizadas.
    """
    
    _instance: Optional['MongoDBConnection'] = None
    _client = None
    _database = None
    
    def __new__(cls) -> 'MongoDBConnection':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(
        self, 
        connection_string: str, 
        database_name: str,
        max_pool_size: int = 10,
        min_pool_size: int = 1,
        max_idle_time_ms: int = 30000,
        connect_timeout_ms: int = 5000,
        server_selection_timeout_ms: int = 5000
    ) -> None:
        """
        Estabelece conexão com MongoDB com configurações otimizadas.
        
        Args:
            connection_string: URL de conexão do MongoDB
            database_name: Nome do banco de dados
            max_pool_size: Máximo de conexões no pool
            min_pool_size: Mínimo de conexões no pool
            max_idle_time_ms: Tempo máximo de idle das conexões
            connect_timeout_ms: Timeout de conexão
            server_selection_timeout_ms: Timeout de seleção do servidor
        """
        try:
            if self._client is None:
                self._client = AsyncIOMotorClient(
                    connection_string,
                    maxPoolSize=max_pool_size,
                    minPoolSize=min_pool_size,
                    maxIdleTimeMS=max_idle_time_ms,
                    connectTimeoutMS=connect_timeout_ms,
                    serverSelectionTimeoutMS=server_selection_timeout_ms
                )
                
                # Verificar conectividade
                await self._client.admin.command('ping')
                
                self._database = self._client[database_name]
                
                logger.info(
                    f"✅ MongoDB conectado com sucesso: {database_name} "
                    f"(Pool: {min_pool_size}-{max_pool_size})"
                )
                
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ Falha na conexão com MongoDB: {e}")
            raise ConnectionFailure(f"Erro ao conectar com MongoDB: {e}")
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao conectar MongoDB: {e}")
            raise
    
    async def disconnect(self) -> None:
        """
        Fecha todas as conexões com MongoDB.
        """
        if self._client:
            try:
                self._client.close()
                self._client = None
                self._database = None
                logger.info("✅ MongoDB desconectado com sucesso")
            except Exception as e:
                logger.error(f"❌ Erro ao desconectar MongoDB: {e}")
    
    def get_database(self):
        """
        Retorna a instância do banco de dados.
        
        Returns:
            AsyncIOMotorDatabase: Instância do banco
            
        Raises:
            RuntimeError: Se não estiver conectado
        """
        if self._database is None:
            raise RuntimeError(
                "MongoDB não está conectado. Execute connect() primeiro."
            )
        return self._database
    
    def get_client(self):
        """
        Retorna o cliente MongoDB.
        
        Returns:
            AsyncIOMotorClient: Cliente MongoDB
            
        Raises:
            RuntimeError: Se não estiver conectado
        """
        if self._client is None:
            raise RuntimeError(
                "MongoDB não está conectado. Execute connect() primeiro."
            )
        return self._client
    
    @property
    def is_connected(self) -> bool:
        """
        Verifica se está conectado ao MongoDB.
        
        Returns:
            bool: True se conectado, False caso contrário
        """
        return self._client is not None and self._database is not None
