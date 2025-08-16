import pytest
from unittest.mock import AsyncMock
from datetime import date
from decimal import Decimal

from app.application.use_cases.criar_funcionario import CriarFuncionarioUseCase
from app.application.dto.requests import CriarFuncionarioRequest
from app.application.dto.responses import FuncionarioResponse
from app.application.exceptions import ValidationException, DuplicateResourceException
from app.domain.entities.funcionario import Funcionario
from app.domain.entities.value_objects import Email, Cargo, Telefone
from tests.mocks import FuncionarioRepositoryMock
from tests.factories import create_valid_funcionario

class TestCriarFuncionarioUseCase:
    """
    🧪 Testes para o caso de uso de criar funcionários
    ⚠️ OBRIGATÓRIO: Repositórios SEMPRE mockados
    """

    @pytest.fixture
    def mock_repo(self):
        return FuncionarioRepositoryMock()

    @pytest.fixture
    def use_case(self, mock_repo):
        return CriarFuncionarioUseCase(funcionario_repository=mock_repo)

    @pytest.fixture
    def request_funcionario_valido(self):
        return CriarFuncionarioRequest(
            nome_completo="João Silva Santos",
            email="joao@empresa.com",
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15),
            telefone="(11) 99999-9999",
            departamento="Tecnologia",
            salario=Decimal("5000.00")
        )

    @pytest.mark.asyncio
    async def test_cria_funcionario_com_sucesso(self, use_case, mock_repo, request_funcionario_valido):
        """✅ HAPPY PATH: Deve criar funcionário com dados válidos."""
        # ARRANGE
        # Mock repository não tem funcionário com este email
        
        # ACT
        response = await use_case.execute(request_funcionario_valido)
        
        # ASSERT
        assert isinstance(response, FuncionarioResponse)
        assert response.nome_completo == "João Silva Santos"
        assert response.email == "joao@empresa.com"
        assert response.cargo == "Desenvolvedor"
        assert response.id is not None  # ID foi atribuído

        # Verifica se funcionário foi salvo no mock repository
        funcionario_salvo = await mock_repo.buscar_por_email("joao@empresa.com")
        assert funcionario_salvo is not None
        assert funcionario_salvo.nome_completo == "João Silva Santos"

    @pytest.mark.asyncio
    async def test_cria_funcionario_com_campos_opcionais(self, use_case, mock_repo):
        """✅ HAPPY PATH: Deve criar funcionário com apenas campos obrigatórios."""
        # ARRANGE
        request = CriarFuncionarioRequest(
            nome_completo="Maria Silva",
            email="maria@empresa.com",
            cargo="Analista",
            data_admissao=date(2023, 2, 1)
        )
        
        # ACT
        response = await use_case.execute(request)
        
        # ASSERT
        assert response.nome_completo == "Maria Silva"
        assert response.email == "maria@empresa.com"
        assert response.cargo == "Analista"
        assert response.telefone is None
        assert response.departamento is None

    @pytest.mark.asyncio
    async def test_cria_funcionario_com_email_duplicado(self, use_case, mock_repo):
        """❌ Cenário TRISTE: Deve rejeitar funcionário com email existente."""
        # ARRANGE
        # Primeiro, criar um funcionário existente
        funcionario_existente = create_valid_funcionario(
            email=Email("joao@empresa.com")
        )
        await mock_repo.salvar(funcionario_existente)
        
        request = CriarFuncionarioRequest(
            nome_completo="João Duplicado",
            email="joao@empresa.com",  # Email já existe
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15)
        )
        
        # ACT & ASSERT
        with pytest.raises(DuplicateResourceException) as exc_info:
            await use_case.execute(request)
        
        assert "email" in str(exc_info.value).lower()
        assert "joao@empresa.com" in str(exc_info.value)

    @pytest.mark.parametrize("nome_invalido", [
        "",          # Vazio
        "A",         # Muito curto
        "   ",       # Apenas espaços
        None         # None
    ])
    @pytest.mark.asyncio
    async def test_cria_funcionario_com_nome_invalido(self, use_case, nome_invalido):
        """❌ Cenário TRISTE: Deve rejeitar nomes inválidos."""
        # ARRANGE
        request = CriarFuncionarioRequest(
            nome_completo=nome_invalido,
            email="joao@empresa.com",
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15)
        )
        
        # ACT & ASSERT
        with pytest.raises(ValidationException) as exc_info:
            await use_case.execute(request)
        
        assert "nome_completo" in str(exc_info.value)

    @pytest.mark.parametrize("email_invalido", [
        "",                  # Vazio
        "email-sem-arroba",  # Sem @
        "sem-dominio@",      # Sem domínio
        "@sem-usuario.com",  # Sem usuário
        None                 # None
    ])
    @pytest.mark.asyncio
    async def test_cria_funcionario_com_email_invalido(self, use_case, email_invalido):
        """❌ Cenário TRISTE: Deve rejeitar emails inválidos."""
        # ARRANGE
        request = CriarFuncionarioRequest(
            nome_completo="João Silva",
            email=email_invalido,
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15)
        )
        
        # ACT & ASSERT
        with pytest.raises(ValidationException) as exc_info:
            await use_case.execute(request)
        
        assert "email" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_cria_funcionario_com_data_nascimento_futura(self, use_case):
        """❌ Cenário TRISTE: Deve rejeitar data de nascimento futura."""
        # ARRANGE
        data_futura = date(2030, 12, 31)
        request = CriarFuncionarioRequest(
            nome_completo="João Silva",
            email="joao@empresa.com",
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15),
            data_nascimento=data_futura
        )
        
        # ACT & ASSERT
        with pytest.raises(ValidationException) as exc_info:
            await use_case.execute(request)
        
        assert "data_nascimento" in str(exc_info.value).lower()
        assert "passado" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_cria_funcionario_com_salario_negativo(self, use_case):
        """❌ Cenário TRISTE: Deve rejeitar salário negativo."""
        # ARRANGE
        request = CriarFuncionarioRequest(
            nome_completo="João Silva",
            email="joao@empresa.com",
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15),
            salario=Decimal("-1000.00")
        )
        
        # ACT & ASSERT
        with pytest.raises(ValidationException) as exc_info:
            await use_case.execute(request)
        
        assert "salario" in str(exc_info.value).lower()
        assert "maior que zero" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_cria_funcionario_com_cpf_invalido(self, use_case):
        """❌ Cenário TRISTE: Deve rejeitar CPF com formato inválido."""
        # ARRANGE
        request = CriarFuncionarioRequest(
            nome_completo="João Silva",
            email="joao@empresa.com",
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15),
            cpf="123456"  # CPF muito curto
        )
        
        # ACT & ASSERT
        with pytest.raises(ValidationException) as exc_info:
            await use_case.execute(request)
        
        assert "cpf" in str(exc_info.value).lower()
        assert "11 dígitos" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_cria_funcionario_sem_data_admissao_usa_hoje(self, use_case):
        """✅ HAPPY PATH: Deve usar data atual quando data_admissao não informada."""
        # ARRANGE
        request = CriarFuncionarioRequest(
            nome_completo="João Silva",
            email="joao@empresa.com",
            cargo="Desenvolvedor"
            # data_admissao não informada
        )
        
        # ACT
        response = await use_case.execute(request)
        
        # ASSERT
        assert response.data_admissao == date.today()

    @pytest.mark.asyncio
    async def test_cria_funcionario_normaliza_nome(self, use_case):
        """✅ HAPPY PATH: Deve normalizar nome removendo espaços extras."""
        # ARRANGE
        request = CriarFuncionarioRequest(
            nome_completo="   João Silva Santos   ",  # Espaços extras
            email="joao@empresa.com",
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15)
        )
        
        # ACT
        response = await use_case.execute(request)
        
        # ASSERT
        assert response.nome_completo == "João Silva Santos"  # Sem espaços extras

    @pytest.mark.asyncio
    async def test_cria_funcionario_converte_value_objects(self, use_case, mock_repo):
        """✅ HAPPY PATH: Deve criar value objects corretamente."""
        # ARRANGE
        request = CriarFuncionarioRequest(
            nome_completo="João Silva",
            email="JOAO@EMPRESA.COM",  # Maiúscula - deve normalizar
            cargo="desenvolvedor senior",  # Minúscula - deve normalizar
            telefone="11999999999",  # Sem formatação - deve formatar
            data_admissao=date(2023, 1, 15)
        )
        
        # ACT
        response = await use_case.execute(request)
        
        # ASSERT
        # Verificar se value objects foram criados e normalizados
        funcionario_salvo = await mock_repo.buscar_por_email("joao@empresa.com")
        assert funcionario_salvo.email.value == "joao@empresa.com"  # Normalizado
        assert funcionario_salvo.cargo.value == "Desenvolvedor Senior"  # Normalizado
        assert funcionario_salvo.telefone.value == "(11) 99999-9999"  # Formatado

    @pytest.mark.asyncio
    async def test_cria_funcionario_retorna_response_correto(self, use_case, request_funcionario_valido):
        """✅ HAPPY PATH: Deve retornar FuncionarioResponse com dados corretos."""
        # ACT
        response = await use_case.execute(request_funcionario_valido)
        
        # ASSERT
        assert isinstance(response, FuncionarioResponse)
        assert response.nome_completo == request_funcionario_valido.nome_completo
        assert response.email == request_funcionario_valido.email
        assert response.cargo == request_funcionario_valido.cargo
        assert response.data_admissao == request_funcionario_valido.data_admissao
        assert response.telefone == request_funcionario_valido.telefone
        assert response.departamento == request_funcionario_valido.departamento
        assert response.salario == request_funcionario_valido.salario
        assert response.id is not None
        assert response.created_at is not None
        assert response.updated_at is not None
