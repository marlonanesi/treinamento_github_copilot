"""
Coordenador principal da aplicação.

Este módulo contém o coordenador principal que gerencia
a inicialização e coordenação de todos os componentes
da camada de aplicação.
"""

import logging
from typing import Optional
import asyncio

from app.application.services.funcionario_service import FuncionarioApplicationService
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository


class ApplicationCoordinator:
    """
    Coordenador principal da aplicação.
    
    Responsável por:
    - Inicialização dos serviços de aplicação
    - Coordenação entre diferentes bounded contexts (futuro)
    - Gerenciamento de transações distribuídas (futuro)
    - Health checks da aplicação
    """
    
    def __init__(self, funcionario_repository: AbstractFuncionarioRepository):
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Inicializar serviços
        self.funcionario_service = FuncionarioApplicationService(funcionario_repository)
        
        # Estado do coordenador
        self._initialized = False
        self._shutdown = False
    
    async def initialize(self) -> None:
        """
        Inicializa o coordenador e todos os serviços dependentes.
        """
        if self._initialized:
            self.logger.warning("Coordenador já foi inicializado")
            return
        
        self.logger.info("Inicializando ApplicationCoordinator")
        
        try:
            # Aqui podemos adicionar inicializações específicas
            # Por exemplo: configurar pools de conexão, cache, etc.
            
            self._initialized = True
            self.logger.info("ApplicationCoordinator inicializado com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao inicializar ApplicationCoordinator: {str(e)}")
            raise
    
    async def shutdown(self) -> None:
        """
        Finaliza o coordenador e todos os serviços dependentes.
        """
        if self._shutdown:
            self.logger.warning("Coordenador já foi finalizado")
            return
        
        self.logger.info("Finalizando ApplicationCoordinator")
        
        try:
            # Aqui podemos adicionar finalizações específicas
            # Por exemplo: fechar conexões, limpar cache, etc.
            
            self._shutdown = True
            self.logger.info("ApplicationCoordinator finalizado com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao finalizar ApplicationCoordinator: {str(e)}")
            raise
    
    async def health_check(self) -> dict:
        """
        Verifica a saúde da aplicação.
        
        Returns:
            Dicionário com status dos componentes
        """
        if not self._initialized or self._shutdown:
            return {
                "status": "unhealthy",
                "reason": "coordinator_not_initialized",
                "details": {
                    "initialized": self._initialized,
                    "shutdown": self._shutdown
                }
            }
        
        try:
            # Verificações básicas de saúde
            health_status = {
                "status": "healthy",
                "timestamp": asyncio.get_event_loop().time(),
                "services": {
                    "funcionario_service": "healthy",
                    "application_coordinator": "healthy"
                }
            }
            
            self.logger.debug("Health check executado com sucesso")
            return health_status
            
        except Exception as e:
            self.logger.error(f"Erro no health check: {str(e)}")
            return {
                "status": "unhealthy",
                "reason": "health_check_failed",
                "error": str(e)
            }
    
    def get_funcionario_service(self) -> FuncionarioApplicationService:
        """
        Obtém o serviço de funcionários.
        
        Returns:
            Instância do serviço de funcionários
        """
        if not self._initialized:
            raise RuntimeError("ApplicationCoordinator não foi inicializado")
        
        if self._shutdown:
            raise RuntimeError("ApplicationCoordinator foi finalizado")
        
        return self.funcionario_service
    
    @property
    def is_initialized(self) -> bool:
        """
        Verifica se o coordenador foi inicializado.
        """
        return self._initialized
    
    @property
    def is_shutdown(self) -> bool:
        """
        Verifica se o coordenador foi finalizado.
        """
        return self._shutdown


class ApplicationCoordinatorFactory:
    """
    Factory para criar instâncias do ApplicationCoordinator.
    
    Facilita a criação e configuração do coordenador em diferentes
    contextos (desenvolvimento, teste, produção).
    """
    
    @staticmethod
    async def create(
        funcionario_repository: AbstractFuncionarioRepository,
        auto_initialize: bool = True
    ) -> ApplicationCoordinator:
        """
        Cria uma nova instância do ApplicationCoordinator.
        
        Args:
            funcionario_repository: Repositório de funcionários
            auto_initialize: Se deve inicializar automaticamente
            
        Returns:
            Instância configurada do ApplicationCoordinator
        """
        coordinator = ApplicationCoordinator(funcionario_repository)
        
        if auto_initialize:
            await coordinator.initialize()
        
        return coordinator
    
    @staticmethod
    async def create_for_testing(
        funcionario_repository: AbstractFuncionarioRepository
    ) -> ApplicationCoordinator:
        """
        Cria uma instância do ApplicationCoordinator para testes.
        
        Args:
            funcionario_repository: Repositório mock para testes
            
        Returns:
            Instância configurada para testes
        """
        # Para testes, podemos ter configurações específicas
        coordinator = ApplicationCoordinator(funcionario_repository)
        await coordinator.initialize()
        
        return coordinator
