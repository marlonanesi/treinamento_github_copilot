"""
Entidade Funcionario

Implementa a entidade principal do domínio com todas as regras de negócio,
validações e comportamentos específicos de um funcionário.
"""

import re
from datetime import date, datetime
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from decimal import Decimal

from .value_objects import Email, Cargo, Telefone
from ..exceptions.funcionario_exceptions import (
    DadosInvalidosException,
    FuncionarioAtivoEmProjetosException
)


@dataclass
class Funcionario:
    """
    Entidade Funcionario - Representa um funcionário no domínio.
    
    Esta classe encapsula todas as regras de negócio relacionadas
    a funcionários, incluindo validações e comportamentos específicos.
    
    Atributos:
        id: Identificador único (será atribuído pela infraestrutura)
        nome_completo: Nome completo do funcionário (obrigatório)
        email: Email único do funcionário (obrigatório)
        cargo: Cargo do funcionário (obrigatório)
        data_admissao: Data de admissão (obrigatório)
        telefone: Telefone opcional no formato brasileiro
        departamento: Departamento opcional
        ativo: Status de participação em projetos
        created_at: Data/hora de criação do registro
        updated_at: Data/hora da última atualização
    """
    
    nome_completo: str
    email: Email
    cargo: Cargo
    data_admissao: date
    telefone: Optional[Telefone] = None
    departamento: Optional[str] = None
    salario: Optional[Decimal] = None
    ativo: bool = False
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Executado após inicialização para validações adicionais."""
        # Validar nome completo
        self._validar_nome_completo(self.nome_completo)
        
        # Validar data de admissão
        self._validar_data_admissao(self.data_admissao)
        
        # Normalizar departamento
        if self.departamento:
            self.departamento = self.departamento.strip().title()
            if len(self.departamento) < 2:
                raise DadosInvalidosException(
                    "departamento",
                    self.departamento,
                    "Departamento deve ter pelo menos 2 caracteres"
                )
        
        # Garantir que updated_at seja sempre atual na criação
        if not self.id:  # Novo funcionário
            self.updated_at = datetime.utcnow()
    
    @classmethod
    def criar(
        cls,
        nome_completo: str,
        email: str,
        cargo: str,
        data_admissao: date,
        telefone: Optional[str] = None,
        departamento: Optional[str] = None,
        salario: Optional[Decimal] = None,
        ativo: bool = False
    ) -> 'Funcionario':
        """
        Método factory para criar um novo funcionário com validações.
        
        Args:
            nome_completo: Nome completo do funcionário
            email: Email único do funcionário
            cargo: Cargo do funcionário
            data_admissao: Data de admissão
            telefone: Telefone opcional
            departamento: Departamento opcional
            salario: Salário opcional
            ativo: Status em projetos (padrão False)
            
        Returns:
            Funcionario: Nova instância validada
            
        Raises:
            DadosInvalidosException: Se algum dado for inválido
        """
        # Criar value objects com validação
        email_vo = Email(email)
        cargo_vo = Cargo(cargo)
        telefone_vo = Telefone(telefone) if telefone else None
        
        return cls(
            nome_completo=nome_completo,
            email=email_vo,
            cargo=cargo_vo,
            data_admissao=data_admissao,
            telefone=telefone_vo,
            departamento=departamento,
            salario=salario,
            ativo=ativo
        )
    
    def atualizar(
        self,
        nome_completo: Optional[str] = None,
        cargo: Optional[str] = None,
        telefone: Optional[str] = None,
        departamento: Optional[str] = None,
        salario: Optional[Decimal] = None,
        ativo: Optional[bool] = None
    ) -> None:
        """
        Atualiza dados do funcionário com validações.
        
        Nota: Email e data de admissão não podem ser alterados conforme
        regras de negócio.
        
        Args:
            nome_completo: Novo nome completo
            cargo: Novo cargo
            telefone: Novo telefone (pode ser None para remover)
            departamento: Novo departamento (pode ser None para remover)
            salario: Novo salário
            ativo: Novo status em projetos
        """
        if nome_completo is not None:
            self._validar_nome_completo(nome_completo)
            self.nome_completo = nome_completo
        
        if cargo is not None:
            self.cargo = Cargo(cargo)
        
        if telefone is not None:
            self.telefone = Telefone(telefone) if telefone.strip() else None
        
        if departamento is not None:
            if departamento.strip():
                normalized_dept = departamento.strip().title()
                if len(normalized_dept) < 2:
                    raise DadosInvalidosException(
                        "departamento",
                        departamento,
                        "Departamento deve ter pelo menos 2 caracteres"
                    )
                self.departamento = normalized_dept
            else:
                self.departamento = None
        
        if ativo is not None:
            self.ativo = ativo
        
        if salario is not None:
            # Validar que salário não é negativo
            if salario < 0:
                raise DadosInvalidosException(
                    "salario",
                    str(salario),
                    "Salário não pode ser negativo"
                )
            self.salario = salario
        
        # Atualizar timestamp
        self.updated_at = datetime.utcnow()
    
    def marcar_ativo(self) -> None:
        """Marca o funcionário como ativo em projetos."""
        self.ativo = True
        self.updated_at = datetime.utcnow()
    
    def desmarcar_ativo(self) -> None:
        """Remove a marcação de ativo em projetos."""
        self.ativo = False
        self.updated_at = datetime.utcnow()
    
    def pode_ser_excluido(self) -> bool:
        """
        Verifica se o funcionário pode ser excluído.
        
        Regra de negócio: Funcionários ativos em projetos não podem ser excluídos.
        
        Returns:
            bool: True se pode ser excluído, False caso contrário
        """
        return not self.ativo
    
    def validar_exclusao(self) -> None:
        """
        Valida se o funcionário pode ser excluído.
        
        Raises:
            FuncionarioAtivoEmProjetosException: Se não puder ser excluído
        """
        if not self.pode_ser_excluido():
            raise FuncionarioAtivoEmProjetosException(
                funcionario_id=self.id,
                nome=self.nome_completo
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a entidade para dicionário para persistência.
        
        Returns:
            Dict[str, Any]: Representação da entidade em dicionário
        """
        data = {
            'nome_completo': self.nome_completo,
            'email': self.email.value,
            'cargo': self.cargo.value,
            'data_admissao': self.data_admissao.isoformat(),
            'departamento': self.departamento,
            'salario': float(self.salario) if self.salario else None,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if self.id:
            data['_id'] = self.id
        
        if self.telefone:
            data['telefone'] = self.telefone.value
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Funcionario':
        """
        Cria uma instância de Funcionario a partir de um dicionário.
        
        Args:
            data: Dicionário com dados do funcionário
            
        Returns:
            Funcionario: Instância criada a partir dos dados
        """
        # Converter datas string para objetos
        data_admissao = date.fromisoformat(data['data_admissao'])
        created_at = datetime.fromisoformat(data['created_at'])
        updated_at = datetime.fromisoformat(data['updated_at'])
        
        # Criar value objects
        email_vo = Email(data['email'])
        cargo_vo = Cargo(data['cargo'])
        telefone_vo = Telefone(data['telefone']) if data.get('telefone') else None
        
        # Converter salario
        salario = None
        if data.get('salario') is not None:
            salario = Decimal(str(data['salario']))
        
        funcionario = cls(
            id=data.get('_id'),
            nome_completo=data['nome_completo'],
            email=email_vo,
            cargo=cargo_vo,
            data_admissao=data_admissao,
            telefone=telefone_vo,
            departamento=data.get('departamento'),
            salario=salario,
            ativo=data.get('ativo', data.get('ativo', False)),
            created_at=created_at,
            updated_at=updated_at
        )
        
        return funcionario
    
    def _validar_nome_completo(self, nome: str) -> None:
        """
        Valida se o nome completo atende às regras de negócio.
        
        Regras:
        - Deve ter pelo menos 2 palavras
        - Cada palavra deve ter pelo menos 2 caracteres
        - Não pode conter números ou caracteres especiais
        
        Args:
            nome: Nome a ser validado
            
        Raises:
            DadosInvalidosException: Se o nome for inválido
        """
        if not nome or not isinstance(nome, str):
            raise DadosInvalidosException(
                "nome_completo",
                str(nome),
                "Nome completo deve ser uma string não vazia"
            )
        
        nome_limpo = nome.strip()
        
        if len(nome_limpo) < 5:
            raise DadosInvalidosException(
                "nome_completo",
                nome,
                "Nome completo deve ter pelo menos 5 caracteres"
            )
        
        # Verificar se contém apenas letras, espaços, acentos e hífens
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\']+$', nome_limpo):
            raise DadosInvalidosException(
                "nome_completo",
                nome,
                "Nome deve conter apenas letras, espaços, hífens e apostrofes"
            )
        
        # Verificar se tem pelo menos 2 palavras
        palavras = [p.strip() for p in nome_limpo.split() if p.strip()]
        if len(palavras) < 2:
            raise DadosInvalidosException(
                "nome_completo",
                nome,
                "Nome completo deve ter pelo menos 2 palavras"
            )
        
        # Verificar se cada palavra tem pelo menos 2 caracteres
        for palavra in palavras:
            if len(palavra) < 2:
                raise DadosInvalidosException(
                    "nome_completo",
                    nome,
                    "Cada palavra do nome deve ter pelo menos 2 caracteres"
                )
    
    def _validar_data_admissao(self, data: date) -> None:
        """
        Valida se a data de admissão é válida.
        
        Regra: Não pode ser uma data futura.
        
        Args:
            data: Data a ser validada
            
        Raises:
            DadosInvalidosException: Se a data for inválida
        """
        if not isinstance(data, date):
            raise DadosInvalidosException(
                "data_admissao",
                str(data),
                "Data de admissão deve ser um objeto date válido"
            )
        
        if data > date.today():
            raise DadosInvalidosException(
                "data_admissao",
                data.isoformat(),
                "Data de admissão não pode ser futura"
            )
        
        # Validar se não é muito antiga (ex: mais de 50 anos)
        from datetime import timedelta
        data_minima = date.today() - timedelta(days=50 * 365)  # 50 anos
        if data < data_minima:
            raise DadosInvalidosException(
                "data_admissao",
                data.isoformat(),
                "Data de admissão não pode ser anterior a 50 anos"
            )
    
    def __str__(self) -> str:
        return f"{self.nome_completo} ({self.email.value}) - {self.cargo.value}"
    
    def __repr__(self) -> str:
        return (
            f"Funcionario(id={self.id}, nome_completo='{self.nome_completo}', "
            f"email='{self.email.value}', cargo='{self.cargo.value}')"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Funcionario):
            return False
        
        # Se ambos têm ID, comparar por ID
        if self.id and other.id:
            return self.id == other.id
        
        # Caso contrário, comparar por email (único)
        return self.email == other.email
    
    def __hash__(self) -> int:
        if self.id:
            return hash(self.id)
        return hash(self.email.value)
