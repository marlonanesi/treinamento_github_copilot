import pytest
from datetime import date, datetime
from decimal import Decimal
from pydantic import ValidationError

from app.domain.entities.funcionario import Funcionario
from app.domain.entities.value_objects import Email, Cargo, Telefone
from app.domain.exceptions.funcionario_exceptions import (
    DadosInvalidosException,
    FuncionarioAtivoEmProjetosException
)
from tests.factories import create_valid_funcionario

class TestFuncionario:
    """
    🧪 Testes para a entidade Funcionario
    ✅ Sem dependências externas - apenas validações e regras de negócio
    """

    def test_cria_funcionario_valido_com_sucesso(self):
        """✅ HAPPY PATH: Deve criar uma instância de Funcionario com dados válidos."""
        # ARRANGE
        funcionario = create_valid_funcionario(
            nome_completo="Carlos Teste Silva",
            email=Email("carlos.teste@teste.com"),
            cargo=Cargo("Gerente")
        )
        
        # ASSERT
        assert funcionario.nome_completo == "Carlos Teste Silva"
        assert funcionario.email.value == "carlos.teste@teste.com"
        assert funcionario.cargo.value == "Gerente"
        assert funcionario.ativo is False  # Default
        assert funcionario.id is not None

    def test_criar_funcionario_com_factory_method(self):
        """✅ HAPPY PATH: Deve criar funcionário usando método de fábrica."""
        # ARRANGE & ACT
        funcionario = Funcionario.criar(
            nome_completo="João Silva Santos",
            email="joao@empresa.com",
            cargo="Desenvolvedor",
            data_admissao=date(2023, 1, 15),
            telefone="(11) 99999-9999",
            salario=Decimal("5000.00")
        )
        
        # ASSERT
        assert funcionario.nome_completo == "João Silva Santos"
        assert funcionario.email.value == "joao@empresa.com"
        assert funcionario.cargo.value == "Desenvolvedor"
        assert funcionario.telefone.value == "(11) 99999-9999"
        assert funcionario.salario == Decimal("5000.00")

    @pytest.mark.parametrize("nome_invalido", [
        "João",  # Uma palavra só
        "J",     # Muito curto
        "A B",   # Palavras muito curtas
        "",      # Vazio
    ])
    def test_cria_funcionario_com_nome_invalido(self, nome_invalido):
        """❌ Cenário TRISTE: Deve levantar erro ao criar funcionário com nome inválido."""
        # ACT & ASSERT
        with pytest.raises(DadosInvalidosException) as exc_info:
            create_valid_funcionario(nome_completo=nome_invalido)
        
        assert "nome_completo" in str(exc_info.value).lower()

    def test_atualizar_funcionario_com_dados_validos(self):
        """✅ HAPPY PATH: Deve atualizar funcionário com dados válidos."""
        # ARRANGE
        funcionario = create_valid_funcionario()
        updated_at_original = funcionario.updated_at
        
        # ACT
        funcionario.atualizar(
            nome_completo="João Silva Atualizado",
            cargo="Senior Developer",
            salario=Decimal("6000.00")
        )
        
        # ASSERT
        assert funcionario.nome_completo == "João Silva Atualizado"
        assert funcionario.cargo.value == "Senior Developer"
        assert funcionario.salario == Decimal("6000.00")
        assert funcionario.updated_at > updated_at_original

    def test_atualizar_funcionario_preserva_campos_nao_alterados(self):
        """✅ HAPPY PATH: Deve preservar campos não informados na atualização."""
        # ARRANGE
        funcionario = create_valid_funcionario(
            email=Email("original@email.com"),
            departamento="TI Original"
        )
        email_original = funcionario.email
        departamento_original = funcionario.departamento
        
        # ACT
        funcionario.atualizar(cargo="Novo Cargo")
        
        # ASSERT
        assert funcionario.cargo.value == "Novo Cargo"
        assert funcionario.email == email_original  # Preservado
        assert funcionario.departamento == departamento_original  # Preservado

    def test_atualizar_funcionario_com_salario_negativo(self):
        """❌ Cenário TRISTE: Deve rejeitar salário negativo."""
        # ARRANGE
        funcionario = create_valid_funcionario()
        
        # ACT & ASSERT
        with pytest.raises(DadosInvalidosException) as exc_info:
            funcionario.atualizar(salario=Decimal("-1000.00"))
        
        assert "salario" in str(exc_info.value).lower()
        assert "negativo" in str(exc_info.value).lower()

    def test_marcar_funcionario_ativo(self):
        """✅ HAPPY PATH: Deve marcar funcionário como ativo."""
        # ARRANGE
        funcionario = create_valid_funcionario(ativo=False)
        
        # ACT
        funcionario.marcar_ativo()
        
        # ASSERT
        assert funcionario.ativo is True

    def test_desmarcar_funcionario_ativo(self):
        """✅ HAPPY PATH: Deve desmarcar funcionário ativo."""
        # ARRANGE
        funcionario = create_valid_funcionario(ativo=True)
        
        # ACT
        funcionario.desmarcar_ativo()
        
        # ASSERT
        assert funcionario.ativo is False

    def test_pode_ser_excluido_funcionario_inativo(self):
        """✅ HAPPY PATH: Funcionário inativo pode ser excluído."""
        # ARRANGE
        funcionario = create_valid_funcionario(ativo=False)
        
        # ACT & ASSERT
        assert funcionario.pode_ser_excluido() is True

    def test_nao_pode_ser_excluido_funcionario_ativo(self):
        """❌ Cenário TRISTE: Funcionário ativo não pode ser excluído."""
        # ARRANGE
        funcionario = create_valid_funcionario(ativo=True)
        
        # ACT & ASSERT
        assert funcionario.pode_ser_excluido() is False

    def test_validar_exclusao_funcionario_inativo(self):
        """✅ HAPPY PATH: Validação de exclusão passa para funcionário inativo."""
        # ARRANGE
        funcionario = create_valid_funcionario(ativo=False)
        
        # ACT & ASSERT (não deve lançar exceção)
        funcionario.validar_exclusao()

    def test_validar_exclusao_funcionario_ativo(self):
        """❌ Cenário TRISTE: Validação de exclusão falha para funcionário ativo."""
        # ARRANGE
        funcionario = create_valid_funcionario(ativo=True)
        
        # ACT & ASSERT
        with pytest.raises(FuncionarioAtivoEmProjetosException):
            funcionario.validar_exclusao()

    def test_to_dict_converte_corretamente(self):
        """✅ HAPPY PATH: Deve converter funcionário para dicionário."""
        # ARRANGE
        funcionario = create_valid_funcionario(
            nome_completo="João Silva",
            email=Email("joao@test.com"),
            salario=Decimal("5000.00")
        )
        
        # ACT
        funcionario_dict = funcionario.to_dict()
        
        # ASSERT
        assert funcionario_dict["nome_completo"] == "João Silva"
        assert funcionario_dict["email"] == "joao@test.com"
        assert funcionario_dict["salario"] == 5000.0  # Decimal convertido para float
        assert "_id" in funcionario_dict

    def test_from_dict_converte_corretamente(self):
        """✅ HAPPY PATH: Deve criar funcionário a partir de dicionário."""
        # ARRANGE
        funcionario_dict = {
            "_id": "123456789",
            "nome_completo": "Maria Silva",
            "email": "maria@test.com",
            "cargo": "Analista",
            "data_admissao": date(2023, 1, 15),
            "departamento": "TI",
            "salario": 4000.0,
            "ativo": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # ACT
        funcionario = Funcionario.from_dict(funcionario_dict)
        
        # ASSERT
        assert funcionario.id == "123456789"
        assert funcionario.nome_completo == "Maria Silva"
        assert funcionario.email.value == "maria@test.com"
        assert funcionario.cargo.value == "Analista"
        assert funcionario.salario == Decimal("4000.0")

    def test_from_dict_roundtrip_preserva_dados(self):
        """✅ HAPPY PATH: Roundtrip to_dict -> from_dict preserva dados."""
        # ARRANGE
        funcionario_original = create_valid_funcionario()
        
        # ACT
        funcionario_dict = funcionario_original.to_dict()
        funcionario_recriado = Funcionario.from_dict(funcionario_dict)
        
        # ASSERT
        assert funcionario_original == funcionario_recriado
        assert funcionario_original.nome_completo == funcionario_recriado.nome_completo
        assert funcionario_original.email == funcionario_recriado.email
        assert funcionario_original.cargo == funcionario_recriado.cargo

    def test_eq_method_compara_por_id(self):
        """✅ HAPPY PATH: Deve comparar funcionários pelo ID."""
        # ARRANGE
        id_comum = "123e4567-e89b-12d3-a456-426614174000"
        funcionario1 = create_valid_funcionario(
            id=id_comum, 
            email=Email("um@email.com")
        )
        funcionario2 = create_valid_funcionario(
            id=id_comum, 
            email=Email("outro@email.com")
        )
        
        # ACT & ASSERT
        assert funcionario1 == funcionario2

    def test_hash_method_usa_id(self):
        """✅ HAPPY PATH: Hash deve ser baseado no ID."""
        # ARRANGE
        funcionario1 = create_valid_funcionario(id="same-id")
        funcionario2 = create_valid_funcionario(id="same-id")
        funcionario3 = create_valid_funcionario(id="different-id")
        
        # ACT & ASSERT
        assert hash(funcionario1) == hash(funcionario2)
        assert hash(funcionario1) != hash(funcionario3)

    def test_str_representation(self):
        """✅ HAPPY PATH: Representação string deve ser informativa."""
        # ARRANGE
        funcionario = create_valid_funcionario(
            nome_completo="João Silva",
            email=Email("joao@test.com")
        )
        
        # ACT
        str_repr = str(funcionario)
        
        # ASSERT
        assert "João Silva" in str_repr
        assert "joao@test.com" in str_repr

    def test_validar_data_admissao_futura(self):
        """❌ Cenário TRISTE: Data de admissão não pode ser futura."""
        # ARRANGE
        data_futura = date(2030, 12, 31)
        
        # ACT & ASSERT
        with pytest.raises(DadosInvalidosException) as exc_info:
            Funcionario.criar(
                nome_completo="João Silva",
                email="joao@test.com",
                cargo="Desenvolvedor",
                data_admissao=data_futura
            )
        
        assert "data_admissao" in str(exc_info.value).lower()
        assert "futura" in str(exc_info.value).lower()

    def test_validar_data_admissao_muito_antiga(self):
        """❌ Cenário TRISTE: Data de admissão não pode ser muito antiga."""
        # ARRANGE
        data_muito_antiga = date(1970, 1, 1)
        
        # ACT & ASSERT
        with pytest.raises(DadosInvalidosException) as exc_info:
            Funcionario.criar(
                nome_completo="João Silva",
                email="joao@test.com",
                cargo="Desenvolvedor",
                data_admissao=data_muito_antiga
            )
        
        assert "data_admissao" in str(exc_info.value).lower()
        assert "50 anos" in str(exc_info.value).lower()
