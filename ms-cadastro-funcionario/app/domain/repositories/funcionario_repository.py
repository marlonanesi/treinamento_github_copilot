"""
Interface do Repositório de Funcionários

Define o contrato que deve ser implementado pela camada de infraestrutura
para persistência de dados de funcionários.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.funcionario import Funcionario


class AbstractFuncionarioRepository(ABC):
    """
    Interface abstrata para repositório de funcionários.
    
    Define todos os métodos que devem ser implementados pela
    camada de infraestrutura para acesso aos dados.
    """
    
    @abstractmethod
    async def salvar(self, funcionario: Funcionario) -> Funcionario:
        """
        Salva um novo funcionário no repositório.
        
        Args:
            funcionario: Instância da entidade Funcionario a ser salva
            
        Returns:
            Funcionario: Entidade salva com ID atribuído
            
        Raises:
            EmailDuplicadoException: Se o email já existir no sistema
        """
        pass
    
    @abstractmethod
    async def buscar_por_id(self, id: str) -> Optional[Funcionario]:
        """
        Busca um funcionário pelo seu ID.
        
        Args:
            id: ID único do funcionário
            
        Returns:
            Optional[Funcionario]: Funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def buscar_por_email(self, email: str) -> Optional[Funcionario]:
        """
        Busca um funcionário pelo seu email.
        
        Args:
            email: Email do funcionário
            
        Returns:
            Optional[Funcionario]: Funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def listar_todos(self, skip: int = 0, limit: int = 100) -> List[Funcionario]:
        """
        Lista todos os funcionários com paginação.
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            
        Returns:
            List[Funcionario]: Lista de funcionários
        """
        pass
    
    @abstractmethod
    async def listar_por_filtros(
        self, 
        departamento: Optional[str] = None,
        cargo: Optional[str] = None,
        ativo: Optional[bool] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Funcionario]:
        """
        Lista funcionários aplicando filtros opcionais.
        
        Args:
            departamento: Filtro por departamento (opcional)
            cargo: Filtro por cargo (opcional)
            ativo: Filtro por status em projetos (opcional)
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            
        Returns:
            List[Funcionario]: Lista de funcionários filtrados
        """
        pass
    
    @abstractmethod
    async def atualizar(self, funcionario: Funcionario) -> Funcionario:
        """
        Atualiza um funcionário existente.
        
        Args:
            funcionario: Instância da entidade Funcionario com dados atualizados
            
        Returns:
            Funcionario: Entidade atualizada
            
        Raises:
            FuncionarioNaoEncontradoException: Se o funcionário não existir
        """
        pass
    
    @abstractmethod
    async def excluir(self, id: str) -> bool:
        """
        Exclui um funcionário pelo ID.
        
        Args:
            id: ID único do funcionário
            
        Returns:
            bool: True se excluído com sucesso, False se não encontrado
            
        Raises:
            FuncionarioAtivoEmProjetosException: Se funcionário estiver ativo
        """
        pass
    
    @abstractmethod
    async def verificar_email_existe(
        self, 
        email: str, 
        excluir_id: Optional[str] = None
    ) -> bool:
        """
        Verifica se um email já existe no sistema.
        
        Args:
            email: Email a ser verificado
            excluir_id: ID do funcionário a ser excluído da verificação (para updates)
            
        Returns:
            bool: True se email existe, False caso contrário
        """
        pass
    
    @abstractmethod
    async def contar_total(self) -> int:
        """
        Conta o total de funcionários no sistema.
        
        Returns:
            int: Número total de funcionários
        """
        pass
    
    @abstractmethod
    async def contar_por_filtros(
        self,
        departamento: Optional[str] = None,
        cargo: Optional[str] = None,
        ativo: Optional[bool] = None
    ) -> int:
        """
        Conta funcionários aplicando filtros opcionais.
        
        Args:
            departamento: Filtro por departamento (opcional)
            cargo: Filtro por cargo (opcional)
            ativo: Filtro por status em projetos (opcional)
            
        Returns:
            int: Número de funcionários que atendem aos filtros
        """
        pass
