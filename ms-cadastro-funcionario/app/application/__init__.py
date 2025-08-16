"""
Application Layer - Camada de Aplicação

Esta camada implementa a lógica de aplicação seguindo os princípios do DDD:

- **Use Cases**: Casos de uso específicos que orquestram operações de negócio
- **Services**: Serviços de aplicação que coordenam múltiplos casos de uso  
- **DTOs**: Data Transfer Objects para entrada e saída de dados
- **Exceptions**: Exceções específicas da camada de aplicação
- **Validators**: Validadores para regras de aplicação
- **Coordinator**: Coordenador principal da aplicação

A camada de aplicação é stateless e orquestra a interação entre
a camada de domínio e a infraestrutura, sem conter regras de negócio.
"""

# Principais componentes públicos da aplicação
from app.application.coordinator import ApplicationCoordinator, ApplicationCoordinatorFactory
from app.application.services import FuncionarioApplicationService
from app.application.exceptions import (
    ApplicationException,
    ValidationException, 
    BusinessRuleException,
    ResourceNotFoundException,
    DuplicateResourceException,
    UnauthorizedOperationException
)

__all__ = [
    # Coordinator principal
    "ApplicationCoordinator",
    "ApplicationCoordinatorFactory",
    
    # Serviços
    "FuncionarioApplicationService",
    
    # Exceções
    "ApplicationException",
    "ValidationException",
    "BusinessRuleException", 
    "ResourceNotFoundException",
    "DuplicateResourceException",
    "UnauthorizedOperationException",
]
