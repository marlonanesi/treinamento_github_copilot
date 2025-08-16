import pytest
from datetime import date, datetime
from decimal import Decimal
from pydantic import ValidationError

from app.presentation.schemas.funcionario_schemas import (
    FuncionarioCreateSchema,
    FuncionarioUpdateSchema,
    FuncionarioResponseSchema,
    FuncionarioListQuerySchema
)

class TestFuncionarioCreateSchema:
    """
    🧪 Testes para o schema de criação de funcionário
    ✅ Foco em validações Pydantic e normalização
    """

    @pytest.fixture
    def dados_create_validos(self):
        """📝 Dados válidos para criação"""
        return {
            "nome_completo": "joão SILVA santos",
            "email": "JOAO@EMPRESA.COM", 
            "cargo": "desenvolvedor pleno",
            "data_admissao": "2023-01-15",
            "telefone": "(11) 99999-9999",
            "departamento": "tecnologia",
            "salario": 5000.00
        }

    def test_schema_valido_passa_em_todas_validacoes(self, dados_create_validos):
        """✅ HAPPY PATH: Schema válido deve passar em todas as validações."""
        # ACT
        schema = FuncionarioCreateSchema(**dados_create_validos)
        
        # ASSERT
        assert schema.nome_completo == "João Silva Santos"  # Normalizado
        assert schema.email == "joao@empresa.com"  # Normalizado lowercase
        assert schema.cargo == "Desenvolvedor Pleno"  # Normalizado title case
        assert schema.departamento == "Tecnologia"  # Normalizado
        assert schema.data_admissao == date(2023, 1, 15)
        assert schema.salario == Decimal("5000.00")

    def test_dados_sao_normalizados_automaticamente(self):
        """✅ HAPPY PATH: Dados devem ser normalizados automaticamente."""
        # ARRANGE
        dados_nao_normalizados = {
            "nome_completo": "   joão silva santos   ",  # Espaços extras
            "email": "JOAO@EMPRESA.COM",  # Maiúscula
            "cargo": "desenvolvedor pleno",  # Minúscula
            "data_admissao": "2023-01-15"
        }
        
        # ACT
        schema = FuncionarioCreateSchema(**dados_nao_normalizados)
        
        # ASSERT
        assert schema.nome_completo == "João Silva Santos"
        assert schema.email == "joao@empresa.com"
        assert schema.cargo == "Desenvolvedor Pleno"

    @pytest.mark.parametrize("campo_obrigatorio", [
        "nome_completo",
        "email", 
        "cargo",
        "data_admissao"
    ])
    def test_campo_obrigatorio_ausente_lanca_validation_error(self, dados_create_validos, campo_obrigatorio):
        """❌ Cenário TRISTE: Campo obrigatório ausente deve lançar ValidationError."""
        # ARRANGE
        dados_incompletos = dados_create_validos.copy()
        del dados_incompletos[campo_obrigatorio]
        
        # ACT & ASSERT
        with pytest.raises(ValidationError) as exc_info:
            FuncionarioCreateSchema(**dados_incompletos)
        
        # Verificar se erro é do campo correto
        errors = exc_info.value.errors()
        field_errors = [error for error in errors if error['loc'] == (campo_obrigatorio,)]
        assert len(field_errors) > 0
        assert field_errors[0]['type'] == 'missing'

    @pytest.mark.parametrize("nome_invalido", [
        "",           # Vazio
        "A",          # Muito curto
        "João",       # Uma palavra só (dependendo da validação)
    ])
    def test_nome_completo_invalido_lanca_validation_error(self, dados_create_validos, nome_invalido):
        """❌ Cenário TRISTE: Nome completo inválido deve ser rejeitado."""
        # ARRANGE
        dados_create_validos["nome_completo"] = nome_invalido
        
        # ACT & ASSERT
        with pytest.raises(ValidationError) as exc_info:
            FuncionarioCreateSchema(**dados_create_validos)
        
        # Verificar se erro é do campo nome_completo
        errors = exc_info.value.errors()
        nome_errors = [error for error in errors if 'nome_completo' in str(error['loc'])]
        assert len(nome_errors) > 0

    @pytest.mark.parametrize("email_invalido", [
        "email_sem_arroba.com",
        "@sem_usuario.com",
        "sem_dominio@",
        "email..duplo@dominio.com",
        "",
    ])
    def test_email_invalido_lanca_validation_error(self, dados_create_validos, email_invalido):
        """❌ Cenário TRISTE: Email inválido deve ser rejeitado."""
        # ARRANGE
        dados_create_validos["email"] = email_invalido
        
        # ACT & ASSERT
        with pytest.raises(ValidationError) as exc_info:
            FuncionarioCreateSchema(**dados_create_validos)
        
        # Verificar se erro é do campo email
        errors = exc_info.value.errors()
        email_errors = [error for error in errors if 'email' in str(error['loc'])]
        assert len(email_errors) > 0

    def test_data_admissao_futura_lanca_validation_error(self, dados_create_validos):
        """❌ Cenário TRISTE: Data de admissão futura deve ser rejeitada."""
        # ARRANGE
        dados_create_validos["data_admissao"] = "2030-12-31"  # Data futura
        
        # ACT & ASSERT
        with pytest.raises(ValidationError):
            FuncionarioCreateSchema(**dados_create_validos)

    def test_salario_negativo_lanca_validation_error(self, dados_create_validos):
        """❌ Cenário TRISTE: Salário negativo deve ser rejeitado."""
        # ARRANGE
        dados_create_validos["salario"] = -1000.00
        
        # ACT & ASSERT
        with pytest.raises(ValidationError) as exc_info:
            FuncionarioCreateSchema(**dados_create_validos)
        
        # Verificar se erro é relacionado ao salário
        errors = exc_info.value.errors()
        salario_errors = [error for error in errors if 'salario' in str(error['loc'])]
        assert len(salario_errors) > 0

    def test_campos_opcionais_podem_ser_omitidos(self):
        """✅ HAPPY PATH: Campos opcionais podem ser omitidos."""
        # ARRANGE
        dados_minimos = {
            "nome_completo": "João Silva",
            "email": "joao@empresa.com",
            "cargo": "Desenvolvedor",
            "data_admissao": "2023-01-15"
        }
        
        # ACT
        schema = FuncionarioCreateSchema(**dados_minimos)
        
        # ASSERT
        assert schema.telefone is None
        assert schema.departamento is None
        assert schema.salario is None
        assert schema.cpf is None
        assert schema.data_nascimento is None


