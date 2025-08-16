"""
Gerenciamento do banco de dados MongoDB.
"""
import logging
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import IndexModel, ASCENDING, DESCENDING
from pymongo.errors import OperationFailure, ConnectionFailure

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Gerencia inicialização, índices e operações de manutenção do banco.
    """
    
    def __init__(self, database):
        self.database = database
        self.collection_name = "funcionarios"
    
    async def initialize(self) -> None:
        """
        Inicializa o banco de dados criando coleções e índices necessários.
        """
        try:
            # Verificar conectividade primeiro com uma operação simples
            await self.database.command("ping")
            logger.info("🔗 Conexão MongoDB estabelecida com sucesso")
            
            # Tentar verificar se a coleção existe
            try:
                collections = await self.database.list_collection_names()
                if self.collection_name not in collections:
                    logger.info(f"📝 Criando coleção: {self.collection_name}")
                    await self.database.create_collection(self.collection_name)
                else:
                    logger.info(f"📋 Coleção '{self.collection_name}' já existe")
            except Exception as e:
                logger.warning(f"⚠️ Não foi possível verificar coleções: {e}")
                logger.info(f"📝 Continuando com inicialização...")
            
            # Criar índices (essa operação criará a coleção se não existir)
            # Criar índices (temporariamente desabilitado - problema de auth no MongoDB)
            # await self.create_indexes()
            logger.info("⚠️ Criação de índices desabilitada temporariamente")
            
            logger.info("✅ Banco de dados inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar banco de dados: {e}")
            raise
    
    async def create_indexes(self) -> None:
        """
        Cria índices otimizados para performance das queries.
        """
        collection = self.database[self.collection_name]
        
        try:
            # Definir índices
            indexes = [
                # Índice único para email (previne duplicatas)
                IndexModel(
                    [("email", ASCENDING)], 
                    unique=True, 
                    name="idx_email_unique"
                ),
                
                # Índice para departamento (filtros)
                IndexModel(
                    [("departamento", ASCENDING)], 
                    name="idx_departamento"
                ),
                
                # Índice para cargo (filtros)
                IndexModel(
                    [("cargo", ASCENDING)], 
                    name="idx_cargo"
                ),
                
                # Índice para data de criação (ordenação temporal)
                IndexModel(
                    [("created_at", DESCENDING)], 
                    name="idx_created_at"
                ),
                
                # Índice composto para filtros combinados
                IndexModel(
                    [("departamento", ASCENDING), ("cargo", ASCENDING)], 
                    name="idx_departamento_cargo"
                ),
                
                # Índice para status ativo (queries de funcionários ativos)
                IndexModel(
                    [("ativo", ASCENDING)], 
                    name="idx_ativo_projetos"
                ),
                
                # Índice composto para queries complexas
                IndexModel(
                    [("ativo", ASCENDING), ("departamento", ASCENDING)], 
                    name="idx_ativo_departamento"
                )
            ]
            
            # Criar índices
            result = await collection.create_indexes(indexes)
            
            logger.info(f"✅ Índices criados: {len(result)} índices")
            
            # Listar índices existentes para confirmação
            existing_indexes = await collection.list_indexes().to_list(length=None)
            index_names = [idx['name'] for idx in existing_indexes]
            logger.info(f"📋 Índices ativos: {', '.join(index_names)}")
            
        except OperationFailure as e:
            if "already exists" in str(e) or "IndexKeySpecsConflict" in str(e):
                logger.info("📋 Índices já existem ou há conflitos, verificando compatibilidade...")
                
                # Listar índices existentes
                try:
                    existing_indexes = await collection.list_indexes().to_list(length=None)
                    index_names = [idx['name'] for idx in existing_indexes]
                    logger.info(f"📋 Índices existentes: {', '.join(index_names)}")
                    
                    # Verificar se os índices principais existem
                    required_indexes = ["idx_email_unique", "idx_departamento", "idx_cargo"]
                    missing_indexes = [idx for idx in required_indexes if idx not in index_names]
                    
                    if not missing_indexes:
                        logger.info("✅ Todos os índices principais existem")
                    else:
                        logger.warning(f"⚠️ Índices faltando: {missing_indexes}")
                        
                except Exception as list_error:
                    logger.warning(f"⚠️ Não foi possível listar índices: {list_error}")
            else:
                logger.error(f"❌ Erro ao criar índices: {e}")
                raise
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao criar índices: {e}")
            raise
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica a saúde da conexão com o banco de dados.
        
        Returns:
            Dict com informações de saúde
        """
        try:
            # Ping no servidor
            await self.database.command("ping")
            
            # Verificar coleção
            collection = self.database[self.collection_name]
            count = await collection.count_documents({})
            
            # Verificar índices
            indexes = await collection.list_indexes().to_list(length=None)
            index_count = len(indexes)
            
            # Estatísticas da coleção
            stats = await self.database.command("collStats", self.collection_name)
            
            return {
                "status": "healthy",
                "database_name": self.database.name,
                "collection_name": self.collection_name,
                "document_count": count,
                "index_count": index_count,
                "collection_size_bytes": stats.get("size", 0),
                "storage_size_bytes": stats.get("storageSize", 0),
                "indexes": [idx["name"] for idx in indexes]
            }
            
        except ConnectionFailure as e:
            logger.error(f"❌ Falha de conexão no health check: {e}")
            return {
                "status": "unhealthy",
                "error": f"Connection failure: {e}",
                "database_name": self.database.name
            }
        except Exception as e:
            logger.error(f"❌ Erro no health check: {e}")
            return {
                "status": "unhealthy", 
                "error": str(e),
                "database_name": self.database.name
            }
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas da coleção.
        
        Returns:
            Dict com estatísticas da coleção
        """
        try:
            collection = self.database[self.collection_name]
            
            # Contar documentos
            total_docs = await collection.count_documents({})
            active_docs = await collection.count_documents({"ativo": True})
            
            # Estatísticas por departamento
            pipeline = [
                {"$group": {
                    "_id": "$departamento", 
                    "count": {"$sum": 1}
                }},
                {"$sort": {"count": -1}}
            ]
            dept_stats = await collection.aggregate(pipeline).to_list(length=None)
            
            # Estatísticas por cargo
            pipeline = [
                {"$group": {
                    "_id": "$cargo", 
                    "count": {"$sum": 1}
                }},
                {"$sort": {"count": -1}}
            ]
            cargo_stats = await collection.aggregate(pipeline).to_list(length=None)
            
            return {
                "total_funcionarios": total_docs,
                "funcionarios_ativos": active_docs,
                "funcionarios_inativos": total_docs - active_docs,
                "por_departamento": dept_stats,
                "por_cargo": cargo_stats
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas: {e}")
            raise
    
    async def drop_all_indexes(self) -> None:
        """
        Remove todos os índices (exceto _id) - usado para manutenção.
        """
        try:
            collection = self.database[self.collection_name]
            await collection.drop_indexes()
            logger.info("✅ Todos os índices foram removidos")
        except Exception as e:
            logger.error(f"❌ Erro ao remover índices: {e}")
            raise
