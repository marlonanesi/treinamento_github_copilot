"""
Domain Entities - Entidades do Domínio

Contém as entidades principais do domínio de funcionários
e seus value objects associados.
"""

from .funcionario import Funcionario
from .value_objects import Email, Cargo, Telefone, TiposCargo

__all__ = [
    "Funcionario",
    "Email",
    "Cargo", 
    "Telefone",
    "TiposCargo",
]
