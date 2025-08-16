"""
Endpoints de health check da aplicação.

Este módulo implementa endpoints para verificação de saúde
da aplicação, banco de dados e dependências.
"""

import time
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.presentation.schemas import (
    HealthCheckResponseSchema,
    ApplicationHealthSchema,
    DatabaseHealthSchema,
    LivenessProbeSchema,
    ReadinessProbeSchema,
    MetricsSchema,
    HealthStatus
)
from app.presentation.api.dependencies import (
    get_health_dependencies,
    get_mongodb_connection,
    get_application_coordinator
)


# Router para health check
router = APIRouter(prefix="/health", tags=["Health Check"])

# Tempo de início da aplicação
START_TIME = time.time()


@router.get(
    "/",
    response_model=HealthCheckResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Health Check Completo",
    description="Verifica saúde geral da aplicação incluindo banco de dados e dependências"
)
async def health_check(
    health_deps: Dict[str, Any] = Depends(get_health_dependencies)
) -> HealthCheckResponseSchema:
    """
    Endpoint principal de health check.
    
    Verifica o status de todos os componentes da aplicação:
    - Status da aplicação
    - Conectividade com MongoDB
    - Métricas de performance
    
    Returns:
        Status completo de saúde da aplicação
    """
    start_check = time.time()
    
    try:
        # Status da aplicação
        app_health = ApplicationHealthSchema(
            status=HealthStatus.HEALTHY,
            message="Aplicação funcionando normalmente",
            version=health_deps.get("version", "1.0.0"),
            uptime_seconds=time.time() - START_TIME,
            environment=health_deps.get("environment", "development"),
            memory_usage_mb=health_deps.get("memory_usage", 0),
            last_check=datetime.utcnow()
        )
        
        # Verificar banco de dados
        db_health = await _check_database_health()
        
        # Status geral baseado nos componentes
        overall_status = HealthStatus.HEALTHY
        if (app_health.status != HealthStatus.HEALTHY or 
            db_health.status != HealthStatus.HEALTHY):
            overall_status = HealthStatus.DEGRADED
        
        total_time = (time.time() - start_check) * 1000  # em ms
        
        health_response = HealthCheckResponseSchema(
            status=overall_status,
            timestamp=datetime.utcnow(),
            application=app_health,
            database=db_health,
            total_response_time_ms=total_time
        )
        
        return health_response
        
    except Exception as e:
        # Em caso de erro, retornar status degradado
        app_health = ApplicationHealthSchema(
            status=HealthStatus.UNHEALTHY,
            message=f"Erro na verificação de saúde: {str(e)}",
            version="1.0.0",
            uptime_seconds=time.time() - START_TIME,
            environment="unknown",
            last_check=datetime.utcnow()
        )
        
        db_health = DatabaseHealthSchema(
            status=HealthStatus.UNKNOWN,
            message="Não foi possível verificar o banco de dados",
            last_check=datetime.utcnow()
        )
        
        health_response = HealthCheckResponseSchema(
            status=HealthStatus.UNHEALTHY,
            timestamp=datetime.utcnow(),
            application=app_health,
            database=db_health,
            total_response_time_ms=(time.time() - start_check) * 1000
        )
        
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_response.model_dump()
        )


@router.get(
    "/liveness",
    response_model=LivenessProbeSchema,
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Verificação simples se a aplicação está rodando (para Kubernetes)"
)
async def liveness_probe() -> LivenessProbeSchema:
    """
    Endpoint de liveness probe para Kubernetes.
    
    Verifica apenas se a aplicação está rodando,
    sem verificar dependências externas.
    
    Returns:
        Status básico da aplicação
    """
    return LivenessProbeSchema(
        status=HealthStatus.HEALTHY,
        timestamp=datetime.utcnow(),
        uptime_seconds=time.time() - START_TIME
    )


@router.get(
    "/readiness",
    response_model=ReadinessProbeSchema,
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe",
    description="Verifica se a aplicação está pronta para receber requisições"
)
async def readiness_probe() -> ReadinessProbeSchema:
    """
    Endpoint de readiness probe para Kubernetes.
    
    Verifica se a aplicação está pronta para receber tráfego,
    incluindo verificação de dependências críticas.
    
    Returns:
        Status de prontidão da aplicação
    """
    try:
        # Verificar banco de dados
        db_ready = await _is_database_ready()
        
        # TODO: Verificar outras dependências se existirem
        dependencies_ready = True
        
        ready_for_requests = db_ready and dependencies_ready
        
        overall_status = HealthStatus.HEALTHY if ready_for_requests else HealthStatus.UNHEALTHY
        
        readiness = ReadinessProbeSchema(
            status=overall_status,
            timestamp=datetime.utcnow(),
            database_ready=db_ready,
            dependencies_ready=dependencies_ready,
            ready_for_requests=ready_for_requests
        )
        
        if not ready_for_requests:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=readiness.model_dump()
            )
        
        return readiness
        
    except Exception:
        # Em caso de erro, não está pronto
        readiness = ReadinessProbeSchema(
            status=HealthStatus.UNHEALTHY,
            timestamp=datetime.utcnow(),
            database_ready=False,
            dependencies_ready=False,
            ready_for_requests=False
        )
        
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=readiness.model_dump()
        )