class TestFuncionarioUpdateSchema:
    """
    🧪 Testes para o schema de atualização de funcionário
    ✅ Foco em campos opcionais e validação de campos imutáveis
    """

    @pytest.fixture
    def dados_update_validos(self):
        """📝 Dados válidos para atualização"""
        return {
            "cargo": "desenvolvedor senior",
            "departamento": "arquitetura",
            "salario": 6000.00
        }

    def test_schema_update_valido_funciona(self, dados_update_validos):
        """✅ HAPPY PATH: Deve aceitar dados válidos para atualização."""
        # ACT
        schema = FuncionarioUpdateSchema(**dados_update_validos)
        
        # ASSERT
        assert schema.cargo == "Desenvolvedor Senior"  # Normalizado
        assert schema.departamento == "Arquitetura"    # Normalizado
        assert schema.salario == Decimal("6000.00")

    def test_todos_campos_opcionais_em_update(self):
        """✅ HAPPY PATH: Todos os campos devem ser opcionais em update."""
        # ACT
        schema = FuncionarioUpdateSchema()
        
        # ASSERT
        assert schema.nome_completo is None
        assert schema.cargo is None
        assert schema.telefone is None
        assert schema.departamento is None
        assert schema.salario is None

    def test_campos_imutaveis_sao_rejeitados(self):
        """❌ Cenário TRISTE: Campos imutáveis devem ser rejeitados."""
        # ARRANGE
        dados_com_campo_imutavel = {
            "email": "novo@email.com",  # Email é imutável
            "data_admissao": "2023-02-01",  # Data de admissão é imutável
            "cargo": "Novo Cargo"
        }
        
        # ACT & ASSERT
        with pytest.raises(ValidationError) as exc_info:
            FuncionarioUpdateSchema(**dados_com_campo_imutavel)
        
        # Verificar se erro menciona campos imutáveis
        error_message = str(exc_info.value)
        assert "email" in error_message.lower() or "data_admissao" in error_message.lower()

    def test_update_vazio_lanca_validation_error(self):
        """❌ Cenário TRISTE: Update sem nenhum campo deve ser rejeitado."""
        # ACT & ASSERT
        with pytest.raises(ValidationError) as exc_info:
            FuncionarioUpdateSchema(**{})
        
        # Verificar se erro menciona necessidade de pelo menos um campo
        error_message = str(exc_info.value)
        assert "pelo menos um campo" in error_message.lower()

    def test_normalizacao_funciona_em_update(self):
        """✅ HAPPY PATH: Normalização deve funcionar em campos de update."""
        # ARRANGE
        dados_update = {
            "nome_completo": "   joão silva atualizado   ",
            "cargo": "tech lead",
            "departamento": "   inovação   "
        }
        
        # ACT
        schema = FuncionarioUpdateSchema(**dados_update)
        
        # ASSERT
        assert schema.nome_completo == "João Silva Atualizado"
        assert schema.cargo == "Tech Lead"
        assert schema.departamento == "Inovação"


