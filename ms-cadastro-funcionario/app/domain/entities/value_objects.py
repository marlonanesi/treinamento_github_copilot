"""
Value Objects para o Domínio de Funcionários

Implementa objetos de valor que encapsulam validações e regras
específicas para tipos de dados do domínio.
"""

import re
from typing import List
from enum import Enum

from ..exceptions.funcionario_exceptions import DadosInvalidosException, CargoInvalidoException


class Email:
    """
    Value Object para Email com validação de formato.
    
    Garante que o email tenha um formato válido antes de ser usado
    no sistema.
    """
    
    # Regex para validação de email (RFC 5322 simplificado)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    def __init__(self, value: str):
        if not value or not isinstance(value, str):
            raise DadosInvalidosException(
                "email", 
                str(value), 
                "Email deve ser uma string não vazia"
            )
        
        # Normalizar o email (lowercase)
        normalized_value = value.strip().lower()
        
        if not self.is_valid(normalized_value):
            raise DadosInvalidosException(
                "email",
                value,
                "Formato de email inválido"
            )
        
        self._value = normalized_value
    
    @property
    def value(self) -> str:
        """Retorna o valor do email normalizado."""
        return self._value
    
    @classmethod
    def is_valid(cls, email: str) -> bool:
        """
        Verifica se o email tem formato válido.
        
        Args:
            email: String do email a ser validada
            
        Returns:
            bool: True se o email é válido, False caso contrário
        """
        if not email or not isinstance(email, str):
            return False
        
        return bool(cls.EMAIL_PATTERN.match(email.strip()))
    
    def __str__(self) -> str:
        return self._value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Email):
            return self._value == other._value
        if isinstance(other, str):
            return self._value == other.strip().lower()
        return False
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __repr__(self) -> str:
        return f"Email('{self._value}')"


class TiposCargo(Enum):
    """Enumeration com os tipos de cargo válidos no sistema."""
    
    # Desenvolvimento
    DESENVOLVEDOR_JUNIOR = "Desenvolvedor Junior"
    DESENVOLVEDOR_PLENO = "Desenvolvedor Pleno" 
    DESENVOLVEDOR_SENIOR = "Desenvolvedor Senior"
    ARQUITETO_SOFTWARE = "Arquiteto de Software"
    TECH_LEAD = "Tech Lead"
    
    # Análise
    ANALISTA_SISTEMAS = "Analista de Sistemas"
    ANALISTA_NEGOCIO = "Analista de Negócio"
    ANALISTA_DADOS = "Analista de Dados"
    
    # Gestão
    GERENTE_PROJETOS = "Gerente de Projetos"
    COORDENADOR_TI = "Coordenador de TI"
    DIRETOR_TECNOLOGIA = "Diretor de Tecnologia"
    
    # Qualidade
    ANALISTA_QA = "Analista de QA"
    TESTER = "Tester"
    
    # DevOps/Infra
    DEVOPS_ENGINEER = "DevOps Engineer"
    ANALISTA_INFRAESTRUTURA = "Analista de Infraestrutura"
    
    # UX/UI
    UX_DESIGNER = "UX Designer"
    UI_DESIGNER = "UI Designer"
    PRODUCT_DESIGNER = "Product Designer"
    
    # Suporte
    ANALISTA_SUPORTE = "Analista de Suporte"
    
    @classmethod
    def get_all_values(cls) -> List[str]:
        """Retorna lista com todos os valores de cargo válidos."""
        return [cargo.value for cargo in cls]
    
    @classmethod
    def is_valid(cls, valor: str) -> bool:
        """Verifica se um cargo é válido."""
        return valor in cls.get_all_values()


