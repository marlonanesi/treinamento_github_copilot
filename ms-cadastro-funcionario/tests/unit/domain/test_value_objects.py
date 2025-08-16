import pytest
from pydantic import ValidationError

from app.domain.entities.value_objects import Email, Cargo, Telefone, TiposCargo
from app.domain.exceptions.funcionario_exceptions import (
    DadosInvalidosException,
    CargoInvalidoException
)

class TestEmail:
    """
    🧪 Testes para o Value Object Email
    ✅ Sem dependências externas - apenas validações
    """

    @pytest.fixture(params=[
        "joao@empresa.com",
        "MARIA@EMPRESA.COM.BR", 
        "teste.email+tag@dominio.co",
        "user123@domain-with-dash.org",
        "simple@test.co"
    ])
    def emails_validos(self, request):
        return request.param

    @pytest.fixture(params=[
        "email-sem-arroba.com",
        "@dominio.com",
        "email@",
        "email@dominio",
        "email..duplo@dominio.com",
        "",
        None
    ])
    def emails_invalidos(self, request):
        return request.param

    def test_cria_email_valido_normalizado(self, emails_validos):
        """✅ HAPPY PATH: Email válido é normalizado para lowercase."""
        # ACT
        email = Email(emails_validos)
        
        # ASSERT
        assert email.value == emails_validos.strip().lower()
        assert isinstance(email.value, str)

    def test_cria_email_invalido_lanca_excecao(self, emails_invalidos):
        """❌ Cenário TRISTE: Email inválido lança DadosInvalidosException."""
        # ACT & ASSERT
        with pytest.raises(DadosInvalidosException) as exc_info:
            Email(emails_invalidos)
        
        assert "email" in str(exc_info.value).lower()

    def test_is_valid_identifica_emails_validos(self, emails_validos):
        """✅ HAPPY PATH: is_valid identifica emails válidos corretamente."""
        # ACT & ASSERT
        assert Email.is_valid(emails_validos) is True

    def test_is_valid_identifica_emails_invalidos(self, emails_invalidos):
        """❌ Cenário TRISTE: is_valid identifica emails inválidos corretamente."""
        # ACT & ASSERT
        assert Email.is_valid(emails_invalidos) is False

    def test_email_equality_com_string(self):
        """✅ HAPPY PATH: Email deve ser igual a string normalizada."""
        # ARRANGE
        email = Email("JOAO@EMPRESA.COM")
        
        # ACT & ASSERT
        assert email == "joao@empresa.com"
        assert email == "JOAO@EMPRESA.COM"  # Normalização automática
        assert email != "diferente@email.com"

    def test_email_equality_com_outro_email(self):
        """✅ HAPPY PATH: Emails com mesmo valor devem ser iguais."""
        # ARRANGE
        email1 = Email("joao@empresa.com")
        email2 = Email("JOAO@EMPRESA.COM")
        email3 = Email("maria@empresa.com")
        
        # ACT & ASSERT
        assert email1 == email2  # Mesmos emails normalizados
        assert email1 != email3  # Emails diferentes

    def test_email_hash_consistency(self):
        """✅ HAPPY PATH: Emails iguais devem ter mesmo hash."""
        # ARRANGE
        email1 = Email("joao@empresa.com")
        email2 = Email("JOAO@EMPRESA.COM")
        
        # ACT & ASSERT
        assert hash(email1) == hash(email2)

    def test_email_str_representation(self):
        """✅ HAPPY PATH: Representação string deve retornar valor."""
        # ARRANGE
        email = Email("JOAO@EMPRESA.COM")
        
        # ACT & ASSERT
        assert str(email) == "joao@empresa.com"

    def test_email_repr_representation(self):
        """✅ HAPPY PATH: Representação deve ser informativa."""
        # ARRANGE
        email = Email("joao@empresa.com")
        
        # ACT
        repr_str = repr(email)
        
        # ASSERT
        assert "Email" in repr_str
        assert "joao@empresa.com" in repr_str


