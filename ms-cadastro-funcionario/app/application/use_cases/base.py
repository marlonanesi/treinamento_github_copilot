"""
Classe base para casos de uso da aplicação.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
import logging

# Tipos genéricos para entrada e saída dos casos de uso
TRequest = TypeVar('TRequest')
TResponse = TypeVar('TResponse')


class UseCase(ABC, Generic[TRequest, TResponse]):
    """
    Classe base abstrata para todos os casos de uso da aplicação.
    
    Define o contrato padrão que todos os casos de uso devem seguir,
    implementando o padrão Command para encapsular operações de negócio.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        """
        Executa o caso de uso com os dados de entrada fornecidos.
        
        Args:
            request: Dados de entrada para o caso de uso
            
        Returns:
            Dados de saída após a execução do caso de uso
            
        Raises:
            ApplicationException: Para qualquer erro específico da aplicação
        """
        pass
    
    async def __call__(self, request: TRequest) -> TResponse:
        """
        Permite que o caso de uso seja chamado diretamente como uma função.
        
        Adiciona logging automático antes e depois da execução.
        """
        self.logger.info(f"Executando {self.__class__.__name__}")
        self.logger.debug(f"Request: {request}")
        
        try:
            response = await self.execute(request)
            self.logger.info(f"Caso de uso {self.__class__.__name__} executado com sucesso")
            self.logger.debug(f"Response: {response}")
            return response
            
        except Exception as e:
            self.logger.error(f"Erro ao executar {self.__class__.__name__}: {str(e)}")
            raise
    
    def _log_business_rule(self, rule: str, context: dict = None):
        """
        Registra uma regra de negócio sendo aplicada.
        
        Args:
            rule: Descrição da regra de negócio
            context: Contexto adicional sobre a aplicação da regra
        """
        self.logger.info(f"Aplicando regra de negócio: {rule}")
        if context:
            self.logger.debug(f"Contexto da regra: {context}")
    
    def _log_validation(self, field: str, rule: str, value: Any = None):
        """
        Registra uma validação sendo aplicada.
        
        Args:
            field: Nome do campo sendo validado
            rule: Regra de validação aplicada
            value: Valor sendo validado (opcional por segurança)
        """
        if value is not None:
            self.logger.debug(f"Validando campo '{field}' com regra '{rule}': {value}")
        else:
            self.logger.debug(f"Validando campo '{field}' com regra '{rule}'")
