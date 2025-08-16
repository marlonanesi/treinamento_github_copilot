"""
Configuração principal dos routers da API v1.

Este módulo centraliza todos os routers da API versão 1,
configurando prefixos, tags e middleware específicos.
"""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.presentation.api.v1 import funcionarios, health


# Router principal da API v1
api_router = APIRouter(prefix="/api/v1")

# Incluir todos os routers
api_router.include_router(
    health.router,
    tags=["Sistema"]
)

api_router.include_router(
    funcionarios.router,
    tags=["Funcionários"]
)


# ==========================================
# ENDPOINTS RAIZ
# ==========================================

@api_router.get(
    "/",
    tags=["Sistema"],
    summary="Informações da API",
    description="Retorna informações gerais da API"
)
async def api_info():
    """
    Endpoint raiz da API com informações gerais.
    
    Returns:
        Informações básicas da API
    """
    return {
        "name": "MS Cadastro de Funcionários API",
        "version": "1.0.0",
        "description": "API REST para gerenciamento de funcionários",
        "docs": "/docs",
        "health": "/api/v1/health",
        "endpoints": {
            "funcionarios": "/api/v1/funcionarios",
            "health": "/api/v1/health"
        },
        "features": [
            "Cadastro Completo de funcionários",
            "Validações de negócio",
            "Filtros e paginação",
            "Monitoramento de saúde",
            "Documentação automática"
        ]
    }


# ==========================================
# CONFIGURAÇÕES ADICIONAIS
# ==========================================

def configure_api_routes(app):
    """
    Configura todas as rotas da API na aplicação FastAPI.
    
    Args:
        app: Instância da aplicação FastAPI
    """
    # Incluir router principal
    app.include_router(api_router)
    
    # Redirecionar raiz para documentação
    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        """Redireciona raiz para documentação."""
        return RedirectResponse(url="/docs")
    
    # Health check na raiz também
    @app.get("/health", include_in_schema=False, tags=["Sistema"])
    async def root_health():
        """Health check básico na raiz."""
        return {"status": "healthy", "service": "ms-cadastro-funcionario"}
