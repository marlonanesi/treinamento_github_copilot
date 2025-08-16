"""
Serviços da aplicação para orquestração de casos de uso complexos.

Esta camada contém serviços que coordenam múltiplos casos de uso
ou implementam lógica de aplicação mais complexa que não se encaixa
em um único caso de uso.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import date

from app.application.dto.requests import (
    CriarFuncionarioRequest,
    BuscarFuncionarioRequest,
    ListarFuncionariosRequest,
    AtualizarFuncionarioRequest,
    ExcluirFuncionarioRequest
)
from app.application.dto.responses import FuncionarioResponse, ListarFuncionariosResponse
from app.application.exceptions import ApplicationException, BusinessRuleException
from app.application.use_cases import (
    CriarFuncionarioUseCase,
    BuscarFuncionarioUseCase,
    ListarFuncionariosUseCase,
    AtualizarFuncionarioUseCase,
    ExcluirFuncionarioUseCase
)
from app.domain.repositories.funcionario_repository import AbstractFuncionarioRepository


class FuncionarioApplicationService:
    """
    Serviço de aplicação para operações relacionadas a funcionários.
    
    Coordena a execução dos casos de uso e implementa operações
    mais complexas que envolvem múltiplos casos de uso.
    """
    
    def __init__(self, funcionario_repository: AbstractFuncionarioRepository):
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Inicializar casos de uso
        self._criar_funcionario_use_case = CriarFuncionarioUseCase(funcionario_repository)
        self._buscar_funcionario_use_case = BuscarFuncionarioUseCase(funcionario_repository)
        self._listar_funcionarios_use_case = ListarFuncionariosUseCase(funcionario_repository)
        self._atualizar_funcionario_use_case = AtualizarFuncionarioUseCase(funcionario_repository)
        self._excluir_funcionario_use_case = ExcluirFuncionarioUseCase(funcionario_repository)
    
    async def criar_funcionario(self, request: CriarFuncionarioRequest) -> FuncionarioResponse:
        """
        Cria um novo funcionário no sistema.
        
        Args:
            request: Dados do funcionário a ser criado
            
        Returns:
            Dados do funcionário criado
        """
        self.logger.info(f"Iniciando criação de funcionário: {request.nome_completo}")
        
        try:
            response = await self._criar_funcionario_use_case.execute(request)
            self.logger.info(f"Funcionário {response.nome_completo} criado com sucesso")
            return response
            
        except ApplicationException:
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado ao criar funcionário: {str(e)}")
            raise ApplicationException(f"Erro interno ao criar funcionário: {str(e)}")
    
    async def buscar_funcionario(self, funcionario_id: str) -> FuncionarioResponse:
        """
        Busca um funcionário por ID.
        
        Args:
            funcionario_id: ID do funcionário
            
        Returns:
            Dados do funcionário encontrado
        """
        self.logger.info(f"Iniciando busca de funcionário: {funcionario_id}")
        
        request = BuscarFuncionarioRequest(funcionario_id=funcionario_id)
        
        try:
            response = await self._buscar_funcionario_use_case.execute(request)
            self.logger.info(f"Funcionário {response.nome_completo} encontrado")
            return response
            
        except ApplicationException:
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado ao buscar funcionário: {str(e)}")
            raise ApplicationException(f"Erro interno ao buscar funcionário: {str(e)}")
    
    async def listar_funcionarios(
        self,
        departamento: Optional[str] = None,
        cargo: Optional[str] = None,
        ativo: Optional[bool] = None,
        limite: int = 50,
        offset: int = 0
    ) -> ListarFuncionariosResponse:
        """
        Lista funcionários com filtros opcionais.
        
        Args:
            departamento: Filtro por departamento (opcional)
            cargo: Filtro por cargo (opcional)
            ativo: Filtro por status ativo/inativo (opcional)
            limite: Número máximo de resultados
            offset: Número de registros para pular
            
        Returns:
            Lista paginada de funcionários
        """
        self.logger.info(
            f"Iniciando listagem de funcionários - "
            f"Departamento: {departamento}, Cargo: {cargo}, Ativo: {ativo}, "
            f"Limite: {limite}, Offset: {offset}"
        )
        
        request = ListarFuncionariosRequest(
            departamento=departamento,
            cargo=cargo,
            ativo=ativo,
            limite=limite,
            offset=offset
        )
        
        try:
            response = await self._listar_funcionarios_use_case.execute(request)
            self.logger.info(f"Listagem concluída: {len(response.funcionarios)} funcionários retornados")
            return response
            
        except ApplicationException:
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado ao listar funcionários: {str(e)}")
            raise ApplicationException(f"Erro interno ao listar funcionários: {str(e)}")
    
    async def atualizar_funcionario(
        self,
        funcionario_id: str,
        dados_atualizacao: Dict[str, Any]
    ) -> FuncionarioResponse:
        """
        Atualiza dados de um funcionário.
        
        Args:
            funcionario_id: ID do funcionário
            dados_atualizacao: Dicionário com os campos a serem atualizados
            
        Returns:
            Dados do funcionário após atualização
        """
        self.logger.info(f"Iniciando atualização de funcionário: {funcionario_id}")
        
        request = AtualizarFuncionarioRequest(
            funcionario_id=funcionario_id,
            nome_completo=dados_atualizacao.get('nome_completo'),
            cpf=dados_atualizacao.get('cpf'),
            email=dados_atualizacao.get('email'),
            telefone=dados_atualizacao.get('telefone'),
            endereco=dados_atualizacao.get('endereco'),
            data_nascimento=dados_atualizacao.get('data_nascimento'),
            cargo=dados_atualizacao.get('cargo'),
            departamento=dados_atualizacao.get('departamento'),
            salario=dados_atualizacao.get('salario')
        )
        
        try:
            response = await self._atualizar_funcionario_use_case.execute(request)
            self.logger.info(f"Funcionário {response.nome_completo} atualizado com sucesso")
            return response
            
        except ApplicationException:
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado ao atualizar funcionário: {str(e)}")
            raise ApplicationException(f"Erro interno ao atualizar funcionário: {str(e)}")
    
    async def excluir_funcionario(
        self,
        funcionario_id: str,
        exclusao_fisica: bool = False
    ) -> bool:
        """
        Exclui um funcionário do sistema.
        
        Args:
            funcionario_id: ID do funcionário
            exclusao_fisica: Se deve fazer exclusão física (padrão é lógica)
            
        Returns:
            True se a exclusão foi bem-sucedida
        """
        exclusion_type = "física" if exclusao_fisica else "lógica"
        self.logger.info(f"Iniciando exclusão {exclusion_type} de funcionário: {funcionario_id}")
        
        request = ExcluirFuncionarioRequest(
            funcionario_id=funcionario_id,
            exclusao_fisica=exclusao_fisica
        )
        
        try:
            success = await self._excluir_funcionario_use_case.execute(request)
            if success:
                self.logger.info(f"Exclusão {exclusion_type} concluída com sucesso")
            return success
            
        except ApplicationException:
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado ao excluir funcionário: {str(e)}")
            raise ApplicationException(f"Erro interno ao excluir funcionário: {str(e)}")
