"""
Repository Interfaces - Interfaces de Repositório

Define contratos para acesso a dados que devem ser implementados
pela camada de infraestrutura.
"""

from .funcionario_repository import AbstractFuncionarioRepository

__all__ = [
    "AbstractFuncionarioRepository",
]
