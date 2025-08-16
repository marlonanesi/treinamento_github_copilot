"""
Domain Exceptions - Exceções do Domínio

Exceções específicas para regras de negócio do domínio de funcionários.
"""

from .funcionario_exceptions import (
    FuncionarioException,
    FuncionarioNaoEncontradoException,
    EmailDuplicadoException,
    FuncionarioAtivoEmProjetosException,
    DadosInvalidosException,
    CargoInvalidoException,
)

__all__ = [
    "FuncionarioException",
    "FuncionarioNaoEncontradoException", 
    "EmailDuplicadoException",
    "FuncionarioAtivoEmProjetosException",
    "DadosInvalidosException",
    "CargoInvalidoException",
]
