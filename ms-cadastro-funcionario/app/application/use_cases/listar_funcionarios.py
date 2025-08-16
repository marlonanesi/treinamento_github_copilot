"""
Caso de uso para listar funcionários com filtros e paginação.
"""

from typing import List

from app.application.dto.requests import ListarFuncionariosRequest
from app.application.dto.responses import ListarFuncionariosResponse, FuncionarioResponse
from app.application.exceptions import ValidationException
from app.application.use_cases.base import UseCase
from app.domain.entities.funcionario import Funcionario
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository


class ListarFuncionariosUseCase(UseCase[ListarFuncionariosRequest, ListarFuncionariosResponse]):
    """
    Caso de uso responsável por listar funcionários com suporte a:
    - Filtros opcionais (departamento, cargo, ativo/inativo)
    - Paginação (limite e offset)
    - Ordenação básica
    """
    
    def __init__(self, funcionario_repository: AbstractFuncionarioRepository):
        super().__init__()
        self._funcionario_repository = funcionario_repository
    
    async def execute(self, request: ListarFuncionariosRequest) -> ListarFuncionariosResponse:
        """
        Executa a listagem de funcionários com os filtros aplicados.
        
        Args:
            request: Parâmetros de filtro, paginação e ordenação
            
        Returns:
            Lista paginada de funcionários que atendem aos critérios
            
        Raises:
            ValidationException: Se os parâmetros de paginação são inválidos
        """
        # 1. Validar parâmetros de entrada
        self._validate_request(request)
        
        # 2. Aplicar filtros e buscar funcionários
        funcionarios = await self._buscar_funcionarios_filtrados(request)
        
        # 3. Contar total de registros (para paginação)
        total = await self._contar_funcionarios_filtrados(request)
        
        # 4. Criar resposta paginada
        response = ListarFuncionariosResponse.create(
            funcionarios=funcionarios,  # Entidades direto do repositório
            total=total,
            skip=request.offset,
            limit=request.limite
        )
        
        self.logger.info(
            f"Listagem concluída: {len(funcionarios)} funcionários retornados "
            f"de {total} total (página {request.offset // request.limite + 1})"
        )
        
        return response
    
    def _validate_request(self, request: ListarFuncionariosRequest) -> None:
        """
        Valida os parâmetros da requisição de listagem.
        """
        # Validar limite
        if request.limite is not None:
            if request.limite <= 0:
                raise ValidationException(
                    field="limite",
                    value=str(request.limite),
                    rule="deve ser maior que zero"
                )
            if request.limite > 1000:
                raise ValidationException(
                    field="limite",
                    value=str(request.limite),
                    rule="não pode ser maior que 1000"
                )
        
        # Validar offset
        if request.offset is not None and request.offset < 0:
            raise ValidationException(
                field="offset",
                value=str(request.offset),
                rule="deve ser maior ou igual a zero"
            )
        
        self.logger.debug(f"Parâmetros de paginação validados: limite={request.limite}, offset={request.offset}")
    
    async def _buscar_funcionarios_filtrados(self, request: ListarFuncionariosRequest) -> List[Funcionario]:
        """
        Busca funcionários aplicando os filtros especificados.
        """
        # Verificar se há filtros para aplicar
        if self._has_filters(request):
            self.logger.debug(f"Aplicando filtros: departamento={request.departamento}, cargo={request.cargo}, ativo={request.ativo}")
            return await self._funcionario_repository.listar_por_filtros(
                departamento=request.departamento,
                cargo=request.cargo,
                ativo=request.ativo,
                skip=request.offset,
                limit=request.limite
            )
        else:
            self.logger.debug("Listando todos os funcionários sem filtros")
            return await self._funcionario_repository.listar_todos(
                skip=request.offset,
                limit=request.limite
            )

    async def _contar_funcionarios_filtrados(self, request: ListarFuncionariosRequest) -> int:
        """
        Conta o total de funcionários que atendem aos filtros.
        """
        # Usar contagem com filtros se aplicável
        if self._has_filters(request):
            self.logger.debug("Contando funcionários com filtros")
            return await self._funcionario_repository.contar_por_filtros(
                departamento=request.departamento,
                cargo=request.cargo,
                ativo=request.ativo
            )
        else:
            self.logger.debug("Contando todos os funcionários")
            return await self._funcionario_repository.contar_total()
    
    def _has_filters(self, request: ListarFuncionariosRequest) -> bool:
        """
        Verifica se a requisição possui filtros aplicados.
        """
        return any([
            request.departamento,
            request.cargo,
            request.ativo is not None
        ])
