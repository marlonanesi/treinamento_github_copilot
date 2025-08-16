"""
Controllers da API FastAPI.

Este módulo centraliza os controllers responsáveis pela coordenação
entre endpoints HTTP e casos de uso da aplicação.
"""

from .funcionario_controller import FuncionarioController, FuncionarioControllerFactory

__all__ = [
    "FuncionarioController",
    "FuncionarioControllerFactory"
]
