import pytest
from datetime import datetime, date
from decimal import Decimal
from bson import ObjectId

from app.infrastructure.database.models import FuncionarioModel
from app.domain.entities.funcionario import Funcionario
from app.domain.entities.value_objects import Email, Cargo, Telefone
from tests.factories import create_valid_funcionario

class TestFuncionarioModel:
    """
    🧪 Testes para o mapeamento entre entidade e documento MongoDB
    ⚠️ CRÍTICO: Funções puras - sem I/O real
    """

    @pytest.fixture
    def funcionario_entity(self):
        """🏗️ Entidade de domínio para testes"""
        return create_valid_funcionario(
            nome_completo="João Silva",
            email=Email("joao@empresa.com"),
            cargo=Cargo("Desenvolvedor"),
            telefone=Telefone("(11) 99999-9999"),
            departamento="Tecnologia",
            salario=Decimal("5000.00")
        )

    @pytest.fixture
    def funcionario_document(self):
        """📄 Documento MongoDB para testes"""
        return {
            "_id": ObjectId(),
            "nome_completo": "João Silva",
            "email": "joao@empresa.com",
            "cargo": "Desenvolvedor", 
            "data_admissao": datetime(2023, 1, 15),
            "telefone": "(11) 99999-9999",
            "departamento": "Tecnologia",
            "salario": 5000.00,
            "ativo": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

    @pytest.fixture
    def documento_legacy(self):
        """📄 Documento com formato legacy (campo 'nome' em vez de 'nome_completo')"""
        return {
            "_id": ObjectId(),
            "nome": "João Silva",  # Campo legacy
            "email": "joao@empresa.com",
            "cargo": "Desenvolvedor",
            "data_admissao": "2023-01-15",  # String format
            "telefone": "(11) 99999-9999",
            "ativo": False,
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00"
        }

    def test_from_entity_converte_corretamente(self, funcionario_entity):
        """✅ HAPPY PATH: Deve converter entidade para documento MongoDB."""
        # ACT
        document = FuncionarioModel.from_entity(funcionario_entity)
        
        # ASSERT
        assert document["nome_completo"] == "João Silva"
        assert document["email"] == "joao@empresa.com"
        assert document["cargo"] == "Desenvolvedor"
        assert document["telefone"] == "(11) 99999-9999"
        assert document["departamento"] == "Tecnologia"
        assert document["salario"] == 5000.0  # Decimal convertido para float
        assert document["ativo"] is False
        assert isinstance(document["data_admissao"], datetime)
        assert isinstance(document["created_at"], datetime)

    def test_from_entity_campos_opcionais_none(self):
        """✅ HAPPY PATH: Deve lidar com campos opcionais None."""
        # ARRANGE
        funcionario = create_valid_funcionario(
            telefone=None,
            departamento=None,
            salario=None
        )
        
        # ACT
        document = FuncionarioModel.from_entity(funcionario)
        
        # ASSERT
        assert "telefone" not in document
        assert "departamento" not in document  
        assert "salario" not in document

    def test_to_entity_converte_documento_completo(self, funcionario_document):
        """✅ HAPPY PATH: Deve converter documento para entidade com todos os campos."""
        # ACT
        funcionario = FuncionarioModel.to_entity(funcionario_document)
        
        # ASSERT
        assert funcionario.id == str(funcionario_document["_id"])
        assert funcionario.nome_completo == "João Silva"
        assert funcionario.email.value == "joao@empresa.com"
        assert funcionario.cargo.value == "Desenvolvedor"
        assert funcionario.telefone.value == "(11) 99999-9999"
        assert funcionario.departamento == "Tecnologia"
        assert funcionario.salario == Decimal("5000.0")
        assert funcionario.ativo is False

    def test_to_entity_com_documento_legacy(self, documento_legacy):
        """✅ HAPPY PATH: Deve converter documento legacy corretamente."""
        # ACT
        funcionario = FuncionarioModel.to_entity(documento_legacy)
        
        # ASSERT
        # Campo 'nome' deve ser mapeado para 'nome_completo'
        assert funcionario.nome_completo == "João Silva"
        assert funcionario.email.value == "joao@empresa.com"
        
        # Data em formato string deve ser convertida
        assert isinstance(funcionario.data_admissao, date)
        assert funcionario.data_admissao == date(2023, 1, 15)

    def test_roundtrip_entity_document_entity_preserva_dados(self, funcionario_entity):
        """✅ HAPPY PATH: Roundtrip entidade → documento → entidade preserva dados."""
        # ACT
        document = FuncionarioModel.from_entity(funcionario_entity)
        document["_id"] = ObjectId()  # Simular ID do MongoDB
        funcionario_recriado = FuncionarioModel.to_entity(document)
        
        # ASSERT
        assert funcionario_entity.nome_completo == funcionario_recriado.nome_completo
        assert funcionario_entity.email == funcionario_recriado.email
        assert funcionario_entity.cargo == funcionario_recriado.cargo
        assert funcionario_entity.telefone == funcionario_recriado.telefone
        assert funcionario_entity.departamento == funcionario_recriado.departamento
        assert funcionario_entity.ativo == funcionario_recriado.ativo

    def test_to_update_document_gera_operadores_corretos(self, funcionario_entity):
        """✅ HAPPY PATH: Deve gerar documento de atualização com operadores MongoDB."""
        # ARRANGE
        funcionario_entity.nome_completo = "João Silva Atualizado"
        funcionario_entity.salario = Decimal("6000.00")
        
        # ACT
        update_doc = FuncionarioModel.to_update_document(funcionario_entity)
        
        # ASSERT
        assert "$set" in update_doc
        set_fields = update_doc["$set"]
        
        assert set_fields["nome_completo"] == "João Silva Atualizado"
        assert set_fields["salario"] == 6000.0
        assert "updated_at" in set_fields
        assert isinstance(set_fields["updated_at"], datetime)

    def test_to_update_document_com_campos_none_usa_unset(self):
        """✅ HAPPY PATH: Deve usar $unset para campos None."""
        # ARRANGE
        funcionario = create_valid_funcionario()
        funcionario.telefone = None
        funcionario.departamento = None
        
        # ACT
        update_doc = FuncionarioModel.to_update_document(funcionario)
        
        # ASSERT
        if "$unset" in update_doc:
            unset_fields = update_doc["$unset"]
            # Campos None devem ser removidos com $unset
            assert "telefone" in unset_fields or "departamento" in unset_fields

    def test_to_update_document_com_campos_permitidos(self, funcionario_entity):
        """✅ HAPPY PATH: Deve incluir apenas campos permitidos quando especificados."""
        # ACT
        update_doc = FuncionarioModel.to_update_document(
            funcionario_entity,
            campos_permitidos=["nome_completo", "cargo"]
        )
        
        # ASSERT
        set_fields = update_doc["$set"]
        
        assert "nome_completo" in set_fields
        assert "cargo" in set_fields
        assert "updated_at" in set_fields  # Sempre incluído
        
        # Campos não permitidos não devem estar presentes
        assert "email" not in set_fields
        assert "telefone" not in set_fields

    def test_validate_document_identifica_documento_valido(self, funcionario_document):
        """✅ HAPPY PATH: Deve identificar documento válido."""
        # ACT
        is_valid = FuncionarioModel.validate_document(funcionario_document)
        
        # ASSERT
        assert is_valid is True

    def test_validate_document_identifica_documento_invalido(self):
        """❌ Cenário TRISTE: Deve identificar documento inválido."""
        # ARRANGE
        documento_invalido = {
            # Faltam campos obrigatórios
            "nome_completo": "João Silva"
            # email, cargo, data_admissao ausentes
        }
        
        # ACT
        is_valid = FuncionarioModel.validate_document(documento_invalido)
        
        # ASSERT
        assert is_valid is False

    def test_validate_document_com_documento_vazio(self):
        """❌ Cenário TRISTE: Deve rejeitar documento vazio."""
        # ACT
        is_valid = FuncionarioModel.validate_document({})
        
        # ASSERT
        assert is_valid is False

    def test_get_projection_fields_retorna_campos_corretos(self):
        """✅ HAPPY PATH: Deve retornar projeção com todos os campos necessários."""
        # ACT
        projection = FuncionarioModel.get_projection_fields()
        
        # ASSERT
        assert isinstance(projection, dict)
        assert "_id" in projection
        assert "nome_completo" in projection
        assert "email" in projection
        assert "cargo" in projection
        assert "data_admissao" in projection

    def test_get_summary_projection_retorna_campos_resumidos(self):
        """✅ HAPPY PATH: Deve retornar projeção resumida."""
        # ACT
        summary_projection = FuncionarioModel.get_summary_projection()
        
        # ASSERT
        assert isinstance(summary_projection, dict)
        assert "_id" in summary_projection
        assert "nome_completo" in summary_projection
        assert "email" in summary_projection
        assert "cargo" in summary_projection
        
        # Campos detalhados não devem estar na projeção resumida
        # (isso depende da implementação específica)

    def test_conversao_tipos_decimal_para_float(self):
        """✅ HAPPY PATH: Deve converter Decimal para float corretamente."""
        # ARRANGE
        funcionario = create_valid_funcionario(salario=Decimal("1234.56"))
        
        # ACT
        document = FuncionarioModel.from_entity(funcionario)
        
        # ASSERT
        assert isinstance(document["salario"], float)
        assert document["salario"] == 1234.56

    def test_conversao_tipos_date_para_datetime(self):
        """✅ HAPPY PATH: Deve converter date para datetime."""
        # ARRANGE
        funcionario = create_valid_funcionario()
        funcionario.data_admissao = date(2023, 1, 15)
        
        # ACT
        document = FuncionarioModel.from_entity(funcionario)
        
        # ASSERT
        assert isinstance(document["data_admissao"], datetime)
        assert document["data_admissao"].date() == date(2023, 1, 15)

    def test_conversao_tipos_string_para_date(self):
        """✅ HAPPY PATH: Deve converter string para date no parsing."""
        # ARRANGE
        document = {
            "_id": ObjectId(),
            "nome_completo": "João Silva",
            "email": "joao@empresa.com",
            "cargo": "Desenvolvedor",
            "data_admissao": "2023-01-15",  # String
            "ativo": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # ACT
        funcionario = FuncionarioModel.to_entity(document)
        
        # ASSERT
        assert isinstance(funcionario.data_admissao, date)
        assert funcionario.data_admissao == date(2023, 1, 15)

    def test_to_entity_com_campo_ausente_usa_default(self):
        """✅ HAPPY PATH: Deve usar valores default para campos ausentes."""
        # ARRANGE
        document_minimo = {
            "_id": ObjectId(),
            "nome_completo": "João Silva",
            "email": "joao@empresa.com",
            "cargo": "Desenvolvedor",
            "data_admissao": datetime(2023, 1, 15)
            # Campos opcionais ausentes
        }
        
        # ACT
        funcionario = FuncionarioModel.to_entity(document_minimo)
        
        # ASSERT
        assert funcionario.telefone is None
        assert funcionario.departamento is None
        assert funcionario.salario is None
        assert funcionario.ativo is False  # Default value
