"""
Controller para operações de funcionários.

Este módulo implementa o controller que faz a ponte entre os endpoints
FastAPI e a camada de aplicação, transformando dados H        self.logger.info(f"Listando funcionários - Página: {filtros.page}, Tamanho: {filtros.size}")
        
        try:
            # Executar caso de uso com apenas paginação (conforme refinamento)
            lista_response = await self.coordinator.funcionario_service.listar_funcionarios(
                departamento=None,
                cargo=None,
                ativo=None,
                limite=filtros.size,
                offset=(filtros.page - 1) * filtros.size if filtros.page > 1 else 0
            )adas
de casos de uso.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

from app.application.coordinator import ApplicationCoordinator
from app.application.dto.requests import (
    CriarFuncionarioRequest,
    BuscarFuncionarioRequest,
    ListarFuncionariosRequest,
    AtualizarFuncionarioRequest,
    ExcluirFuncionarioRequest
)
from app.application.dto.responses import (
    FuncionarioResponse,
    ListarFuncionariosResponse
)
from app.application.exceptions import (
    ApplicationException,
    ValidationException,
    BusinessRuleException,
    ResourceNotFoundException,
    DuplicateResourceException
)
from app.presentation.schemas import (
    FuncionarioCreateSchema,
    FuncionarioUpdateSchema,
    FuncionarioResponseSchema,
    FuncionarioListQuerySchema,
    FuncionarioListResponseSchema,
    SuccessResponseSchema,
    ErrorResponseSchema
)


logger = logging.getLogger(__name__)


class FuncionarioController:
    """
    Controller para gerenciamento de funcionários.
    
    Responsável por coordenar as operações HTTP com os casos de uso
    da camada de aplicação, incluindo transformação de dados e
    tratamento de exceções.
    """
    
    def __init__(self, coordinator: ApplicationCoordinator):
        """
        Inicializa o controller.
        
        Args:
            coordinator: Coordenador de aplicação
        """
        self.coordinator = coordinator
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    # ==========================================
    # OPERAÇÕES CRUD
    # ==========================================
    
    async def criar_funcionario(
        self, 
        dados: FuncionarioCreateSchema
    ) -> SuccessResponseSchema[FuncionarioResponseSchema]:
        """
        Cria um novo funcionário.
        
        Args:
            dados: Dados do funcionário para criação
            
        Returns:
            Resposta de sucesso com dados do funcionário criado
            
        Raises:
            ValidationException: Dados inválidos
            DuplicateResourceException: Email já existe
            BusinessRuleException: Regra de negócio violada
        """
        self.logger.info(f"Iniciando criação de funcionário: {dados.email}")
        
        try:
            # Converter schema para request DTO
            request = CriarFuncionarioRequest(
                nome_completo=dados.nome_completo,
                email=dados.email,
                cpf=dados.cpf,
                telefone=dados.telefone,
                endereco=dados.endereco,
                data_nascimento=dados.data_nascimento,
                data_admissao=dados.data_admissao,
                cargo=dados.cargo,
                departamento=dados.departamento,
                salario=dados.salario
            )
            
            # Executar caso de uso
            funcionario_response = await self.coordinator.funcionario_service.criar_funcionario(request)
            
            # Converter response para schema
            funcionario_schema = self._convert_to_response_schema(funcionario_response)
            
            self.logger.info(f"Funcionário criado com sucesso: {funcionario_response.id}")
            
            return SuccessResponseSchema(
                success=True,
                message="Funcionário criado com sucesso",
                data=funcionario_schema,
                timestamp=datetime.utcnow()
            )
            
        except ApplicationException as e:
            self.logger.error(f"Erro na criação do funcionário: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado na criação do funcionário: {str(e)}")
            raise ApplicationException(f"Erro interno: {str(e)}")
    
    async def buscar_funcionario(
        self, 
        funcionario_id: str
    ) -> SuccessResponseSchema[FuncionarioResponseSchema]:
        """
        Busca um funcionário por ID.
        
        Args:
            funcionario_id: ID do funcionário
            
        Returns:
            Resposta com dados do funcionário
            
        Raises:
            ResourceNotFoundException: Funcionário não encontrado
        """
        self.logger.info(f"Buscando funcionário: {funcionario_id}")
        
        try:
            funcionario_response = await self.coordinator.funcionario_service.buscar_funcionario(funcionario_id)
            
            funcionario_schema = self._convert_to_response_schema(funcionario_response)
            
            self.logger.debug(f"Funcionário encontrado: {funcionario_id}")
            
            return SuccessResponseSchema(
                success=True,
                message="Funcionário encontrado",
                data=funcionario_schema,
                timestamp=datetime.utcnow()
            )
            
        except ApplicationException as e:
            self.logger.error(f"Erro na busca do funcionário {funcionario_id}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado na busca do funcionário {funcionario_id}: {str(e)}")
            raise ApplicationException(f"Erro interno: {str(e)}")
    
    async def listar_funcionarios(
        self, 
        filtros: FuncionarioListQuerySchema
    ) -> SuccessResponseSchema[FuncionarioListResponseSchema]:
        """
        Lista funcionários com filtros e paginação.
        
        Args:
            filtros: Parâmetros de consulta
            
        Returns:
            Resposta com lista paginada de funcionários
        """
        self.logger.info(f"Listando funcionários - Página: {filtros.page}, Tamanho: {filtros.size}, Departamento: {filtros.departamento}, Cargo: {filtros.cargo}")
        
        try:
            # Executar caso de uso com filtros opcionais
            lista_response = await self.coordinator.funcionario_service.listar_funcionarios(
                departamento=filtros.departamento,
                cargo=filtros.cargo,
                ativo=None,
                limite=filtros.size,
                offset=(filtros.page - 1) * filtros.size if filtros.page > 1 else 0
            )
            
            # Converter funcionários para schemas
            funcionarios_schema = [
                self._convert_to_response_schema(func) 
                for func in lista_response.funcionarios
            ]
            
            # Criar schema de resposta paginada
            lista_schema = FuncionarioListResponseSchema(
                funcionarios=funcionarios_schema,
                total=lista_response.total,
                skip=lista_response.skip,
                limit=lista_response.limit,
                has_next=lista_response.has_next
            )
            
            self.logger.info(f"Listagem concluída - {len(funcionarios_schema)} funcionários encontrados")
            
            return SuccessResponseSchema(
                success=True,
                message=f"{lista_response.total} funcionários encontrados",
                data=lista_schema,
                timestamp=datetime.utcnow()
            )
            
        except ApplicationException as e:
            self.logger.error(f"Erro na listagem de funcionários: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado na listagem de funcionários: {str(e)}")
            raise ApplicationException(f"Erro interno: {str(e)}")
    
    async def atualizar_funcionario(
        self, 
        funcionario_id: str,
        dados: FuncionarioUpdateSchema
    ) -> SuccessResponseSchema[FuncionarioResponseSchema]:
        """
        Atualiza dados de um funcionário.
        
        Args:
            funcionario_id: ID do funcionário
            dados: Dados para atualização
            
        Returns:
            Resposta com dados atualizados do funcionário
            
        Raises:
            ResourceNotFoundException: Funcionário não encontrado
            ValidationException: Dados inválidos
            BusinessRuleException: Regra de negócio violada
        """
        self.logger.info(f"Atualizando funcionário: {funcionario_id}")
        
        try:
            # Converter dados para dicionário (usando campos corretos)
            update_data = {}
            if dados.nome_completo is not None:
                update_data['nome_completo'] = dados.nome_completo
            if dados.telefone is not None:
                update_data['telefone'] = dados.telefone
            if dados.cargo is not None:
                update_data['cargo'] = dados.cargo
            if dados.departamento is not None:
                update_data['departamento'] = dados.departamento
            if dados.salario is not None:
                update_data['salario'] = dados.salario
            if dados.data_nascimento is not None:
                update_data['data_nascimento'] = dados.data_nascimento
            if dados.endereco is not None:
                update_data['endereco'] = dados.endereco
            
            # Executar caso de uso com parâmetros individuais
            funcionario_response = await self.coordinator.funcionario_service.atualizar_funcionario(
                funcionario_id, update_data
            )
            
            # Converter response para schema
            funcionario_schema = self._convert_to_response_schema(funcionario_response)
            
            self.logger.info(f"Funcionário atualizado com sucesso: {funcionario_id}")
            
            return SuccessResponseSchema(
                success=True,
                message="Funcionário atualizado com sucesso",
                data=funcionario_schema,
                timestamp=datetime.utcnow()
            )
            
        except ApplicationException as e:
            self.logger.error(f"Erro na atualização do funcionário {funcionario_id}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado na atualização do funcionário {funcionario_id}: {str(e)}")
            raise ApplicationException(f"Erro interno: {str(e)}")
    
    async def excluir_funcionario(self, funcionario_id: str) -> SuccessResponseSchema[Dict[str, Any]]:
        """
        Exclui um funcionário.
        
        Args:
            funcionario_id: ID do funcionário
            
        Returns:
            Resposta de confirmação da exclusão
            
        Raises:
            ResourceNotFoundException: Funcionário não encontrado
            BusinessRuleException: Funcionário ativo em projetos
        """
        self.logger.info(f"Excluindo funcionário: {funcionario_id}")
        
        try:
            request = ExcluirFuncionarioRequest(funcionario_id=funcionario_id)
            await self.coordinator.funcionario_service.excluir_funcionario(request)
            
            self.logger.info(f"Funcionário excluído com sucesso: {funcionario_id}")
            
            return SuccessResponseSchema(
                success=True,
                message="Funcionário excluído com sucesso",
                data={
                    "funcionario_id": funcionario_id,
                    "excluido_em": datetime.utcnow().isoformat()
                },
                timestamp=datetime.utcnow()
            )
            
        except ApplicationException as e:
            self.logger.error(f"Erro na exclusão do funcionário {funcionario_id}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado na exclusão do funcionário {funcionario_id}: {str(e)}")
            raise ApplicationException(f"Erro interno: {str(e)}")
    
    # ==========================================
    # MÉTODOS UTILITÁRIOS
    # ==========================================
    
    def _convert_to_response_schema(self, funcionario_response: FuncionarioResponse) -> FuncionarioResponseSchema:
        """
        Converte FuncionarioResponse para FuncionarioResponseSchema.
        
        Args:
            funcionario_response: Response do caso de uso
            
        Returns:
            Schema de resposta
        """
        return FuncionarioResponseSchema(
            id=funcionario_response.id,
            nome_completo=funcionario_response.nome_completo,
            email=funcionario_response.email,
            telefone=funcionario_response.telefone,
            cpf=getattr(funcionario_response, 'cpf', None),
            data_nascimento=getattr(funcionario_response, 'data_nascimento', None),
            data_admissao=funcionario_response.data_admissao,
            cargo=funcionario_response.cargo,
            departamento=funcionario_response.departamento,
            endereco=getattr(funcionario_response, 'endereco', None),
            salario=funcionario_response.salario,
            ativo=getattr(funcionario_response, 'ativo', False),
            created_at=funcionario_response.created_at,
            updated_at=funcionario_response.updated_at
        )
    
    def _log_request_context(self, operation: str, **kwargs):
        """
        Loga contexto da requisição para debugging.
        
        Args:
            operation: Nome da operação
            **kwargs: Dados contextuais
        """
        self.logger.debug(f"Operação: {operation}", extra={
            "operation": operation,
            "context": kwargs,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde do controller.
        
        Returns:
            Dict com status de saúde
        """
        try:
            # Testar acesso ao coordinator
            if self.coordinator is None:
                return {"status": "unhealthy", "message": "Coordinator não disponível"}
            
            # TODO: Adicionar mais verificações conforme necessário
            
            return {
                "status": "healthy",
                "message": "Controller funcionando normalmente",
                "coordinator_available": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy", 
                "message": f"Erro no controller: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }


# ==========================================
# FACTORY PARA O CONTROLLER
# ==========================================

class FuncionarioControllerFactory:
    """
    Factory para criação do controller de funcionário.
    
    Facilita testes e configuração de dependências.
    """
    
    @staticmethod
    async def create_controller(coordinator: ApplicationCoordinator) -> FuncionarioController:
        """
        Cria instância do controller.
        
        Args:
            coordinator: Coordenador de aplicação
            
        Returns:
            Instância configurada do controller
        """
        controller = FuncionarioController(coordinator)
        
        # TODO: Adicionar configurações específicas se necessário
        
        return controller
