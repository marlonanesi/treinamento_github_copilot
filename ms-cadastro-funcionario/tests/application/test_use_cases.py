"""
Testes para a camada de aplicação - casos de uso.
"""

import pytest
from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.application.dto.requests import CriarFuncionarioRequest, BuscarFuncionarioRequest
from app.application.dto.responses import FuncionarioResponse
from app.application.exceptions import ValidationException, ResourceNotFoundException, DuplicateResourceException
from app.application.use_cases.criar_funcionario import CriarFuncionarioUseCase
from app.application.use_cases.buscar_funcionario import BuscarFuncionarioUseCase
from app.domain.entities.funcionario import Funcionario


class TestCriarFuncionarioUseCase:
    """Testes para o caso de uso de criação de funcionário."""
    
    @pytest.fixture
    def mock_repository(self):
        """Cria um mock do repositório para testes."""
        repository = AsyncMock()
        return repository
    
    @pytest.fixture  
    def use_case(self, mock_repository):
        """Cria instância do caso de uso com repositório mock."""
        return CriarFuncionarioUseCase(mock_repository)
    
    @pytest.fixture
    def valid_request(self):
        """Cria uma requisição válida para testes."""
        return CriarFuncionarioRequest(
            nome_completo="João da Silva",
            cpf="12345678901",
            email="joao@example.com",
            telefone="(11) 99999-9999",
            endereco="Rua A, 123",
            data_nascimento=date(1990, 1, 1),
            cargo="Desenvolvedor",
            departamento="TI",
            salario=Decimal("5000.00"),
            data_admissao=date.today()
        )
    
    async def test_criar_funcionario_sucesso(self, use_case, mock_repository, valid_request):
        """Testa criação bem-sucedida de funcionário."""
        # Arrange
        funcionario_criado = Funcionario(
            nome_completo=valid_request.nome_completo,
            cpf=valid_request.cpf,
            email=valid_request.email,
            telefone=valid_request.telefone,
            endereco=valid_request.endereco,
            data_nascimento=valid_request.data_nascimento,
            cargo=valid_request.cargo,
            departamento=valid_request.departamento,
            salario=valid_request.salario,
            data_admissao=valid_request.data_admissao
        )
        funcionario_criado.id = "123"
        
        mock_repository.buscar_por_cpf.return_value = None
        mock_repository.buscar_por_email.return_value = None
        mock_repository.criar.return_value = funcionario_criado
        
        # Act
        response = await use_case.execute(valid_request)
        
        # Assert
        assert response.id == "123"
        assert response.nome_completo == valid_request.nome_completo
        assert response.cpf == valid_request.cpf
        assert response.email == valid_request.email
        mock_repository.criar.assert_called_once()
    
    async def test_validacao_nome_invalido(self, use_case, mock_repository):
        """Testa validação de nome inválido."""
        # Arrange
        request = CriarFuncionarioRequest(
            nome_completo="J",  # Nome muito curto
            cpf="12345678901",
            email="joao@example.com"
        )
        
        # Act & Assert
        with pytest.raises(ValidationException) as exc_info:
            await use_case.execute(request)
        
        assert exc_info.value.details["field"] == "nome_completo"
    
    async def test_cpf_duplicado(self, use_case, mock_repository, valid_request):
        """Testa validação de CPF duplicado."""
        # Arrange
        funcionario_existente = Funcionario(
            nome_completo="Outro funcionário",
            cpf=valid_request.cpf,
            email="outro@example.com"
        )
        funcionario_existente.id = "456"
        
        mock_repository.buscar_por_cpf.return_value = funcionario_existente
        
        # Act & Assert
        with pytest.raises(DuplicateResourceException) as exc_info:
            await use_case.execute(valid_request)
        
        assert exc_info.value.details["field"] == "CPF"


class TestBuscarFuncionarioUseCase:
    """Testes para o caso de uso de busca de funcionário."""
    
    @pytest.fixture
    def mock_repository(self):
        """Cria um mock do repositório para testes."""
        return AsyncMock()
    
    @pytest.fixture
    def use_case(self, mock_repository):
        """Cria instância do caso de uso com repositório mock."""
        return BuscarFuncionarioUseCase(mock_repository)
    
    async def test_buscar_funcionario_sucesso(self, use_case, mock_repository):
        """Testa busca bem-sucedida de funcionário."""
        # Arrange
        funcionario_id = "123"
        funcionario = Funcionario(
            nome_completo="João da Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        funcionario.id = funcionario_id
        
        mock_repository.buscar_por_id.return_value = funcionario
        
        request = BuscarFuncionarioRequest(funcionario_id=funcionario_id)
        
        # Act
        response = await use_case.execute(request)
        
        # Assert
        assert response.id == funcionario_id
        assert response.nome_completo == funcionario.nome_completo
        mock_repository.buscar_por_id.assert_called_once_with(funcionario_id)
    
    async def test_funcionario_nao_encontrado(self, use_case, mock_repository):
        """Testa busca de funcionário inexistente."""
        # Arrange
        funcionario_id = "999"
        mock_repository.buscar_por_id.return_value = None
        
        request = BuscarFuncionarioRequest(funcionario_id=funcionario_id)
        
        # Act & Assert
        with pytest.raises(ResourceNotFoundException) as exc_info:
            await use_case.execute(request)
        
        assert exc_info.value.details["identifier"] == funcionario_id
    
    async def test_validacao_id_invalido(self, use_case, mock_repository):
        """Testa validação de ID inválido."""
        # Arrange
        request = BuscarFuncionarioRequest(funcionario_id="")
        
        # Act & Assert
        with pytest.raises(ValidationException) as exc_info:
            await use_case.execute(request)
        
        assert exc_info.value.details["field"] == "funcionario_id"
