"""
Configurações da aplicação.

Este módulo centraliza todas as configurações do sistema,
usando variáveis de ambiente com valores padrão seguros.
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """
    Configurações da aplicação com validação Pydantic.
    
    Todas as configurações podem ser sobrescritas via
    variáveis de ambiente com o prefixo MS_FUNCIONARIO_.
    """
    
    # ==========================================
    # CONFIGURAÇÕES BÁSICAS
    # ==========================================
    
    APP_NAME: str = Field(
        default="MS Cadastro de Funcionários",
        description="Nome da aplicação"
    )
    
    VERSION: str = Field(
        default="1.0.0",
        description="Versão da aplicação"
    )
    
    DEBUG: bool = Field(
        default=True,
        description="Modo debug (desenvolvimento)"
    )
    
    # ==========================================
    # SERVIDOR
    # ==========================================
    
    HOST: str = Field(
        default="0.0.0.0",
        description="Host do servidor"
    )
    
    PORT: int = Field(
        default=8000,
        ge=1000,
        le=65535,
        description="Porta do servidor"
    )
    
    # ==========================================
    # LOGGING
    # ==========================================
    
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Nível de logging"
    )
    
    @validator('LOG_LEVEL')
    def validate_log_level(cls, v):
        """Valida nível de logging."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'LOG_LEVEL deve ser um de: {valid_levels}')
        return v.upper()
    
    # ==========================================
    # BANCO DE DADOS
    # ==========================================
    
    # MongoDB
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        description="URL de conexão MongoDB"
    )
    
    MONGODB_DATABASE: str = Field(
        default="ms_funcionario_db",
        description="Nome do banco de dados"
    )
    
    MONGODB_COLLECTION_FUNCIONARIOS: str = Field(
        default="funcionarios",
        description="Nome da coleção de funcionários"
    )
    
    # Pool de conexões
    MONGODB_MIN_POOL_SIZE: int = Field(
        default=1,
        ge=1,
        description="Tamanho mínimo do pool de conexões"
    )
    
    MONGODB_MAX_POOL_SIZE: int = Field(
        default=10,
        ge=1,
        description="Tamanho máximo do pool de conexões"
    )
    
    MONGODB_SERVER_SELECTION_TIMEOUT: int = Field(
        default=5000,
        ge=1000,
        description="Timeout para seleção de servidor (ms)"
    )
    
    # ==========================================
    # SEGURANÇA E CORS
    # ==========================================
    
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Origens permitidas para CORS"
    )
    
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        min_length=32,
        description="Chave secreta para JWT e outras operações"
    )
    
    # ==========================================
    # VALIDAÇÕES DE NEGÓCIO
    # ==========================================
    
    # Funcionários
    IDADE_MINIMA_FUNCIONARIO: int = Field(
        default=16,
        ge=16,
        le=100,
        description="Idade mínima para funcionário"
    )
    
    SALARIO_MINIMO: float = Field(
        default=1212.00,  # Salário mínimo Brasil 2024
        ge=0,
        description="Salário mínimo permitido"
    )
    
    SALARIO_MAXIMO: float = Field(
        default=100000.00,
        ge=1000,
        description="Salário máximo permitido"
    )
    
    # Email corporativo
    DOMINIO_EMAIL_CORPORATIVO: str = Field(
        default="empresa.com.br",
        description="Domínio obrigatório para email corporativo"
    )
    
    EXIGIR_EMAIL_CORPORATIVO: bool = Field(
        default=True,
        description="Se deve exigir email corporativo"
    )
    
    # ==========================================
    # PAGINAÇÃO
    # ==========================================
    
    PAGE_SIZE_DEFAULT: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Tamanho padrão de página"
    )
    
    PAGE_SIZE_MAX: int = Field(
        default=100,
        ge=10,
        le=1000,
        description="Tamanho máximo de página"
    )
    
    # ==========================================
    # CACHE E PERFORMANCE
    # ==========================================
    
    CACHE_TTL: int = Field(
        default=300,  # 5 minutos
        ge=60,
        description="TTL do cache em segundos"
    )
    
    REQUEST_TIMEOUT: int = Field(
        default=30,
        ge=5,
        le=300,
        description="Timeout de requisições em segundos"
    )
    
    # ==========================================
    # MONITORAMENTO
    # ==========================================
    
    ENABLE_METRICS: bool = Field(
        default=True,
        description="Habilitar coleta de métricas"
    )
    
    HEALTH_CHECK_TIMEOUT: int = Field(
        default=5,
        ge=1,
        le=30,
        description="Timeout para health checks em segundos"
    )
    
    # ==========================================
    # CONFIGURAÇÃO PYDANTIC
    # ==========================================
    
    class Config:
        """Configuração do Pydantic."""
        
        # Prefixo para variáveis de ambiente
        env_prefix = "MS_FUNCIONARIO_"
        
        # Arquivo .env
        env_file = ".env"
        env_file_encoding = "utf-8"
        
        # Validar valores na atribuição
        validate_assignment = True
        
        # Permitir campos extras
        extra = "ignore"
        
        # Case sensitive
        case_sensitive = True


# ==========================================
# INSTÂNCIA GLOBAL
# ==========================================

# Criar instância das configurações
settings = Settings()


# ==========================================
# FUNÇÕES UTILITÁRIAS
# ==========================================

def get_database_url() -> str:
    """
    Obtém URL completa do banco de dados.
    
    Returns:
        str: URL completa do MongoDB
    """
    return f"{settings.MONGODB_URL}/{settings.MONGODB_DATABASE}"


def is_production() -> bool:
    """
    Verifica se está em ambiente de produção.
    
    Returns:
        bool: True se produção, False se desenvolvimento
    """
    return not settings.DEBUG


def get_cors_origins() -> List[str]:
    """
    Obtém lista de origens permitidas para CORS.
    
    Returns:
        List[str]: Lista de origens
    """
    if settings.DEBUG:
        # Em desenvolvimento, permitir localhost em várias portas
        return [
            "http://localhost:3000",
            "http://localhost:3001", 
            "http://localhost:8080",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://127.0.0.1:8080"
        ]
    
    return settings.ALLOWED_ORIGINS


def get_log_config() -> dict:
    """
    Obtém configuração de logging estruturado.
    
    Returns:
        dict: Configuração de logging
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json" if is_production() else "default",
                "level": settings.LOG_LEVEL
            }
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console"]
        }
    }


# ==========================================
# VALIDAÇÕES ADICIONAIS
# ==========================================

def validate_settings():
    """
    Valida configurações no startup da aplicação.
    
    Raises:
        ValueError: Se alguma configuração for inválida
    """
    # Validar MongoDB URL
    if not settings.MONGODB_URL.startswith(('mongodb://', 'mongodb+srv://')):
        raise ValueError("MONGODB_URL deve começar com mongodb:// ou mongodb+srv://")
    
    # Validar salários
    if settings.SALARIO_MINIMO >= settings.SALARIO_MAXIMO:
        raise ValueError("SALARIO_MINIMO deve ser menor que SALARIO_MAXIMO")
    
    # Validar paginação
    if settings.PAGE_SIZE_DEFAULT > settings.PAGE_SIZE_MAX:
        raise ValueError("PAGE_SIZE_DEFAULT deve ser menor ou igual a PAGE_SIZE_MAX")
    
    # Validar chave secreta em produção
    if is_production() and settings.SECRET_KEY == "dev-secret-key-change-in-production":
        raise ValueError("SECRET_KEY deve ser alterada em produção")


# Validar na importação
if __name__ != "__main__":
    validate_settings()