class TestTiposCargo:
    """
    🧪 Testes para o Enum TiposCargo
    ✅ Sem dependências externas
    """

    def test_get_all_values_retorna_lista_completa(self):
        """✅ HAPPY PATH: Deve retornar todos os valores de cargo válidos."""
        # ACT
        valores = TiposCargo.get_all_values()
        
        # ASSERT
        assert isinstance(valores, list)
        assert len(valores) > 0
        assert "Desenvolvedor Junior" in valores
        assert "Desenvolvedor Senior" in valores
        assert "Gerente de Projetos" in valores

    def test_is_valid_identifica_cargo_valido(self):
        """✅ HAPPY PATH: Deve identificar cargos válidos."""
        # ARRANGE
        cargo_valido = "Desenvolvedor Senior"
        
        # ACT & ASSERT
        assert TiposCargo.is_valid(cargo_valido) is True

    def test_is_valid_identifica_cargo_invalido(self):
        """❌ Cenário TRISTE: Deve identificar cargos inválidos."""
        # ARRANGE
        cargo_invalido = "Cargo Inexistente"
        
        # ACT & ASSERT
        assert TiposCargo.is_valid(cargo_invalido) is False


class TestCargo:
    """
    🧪 Testes para o Value Object Cargo
    ✅ Sem dependências externas - apenas validações
    """

    @pytest.fixture(params=[
        "Desenvolvedor Junior",
        "desenvolvedor senior",
        "GERENTE DE PROJETOS",
        "Analista de Sistemas"
    ])
    def cargos_predefinidos(self, request):
        return request.param

    @pytest.fixture(params=[
        "Cargo Personalizado",
        "novo cargo customizado",
        "ESPECIALISTA EM IA"
    ])
    def cargos_personalizados(self, request):
        return request.param

    def test_cria_cargo_predefinido_com_sucesso(self, cargos_predefinidos):
        """✅ HAPPY PATH: Cargo pré-definido é aceito e normalizado."""
        # ACT
        cargo = Cargo(cargos_predefinidos)
        
        # ASSERT
        assert cargo.value == cargos_predefinidos.strip().title()
        assert cargo.is_predefined is True

    def test_cria_cargo_personalizado_permitido(self, cargos_personalizados):
        """✅ HAPPY PATH: Cargo personalizado é aceito quando permitido."""
        # ACT
        cargo = Cargo(cargos_personalizados, permitir_cargo_personalizado=True)
        
        # ASSERT
        assert cargo.value == cargos_personalizados.strip().title()
        assert cargo.is_predefined is False

    def test_cria_cargo_personalizado_nao_permitido(self, cargos_personalizados):
        """❌ Cenário TRISTE: Cargo personalizado é rejeitado quando não permitido."""
        # ACT & ASSERT
        with pytest.raises(CargoInvalidoException) as exc_info:
            Cargo(cargos_personalizados, permitir_cargo_personalizado=False)
        
        assert cargos_personalizados.strip().title() in str(exc_info.value)

    @pytest.mark.parametrize("cargo_invalido", [
        "",
        "A",  # Muito curto
        "   ",  # Apenas espaços
        None
    ])
    def test_cria_cargo_com_valor_invalido(self, cargo_invalido):
        """❌ Cenário TRISTE: Valores inválidos devem ser rejeitados."""
        # ACT & ASSERT
        with pytest.raises(DadosInvalidosException) as exc_info:
            Cargo(cargo_invalido)
        
        assert "cargo" in str(exc_info.value).lower()

    def test_cargo_equality_com_string(self):
        """✅ HAPPY PATH: Cargo deve ser igual a string normalizada."""
        # ARRANGE
        cargo = Cargo("desenvolvedor senior")
        
        # ACT & ASSERT
        assert cargo == "Desenvolvedor Senior"
        assert cargo == "desenvolvedor senior"
        assert cargo != "Analista"

    def test_cargo_equality_com_outro_cargo(self):
        """✅ HAPPY PATH: Cargos com mesmo valor devem ser iguais."""
        # ARRANGE
        cargo1 = Cargo("desenvolvedor senior")
        cargo2 = Cargo("DESENVOLVEDOR SENIOR")
        cargo3 = Cargo("Analista")
        
        # ACT & ASSERT
        assert cargo1 == cargo2
        assert cargo1 != cargo3

    def test_cargo_hash_consistency(self):
        """✅ HAPPY PATH: Cargos iguais devem ter mesmo hash."""
        # ARRANGE
        cargo1 = Cargo("desenvolvedor senior")
        cargo2 = Cargo("DESENVOLVEDOR SENIOR")
        
        # ACT & ASSERT
        assert hash(cargo1) == hash(cargo2)

    def test_cargo_str_representation(self):
        """✅ HAPPY PATH: Representação string deve retornar valor normalizado."""
        # ARRANGE
        cargo = Cargo("desenvolvedor senior")
        
        # ACT & ASSERT
        assert str(cargo) == "Desenvolvedor Senior"


