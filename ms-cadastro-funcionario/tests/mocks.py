import uuid
from unittest.mock import AsyncMock
from typing import Optional

from app.domain.entities.funcionario import Funcionario
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository
from app.application.exceptions import ApplicationException

class FuncionarioRepositoryMock:
    """🎭 Mock do repositório - SUBSTITUI acesso ao banco real"""
    
    def __init__(self):
        self.db = {}  # Simula banco em memória

    async def salvar(self, funcionario: Funcionario) -> Funcionario:
        if not funcionario.id:
            funcionario.id = str(uuid.uuid4())
        self.db[funcionario.id] = funcionario
        return funcionario

    async def buscar_por_id(self, funcionario_id: str) -> Optional[Funcionario]:
        return self.db.get(funcionario_id)
    
    async def buscar_por_email(self, email: str) -> Optional[Funcionario]:
        for funcionario in self.db.values():
            if funcionario.email.value == email:
                return funcionario
        return None

    async def atualizar(self, funcionario: Funcionario) -> Funcionario:
        if funcionario.id not in self.db:
            return None
        self.db[funcionario.id] = funcionario
        return funcionario
    
    async def excluir(self, funcionario_id: str) -> bool:
        if funcionario_id in self.db:
            del self.db[funcionario_id]
            return True
        return False

    async def listar_por_filtros(
        self, 
        departamento: Optional[str] = None,
        cargo: Optional[str] = None,
        ativo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ):
        """Lista funcionários com filtros aplicados"""
        funcionarios = list(self.db.values())
        
        # Aplicar filtros
        if departamento:
            funcionarios = [f for f in funcionarios if f.departamento == departamento]
        if cargo:
            funcionarios = [f for f in funcionarios if f.cargo.value == cargo]
        if ativo is not None:
            funcionarios = [f for f in funcionarios if f.ativo == ativo]
        
        # Aplicar paginação
        total = len(funcionarios)
        funcionarios_paginated = funcionarios[skip:skip + limit]
        
        return funcionarios_paginated

class FuncionarioUseCaseMock:
    """🎭 Mock do caso de uso - ISOLA lógica de negócio"""
    
    def __init__(self, funcionario: Funcionario = None):
        self.funcionario = funcionario
        self.get_by_id = AsyncMock(return_value=funcionario)
        self.create = AsyncMock(return_value=funcionario)
        self.update = AsyncMock(return_value=funcionario)
        self.delete = AsyncMock(return_value=None)
        
        # Simula comportamento de erro quando ID não existe
        if funcionario:
            self.get_by_id.side_effect = lambda id: funcionario if id == funcionario.id else None
