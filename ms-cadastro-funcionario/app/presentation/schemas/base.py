"""
Schema base para todos os modelos Pydantic da aplicação.

Este módulo define a classe base que será herdada por todos os schemas,
fornecendo configurações comuns e funcionalidades compartilhadas.
"""

import json
from datetime import datetime, date
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict, field_validator
from decimal import Decimal


class BaseSchema(BaseModel):
    """
    Schema base para todos os modelos Pydantic da aplicação.
    
    Fornece configurações padrão e funcionalidades comuns que serão
    herdadas por todos os outros schemas da aplicação.
    """
    
    # Configuração do Pydantic v2
    model_config = ConfigDict(
        # Permite criação de modelos a partir de atributos de objetos (ORMs)
        from_attributes=True,
        
        # Valida valores na atribuição, não apenas na criação
        validate_assignment=True,
        
        # Permite campos extras (pode ser útil para flexibilidade)
        extra="forbid",
        
        # Configurações para serialização JSON
        json_encoders={
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v),
        },
        
        # Use enum values instead of enum names
        use_enum_values=True,
        
        # Configurações de validação
        str_strip_whitespace=True,
        str_min_length=0,
    )
    
    @field_validator('*', mode='before')
    @classmethod
    def normalize_strings(cls, v: Any) -> Any:
        """
        Normaliza strings removendo espaços extras e convertendo strings vazias para None.
        
        Args:
            v: Valor a ser normalizado
            
        Returns:
            Valor normalizado
        """
        if isinstance(v, str):
            # Remove espaços no início e fim
            v = v.strip()
            # Converte string vazia para None (exceto se o campo permitir string vazia)
            if v == "":
                return None
            return v
        return v
    
    def model_dump_json_custom(self, **kwargs) -> str:
        """
        Serialização JSON customizada com tratamento especial para tipos específicos.
        
        Args:
            **kwargs: Argumentos adicionais para model_dump
            
        Returns:
            String JSON formatada
        """
        # Configurações padrão para serialização
        dump_kwargs = {
            'exclude_none': True,
            'by_alias': True,
            **kwargs
        }
        
        # Obtém o dicionário de dados
        data = self.model_dump(**dump_kwargs)
        
        # Aplica encoders customizados
        return json.dumps(data, default=self._json_encoder, ensure_ascii=False, indent=2)
    
    @staticmethod
    def _json_encoder(obj: Any) -> Any:
        """
        Encoder customizado para tipos específicos na serialização JSON.
        
        Args:
            obj: Objeto a ser serializado
            
        Returns:
            Objeto serializado
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def to_dict(self, exclude_none: bool = True, by_alias: bool = True) -> Dict[str, Any]:
        """
        Converte o modelo para dicionário com configurações customizáveis.
        
        Args:
            exclude_none: Se deve excluir campos None
            by_alias: Se deve usar aliases dos campos
            
        Returns:
            Dicionário com os dados do modelo
        """
        return self.model_dump(
            exclude_none=exclude_none,
            by_alias=by_alias
        )
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseSchema":
        """
        Cria uma instância do schema a partir de um dicionário.
        
        Args:
            data: Dicionário com os dados
            
        Returns:
            Instância do schema
        """
        return cls.model_validate(data)
    
    def update_from_dict(self, data: Dict[str, Any]) -> "BaseSchema":
        """
        Atualiza campos do modelo com dados de um dicionário.
        
        Args:
            data: Dicionário com os novos dados
            
        Returns:
            Nova instância do modelo atualizado
        """
        # Obtém dados atuais
        current_data = self.model_dump()
        
        # Atualiza com novos dados
        current_data.update({k: v for k, v in data.items() if v is not None})
        
        # Retorna nova instância
        return self.__class__.model_validate(current_data)
    
    def __str__(self) -> str:
        """
        Representação em string do modelo.
        
        Returns:
            String representando o modelo
        """
        return f"{self.__class__.__name__}({self.model_dump()})"
    
    def __repr__(self) -> str:
        """
        Representação técnica do modelo.
        
        Returns:
            String técnica representando o modelo
        """
        return self.__str__()


class TimestampMixin(BaseModel):
    """
    Mixin para schemas que possuem timestamps de criação e atualização.
    """
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Configuração específica para o mixin de timestamps."""
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z" if v else None
        }


class PaginationMixin(BaseModel):
    """
    Mixin para schemas que possuem metadados de paginação.
    """
    
    total: int
    skip: int
    limit: int
    has_next: bool
    
    @property
    def current_page(self) -> int:
        """
        Calcula a página atual baseada no skip e limit.
        
        Returns:
            Número da página atual (baseado em 1)
        """
        if self.limit <= 0:
            return 1
        return (self.skip // self.limit) + 1
    
    @property
    def total_pages(self) -> int:
        """
        Calcula o total de páginas baseado no total e limit.
        
        Returns:
            Número total de páginas
        """
        if self.limit <= 0:
            return 1
        return (self.total + self.limit - 1) // self.limit
