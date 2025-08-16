"""
Schemas para endpoints de health check e status da aplicação.

Este módulo define schemas para verificação de saúde da aplicação
e seus componentes (banco de dados, serviços externos, etc.).
"""

from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import Field
from enum import Enum

from .base import BaseSchema


class HealthStatus(str, Enum):
    """
    Enum para status de saúde dos componentes.
    """
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class ComponentHealthSchema(BaseSchema):
    """
    Schema para status de saúde de um componente individual.
    """
    
    status: HealthStatus = Field(
        ...,
        description="Status do componente",
        example=HealthStatus.HEALTHY
    )
    
    message: Optional[str] = Field(
        None,
        description="Mensagem descritiva do status",
        example="Conexão com banco de dados funcionando normalmente"
    )
    
    response_time_ms: Optional[float] = Field(
        None,
        description="Tempo de resposta em milissegundos",
        example=15.5
    )
    
    last_check: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da última verificação",
        example="2024-01-15T10:30:00Z"
    )
    
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Detalhes específicos do componente",
        example={"version": "7.0", "connections": 5}
    )


class DatabaseHealthSchema(ComponentHealthSchema):
    """
    Schema específico para saúde do banco de dados.
    """
    
    connection_pool_size: Optional[int] = Field(
        None,
        description="Tamanho atual do pool de conexões",
        example=10
    )
    
    active_connections: Optional[int] = Field(
        None,
        description="Número de conexões ativas",
        example=3
    )
    
    database_version: Optional[str] = Field(
        None,
        description="Versão do MongoDB",
        example="7.0.4"
    )
    
    class Config:
        """Configuração com exemplo específico para banco."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "Conexão com MongoDB funcionando normalmente",
                "response_time_ms": 12.3,
                "last_check": "2024-01-15T10:30:00Z",
                "connection_pool_size": 10,
                "active_connections": 3,
                "database_version": "7.0.4"
            }
        }


class ApplicationHealthSchema(ComponentHealthSchema):
    """
    Schema específico para saúde da aplicação.
    """
    
    version: str = Field(
        ...,
        description="Versão da aplicação",
        example="1.0.0"
    )
    
    uptime_seconds: float = Field(
        ...,
        description="Tempo de atividade em segundos",
        example=3600.5
    )
    
    environment: str = Field(
        ...,
        description="Ambiente de execução",
        example="production"
    )
    
    memory_usage_mb: Optional[float] = Field(
        None,
        description="Uso de memória em MB",
        example=128.5
    )
    
    class Config:
        """Configuração com exemplo específico para aplicação."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "Aplicação funcionando normalmente",
                "last_check": "2024-01-15T10:30:00Z",
                "version": "1.0.0",
                "uptime_seconds": 3600.5,
                "environment": "production",
                "memory_usage_mb": 128.5
            }
        }


