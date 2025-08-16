"""
Schemas Pydantic para operações relacionadas a funcionários.

Este módulo contém todos os schemas de entrada, saída e validação
para as operações CRUD de funcionários.
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import Field, field_validator, model_validator, EmailStr
from decimal import Decimal

from .base import BaseSchema, TimestampMixin, PaginationMixin
from .validators import CustomValidators


class FuncionarioCreateSchema(BaseSchema):
    """
    Schema para criação de funcionário.
    
    Contém todos os campos necessários e opcionais para criar um novo funcionário,
    com validações apropriadas para cada campo.
    """
    
    nome_completo: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome completo do funcionário (mínimo 2 palavras)",
        example="João Silva Santos"
    )
    
    email: EmailStr = Field(
        ...,
        description="Email único do funcionário",
        example="joao.santos@company.com"
    )
    
    cargo: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Cargo do funcionário",
        example="Desenvolvedor Senior"
    )
    
    data_admissao: date = Field(
        ...,
        description="Data de admissão do funcionário",
        example="2023-01-15"
    )
    
    telefone: Optional[str] = Field(
        None,
        max_length=20,
        description="Telefone no formato brasileiro",
        example="(11) 99999-9999"
    )
    
    cpf: Optional[str] = Field(
        None,
        min_length=11,
        max_length=14,
        description="CPF do funcionário (opcional, somente números ou formatado)",
        example="12345678901"
    )
    
    departamento: Optional[str] = Field(
        None,
        max_length=50,
        description="Departamento do funcionário",
        example="Tecnologia"
    )
    
    data_nascimento: Optional[date] = Field(
        None,
        description="Data de nascimento do funcionário",
        example="1985-03-20"
    )
    
    endereco: Optional[str] = Field(
        None,
        max_length=200,
        description="Endereço completo do funcionário",
        example="Rua das Flores, 123 - São Paulo, SP"
    )
    
    salario: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Salário do funcionário",
        example=5000.00
    )
    
    # Validadores customizados
    @field_validator('nome_completo')
    @classmethod
    def validar_nome_completo(cls, v: str) -> str:
        """Valida e normaliza nome completo."""
        return CustomValidators.validar_nome_completo(v)
    
    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v: Optional[str]) -> Optional[str]:
        """Valida formato de telefone brasileiro."""
        return CustomValidators.validar_telefone_brasileiro(v)
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v: str) -> str:
        """Valida e normaliza email."""
        return CustomValidators.validar_email_corporativo(str(v))
    
    @field_validator('cargo')
    @classmethod
    def validar_cargo(cls, v: str) -> str:
        """Valida e normaliza cargo."""
        return CustomValidators.normalizar_cargo(v)
    
    @field_validator('departamento')
    @classmethod
    def validar_departamento(cls, v: Optional[str]) -> Optional[str]:
        """Valida e normaliza departamento."""
        return CustomValidators.normalizar_departamento(v)
    
    @field_validator('data_admissao')
    @classmethod
    def validar_data_admissao(cls, v: date) -> date:
        """Valida data de admissão."""
        return CustomValidators.validar_data_admissao(v)
    
    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento(cls, v: Optional[date]) -> Optional[date]:
        """Valida data de nascimento."""
        return CustomValidators.validar_data_nascimento(v)
    
    @field_validator('salario')
    @classmethod
    def validar_salario(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Valida salário."""
        if v is None:
            return None
        salario_validado = CustomValidators.validar_salario(v)
        return Decimal(str(salario_validado)) if salario_validado else None
    
    class Config:
        """Configuração do schema com exemplo completo."""
        json_schema_extra = {
            "example": {
                "nome_completo": "João Silva Santos",
                "email": "joao.santos@company.com",
                "cargo": "Desenvolvedor Senior",
                "data_admissao": "2023-01-15",
                "telefone": "(11) 99999-9999",
                "departamento": "Tecnologia",
                "data_nascimento": "1985-03-20",
                "endereco": "Rua das Flores, 123 - São Paulo, SP",
                "salario": 5000.00
            }
        }


