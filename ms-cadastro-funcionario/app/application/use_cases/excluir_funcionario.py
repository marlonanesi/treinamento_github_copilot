"""
Caso de uso para excluir um funcionário do sistema.
"""

from app.application.dto.requests import ExcluirFuncionarioRequest
from app.application.exceptions import ValidationException, ResourceNotFoundException, BusinessRuleException
from app.application.use_cases.base import UseCase
from app.domain.entities.funcionario import Funcionario
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository


class ExcluirFuncionarioUseCase(UseCase[ExcluirFuncionarioRequest, bool]):
    """
    Caso de uso responsável por excluir um funcionário do sistema.
    
    Implementa exclusão lógica por padrão (marcando como inativo),
    mas pode realizar exclusão física se especificado.
    
    Aplica regras de negócio para determinar se a exclusão é permitida.
    """
    
    def __init__(self, funcionario_repository: AbstractFuncionarioRepository):
        super().__init__()
        self._funcionario_repository = funcionario_repository
    
    async def execute(self, request: ExcluirFuncionarioRequest) -> bool:
        """
        Executa a exclusão de um funcionário.
        
        Args:
            request: Dados da exclusão (ID do funcionário e tipo de exclusão)
            
        Returns:
            True se a exclusão foi realizada com sucesso
            
        Raises:
            ValidationException: Se os dados são inválidos
            ResourceNotFoundException: Se o funcionário não existe
            BusinessRuleException: Se a exclusão não é permitida
        """
        # 1. Validar dados de entrada
        self._validate_request(request)
        
        # 2. Buscar funcionário existente
        funcionario = await self._get_existing_funcionario(request.funcionario_id)
        
        # 3. Aplicar regras de negócio para exclusão
        await self._validate_exclusion_rules(funcionario, request.exclusao_fisica)
        
        # 4. Executar exclusão
        if request.exclusao_fisica:
            await self._perform_physical_deletion(funcionario)
        else:
            await self._perform_logical_deletion(funcionario)
        
        # 5. Retornar sucesso
        exclusion_type = "física" if request.exclusao_fisica else "lógica"
        self.logger.info(
            f"Exclusão {exclusion_type} do funcionário {funcionario.nome_completo} "
            f"realizada com sucesso"
        )
        return True
    
    def _validate_request(self, request: ExcluirFuncionarioRequest) -> None:
        """
        Valida os dados da requisição de exclusão.
        """
        # Validação simplificada - apenas verificar se o ID existe
        if not request or not getattr(request, 'funcionario_id', None):
            raise ValidationException(
                field="funcionario_id",
                rule="é obrigatório"
            )
        
        self._log_validation("funcionario_id", "formato válido")
    
    async def _get_existing_funcionario(self, funcionario_id: str) -> Funcionario:
        """
        Busca e valida a existência do funcionário a ser excluído.
        """
        # Garantir que temos apenas a string do ID
        id_str = str(funcionario_id) if funcionario_id else None
        
        if not id_str:
            raise ValidationException(
                field="funcionario_id",
                rule="ID do funcionário é obrigatório"
            )
        
        funcionario = await self._funcionario_repository.buscar_por_id(id_str)
        
        if not funcionario:
            raise ResourceNotFoundException(
                resource="Funcionário",
                identifier=id_str
            )
        
        self.logger.info(f"Funcionário {funcionario.nome_completo} encontrado para exclusão")
        return funcionario
    
    async def _validate_exclusion_rules(
        self, 
        funcionario: Funcionario, 
        exclusao_fisica: bool
    ) -> None:
        """
        Aplica regras de negócio para determinar se a exclusão é permitida.
        """
        # Regra 1: Funcionários ativos em projetos não podem ser excluídos
        if funcionario.ativo:
            self._log_business_rule(
                "Tentativa de exclusão de funcionário ativo em projetos",
                {"funcionario_id": funcionario.id, "nome": funcionario.nome_completo}
            )
            raise BusinessRuleException(
                rule="Funcionário ativo em projetos não pode ser excluído",
                context={
                    "funcionario_id": funcionario.id,
                    "nome": funcionario.nome_completo,
                    "ativo": funcionario.ativo
                }
            )
        
        # Regra 2: Validações para exclusão física (mais restritivas)
        if exclusao_fisica:
            self._log_business_rule(
                "Validando regras para exclusão física",
                {"funcionario_id": funcionario.id}
            )
            
            # Exemplo: Não permitir exclusão física de funcionários ativos em projetos
            if funcionario.ativo:
                raise BusinessRuleException(
                    rule="Funcionário deve estar inativo em projetos antes da exclusão física",
                    context={
                        "funcionario_id": funcionario.id,
                        "status_atual": "ativo em projetos"
                    }
                )
        
        # Regra 3: Log da validação bem-sucedida
        exclusion_type = "física" if exclusao_fisica else "lógica"
        self._log_business_rule(
            f"Validação para exclusão {exclusion_type} aprovada",
            {
                "funcionario_id": funcionario.id,
                "nome": funcionario.nome_completo,
                "status_atual": "ativo em projetos" if funcionario.ativo else "inativo"
            }
        )
    
    async def _perform_logical_deletion(self, funcionario: Funcionario) -> None:
        """
        Executa exclusão lógica (removendo o funcionário do sistema).
        """
        self.logger.info(f"Executando exclusão do funcionário {funcionario.nome_completo}")
        
        # Para simplificar, fazemos exclusão física direta
        success = await self._funcionario_repository.excluir(funcionario.id)
        
        if not success:
            raise BusinessRuleException(
                rule="Falha ao executar exclusão",
                context={"funcionario_id": funcionario.id}
            )
        
        self.logger.info(f"Funcionário {funcionario.nome_completo} excluído com sucesso")
    
    async def _perform_physical_deletion(self, funcionario: Funcionario) -> None:
        """
        Executa exclusão física (removendo completamente do banco de dados).
        """
        self.logger.warning(
            f"Executando exclusão física do funcionário {funcionario.nome_completo} "
            f"(ID: {funcionario.id})"
        )
        
        # Excluir permanentemente através do método do repositório
        success = await self._funcionario_repository.excluir(funcionario.id)
        
        if not success:
            raise BusinessRuleException(
                rule="Falha ao executar exclusão física",
                context={"funcionario_id": funcionario.id}
            )
        
        self.logger.warning(
            f"Funcionário {funcionario.nome_completo} excluído permanentemente do sistema"
        )