class HealthCheckResponseSchema(BaseSchema):
    """
    Schema principal para resposta de health check da aplicação.
    
    Agregra status de todos os componentes em uma resposta unificada.
    """
    
    status: HealthStatus = Field(
        ...,
        description="Status geral da aplicação",
        example=HealthStatus.HEALTHY
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da verificação geral",
        example="2024-01-15T10:30:00Z"
    )
    
    application: ApplicationHealthSchema = Field(
        ...,
        description="Status da aplicação"
    )
    
    database: DatabaseHealthSchema = Field(
        ...,
        description="Status do banco de dados"
    )
    
    components: Dict[str, ComponentHealthSchema] = Field(
        default_factory=dict,
        description="Status de componentes adicionais",
        example={}
    )
    
    total_response_time_ms: Optional[float] = Field(
        None,
        description="Tempo total de resposta do health check",
        example=25.8
    )
    
    @property
    def is_healthy(self) -> bool:
        """
        Verifica se a aplicação está completamente saudável.
        
        Returns:
            True se todos os componentes estão saudáveis
        """
        return (
            self.status == HealthStatus.HEALTHY and
            self.application.status == HealthStatus.HEALTHY and
            self.database.status == HealthStatus.HEALTHY and
            all(comp.status == HealthStatus.HEALTHY for comp in self.components.values())
        )
    
    class Config:
        """Configuração com exemplo completo de health check."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00Z",
                "application": {
                    "status": "healthy",
                    "message": "Aplicação funcionando normalmente",
                    "last_check": "2024-01-15T10:30:00Z",
                    "version": "1.0.0",
                    "uptime_seconds": 3600.5,
                    "environment": "production",
                    "memory_usage_mb": 128.5
                },
                "database": {
                    "status": "healthy",
                    "message": "Conexão com MongoDB funcionando normalmente",
                    "response_time_ms": 12.3,
                    "last_check": "2024-01-15T10:30:00Z",
                    "connection_pool_size": 10,
                    "active_connections": 3,
                    "database_version": "7.0.4"
                },
                "components": {},
                "total_response_time_ms": 25.8
            }
        }


class LivenessProbeSchema(BaseSchema):
    """
    Schema simplificado para liveness probe (Kubernetes/Docker).
    
    Verifica apenas se a aplicação está rodando, sem detalhes de componentes.
    """
    
    status: HealthStatus = Field(
        ...,
        description="Status básico da aplicação",
        example=HealthStatus.HEALTHY
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da verificação",
        example="2024-01-15T10:30:00Z"
    )
    
    uptime_seconds: float = Field(
        ...,
        description="Tempo de atividade",
        example=3600.5
    )
    
    class Config:
        """Configuração com exemplo de liveness probe."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00Z",
                "uptime_seconds": 3600.5
            }
        }


class ReadinessProbeSchema(BaseSchema):
    """
    Schema para readiness probe (Kubernetes/Docker).
    
    Verifica se a aplicação está pronta para receber requisições,
    incluindo status de dependências críticas.
    """
    
    status: HealthStatus = Field(
        ...,
        description="Status de prontidão da aplicação",
        example=HealthStatus.HEALTHY
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da verificação",
        example="2024-01-15T10:30:00Z"
    )
    
    database_ready: bool = Field(
        ...,
        description="Indica se o banco de dados está pronto",
        example=True
    )
    
    dependencies_ready: bool = Field(
        ...,
        description="Indica se todas as dependências estão prontas",
        example=True
    )
    
    ready_for_requests: bool = Field(
        ...,
        description="Indica se está pronto para receber requisições",
        example=True
    )
    
    class Config:
        """Configuração com exemplo de readiness probe."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00Z",
                "database_ready": True,
                "dependencies_ready": True,
                "ready_for_requests": True
            }
        }


class MetricsSchema(BaseSchema):
    """
    Schema para métricas básicas da aplicação.
    
    Fornece informações sobre performance e uso de recursos.
    """
    
    requests_total: int = Field(
        ...,
        description="Total de requisições processadas",
        example=12547
    )
    
    requests_per_second: float = Field(
        ...,
        description="Taxa de requisições por segundo (média)",
        example=15.3
    )
    
    average_response_time_ms: float = Field(
        ...,
        description="Tempo médio de resposta em milissegundos",
        example=125.7
    )
    
    error_rate_percent: float = Field(
        ...,
        description="Taxa de erro em porcentagem",
        example=0.2
    )
    
    active_connections: int = Field(
        ...,
        description="Conexões ativas no momento",
        example=23
    )
    
    memory_usage_mb: float = Field(
        ...,
        description="Uso atual de memória em MB",
        example=256.8
    )
    
    cpu_usage_percent: float = Field(
        ...,
        description="Uso atual de CPU em porcentagem",
        example=35.2
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp das métricas",
        example="2024-01-15T10:30:00Z"
    )
    
    class Config:
        """Configuração com exemplo de métricas."""
        json_schema_extra = {
            "example": {
                "requests_total": 12547,
                "requests_per_second": 15.3,
                "average_response_time_ms": 125.7,
                "error_rate_percent": 0.2,
                "active_connections": 23,
                "memory_usage_mb": 256.8,
                "cpu_usage_percent": 35.2,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
