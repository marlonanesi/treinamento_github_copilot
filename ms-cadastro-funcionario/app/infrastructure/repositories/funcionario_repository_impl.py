"""
Implementação concreta do repositório de funcionários para MongoDB.
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError, WriteError
from motor.motor_asyncio import AsyncIOMotorCollection

from app.domain.entities.funcionario import Funcionario
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository
from app.domain.exceptions.funcionario_exceptions import (
    EmailDuplicadoException,
    FuncionarioNaoEncontradoException,
    DadosInvalidosException,
    ErroOperacaoException
)
from app.infrastructure.database.models import FuncionarioModel

logger = logging.getLogger(__name__)


class FuncionarioRepositoryImpl(AbstractFuncionarioRepository):
    """
    Implementação do repositório de funcionários usando MongoDB.
    
    Implementa todas as operações definidas na interface abstrata,
    convertendo exceções de MongoDB para exceções de domínio.
    """
    
    def __init__(self, database):
        """
        Inicializa o repositório com uma instância do banco de dados.
        
        Args:
            database: Instância do banco de dados MongoDB
        """
        self.database = database
        self.collection = database["funcionarios"]
    
    async def salvar(self, funcionario: Funcionario) -> Funcionario:
        """
        Salva um novo funcionário no banco de dados.
        
        Args:
            funcionario: Instância do funcionário a ser salvo
            
        Returns:
            Funcionario: Funcionário salvo com ID atribuído
            
        Raises:
            EmailDuplicadoException: Se email já existe
            DadosInvalidosException: Se dados são inválidos
        """
        try:
            # Converter entidade para documento
            document = FuncionarioModel.from_entity(funcionario)
            
            # Remover _id se existir (será gerado automaticamente)
            if "_id" in document:
                del document["_id"]
            
            logger.debug(f"💾 Salvando funcionário: {funcionario.email.value}")
            
            # Inserir no MongoDB
            result = await self.collection.insert_one(document)
            
            # Atribuir ID gerado
            funcionario.id = str(result.inserted_id)
            
            logger.info(f"✅ Funcionário salvo: {funcionario.nome_completo} ({result.inserted_id})")
            
            return funcionario
            
        except DuplicateKeyError as e:
            logger.warning(f"⚠️ Email duplicado: {funcionario.email.value}")
            raise EmailDuplicadoException(funcionario.email.value)
        except WriteError as e:
            logger.error(f"❌ Erro de escrita no MongoDB: {e}")
            raise DadosInvalidosException("funcionario", str(funcionario), f"Erro de validação: {e}")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar funcionário: {e}")
            raise ErroOperacaoException(f"Falha ao salvar funcionário: {e}")
    
    async def buscar_por_id(self, funcionario_id: str) -> Optional[Funcionario]:
        """
        Busca funcionário por ID.
        
        Args:
            funcionario_id: ID do funcionário
            
        Returns:
            Funcionario se encontrado, None caso contrário
        """
        try:
            # Validar ObjectId
            if not ObjectId.is_valid(funcionario_id):
                logger.warning(f"⚠️ ID inválido: {funcionario_id}")
                return None
            
            logger.debug(f"🔍 Buscando funcionário por ID: {funcionario_id}")
            
            # Buscar no MongoDB
            document = await self.collection.find_one({"_id": ObjectId(funcionario_id)})
            
            if document:
                funcionario = FuncionarioModel.to_entity(document)
                logger.debug(f"✅ Funcionário encontrado: {funcionario.nome_completo}")
                return funcionario
            
            logger.debug(f"❌ Funcionário não encontrado: {funcionario_id}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar funcionário por ID: {e}")
            raise ErroOperacaoException(f"Falha ao buscar funcionário: {e}")
    
    async def buscar_por_email(self, email: str) -> Optional[Funcionario]:
        """
        Busca funcionário por email.
        
        Args:
            email: Email do funcionário
            
        Returns:
            Funcionario se encontrado, None caso contrário
        """
        try:
            logger.debug(f"🔍 Buscando funcionário por email: {email}")
            
            # Buscar usando índice único de email
            document = await self.collection.find_one({"email": email})
            
            if document:
                funcionario = FuncionarioModel.to_entity(document)
                logger.debug(f"✅ Funcionário encontrado: {funcionario.nome_completo}")
                return funcionario
            
            logger.debug(f"❌ Funcionário não encontrado: {email}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar funcionário por email: {e}")
            raise ErroOperacaoException(f"Falha ao buscar funcionário por email: {e}")
    
    async def listar_todos(self, skip: int = 0, limit: int = 100) -> List[Funcionario]:
        """
        Lista todos os funcionários com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de funcionários
        """
        try:
            logger.debug(f"📋 Listando funcionários (skip={skip}, limit={limit})")
            
            # Query com paginação e ordenação por data de criação
            cursor = self.collection.find().sort("created_at", -1).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            # Converter documentos para entidades
            funcionarios = [FuncionarioModel.to_entity(doc) for doc in documents]
            
            logger.info(f"✅ {len(funcionarios)} funcionários listados")
            return funcionarios
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar funcionários: {e}")
            raise ErroOperacaoException(f"Falha ao listar funcionários: {e}")
    
    async def listar_por_filtros(
        self,
        departamento: Optional[str] = None,
        cargo: Optional[str] = None,
        ativo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Funcionario]:
        """
        Lista funcionários aplicando filtros específicos.
        
        Args:
            departamento: Filtro por departamento
            cargo: Filtro por cargo
            ativo: Filtro por status ativo
            skip: Número de registros para pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de funcionários filtrados
        """
        try:
            # Construir query dinâmica
            query_filters = {}
            
            if departamento:
                query_filters["departamento"] = departamento
            
            if cargo:
                query_filters["cargo"] = cargo
            
            if ativo is not None:
                query_filters["ativo"] = ativo
            
            logger.debug(f"🔍 Filtrando funcionários: {query_filters} (skip={skip}, limit={limit})")
            
            # Executar query com filtros e paginação
            cursor = self.collection.find(query_filters).sort("created_at", -1).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            # Converter documentos para entidades
            funcionarios = [FuncionarioModel.to_entity(doc) for doc in documents]
            
            logger.info(f"✅ {len(funcionarios)} funcionários encontrados com filtros")
            return funcionarios
            
        except Exception as e:
            logger.error(f"❌ Erro ao filtrar funcionários: {e}")
            raise ErroOperacaoException(f"Falha ao filtrar funcionários: {e}")
    
    async def contar_total(self) -> int:
        """
        Conta o total de funcionários.
        
        Returns:
            Número total de funcionários
        """
        try:
            count = await self.collection.count_documents({})
            logger.debug(f"📊 Total de funcionários: {count}")
            return count
        except Exception as e:
            logger.error(f"❌ Erro ao contar funcionários: {e}")
            raise ErroOperacaoException(f"Falha ao contar funcionários: {e}")
    
    async def contar_por_filtros(
        self,
        departamento: Optional[str] = None,
        cargo: Optional[str] = None,
        ativo: Optional[bool] = None
    ) -> int:
        """
        Conta funcionários aplicando filtros.
        
        Args:
            departamento: Filtro por departamento
            cargo: Filtro por cargo
            ativo: Filtro por status ativo
            
        Returns:
            Número de funcionários que atendem aos filtros
        """
        try:
            # Construir query dinâmica
            query_filters = {}
            
            if departamento:
                query_filters["departamento"] = departamento
            
            if cargo:
                query_filters["cargo"] = cargo
            
            if ativo is not None:
                query_filters["ativo"] = ativo
            
            count = await self.collection.count_documents(query_filters)
            logger.debug(f"📊 Funcionários com filtros: {count}")
            return count
            
        except Exception as e:
            logger.error(f"❌ Erro ao contar funcionários com filtros: {e}")
            raise ErroOperacaoException(f"Falha ao contar funcionários: {e}")
    
    async def atualizar(self, funcionario: Funcionario) -> Funcionario:
        """
        Atualiza um funcionário existente.
        
        Args:
            funcionario: Funcionário com dados atualizados
            
        Returns:
            Funcionario atualizado
            
        Raises:
            FuncionarioNaoEncontradoException: Se funcionário não existe
        """
        try:
            if not funcionario.id:
                raise DadosInvalidosException("id", "None", "ID do funcionário é obrigatório para atualização")
            
            if not ObjectId.is_valid(funcionario.id):
                raise DadosInvalidosException("id", funcionario.id, "ID do funcionário inválido")
            
            # Definir timestamp de atualização
            funcionario.updated_at = datetime.now()
            
            # Construir documento de atualização (exclui campos imutáveis)
            update_doc = FuncionarioModel.to_update_document(
                funcionario,
                campos_permitidos=["nome", "cargo", "telefone", "departamento", "ativo", "updated_at"]
            )
            
            logger.debug(f"📝 Atualizando funcionário: {funcionario.id}")
            
            # Executar atualização
            result = await self.collection.update_one(
                {"_id": ObjectId(funcionario.id)},
                update_doc
            )
            
            if result.matched_count == 0:
                logger.warning(f"⚠️ Funcionário não encontrado para atualização: {funcionario.id}")
                raise FuncionarioNaoEncontradoException(funcionario.id)
            
            logger.info(f"✅ Funcionário atualizado: {funcionario.nome_completo} ({funcionario.id})")
            return funcionario
            
        except FuncionarioNaoEncontradoException:
            raise
        except DadosInvalidosException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar funcionário: {e}")
            raise ErroOperacaoException(f"Falha ao atualizar funcionário: {e}")
    
    async def excluir(self, funcionario_id: str) -> bool:
        """
        Exclui um funcionário.
        
        Args:
            funcionario_id: ID do funcionário a ser excluído
            
        Returns:
            True se excluído com sucesso, False se não encontrado
        """
        try:
            if not ObjectId.is_valid(funcionario_id):
                raise DadosInvalidosException("id", funcionario_id, "ID do funcionário inválido")
            
            logger.debug(f"🗑️ Excluindo funcionário: {funcionario_id}")
            
            # Executar exclusão
            result = await self.collection.delete_one({"_id": ObjectId(funcionario_id)})
            
            if result.deleted_count > 0:
                logger.info(f"✅ Funcionário excluído: {funcionario_id}")
                return True
            else:
                logger.warning(f"⚠️ Funcionário não encontrado para exclusão: {funcionario_id}")
                return False
            
        except DadosInvalidosException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao excluir funcionário: {e}")
            raise ErroOperacaoException(f"Falha ao excluir funcionário: {e}")
    
    async def verificar_email_existe(self, email: str, excluir_id: Optional[str] = None) -> bool:
        """
        Verifica se um email já existe no sistema.
        
        Args:
            email: Email a ser verificado
            excluir_id: ID a ser excluído da verificação (para updates)
            
        Returns:
            True se email existe, False caso contrário
        """
        try:
            logger.debug(f"✉️ Verificando existência de email: {email}")
            
            # Construir query
            query = {"email": email}
            
            # Excluir ID específico se fornecido (para updates)
            if excluir_id and ObjectId.is_valid(excluir_id):
                query["_id"] = {"$ne": ObjectId(excluir_id)}
            
            # Contar documentos
            count = await self.collection.count_documents(query)
            
            exists = count > 0
            logger.debug(f"📧 Email {'existe' if exists else 'não existe'}: {email}")
            
            return exists
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar email: {e}")
            raise ErroOperacaoException(f"Falha ao verificar email: {e}")
