"""
Casos de uso da aplicação (Application Layer).

Este módulo contém todos os casos de uso que orquestram as operações
de negócio do sistema, implementando a lógica de aplicação de acordo
com os princípios do Domain-Driven Design.
"""

from app.application.use_cases.base import UseCase
from app.application.use_cases.criar_funcionario import CriarFuncionarioUseCase
from app.application.use_cases.buscar_funcionario import BuscarFuncionarioUseCase
from app.application.use_cases.listar_funcionarios import ListarFuncionariosUseCase
from app.application.use_cases.atualizar_funcionario import AtualizarFuncionarioUseCase
from app.application.use_cases.excluir_funcionario import ExcluirFuncionarioUseCase

__all__ = [
    # Classe base
    "UseCase",
    
    # Casos de uso CRUD
    "CriarFuncionarioUseCase",
    "BuscarFuncionarioUseCase",
    "ListarFuncionariosUseCase",
    "AtualizarFuncionarioUseCase",
    "ExcluirFuncionarioUseCase",
]
