import uuid
from datetime import date
from decimal import Decimal
from pydantic import ValidationError

from app.domain.entities.funcionario import Funcionario
from app.domain.entities.value_objects import Email, Cargo, Telefone
from app.presentation.schemas.funcionario_schemas import FuncionarioCreateSchema

def create_valid_funcionario(**kwargs):
    """🏗️ Cria uma instância válida da entidade Funcionario."""
    defaults = {
        "nome_completo": "João da Silva Santos",
        "email": Email("joao.silva@exemplo.com"),
        "cargo": Cargo("Desenvolvedor"),
        "data_admissao": date(2023, 1, 15),
        "telefone": None,
        "departamento": "Tecnologia",
        "salario": Decimal("5000.00"),
        "ativo": False,
        "id": str(uuid.uuid4())
    }
    defaults.update(kwargs)
    return Funcionario(**defaults)

def create_valid_create_schema(**kwargs):
    """📝 Cria um schema válido para criação de funcionário."""
    defaults = {
        "nome_completo": "Maria de Souza Silva",
        "email": "maria.souza@exemplo.com",
        "cargo": "Desenvolvedor",
        "data_admissao": date(2023, 2, 15),
        "telefone": "(11) 99999-9999",
        "departamento": "Tecnologia",
        "salario": Decimal("5500.00")
    }
    defaults.update(kwargs)
    return FuncionarioCreateSchema(**defaults)
