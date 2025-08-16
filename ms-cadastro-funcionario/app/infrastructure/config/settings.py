"""
Configurações Centralizadas do Microserviço

Este módulo contém todas as configurações da aplicação usando Pydantic Settings
para validação automática e carregamento de variáveis de ambiente.
"""

import os
import json
import logging
from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Classe de configurações da aplicação.
    
    Utiliza Pydantic BaseSettings para carregamento automático de variáveis
    de ambiente com validação de tipos e valores padrão.
    """
    
    # Configurações da API
    API_HOST: str = Field(default="0.0.0.0", description="Host da API")
    API_PORT: int = Field(default=8000, description="Porta da API")
    API_VERSION: str = Field(default="v1", description="Versão da API")
    
    # Configurações do Banco de Dados
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        description="URL de conexão com MongoDB"
    )
    DATABASE_NAME: str = Field(
        default="funcionarios_db",
        description="Nome do banco de dados"
    )
    
    # Configurações de Ambiente
    ENVIRONMENT: str = Field(
        default="development",
        description="Ambiente de execução (development/production)"
    )
    DEBUG: bool = Field(default=False, description="Modo debug")
    LOG_LEVEL: str = Field(default="INFO", description="Nível de log")
    
    
    # Configurações do MongoDB (para Docker Compose)
    MONGO_INITDB_ROOT_USERNAME: Optional[str] = Field(
        default=None,
        description="Usuário root do MongoDB"
    )
    MONGO_INITDB_ROOT_PASSWORD: Optional[str] = Field(
        default=None,
        description="Senha root do MongoDB"
    )
    
    class Config:
        """Configuração do Pydantic."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignorar variáveis extras
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validar ambiente permitido."""
        valid_environments = ["development", "production", "testing"]
        if v not in valid_environments:
            raise ValueError(f"Environment must be one of: {valid_environments}")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Validar nível de log."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @validator("API_PORT")
    def validate_port(cls, v):
        """Validar porta da API."""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    @validator("DEBUG", pre=True)
    def coerce_debug(cls, v):
        if isinstance(v, bool):
            return v
        s = str(v).strip().lower()
        return s in {"1", "true", "yes", "y", "on"}
    
    def is_development(self) -> bool:
        """Verifica se está em ambiente de desenvolvimento."""
        return self.ENVIRONMENT == "development"
    
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção."""
        return self.ENVIRONMENT == "production"
    
    def get_mongodb_connection_string(self) -> str:
        """
        Retorna string de conexão formatada para MongoDB.
        
        Returns:
            str: String de conexão MongoDB
        """
        # Se tiver credenciais definidas, usar na string de conexão
        if self.MONGO_INITDB_ROOT_USERNAME and self.MONGO_INITDB_ROOT_PASSWORD:
            base_url = self.MONGODB_URL.replace("mongodb://", "")
            return f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{base_url}"
        
        return self.MONGODB_URL
    
    def setup_logging(self) -> None:
        """Configura o sistema de logging da aplicação."""
        logging.basicConfig(
            level=getattr(logging, self.LOG_LEVEL),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Configurar loggers específicos
        if self.is_development():
            # Em desenvolvimento, mostrar logs mais detalhados
            logging.getLogger("uvicorn.access").setLevel(logging.INFO)
            logging.getLogger("motor").setLevel(logging.INFO)
        else:
            # Em produção, reduzir verbosidade
            logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
            logging.getLogger("motor").setLevel(logging.WARNING)


@lru_cache()
def get_settings() -> Settings:
    """
    Factory function para obter instância única das configurações.
    
    Utiliza lru_cache para garantir que apenas uma instância seja criada
    durante o ciclo de vida da aplicação (Singleton pattern).
    
    Returns:
        Settings: Instância das configurações da aplicação
    """
    return Settings()
