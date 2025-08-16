"""
DTOs (Data Transfer Objects) para responses da camada de aplicação.
"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional
from decimal import Decimal

from app.domain.entities.funcionario import Funcionario


@dataclass
class FuncionarioResponse:
    """
    DTO para response de funcionário.
    """
    id: str
    nome_completo: str
    email: str
    cargo: str
    data_admissao: date
    telefone: Optional[str]
    departamento: Optional[str]
    salario: Optional[Decimal]
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    @classmethod
    def from_entity(cls, funcionario: Funcionario) -> 'FuncionarioResponse':
        """
        Cria um DTO Response a partir de uma entidade de domínio.
        
        Args:
            funcionario: Entidade Funcionario do domínio
            
        Returns:
            FuncionarioResponse: DTO com dados do funcionário
        """
        return cls(
            id=funcionario.id or "",
            nome_completo=funcionario.nome_completo,
            email=funcionario.email.value,
            cargo=funcionario.cargo.value,
            data_admissao=funcionario.data_admissao,
            telefone=funcionario.telefone.value if funcionario.telefone else None,
            departamento=funcionario.departamento,
            salario=funcionario.salario,
            ativo=funcionario.ativo,
            created_at=funcionario.created_at,
            updated_at=funcionario.updated_at
        )


@dataclass
class ListarFuncionariosResponse:
    """
    DTO para response de listagem de funcionários com metadados de paginação.
    """
    funcionarios: List[FuncionarioResponse]
    total: int
    skip: int
    limit: int
    has_next: bool
    
    @classmethod
    def create(
        cls,
        funcionarios: List[Funcionario],
        total: int,
        skip: int,
        limit: int
    ) -> 'ListarFuncionariosResponse':
        """
        Cria response de listagem a partir de entidades de domínio.
        
        Args:
            funcionarios: Lista de entidades Funcionario
            total: Total de funcionários (sem paginação)
            skip: Offset atual
            limit: Limite atual
            
        Returns:
            ListarFuncionariosResponse: DTO com lista e metadados
        """
        funcionarios_dto = [
            FuncionarioResponse.from_entity(f) for f in funcionarios
        ]
        
        has_next = (skip + len(funcionarios)) < total
        
        return cls(
            funcionarios=funcionarios_dto,
            total=total,
            skip=skip,
            limit=limit,
            has_next=has_next
        )
