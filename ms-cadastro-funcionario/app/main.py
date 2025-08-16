"""
Ponto de entrada principal do Microserviço de Cadastro de Funcionários

Este módulo configura e inicializa a aplicação FastAPI com configurações
centralizadas e logging estruturado.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.infrastructure.config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação FastAPI.
    
    Executa ações de inicialização e finalização da aplicação.
    """
    settings = get_settings()
    
    # Startup
    logging.info("🚀 Iniciando Microserviço de Cadastro de Funcionários...")
    logging.info(f"📊 Ambiente: {settings.ENVIRONMENT}")
    logging.info(f"🔧 Debug: {settings.DEBUG}")
    
    # Futuro: Inicializar conexões de banco, criar índices, etc.
    
    yield
    
    # Shutdown
    logging.info("🛑 Finalizando Microserviço de Cadastro de Funcionários...")


def create_app() -> FastAPI:
    """
    Factory para criar e configurar a instância do FastAPI.
    
    Returns:
        FastAPI: Instância configurada da aplicação
    """
    settings = get_settings()
    
    # Configurar logging
    settings.setup_logging()
    
    app = FastAPI(
        title="Microserviço de Cadastro de Funcionários",
        description="API para gerenciamento de funcionários da TechNovaMBA Solutions",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # Configuração de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Endpoint de health check da aplicação.
        
        Returns:
            dict: Status da aplicação e informações de sistema
        """
        return {
            "status": "healthy",
            "service": "ms-cadastro-funcionario",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
            "database": {
                "type": "MongoDB",
                "status": "connected"  # Futuro: verificar conexão real
            }
        }
    
    return app


# Instância da aplicação
app = create_app()


if __name__ == "__main__":
    # Configuração para execução local
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.is_development(),
        log_level=settings.LOG_LEVEL.lower()
    )
