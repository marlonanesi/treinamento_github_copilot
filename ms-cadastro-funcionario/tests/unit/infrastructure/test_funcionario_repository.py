import pytest
from unittest.mock import AsyncMock, Mock
from bson import ObjectId
from datetime import datetime
from pymongo.errors import DuplicateKeyError, WriteError

from app.infrastructure.repositories.funcionario_repository_impl import FuncionarioRepositoryImpl
from app.domain.exceptions.funcionario_exceptions import (
    EmailDuplicadoException,
    FuncionarioNaoEncontradoException,
    DadosInvalidosException,
    ErroOperacaoException
)
from tests.factories import create_valid_funcionario

class TestFuncionarioRepositoryImpl:
    """
    🧪 Testes para a camada de infraestrutura
    🚨 ATENÇÃO: Motor Collection SEMPRE mockada via AsyncMock
    ❌ NUNCA conectar com MongoDB real
    """
    
    @pytest.fixture
    def mock_collection(self):
        """🎭 Mock da collection do Motor"""
        collection = AsyncMock()
        # Configurar métodos assíncronos padrão
        collection.insert_one = AsyncMock()
        collection.find_one = AsyncMock()
        collection.update_one = AsyncMock()
        collection.delete_one = AsyncMock()
        collection.find = AsyncMock()
        return collection

    @pytest.fixture
    def mock_database(self, mock_collection):
        """🎭 Mock do database que retorna a collection"""
        db = Mock()
        db.__getitem__.return_value = mock_collection
        return db

    @pytest.fixture
    def repository(self, mock_database):
        """🧪 Instância do repositório com dependencies mockadas"""
        return FuncionarioRepositoryImpl(mock_database)

    @pytest.fixture
    def funcionario_document(self):
        """📄 Documento MongoDB de exemplo"""
        return {
            "_id": ObjectId(),
            "nome_completo": "João Silva",
            "email": "joao@empresa.com",
            "cargo": "Desenvolvedor",
            "data_admissao": datetime(2023, 1, 15),
            "telefone": "(11) 99999-9999",
            "departamento": "Tecnologia",
            "salario": 5000.0,
            "ativo": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

    @pytest.mark.asyncio
    async def test_salvar_chama_insert_one_com_documento_correto(self, repository, mock_collection):
        """
        ✅ HAPPY PATH: Deve chamar `insert_one` do Motor com documento mapeado corretamente.
        🎭 Mock verifica chamada sem executar operação real
        """
        # ARRANGE
        funcionario = create_valid_funcionario()
        mock_result = Mock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one.return_value = mock_result
        
        # ACT
        resultado = await repository.salvar(funcionario)
        
        # ASSERT
        # Verifica se Motor foi chamado
        mock_collection.insert_one.assert_called_once()
        
        # Verifica se documento foi criado corretamente
        call_args = mock_collection.insert_one.call_args[0][0]
        assert call_args["nome_completo"] == funcionario.nome_completo
        assert call_args["email"] == funcionario.email.value
        assert call_args["cargo"] == funcionario.cargo.value
        assert "_id" not in call_args  # ID removido para inserção
        
        # Verifica se ID foi atribuído ao funcionário
        assert resultado.id == str(mock_result.inserted_id)

    @pytest.mark.asyncio
    async def test_salvar_com_email_duplicado_lanca_excecao(self, repository, mock_collection):
        """
        ❌ Cenário TRISTE: Deve lançar EmailDuplicadoException em caso de email duplicado.
        """
        # ARRANGE
        funcionario = create_valid_funcionario()
        mock_collection.insert_one.side_effect = DuplicateKeyError("E11000 duplicate key")
        
        # ACT & ASSERT
        with pytest.raises(EmailDuplicadoException) as exc_info:
            await repository.salvar(funcionario)
        
        assert funcionario.email.value in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_salvar_com_write_error_lanca_excecao(self, repository, mock_collection):
        """
        ❌ Cenário TRISTE: Deve lançar DadosInvalidosException em caso de erro de validação.
        """
        # ARRANGE
        funcionario = create_valid_funcionario()
        mock_collection.insert_one.side_effect = WriteError("Validation failed")
        
        # ACT & ASSERT
        with pytest.raises(DadosInvalidosException):
            await repository.salvar(funcionario)

    @pytest.mark.asyncio
    async def test_buscar_por_id_chama_find_one_com_filtro_correto(self, repository, mock_collection, funcionario_document):
        """
        ✅ HAPPY PATH: Deve chamar `find_one` do Motor com filtro "_id" correto.
        """
        # ARRANGE
        funcionario_id = str(funcionario_document["_id"])
        mock_collection.find_one.return_value = funcionario_document
        
        # ACT
        resultado = await repository.buscar_por_id(funcionario_id)
        
        # ASSERT
        # Verifica chamada para MongoDB
        mock_collection.find_one.assert_called_once_with({"_id": ObjectId(funcionario_id)})
        
        # Verifica conversão para entidade
        assert resultado is not None
        assert resultado.nome_completo == funcionario_document["nome_completo"]
        assert resultado.email.value == funcionario_document["email"]

    @pytest.mark.asyncio
    async def test_buscar_por_id_com_id_invalido_retorna_none(self, repository, mock_collection):
        """
        ❌ Cenário TRISTE: Deve retornar None para ID inválido.
        """
        # ARRANGE
        id_invalido = "id_invalido_nao_objectid"
        
        # ACT
        resultado = await repository.buscar_por_id(id_invalido)
        
        # ASSERT
        assert resultado is None
        # Não deve chamar o MongoDB para IDs inválidos
        mock_collection.find_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_buscar_por_id_nao_encontrado_retorna_none(self, repository, mock_collection):
        """
        ❌ Cenário TRISTE: Deve retornar None quando funcionário não existe.
        """
        # ARRANGE
        funcionario_id = str(ObjectId())
        mock_collection.find_one.return_value = None
        
        # ACT
        resultado = await repository.buscar_por_id(funcionario_id)
        
        # ASSERT
        assert resultado is None

    @pytest.mark.asyncio
    async def test_buscar_por_email_chama_find_one_com_filtro_email(self, repository, mock_collection, funcionario_document):
        """
        ✅ HAPPY PATH: Deve chamar `find_one` com filtro de email correto.
        """
        # ARRANGE
        email = funcionario_document["email"]
        mock_collection.find_one.return_value = funcionario_document
        
        # ACT
        resultado = await repository.buscar_por_email(email)
        
        # ASSERT
        mock_collection.find_one.assert_called_once_with({"email": email})
        assert resultado is not None
        assert resultado.email.value == email

    @pytest.mark.asyncio
    async def test_atualizar_chama_update_one_com_filtro_e_documento_corretos(self, repository, mock_collection):
        """
        ✅ HAPPY PATH: Deve chamar `update_one` com filtro e documento de atualização corretos.
        """
        # ARRANGE
        funcionario = create_valid_funcionario()
        funcionario.id = str(ObjectId())
        
        # Mock para simular sucesso na atualização
        mock_result = Mock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        
        # ACT
        resultado = await repository.atualizar(funcionario)
        
        # ASSERT
        # Verifica se update_one foi chamado
        mock_collection.update_one.assert_called_once()
        
        # Verifica parâmetros da chamada
        call_args = mock_collection.update_one.call_args
        filtro = call_args[0][0]
        update_doc = call_args[0][1]
        
        assert filtro == {"_id": ObjectId(funcionario.id)}
        assert "$set" in update_doc
        assert update_doc["$set"]["nome_completo"] == funcionario.nome_completo
        
        # Verifica retorno
        assert resultado == funcionario

    @pytest.mark.asyncio
    async def test_atualizar_funcionario_nao_encontrado_lanca_excecao(self, repository, mock_collection):
        """
        ❌ Cenário TRISTE: Deve lançar exceção quando funcionário não existe para atualização.
        """
        # ARRANGE
        funcionario = create_valid_funcionario()
        funcionario.id = str(ObjectId())
        
        mock_result = Mock()
        mock_result.modified_count = 0  # Nenhum documento modificado
        mock_collection.update_one.return_value = mock_result
        
        # ACT & ASSERT
        with pytest.raises(FuncionarioNaoEncontradoException):
            await repository.atualizar(funcionario)

    @pytest.mark.asyncio
    async def test_excluir_chama_delete_one_com_filtro_correto(self, repository, mock_collection):
        """
        ✅ HAPPY PATH: Deve chamar `delete_one` com o filtro "_id" correto.
        """
        # ARRANGE
        funcionario_id = str(ObjectId())
        mock_result = Mock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        
        # ACT
        resultado = await repository.excluir(funcionario_id)
        
        # ASSERT
        mock_collection.delete_one.assert_called_once_with({"_id": ObjectId(funcionario_id)})
        assert resultado is True

    @pytest.mark.asyncio
    async def test_excluir_funcionario_nao_encontrado_retorna_false(self, repository, mock_collection):
        """
        ❌ Cenário TRISTE: Deve retornar False quando funcionário não existe para exclusão.
        """
        # ARRANGE
        funcionario_id = str(ObjectId())
        mock_result = Mock()
        mock_result.deleted_count = 0
        mock_collection.delete_one.return_value = mock_result
        
        # ACT
        resultado = await repository.excluir(funcionario_id)
        
        # ASSERT
        assert resultado is False

    @pytest.mark.asyncio
    async def test_listar_por_filtros_aplica_filtros_corretamente(self, repository, mock_collection):
        """
        ✅ HAPPY PATH: Deve aplicar filtros e paginação corretamente na query.
        """
        # ARRANGE
        mock_cursor = AsyncMock()
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        mock_cursor.to_list.return_value = []
        mock_collection.find.return_value = mock_cursor
        
        # ACT
        await repository.listar_por_filtros(
            departamento="Tecnologia",
            cargo="Desenvolvedor",
            ativo=False,
            skip=10,
            limit=5
        )
        
        # ASSERT
        # Verifica filtros aplicados
        expected_filter = {
            "departamento": "Tecnologia",
            "cargo": "Desenvolvedor",
            "ativo": False
        }
        mock_collection.find.assert_called_once_with(expected_filter)
        
        # Verifica paginação
        mock_cursor.skip.assert_called_once_with(10)
        mock_cursor.limit.assert_called_once_with(5)

    @pytest.mark.asyncio
    async def test_listar_por_filtros_sem_filtros_busca_todos(self, repository, mock_collection):
        """
        ✅ HAPPY PATH: Deve buscar todos quando nenhum filtro é aplicado.
        """
        # ARRANGE
        mock_cursor = AsyncMock()
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        mock_cursor.to_list.return_value = []
        mock_collection.find.return_value = mock_cursor
        
        # ACT
        await repository.listar_por_filtros()
        
        # ASSERT
        # Sem filtros, deve buscar com filtro vazio
        mock_collection.find.assert_called_once_with({})

    @pytest.mark.asyncio
    async def test_verificar_email_existe_encontra_email_existente(self, repository, mock_collection, funcionario_document):
        """
        ✅ HAPPY PATH: Deve encontrar email existente no sistema.
        """
        # ARRANGE
        email = "joao@empresa.com"
        mock_collection.find_one.return_value = funcionario_document
        
        # ACT
        existe = await repository.verificar_email_existe(email)
        
        # ASSERT
        assert existe is True
        mock_collection.find_one.assert_called_once_with({"email": email})

    @pytest.mark.asyncio
    async def test_verificar_email_existe_com_exclusao_id(self, repository, mock_collection):
        """
        ✅ HAPPY PATH: Deve excluir ID específico da verificação de email.
        """
        # ARRANGE
        email = "joao@empresa.com"
        excluir_id = str(ObjectId())
        mock_collection.find_one.return_value = None
        
        # ACT
        existe = await repository.verificar_email_existe(email, excluir_id)
        
        # ASSERT
        expected_filter = {
            "email": email,
            "_id": {"$ne": ObjectId(excluir_id)}
        }
        mock_collection.find_one.assert_called_once_with(expected_filter)
        assert existe is False
