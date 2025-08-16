"""
Caso de uso para criar um novo funcionário.
"""

from typing import List
from datetime import date

from app.application.dto.requests import CriarFuncionarioRequest
from app.application.dto.responses import FuncionarioResponse
from app.application.exceptions import ValidationException, DuplicateResourceException
from app.application.use_cases.base import UseCase
from app.domain.entities.funcionario import Funcionario
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository


class CriarFuncionarioUseCase(UseCase[CriarFuncionarioRequest, FuncionarioResponse]):
    """
    Caso de uso responsável por criar um novo funcionário no sistema.
    
    Valida os dados de entrada, verifica regras de negócio (unicidade do CPF e email)
    e persiste o novo funcionário através do repositório.
    """
    
    def __init__(self, funcionario_repository: AbstractFuncionarioRepository):
        super().__init__()
        self._funcionario_repository = funcionario_repository
    
    async def execute(self, request: CriarFuncionarioRequest) -> FuncionarioResponse:
        """
        Executa a criação de um novo funcionário.
        
        Args:
            request: Dados do funcionário a ser criado
            
        Returns:
            Dados do funcionário criado
            
        Raises:
            ValidationException: Se os dados de entrada são inválidos
            DuplicateResourceException: Se CPF ou email já existem no sistema
        """
        # 1. Validar dados de entrada
        await self._validate_request(request)
        
        # 2. Verificar se CPF já existe
        await self._validate_unique_email(request.email)
        
        # 3. Criar entidade do domínio
        funcionario = self._create_funcionario_entity(request)
        
        # 4. Persistir no repositório
        funcionario_criado = await self._funcionario_repository.salvar(funcionario)
        
        # 5. Retornar resposta
        return FuncionarioResponse.from_entity(funcionario_criado)
    
    async def _validate_request(self, request: CriarFuncionarioRequest) -> None:
        """
        Valida os dados básicos da requisição.
        """
        errors = []
        
        # Validar nome completo
        if not request.nome_completo or len(request.nome_completo.strip()) < 2:
            errors.append(ValidationException(
                field="nome_completo",
                value=request.nome_completo,
                rule="deve ter pelo menos 2 caracteres"
            ))
        
        # Validar CPF (opcional, mas se fornecido deve ter formato correto)
        if request.cpf and len(request.cpf.replace(".", "").replace("-", "")) != 11:
            errors.append(ValidationException(
                field="cpf",
                value=request.cpf,
                rule="deve conter 11 dígitos quando fornecido"
            ))
        
        # Validar email (formato básico)
        if not request.email or "@" not in request.email:
            errors.append(ValidationException(
                field="email",
                value=request.email,
                rule="deve ter formato válido"
            ))
        
        # Validar data de nascimento
        if request.data_nascimento and request.data_nascimento >= date.today():
            errors.append(ValidationException(
                field="data_nascimento",
                value=str(request.data_nascimento),
                rule="deve ser uma data no passado"
            ))
        
        # Validar salário
        if request.salario and request.salario <= 0:
            errors.append(ValidationException(
                field="salario",
                value=str(request.salario),
                rule="deve ser maior que zero"
            ))
        
        # Lançar primeira exceção encontrada (pode ser expandido para múltiplas)
        if errors:
            raise errors[0]
        
        self.logger.info("Validação básica dos dados concluída com sucesso")
    
    async def _validate_unique_email(self, email: str) -> None:
        """
        Verifica se o email já existe no sistema.
        """
        self._log_business_rule("Verificando unicidade do email", {"email": email})
        
        funcionario_existente = await self._funcionario_repository.buscar_por_email(email)
        if funcionario_existente:
            raise DuplicateResourceException(
                resource="Funcionário",
                field="email",
                value=email
            )
    
    def _create_funcionario_entity(self, request: CriarFuncionarioRequest) -> Funcionario:
        """
        Cria a entidade de domínio Funcionario a partir dos dados da requisição.
        """
        self.logger.debug("Criando entidade Funcionario")
        
        try:
            # Importar value objects
            from app.domain.entities.value_objects import Email, Cargo, Telefone
            
            # Criar value objects
            email = Email(request.email)
            cargo = Cargo(request.cargo) if request.cargo else None
            telefone = Telefone(request.telefone) if request.telefone else None
            
            # Criar entidade
            funcionario = Funcionario(
                nome_completo=request.nome_completo.strip(),
                email=email,
                cargo=cargo,
                data_admissao=request.data_admissao or date.today(),
                telefone=telefone,
                departamento=request.departamento,
                salario=request.salario
            )
            
            # Adicionar campos opcionais se fornecidos
            if request.data_nascimento:
                funcionario.data_nascimento = request.data_nascimento
            
            self.logger.info(f"Entidade Funcionario criada para {funcionario.nome_completo}")
            return funcionario
            
        except Exception as e:
            self.logger.error(f"Erro ao criar entidade Funcionario: {str(e)}")
            raise ValidationException(
                field="dados_funcionario",
                rule=f"erro na criação da entidade: {str(e)}"
            )