@router.get(
    "/metrics",
    response_model=MetricsSchema,
    status_code=status.HTTP_200_OK,
    summary="Métricas da Aplicação",
    description="Retorna métricas básicas de performance e uso da aplicação"
)
async def get_metrics() -> MetricsSchema:
    """
    Endpoint para métricas da aplicação.
    
    Fornece informações sobre performance, uso de recursos
    e estatísticas de operação.
    
    Returns:
        Métricas da aplicação
    """
    try:
        # TODO: Integrar com sistema de métricas real
        # Por enquanto, valores simulados baseados em dados disponíveis
        
        uptime = time.time() - START_TIME
        
        # Simular algumas métricas (em produção, vir de coletores reais)
        import psutil
        
        metrics = MetricsSchema(
            requests_total=1000,  # TODO: Pegar do middleware de métricas
            requests_per_second=15.3,
            average_response_time_ms=125.7,
            error_rate_percent=0.2,
            active_connections=5,
            memory_usage_mb=psutil.virtual_memory().used / (1024 * 1024),
            cpu_usage_percent=psutil.cpu_percent(interval=1),
            timestamp=datetime.utcnow()
        )
        
        return metrics
        
    except Exception as e:
        # Retornar métricas básicas em caso de erro
        return MetricsSchema(
            requests_total=0,
            requests_per_second=0.0,
            average_response_time_ms=0.0,
            error_rate_percent=0.0,
            active_connections=0,
            memory_usage_mb=0.0,
            cpu_usage_percent=0.0,
            timestamp=datetime.utcnow()
        )


@router.get(
    "/version",
    status_code=status.HTTP_200_OK,
    summary="Informações de Versão",
    description="Retorna informações de versão da aplicação"
)
async def get_version() -> Dict[str, Any]:
    """
    Endpoint para informações de versão.
    
    Returns:
        Informações sobre versão e build da aplicação
    """
    return {
        "name": "Microserviço de Cadastro de Funcionários",
        "version": "1.0.0",
        "description": "API para gerenciamento de funcionários da TechNovaMBA Solutions",
        "environment": "development",  # TODO: Pegar do config
        "build_date": "2024-01-15",  # TODO: Pegar do build
        "git_commit": "unknown",  # TODO: Pegar do CI/CD
        "python_version": "3.11+",
        "fastapi_version": "0.104+",
        "uptime_seconds": time.time() - START_TIME,
        "timestamp": datetime.utcnow().isoformat()
    }


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

async def _check_database_health() -> DatabaseHealthSchema:
    """
    Verifica saúde do banco de dados MongoDB.
    
    Returns:
        Schema com status do banco
    """
    start_time = time.time()
    
    try:
        # TODO: Implementar verificação real do MongoDB
        # Por enquanto, simulação
        
        # Simular tempo de resposta
        response_time = (time.time() - start_time) * 1000
        
        return DatabaseHealthSchema(
            status=HealthStatus.HEALTHY,
            message="Conexão com MongoDB funcionando normalmente",
            response_time_ms=response_time,
            last_check=datetime.utcnow(),
            connection_pool_size=10,
            active_connections=3,
            database_version="7.0.4"
        )
        
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        
        return DatabaseHealthSchema(
            status=HealthStatus.UNHEALTHY,
            message=f"Erro na conexão com MongoDB: {str(e)}",
            response_time_ms=response_time,
            last_check=datetime.utcnow()
        )


async def _is_database_ready() -> bool:
    """
    Verifica se o banco de dados está pronto para receber conexões.
    
    Returns:
        True se o banco estiver pronto
    """
    try:
        # TODO: Implementar verificação real
        # Por enquanto, retorna True simulando conexão ok
        return True
        
    except Exception:
        return False


async def _get_application_metrics() -> Dict[str, Any]:
    """
    Coleta métricas internas da aplicação.
    
    Returns:
        Dict com métricas coletadas
    """
    try:
        import psutil
        
        return {
            "memory_usage_mb": psutil.virtual_memory().used / (1024 * 1024),
            "memory_percent": psutil.virtual_memory().percent,
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "disk_usage_percent": psutil.disk_usage("/").percent,
            "network_io": dict(psutil.net_io_counters()._asdict()) if psutil.net_io_counters() else {},
            "process_count": len(psutil.pids()),
            "uptime": time.time() - START_TIME
        }
        
    except Exception:
        return {
            "memory_usage_mb": 0,
            "memory_percent": 0,
            "cpu_percent": 0,
            "uptime": time.time() - START_TIME
        }


# ==========================================
# ENDPOINTS ADMINISTRATIVOS
# ==========================================

@router.get(
    "/deep",
    status_code=status.HTTP_200_OK,
    summary="Health Check Profundo",
    description="Verificação detalhada de todos os componentes (uso administrativo)"
)
async def deep_health_check() -> Dict[str, Any]:
    """
    Health check profundo para diagnósticos.
    
    Inclui informações detalhadas sobre todos os componentes
    e dependências da aplicação.
    
    Returns:
        Informações detalhadas de saúde
    """
    try:
        # Coletar informações de todos os componentes
        app_metrics = await _get_application_metrics()
        db_health = await _check_database_health()
        
        return {
            "overall_status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": time.time() - START_TIME,
            "application": {
                "status": "healthy",
                "version": "1.0.0",
                "environment": "development",
                "metrics": app_metrics
            },
            "database": db_health.model_dump(),
            "dependencies": {
                "mongodb": db_health.status.value,
                # TODO: Adicionar outras dependências
            },
            "system_info": {
                "python_version": "3.11+",
                "platform": "unknown",  # TODO: Detectar plataforma
                "architecture": "unknown"  # TODO: Detectar arquitetura
            }
        }
        
    except Exception as e:
        return {
            "overall_status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": time.time() - START_TIME
        }
