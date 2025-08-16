"""
Caso de uso para atualizar dados de um funcionário existente.
"""

from datetime import date
from typing import Dict, Any

from app.application.dto.requests import AtualizarFuncionarioRequest
from app.application.dto.responses import FuncionarioResponse
from app.application.exceptions import ValidationException, ResourceNotFoundException, DuplicateResourceException
from app.application.use_cases.base import UseCase
from app.domain.entities.funcionario import Funcionario
from app.domain.entities.value_objects import Telefone, Cargo
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository
from app.domain.entities.funcionario import Funcionario
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository


class AtualizarFuncionarioUseCase(UseCase[AtualizarFuncionarioRequest, FuncionarioResponse]):
    """
    Caso de uso responsável por atualizar dados de um funcionário existente.
    
    Valida os dados de entrada, verifica se o funcionário existe,
    aplica regras de negócio para campos únicos e persiste as alterações.
    """
    
    def __init__(self, funcionario_repository: AbstractFuncionarioRepository):
        super().__init__()
        self._funcionario_repository = funcionario_repository
    
    async def execute(self, request: AtualizarFuncionarioRequest) -> FuncionarioResponse:
        """
        Executa a atualização de um funcionário.
        
        Args:
            request: Dados da atualização
            
        Returns:
            Dados do funcionário após a atualização
            
        Raises:
            ValidationException: Se os dados são inválidos
            ResourceNotFoundException: Se o funcionário não existe
            DuplicateResourceException: Se CPF ou email já existem para outro funcionário
        """
        # 1. Validar dados de entrada
        self._validate_request(request)
        
        # 2. Buscar funcionário existente
        funcionario_atual = await self._get_existing_funcionario(request.funcionario_id)
        
        # 3. Validar campos únicos se foram alterados
        await self._validate_unique_fields(request, funcionario_atual)
        
        # 4. Aplicar atualizações na entidade existente
        funcionario_atualizado = self._apply_updates_to_entity(funcionario_atual, request)
        
        # 5. Salvar funcionário atualizado no repositório
        funcionario_salvo = await self._funcionario_repository.atualizar(funcionario_atualizado)
        
        # 6. Retornar resposta
        self.logger.info(f"Funcionário {funcionario_salvo.nome_completo} atualizado com sucesso")
        return FuncionarioResponse.from_entity(funcionario_salvo)
    
    def _validate_request(self, request: AtualizarFuncionarioRequest) -> None:
        """
        Valida os dados básicos da requisição de atualização.
        """
        # Validar ID do funcionário
        if not request.funcionario_id:
            raise ValidationException(
                field="funcionario_id",
                rule="é obrigatório"
            )
        
        # Validar que pelo menos um campo foi fornecido para atualização
        campos_atualizacao = [
            request.nome_completo, request.cpf, request.email, request.telefone,
            request.endereco, request.data_nascimento, request.cargo,
            request.departamento, request.salario
        ]
        
        if not any(campo is not None for campo in campos_atualizacao):
            raise ValidationException(
                field="dados_atualizacao",
                rule="pelo menos um campo deve ser fornecido para atualização"
            )
        
        # Validar campos específicos se fornecidos
        if request.nome_completo is not None:
            if len(request.nome_completo.strip()) < 2:
                raise ValidationException(
                    field="nome_completo",
                    value=request.nome_completo,
                    rule="deve ter pelo menos 2 caracteres"
                )
        
        if request.cpf is not None:
            if len(request.cpf.replace(".", "").replace("-", "")) != 11:
                raise ValidationException(
                    field="cpf",
                    value=request.cpf,
                    rule="deve conter 11 dígitos"
                )
        
        if request.email is not None:
            if "@" not in request.email:
                raise ValidationException(
                    field="email",
                    value=request.email,
                    rule="deve ter formato válido"
                )
        
        if request.data_nascimento is not None:
            if request.data_nascimento >= date.today():
                raise ValidationException(
                    field="data_nascimento",
                    value=str(request.data_nascimento),
                    rule="deve ser uma data no passado"
                )
        
        if request.salario is not None:
            if request.salario <= 0:
                raise ValidationException(
                    field="salario",
                    value=str(request.salario),
                    rule="deve ser maior que zero"
                )
        
        self.logger.debug("Validação dos dados de atualização concluída")
    
    async def _get_existing_funcionario(self, funcionario_id: str) -> Funcionario:
        """
        Busca e valida a existência do funcionário a ser atualizado.
        """
        funcionario = await self._funcionario_repository.buscar_por_id(funcionario_id)
        
        if not funcionario:
            raise ResourceNotFoundException(
                resource="Funcionário",
                identifier=funcionario_id
            )
        
        self.logger.info(f"Funcionário {funcionario.nome_completo} encontrado para atualização")
        return funcionario
    
    async def _validate_unique_fields(
        self, 
        request: AtualizarFuncionarioRequest, 
        funcionario_atual: Funcionario
    ) -> None:
        """
        Valida campos únicos apenas se foram alterados.
        """
        # Validar CPF se foi alterado
        if request.cpf is not None and request.cpf != funcionario_atual.cpf:
            self._log_business_rule("Validando alteração de CPF", {"novo_cpf": request.cpf[:3] + "***"})
            
            funcionario_existente = await self._funcionario_repository.buscar_por_cpf(request.cpf)
            if funcionario_existente and funcionario_existente.id != funcionario_atual.id:
                raise DuplicateResourceException(
                    resource="Funcionário",
                    field="CPF",
                    value=request.cpf
                )
        
        # Validar email se foi alterado
        if request.email is not None and request.email != funcionario_atual.email:
            self._log_business_rule("Validando alteração de email", {"novo_email": request.email})
            
            funcionario_existente = await self._funcionario_repository.buscar_por_email(request.email)
            if funcionario_existente and funcionario_existente.id != funcionario_atual.id:
                raise DuplicateResourceException(
                    resource="Funcionário",
                    field="email",
                    value=request.email
                )
    
    def _prepare_update_data(self, request: AtualizarFuncionarioRequest) -> Dict[str, Any]:
        """
        Prepara o dicionário com os dados para atualização.
        
        Inclui apenas os campos que foram fornecidos na requisição.
        """
        dados = {}
        
        if request.nome_completo is not None:
            dados["nome_completo"] = request.nome_completo.strip()
        
        if request.cpf is not None:
            dados["cpf"] = request.cpf
        
        if request.email is not None:
            dados["email"] = request.email
        
        if request.telefone is not None:
            dados["telefone"] = request.telefone
        
        if request.endereco is not None:
            dados["endereco"] = request.endereco
        
        if request.data_nascimento is not None:
            dados["data_nascimento"] = request.data_nascimento
        
        if request.cargo is not None:
            dados["cargo"] = request.cargo
        
        if request.departamento is not None:
            dados["departamento"] = request.departamento
        
        if request.salario is not None:
            dados["salario"] = request.salario
        
        self.logger.debug(f"Preparados {len(dados)} campos para atualização")
        return dados
    
    def _apply_updates_to_entity(self, funcionario: Funcionario, request: AtualizarFuncionarioRequest) -> Funcionario:
        """
        Aplica as atualizações na entidade funcionário.
        
        Args:
            funcionario: Entidade funcionário atual
            request: Request com dados de atualização
            
        Returns:
            Funcionario com dados atualizados
        """
        # Usar o método atualizar da entidade para garantir validações
        funcionario.atualizar(
            nome_completo=request.nome_completo,
            cargo=request.cargo,
            telefone=request.telefone,
            departamento=request.departamento,
            salario=request.salario,
            ativo=None  # Não atualizamos este campo via API
        )
        
        return funcionario