class TestFuncionarioListQuerySchema:
    """
    🧪 Testes para o schema de query de listagem
    ✅ Foco em paginação e filtros
    """

    def test_schema_query_com_defaults(self):
        """✅ HAPPY PATH: Deve usar valores padrão quando não informado."""
        # ACT
        schema = FuncionarioListQuerySchema()
        
        # ASSERT
        assert schema.page == 1
        assert schema.size == 10
        assert schema.departamento is None
        assert schema.cargo is None

    def test_schema_query_com_filtros(self):
        """✅ HAPPY PATH: Deve aceitar filtros opcionais."""
        # ARRANGE
        dados_query = {
            "page": 2,
            "size": 20,
            "departamento": "Tecnologia",
            "cargo": "Desenvolvedor Senior"
        }
        
        # ACT
        schema = FuncionarioListQuerySchema(**dados_query)
        
        # ASSERT
        assert schema.page == 2
        assert schema.size == 20
        assert schema.departamento == "Tecnologia"
        assert schema.cargo == "Desenvolvedor Senior"

    def test_page_menor_que_1_lanca_validation_error(self):
        """❌ Cenário TRISTE: Page menor que 1 deve ser rejeitada."""
        # ACT & ASSERT
        with pytest.raises(ValidationError) as exc_info:
            FuncionarioListQuerySchema(page=0)
        
        # Verificar se erro é do campo page
        errors = exc_info.value.errors()
        page_errors = [error for error in errors if 'page' in str(error['loc'])]
        assert len(page_errors) > 0

    def test_size_acima_do_limite_lanca_validation_error(self):
        """❌ Cenário TRISTE: Size acima do limite deve ser rejeitado."""
        # ACT & ASSERT
        with pytest.raises(ValidationError) as exc_info:
            FuncionarioListQuerySchema(size=101)  # Limite é 100
        
        # Verificar se erro é do campo size
        errors = exc_info.value.errors()
        size_errors = [error for error in errors if 'size' in str(error['loc'])]
        assert len(size_errors) > 0

    def test_size_menor_que_1_lanca_validation_error(self):
        """❌ Cenário TRISTE: Size menor que 1 deve ser rejeitado."""
        # ACT & ASSERT
        with pytest.raises(ValidationError):
            FuncionarioListQuerySchema(size=0)


class TestFuncionarioResponseSchema:
    """
    🧪 Testes para o schema de resposta
    ✅ Foco em serialização correta dos dados
    """

    def test_response_schema_com_todos_campos(self):
        """✅ HAPPY PATH: Deve aceitar todos os campos de resposta."""
        # ARRANGE
        dados_response = {
            "id": "507f1f77bcf86cd799439011",
            "nome_completo": "João Silva",
            "email": "joao@empresa.com",
            "cargo": "Desenvolvedor",
            "data_admissao": date(2023, 1, 15),
            "telefone": "(11) 99999-9999",
            "departamento": "Tecnologia",
            "salario": Decimal("5000.00"),
            "ativo": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # ACT
        schema = FuncionarioResponseSchema(**dados_response)
        
        # ASSERT
        assert schema.id == "507f1f77bcf86cd799439011"
        assert schema.nome_completo == "João Silva"
        assert schema.email == "joao@empresa.com"
        assert schema.cargo == "Desenvolvedor"
        assert schema.ativo is False

    def test_response_schema_com_campos_opcionais_none(self):
        """✅ HAPPY PATH: Deve aceitar campos opcionais como None."""
        # ARRANGE
        dados_minimos = {
            "id": "507f1f77bcf86cd799439011",
            "nome_completo": "João Silva",
            "email": "joao@empresa.com",
            "cargo": "Desenvolvedor",
            "data_admissao": date(2023, 1, 15),
            "ativo": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # ACT
        schema = FuncionarioResponseSchema(**dados_minimos)
        
        # ASSERT
        assert schema.telefone is None
        assert schema.departamento is None
        assert schema.salario is None
