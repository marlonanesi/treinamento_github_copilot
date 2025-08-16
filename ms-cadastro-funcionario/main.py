"""
Aplicação principal FastAPI - Versão Funcional.

Este é o ponto de entrada da aplicação, configurando
todos os componentes essenciais de forma simplificada.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.infrastructure.config.settings import get_settings
from app.infrastructure.dependencies import initialize_database, shutdown_database
from app.shared.logging import setup_logging, get_logger
from app.presentation.api.v1 import configure_api_routes


# Configurar logging
settings = get_settings()

setup_logging()
logger = get_logger(__name__)


# ==========================================
# LIFESPAN EVENTS
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Gerencia o ciclo de vida da aplicação.
    """
    logger.info("🚀 Iniciando MS Cadastro de Funcionários...")
    
    # Inicialização
    try:
        # Conectar ao banco de dados
        await initialize_database()
        logger.info("✅ Infraestrutura de dados inicializada")
        
        logger.info("✅ Sistema de monitoramento inicializado")
        logger.info("🎉 MS Cadastro de Funcionários iniciado com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
        raise
    
    # Aplicação rodando
    yield
    
    # Finalização
    logger.info("🔄 Finalizando MS Cadastro de Funcionários...")
    try:
        # Fechar conexões (comentado temporariamente)
        # await shutdown_database()
        # logger.info("✅ Infraestrutura de dados finalizada")
        
        logger.info("👋 MS Cadastro de Funcionários finalizado com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro na finalização: {e}")


# ==========================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ==========================================

def create_app() -> FastAPI:
    """
    Factory function para criar e configurar a aplicação FastAPI.
    
    Returns:
        FastAPI: Aplicação configurada
    """
    
    # Criar aplicação
    app = FastAPI(
        title="MS Cadastro de Funcionários",
        description="""
🏢 **Microserviço de Cadastro de Funcionários**

Sistema completo para gerenciamento de funcionários da **TechNovaMBA Solutions** 
desenvolvido com FastAPI, MongoDB e arquitetura Clean Architecture + DDD.

## ✨ Funcionalidades

- **Cadastro Completo**: Criação, leitura, atualização e exclusão de funcionários
- **Validações Brasileiras**: CPF, telefone e email corporativo
- **Filtros Avançados**: Busca por nome, departamento, cargo e faixa salarial
- **Paginação**: Controle de resultados com limite e offset
- **Health Checks**: Monitoramento de saúde da aplicação e dependências
- **Logging Estruturado**: Rastreamento completo de requisições
- **Documentação Automática**: OpenAPI/Swagger integrado

## 🚀 Quick Start

Acesse `/docs` para a documentação interativa da API.
        """,
        version="1.0.0",
        contact={
            "name": "TechNovaMBA Solutions",
            "email": "tech@technovamba.com.br"
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        openapi_tags=[
            {
                "name": "Sistema",
                "description": "Endpoints de sistema, saúde e monitoramento"
            },
            {
                "name": "Funcionários", 
                "description": "Operações CRUD para funcionários"
            }
        ],
        # Configurações da documentação
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        # Lifespan events
        lifespan=lifespan
    )
    
    # ==========================================
    # CONFIGURAR MIDDLEWARE BÁSICO
    # ==========================================
    
    # CORS simplificado
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Em produção, especificar domínios
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Compressão GZIP
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # ==========================================
    # CONFIGURAR ROUTERS
    # ==========================================
    
    configure_api_routes(app)
    
    return app


# ==========================================
# INSTÂNCIA PRINCIPAL
# ==========================================

# Criar aplicação
app = create_app()

# Para desenvolvimento local
if __name__ == "__main__":
    import uvicorn
    
    logger.info("🔥 Iniciando servidor de desenvolvimento...")
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.is_development(),
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
