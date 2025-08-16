"""
DTOs (Data Transfer Objects) para requests da camada de aplicação.
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional
from decimal import Decimal


@dataclass
class CriarFuncionarioRequest:
    """
    DTO para request de criação de funcionário.
    """
    nome_completo: str
    email: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    data_nascimento: Optional[date] = None
    cargo: Optional[str] = None
    departamento: Optional[str] = None
    salario: Optional[Decimal] = None
    data_admissao: Optional[date] = None


@dataclass
class BuscarFuncionarioRequest:
    """
    DTO para request de busca de funcionário por ID.
    """
    funcionario_id: str


@dataclass
class ListarFuncionariosRequest:
    """
    DTO para request de listagem de funcionários com filtros e paginação.
    """
    departamento: Optional[str] = None
    cargo: Optional[str] = None
    ativo: Optional[bool] = None
    limite: int = 50
    offset: int = 0


@dataclass
class AtualizarFuncionarioRequest:
    """
    DTO para request de atualização de funcionário.
    """
    funcionario_id: str
    nome_completo: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    data_nascimento: Optional[date] = None
    cargo: Optional[str] = None
    departamento: Optional[str] = None
    salario: Optional[Decimal] = None


@dataclass
class ExcluirFuncionarioRequest:
    """
    DTO para request de exclusão de funcionário.
    """
    funcionario_id: str
    exclusao_fisica: bool = False
    
    def __str__(self):
        return self.funcionario_id
