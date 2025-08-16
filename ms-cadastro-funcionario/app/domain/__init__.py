"""
Domain Layer - Camada de Domínio

Contém entidades, regras de negócio, interfaces de repositório
e exceções específicas do domínio de funcionários.

Esta camada é independente de infraestrutura e frameworks,
contendo apenas a lógica de negócio pura do sistema.
"""

from .entities import Funcionario, Email, Cargo, Telefone, TiposCargo
from .repositories import AbstractFuncionarioRepository
from .exceptions import (
    FuncionarioException,
    FuncionarioNaoEncontradoException,
    EmailDuplicadoException,
    FuncionarioAtivoEmProjetosException,
    DadosInvalidosException,
    CargoInvalidoException,
)

__all__ = [
    # Entidades e Value Objects
    "Funcionario",
    "Email", 
    "Cargo",
    "Telefone",
    "TiposCargo",
    
    # Interfaces de Repositório
    "AbstractFuncionarioRepository",
    
    # Exceções de Domínio
    "FuncionarioException",
    "FuncionarioNaoEncontradoException",
    "EmailDuplicadoException", 
    "FuncionarioAtivoEmProjetosException",
    "DadosInvalidosException",
    "CargoInvalidoException",
]