class TestTelefone:
    """
    🧪 Testes para o Value Object Telefone
    ✅ Sem dependências externas - apenas validações
    """

    @pytest.fixture(params=[
        "(11) 99999-9999",  # Celular
        "(11) 9999-9999",   # Fixo
        "(21) 88888-8888",  # Celular
        "(47) 3333-4444"    # Fixo
    ])
    def telefones_validos(self, request):
        return request.param

    @pytest.fixture(params=[
        "11999999999",      # Sem formatação
        "(11) 999999999",   # Com parênteses
        "11 99999-9999",    # Sem parênteses
        "11 9999-9999"      # Fixo sem parênteses
    ])
    def telefones_para_normalizar(self, request):
        return request.param

    @pytest.fixture(params=[
        "(11) 999-9999",    # Muito curto
        "(111) 9999-9999",  # DDD muito grande
        "123456789",        # Muito curto
        "+55 11 99999-9999", # Formato internacional
        "",                 # Vazio
        None
    ])
    def telefones_invalidos(self, request):
        return request.param

    def test_cria_telefone_valido(self, telefones_validos):
        """✅ HAPPY PATH: Telefone válido é aceito."""
        # ACT
        telefone = Telefone(telefones_validos)
        
        # ASSERT
        assert telefone.value == telefones_validos
        assert isinstance(telefone.value, str)

    def test_normaliza_telefone_corretamente(self):
        """✅ HAPPY PATH: Telefone deve ser normalizado para formato padrão."""
        # ARRANGE & ACT
        telefone_celular = Telefone("11999999999")
        telefone_fixo = Telefone("1133334444")
        
        # ASSERT
        assert telefone_celular.value == "(11) 99999-9999"
        assert telefone_fixo.value == "(11) 3333-4444"

    def test_cria_telefone_invalido_lanca_excecao(self, telefones_invalidos):
        """❌ Cenário TRISTE: Telefone inválido lança DadosInvalidosException."""
        # ACT & ASSERT
        with pytest.raises(DadosInvalidosException) as exc_info:
            Telefone(telefones_invalidos)
        
        assert "telefone" in str(exc_info.value).lower()

    def test_is_valid_identifica_telefones_validos(self, telefones_validos):
        """✅ HAPPY PATH: is_valid identifica telefones válidos."""
        # ACT & ASSERT
        assert Telefone.is_valid(telefones_validos) is True

    def test_is_valid_identifica_telefones_invalidos(self, telefones_invalidos):
        """❌ Cenário TRISTE: is_valid identifica telefones inválidos."""
        # ACT & ASSERT
        assert Telefone.is_valid(telefones_invalidos) is False

    def test_telefone_equality_com_string(self):
        """✅ HAPPY PATH: Telefone deve ser igual a string equivalente."""
        # ARRANGE
        telefone = Telefone("(11) 99999-9999")
        
        # ACT & ASSERT
        assert telefone == "(11) 99999-9999"

    def test_telefone_equality_com_outro_telefone(self):
        """✅ HAPPY PATH: Telefones iguais devem ser comparados corretamente."""
        # ARRANGE
        telefone1 = Telefone("(11) 99999-9999")
        telefone2 = Telefone("11999999999")  # Será normalizado
        telefone3 = Telefone("(11) 88888-8888")
        
        # ACT & ASSERT
        assert telefone1 == telefone2  # Normalizados iguais
        assert telefone1 != telefone3  # Diferentes

    def test_telefone_hash_consistency(self):
        """✅ HAPPY PATH: Telefones iguais devem ter mesmo hash."""
        # ARRANGE
        telefone1 = Telefone("(11) 99999-9999")
        telefone2 = Telefone("11999999999")
        
        # ACT & ASSERT
        assert hash(telefone1) == hash(telefone2)

    def test_telefone_str_representation(self):
        """✅ HAPPY PATH: Representação string deve retornar valor normalizado."""
        # ARRANGE
        telefone = Telefone("11999999999")
        
        # ACT & ASSERT
        assert str(telefone) == "(11) 99999-9999"

    def test_telefone_repr_representation(self):
        """✅ HAPPY PATH: Representação deve ser informativa."""
        # ARRANGE
        telefone = Telefone("(11) 99999-9999")
        
        # ACT
        repr_str = repr(telefone)
        
        # ASSERT
        assert "Telefone" in repr_str
        assert "(11) 99999-9999" in repr_str