class Cargo:
    """
    Value Object para Cargo com validação de cargo válido.
    
    Permite apenas cargos pré-definidos no sistema ou aceita
    cargos personalizados conforme configuração.
    """
    
    def __init__(self, value: str, permitir_cargo_personalizado: bool = True):
        if not value or not isinstance(value, str):
            raise DadosInvalidosException(
                "cargo",
                str(value),
                "Cargo deve ser uma string não vazia"
            )
        
        # Normalizar o cargo (title case)
        normalized_value = value.strip().title()
        
        # Verificar se é um cargo válido
        if not TiposCargo.is_valid(normalized_value):
            if not permitir_cargo_personalizado:
                raise CargoInvalidoException(
                    normalized_value,
                    TiposCargo.get_all_values()
                )
            # Se permite cargo personalizado, apenas valida se não está vazio
            if len(normalized_value.strip()) < 2:
                raise DadosInvalidosException(
                    "cargo",
                    normalized_value,
                    "Cargo deve ter pelo menos 2 caracteres"
                )
        
        self._value = normalized_value
    
    @property
    def value(self) -> str:
        """Retorna o valor do cargo normalizado."""
        return self._value
    
    @property
    def is_predefined(self) -> bool:
        """Verifica se o cargo é um dos pré-definidos no sistema."""
        return TiposCargo.is_valid(self._value)
    
    def __str__(self) -> str:
        return self._value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Cargo):
            return self._value == other._value
        if isinstance(other, str):
            return self._value == other.strip().title()
        return False
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __repr__(self) -> str:
        return f"Cargo('{self._value}')"


class Telefone:
    """
    Value Object para Telefone com validação de formato brasileiro.
    
    Aceita formatos: (11) 99999-9999 ou (11) 9999-9999
    """
    
    # Regex para telefone brasileiro
    TELEFONE_PATTERN = re.compile(
        r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
    )
    
    def __init__(self, value: str):
        if not value:
            raise DadosInvalidosException(
                "telefone",
                value,
                "Telefone não pode ser vazio"
            )
        
        if not isinstance(value, str):
            raise DadosInvalidosException(
                "telefone", 
                str(value),
                "Telefone deve ser uma string"
            )
        
        # Normalizar e validar o telefone
        normalized_value = self._normalize(value)
        
        if not self.is_valid(normalized_value):
            raise DadosInvalidosException(
                "telefone",
                value,
                "Formato deve ser (XX) XXXX-XXXX ou (XX) XXXXX-XXXX"
            )
        
        self._value = normalized_value
    
    def _normalize(self, value: str) -> str:
        """Normaliza o telefone para o formato padrão."""
        # Remove espaços extras e caracteres especiais desnecessários
        clean = re.sub(r'[^\d()\s-]', '', value.strip())
        
        # Se não tem parênteses, tenta adicionar
        if '(' not in clean and ')' not in clean:
            # Assume que os 2 primeiros dígitos são o DDD
            digits_only = re.sub(r'[^\d]', '', clean)
            if len(digits_only) >= 10:
                ddd = digits_only[:2]
                numero = digits_only[2:]
                if len(numero) == 8:  # Telefone fixo
                    clean = f"({ddd}) {numero[:4]}-{numero[4:]}"
                elif len(numero) == 9:  # Celular
                    clean = f"({ddd}) {numero[:5]}-{numero[5:]}"
        
        return clean
    
    @property
    def value(self) -> str:
        """Retorna o valor do telefone normalizado."""
        return self._value
    
    @classmethod
    def is_valid(cls, telefone: str) -> bool:
        """
        Verifica se o telefone tem formato válido.
        
        Args:
            telefone: String do telefone a ser validada
            
        Returns:
            bool: True se o telefone é válido, False caso contrário
        """
        if not telefone or not isinstance(telefone, str):
            return False
        
        return bool(cls.TELEFONE_PATTERN.match(telefone.strip()))
    
    def __str__(self) -> str:
        return self._value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Telefone):
            return self._value == other._value
        if isinstance(other, str):
            try:
                return self._value == Telefone(other)._value
            except DadosInvalidosException:
                return False
        return False
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __repr__(self) -> str:
        return f"Telefone('{self._value}')"
