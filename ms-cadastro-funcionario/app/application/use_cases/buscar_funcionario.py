"""
Caso de uso para buscar um funcionário por ID.
"""

from app.application.dto.requests import BuscarFuncionarioRequest
from app.application.dto.responses import FuncionarioResponse
from app.application.exceptions import ValidationException, ResourceNotFoundException
from app.application.use_cases.base import UseCase
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository


class BuscarFuncionarioUseCase(UseCase[BuscarFuncionarioRequest, FuncionarioResponse]):
    """
    Caso de uso responsável por buscar um funcionário específico por seu ID.
    
    Valida o ID fornecido e retorna os dados completos do funcionário
    se ele existir no sistema.
    """
    
    def __init__(self, funcionario_repository: AbstractFuncionarioRepository):
        super().__init__()
        self._funcionario_repository = funcionario_repository
    
    async def execute(self, request: BuscarFuncionarioRequest) -> FuncionarioResponse:
        """
        Executa a busca de um funcionário por ID.
        
        Args:
            request: Dados da busca (contendo o ID do funcionário)
            
        Returns:
            Dados completos do funcionário encontrado
            
        Raises:
            ValidationException: Se o ID fornecido é inválido
            ResourceNotFoundException: Se o funcionário não for encontrado
        """
        # 1. Validar dados de entrada
        self._validate_request(request)
        
        # 2. Buscar funcionário no repositório
        funcionario = await self._funcionario_repository.buscar_por_id(request.funcionario_id)
        
        # 3. Verificar se foi encontrado
        if not funcionario:
            self.logger.warning(f"Funcionário com ID {request.funcionario_id} não encontrado")
            raise ResourceNotFoundException(
                resource="Funcionário",
                identifier=request.funcionario_id
            )
        
        # 4. Retornar resposta
        self.logger.info(f"Funcionário {funcionario.nome_completo} encontrado com sucesso")
        return FuncionarioResponse.from_entity(funcionario)
    
    def _validate_request(self, request: BuscarFuncionarioRequest) -> None:
        """
        Valida os dados da requisição de busca.
        """
        if not request.funcionario_id:
            raise ValidationException(
                field="funcionario_id",
                value=request.funcionario_id,
                rule="é obrigatório"
            )
        
        if not isinstance(request.funcionario_id, str) or len(request.funcionario_id.strip()) == 0:
            raise ValidationException(
                field="funcionario_id",
                value=request.funcionario_id,
                rule="deve ser uma string não vazia"
            )
        
        self._log_validation("funcionario_id", "formato válido", request.funcionario_id)