class FuncionarioUpdateSchema(BaseSchema):
    """
    Schema para atualização de funcionário.
    
    Todos os campos são opcionais, permitindo atualizações parciais.
    Email e data_admissao são campos imutáveis e não podem ser alterados.
    """
    
    nome_completo: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nome completo do funcionário",
        example="João Silva Santos"
    )
    
    cargo: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Cargo do funcionário",
        example="Tech Lead"
    )
    
    telefone: Optional[str] = Field(
        None,
        max_length=20,
        description="Telefone no formato brasileiro",
        example="(11) 88888-8888"
    )
    
    departamento: Optional[str] = Field(
        None,
        max_length=50,
        description="Departamento do funcionário",
        example="Arquitetura"
    )
    
    data_nascimento: Optional[date] = Field(
        None,
        description="Data de nascimento do funcionário",
        example="1985-03-20"
    )
    
    endereco: Optional[str] = Field(
        None,
        max_length=200,
        description="Endereço completo do funcionário",
        example="Av. Paulista, 456 - São Paulo, SP"
    )
    
    salario: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Salário do funcionário",
        example=6000.00
    )
    
    # Validadores customizados (similares ao create, mas para campos opcionais)
    @field_validator('nome_completo')
    @classmethod
    def validar_nome_completo(cls, v: Optional[str]) -> Optional[str]:
        """Valida e normaliza nome completo."""
        return CustomValidators.validar_nome_completo(v) if v else None
    
    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v: Optional[str]) -> Optional[str]:
        """Valida formato de telefone brasileiro."""
        return CustomValidators.validar_telefone_brasileiro(v)
    
    @field_validator('cargo')
    @classmethod
    def validar_cargo(cls, v: Optional[str]) -> Optional[str]:
        """Valida e normaliza cargo."""
        return CustomValidators.normalizar_cargo(v) if v else None
    
    @field_validator('departamento')
    @classmethod
    def validar_departamento(cls, v: Optional[str]) -> Optional[str]:
        """Valida e normaliza departamento."""
        return CustomValidators.normalizar_departamento(v)
    
    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento(cls, v: Optional[date]) -> Optional[date]:
        """Valida data de nascimento."""
        return CustomValidators.validar_data_nascimento(v)
    
    @field_validator('salario')
    @classmethod
    def validar_salario(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Valida salário."""
        if v is None:
            return None
        salario_validado = CustomValidators.validar_salario(v)
        return Decimal(str(salario_validado)) if salario_validado else None
    
    @model_validator(mode='before')
    @classmethod
    def validar_campos_imutaveis(cls, values):
        """
        Valida que campos imutáveis não estão sendo alterados.
        
        Args:
            values: Valores do modelo
            
        Returns:
            Valores validados
            
        Raises:
            ValueError: Se campos imutáveis foram fornecidos
        """
        if isinstance(values, dict):
            campos_imutaveis = ['email', 'data_admissao']
            campos_fornecidos = [campo for campo in campos_imutaveis if campo in values]
            
            if campos_fornecidos:
                raise ValueError(
                    f"Os seguintes campos não podem ser alterados: {', '.join(campos_fornecidos)}"
                )
        
        return values
    
    @model_validator(mode='before')
    @classmethod
    def validar_pelo_menos_um_campo(cls, values):
        """
        Valida que pelo menos um campo foi fornecido para atualização.
        
        Args:
            values: Valores do modelo
            
        Returns:
            Valores validados
            
        Raises:
            ValueError: Se nenhum campo foi fornecido
        """
        if isinstance(values, dict):
            # Remove None values para verificar se há campos válidos
            campos_validos = {k: v for k, v in values.items() if v is not None}
            
            if not campos_validos:
                raise ValueError("Pelo menos um campo deve ser fornecido para atualização")
        
        return values
    
    class Config:
        """Configuração do schema com exemplo de atualização."""
        json_schema_extra = {
            "example": {
                "cargo": "Tech Lead",
                "departamento": "Arquitetura",
                "salario": 6000.00
            }
        }


class FuncionarioResponseSchema(BaseSchema, TimestampMixin):
    """
    Schema para resposta de funcionário.
    
    Representa todos os dados de um funcionário que serão retornados pela API,
    incluindo campos calculados e timestamps.
    """
    
    id: str = Field(
        ...,
        description="ID único do funcionário",
        example="60d5ecb74b24c3b3d8f8e1a2"
    )
    
    nome_completo: str = Field(
        ...,
        description="Nome completo do funcionário",
        example="João Silva Santos"
    )
    
    email: str = Field(
        ...,
        description="Email do funcionário",
        example="joao.santos@company.com"
    )
    
    cargo: str = Field(
        ...,
        description="Cargo do funcionário",
        example="Desenvolvedor Senior"
    )
    
    data_admissao: date = Field(
        ...,
        description="Data de admissão",
        example="2023-01-15"
    )
    
    telefone: Optional[str] = Field(
        None,
        description="Telefone formatado",
        example="(11) 99999-9999"
    )
    
    cpf: Optional[str] = Field(
        None,
        description="CPF do funcionário",
        example="12345678901"
    )
    
    departamento: Optional[str] = Field(
        None,
        description="Departamento do funcionário",
        example="Tecnologia"
    )
    
    data_nascimento: Optional[date] = Field(
        None,
        description="Data de nascimento",
        example="1985-03-20"
    )
    
    endereco: Optional[str] = Field(
        None,
        description="Endereço completo",
        example="Rua das Flores, 123 - São Paulo, SP"
    )
    
    salario: Optional[Decimal] = Field(
        None,
        description="Salário do funcionário",
        example=5000.00
    )
    
    ativo: bool = Field(
        False,
        description="Indica se o funcionário está ativo",
        example=False
    )
    
    # Campos de timestamp herdados de TimestampMixin
    # created_at: datetime
    # updated_at: datetime
    
    class Config:
        """Configuração do schema com exemplo completo de resposta."""
        json_schema_extra = {
            "example": {
                "id": "60d5ecb74b24c3b3d8f8e1a2",
                "nome_completo": "João Silva Santos",
                "email": "joao.santos@company.com",
                "cargo": "Desenvolvedor Senior",
                "data_admissao": "2023-01-15",
                "telefone": "(11) 99999-9999",
                "departamento": "Tecnologia",
                "data_nascimento": "1985-03-20",
                "endereco": "Rua das Flores, 123 - São Paulo, SP",
                "salario": 5000.00,
                "ativo": False,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            }
        }


class FuncionarioListQuerySchema(BaseSchema):
    """
    Schema para parâmetros de consulta da listagem de funcionários.
    
    Define parâmetros de paginação e filtros opcionais.
    """
    
    page: int = Field(
        1,
        ge=1,
        description="Número da página (inicia em 1)",
        example=1
    )
    
    size: int = Field(
        10,
        ge=1,
        le=100,
        description="Tamanho da página",
        example=10
    )
    
    departamento: Optional[str] = Field(
        None,
        max_length=50,
        description="Filtro por departamento (opcional)",
        example="Tecnologia"
    )
    
    cargo: Optional[str] = Field(
        None,
        max_length=50,
        description="Filtro por cargo (opcional)",
        example="Desenvolvedor"
    )
    
    class Config:
        """Configuração do schema com exemplos de consulta."""
        json_schema_extra = {
            "examples": [
                {
                    "page": 1,
                    "size": 10
                },
                {
                    "page": 1,
                    "size": 20,
                    "departamento": "Tecnologia"
                },
                {
                    "page": 1,
                    "size": 10,
                    "cargo": "Desenvolvedor Senior"
                },
                {
                    "page": 2,
                    "size": 15,
                    "departamento": "RH",
                    "cargo": "Analista"
                }
            ]
        }


class FuncionarioListResponseSchema(BaseSchema, PaginationMixin):
    """
    Schema para resposta da listagem de funcionários.
    
    Inclui a lista de funcionários e metadados de paginação.
    """
    
    funcionarios: List[FuncionarioResponseSchema] = Field(
        ...,
        description="Lista de funcionários encontrados"
    )
    
    # Campos de paginação herdados de PaginationMixin
    # total: int
    # skip: int
    # limit: int
    # has_next: bool
    
    class Config:
        """Configuração do schema com exemplo de listagem."""
        json_schema_extra = {
            "example": {
                "funcionarios": [
                    {
                        "id": "60d5ecb74b24c3b3d8f8e1a2",
                        "nome_completo": "João Silva Santos",
                        "email": "joao.santos@company.com",
                        "cargo": "Desenvolvedor Senior",
                        "data_admissao": "2023-01-15",
                        "telefone": "(11) 99999-9999",
                        "departamento": "Tecnologia",
                        "ativo": False,
                        "created_at": "2024-01-15T10:00:00Z",
                        "updated_at": "2024-01-15T10:00:00Z"
                    }
                ],
                "total": 25,
                "skip": 0,
                "limit": 10,
                "has_next": True
            }
        }


class FuncionarioDeleteSchema(BaseSchema):
    """
    Schema para resposta de exclusão de funcionário.
    """
    
    deleted_id: str = Field(
        ...,
        description="ID do funcionário excluído",
        example="60d5ecb74b24c3b3d8f8e1a2"
    )
    
    deleted_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da exclusão",
        example="2024-01-15T10:30:00Z"
    )
    
    class Config:
        """Configuração do schema com exemplo de exclusão."""
        json_schema_extra = {
            "example": {
                "deleted_id": "60d5ecb74b24c3b3d8f8e1a2",
                "deleted_at": "2024-01-15T10:30:00Z"
            }
        }
