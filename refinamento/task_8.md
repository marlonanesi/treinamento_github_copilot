# Task 8 - Integração e Configuração Final

## Objetivo
Integrar todas as camadas do microserviço, configurar a aplicação completa, implementar logging, monitoramento básico e finalizar a configuração para ambiente de desenvolvimento.

## Principais Entregas
- Integração completa de todas as camadas
- Sistema de logging estruturado
- Configuração de startup e shutdown
- Scripts de inicialização e utilitários
- Validação end-to-end do sistema
- Documentação de uso

## Critério de Pronto
- ✅ Aplicação inicializa sem erros
- ✅ Todas as operações CRUD funcionais
- ✅ Logging estruturado implementado
- ✅ Docker Compose funcional
- ✅ Documentação completa do projeto
- ✅ Sistema preparado para testes futuros

## Prompt de Execução

Como especialista em arquitetura de software e DevOps, finalize a integração do microserviço `ms-cadastro-funcionario` seguindo estas especificações como base, leia os arquivos e integre as funcionalidades:

**Configuração Principal da Aplicação (app/main.py):**
```python
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.connection import MongoDBConnection
from app.infrastructure.database.database_manager import DatabaseManager
from app.presentation.api.api_v1 import api_router
from app.presentation.api.middleware.exception_handler import add_exception_handlers
from app.presentation.api.middleware.logging_middleware import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    settings = get_settings()
    
    # Startup
    logging.info("Iniciando microserviço de funcionários...")
    
    # Conectar ao MongoDB
    mongo_connection = MongoDBConnection()
    await mongo_connection.connect()
    
    # Inicializar índices
    db_manager = DatabaseManager()
    await db_manager.create_indexes()
    
    logging.info("Microserviço iniciado com sucesso!")
    
    yield
    
    # Shutdown
    logging.info("Finalizando microserviço...")
    await mongo_connection.disconnect()
    logging.info("Microserviço finalizado!")

def create_app() -> FastAPI:
    """Factory para criar instância do FastAPI"""
    settings = get_settings()
    
    app = FastAPI(
        title="Microserviço de Cadastro de Funcionários",
        description="API para gerenciamento de funcionários da TechNovaMBA Solutions",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Adicionar middleware de logging
    app.add_middleware(LoggingMiddleware)
    
    # Configurar tratamento de exceções
    add_exception_handlers(app)
    
    # Incluir routers
    app.include_router(api_router)
    
    return app

app = create_app()
```

**Sistema de Logging (app/shared/logging/logger.py):**
```python
import logging
import json
from datetime import datetime
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """Formatter personalizado para logs em JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Adicionar contexto extra se disponível
        if hasattr(record, 'correlation_id'):
            log_entry['correlation_id'] = record.correlation_id
            
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
            
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logging():
    """Configurar sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    # Configurar formatters para diferentes handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(JSONFormatter())
```

**Configurações Finais (app/infrastructure/config/settings.py - Atualização):**
```python
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "funcionarios_db"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_VERSION: str = "v1"
    
    # Security
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

**Scripts de Utilitários:**

**Script de Inicialização (scripts/start_dev.sh):**
```bash
#!/bin/bash
echo "🚀 Iniciando ambiente de desenvolvimento..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Copiar arquivo de ambiente se não existir
if [ ! -f .env ]; then
    echo "📝 Copiando arquivo de configuração..."
    cp .env.example .env
fi

# Iniciar containers
echo "🐳 Iniciando containers..."
docker-compose up -d --build

# Aguardar MongoDB estar pronto
echo "⏳ Aguardando MongoDB estar pronto..."
sleep 10

# Verificar saúde da aplicação
echo "🔍 Verificando saúde da aplicação..."
curl -f http://localhost:8000/api/v1/health || {
    echo "❌ Aplicação não está saudável"
    exit 1
}

echo "✅ Ambiente de desenvolvimento iniciado com sucesso!"
echo "📚 Documentação disponível em: http://localhost:8000/docs"
```

**Script de Limpeza (scripts/clean.sh):**
```bash
#!/bin/bash
echo "🧹 Limpando ambiente..."

# Parar containers
docker-compose down

# Remover volumes (opcional - comentado por segurança)
# docker-compose down -v

# Remover imagens não utilizadas
docker image prune -f

echo "✅ Ambiente limpo!"
```

**Configuração Docker Atualizada (docker-compose.yml):**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - DATABASE_NAME=funcionarios_db
      - ENVIRONMENT=development
      - LOG_LEVEL=INFO
    volumes:
      - .:/app
      - /app/__pycache__
    depends_on:
      mongodb:
        condition: service_healthy
    networks:
      - funcionarios-network
    restart: unless-stopped

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password123
      - MONGO_INITDB_DATABASE=funcionarios_db
    volumes:
      - mongodb_data:/data/db
      - ./scripts/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    networks:
      - funcionarios-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

volumes:
  mongodb_data:

networks:
  funcionarios-network:
    driver: bridge
```

**Script de Inicialização MongoDB (scripts/mongo-init.js):**
```javascript
// Criar usuário para a aplicação
db = db.getSiblingDB('funcionarios_db');

db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    {
      role: 'readWrite',
      db: 'funcionarios_db'
    }
  ]
});

// Criar índices iniciais
db.funcionarios.createIndex({ "email": 1 }, { unique: true });
db.funcionarios.createIndex({ "departamento": 1 });
db.funcionarios.createIndex({ "cargo": 1 });
db.funcionarios.createIndex({ "departamento": 1, "cargo": 1 });
db.funcionarios.createIndex({ "created_at": 1 });

print('Database initialized successfully');
```

**Middleware de Correlação (app/shared/middleware/correlation.py):**
```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        
        response = await call_next(request)
        response.headers['X-Correlation-ID'] = correlation_id
        
        return response
```

**README.md Completo:**
```markdown
# Microserviço de Cadastro de Funcionários

Sistema de gerenciamento de funcionários da TechNovaMBA Solutions usando FastAPI, MongoDB e Docker.

## 🚀 Quick Start

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)

### Executando com Docker
```bash
# Clonar repositório
git clone <repository-url>
cd ms-cadastro-funcionario

# Iniciar ambiente
./scripts/start_dev.sh
```

### Acessando a aplicação
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs
- MongoDB: localhost:27017

## 📋 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /api/v1/funcionarios | Criar funcionário |
| GET | /api/v1/funcionarios | Listar funcionários |
| GET | /api/v1/funcionarios/{id} | Buscar funcionário |
| PUT | /api/v1/funcionarios/{id} | Atualizar funcionário |
| DELETE | /api/v1/funcionarios/{id} | Excluir funcionário |
| GET | /api/v1/health | Health check |

## 🏗 Arquitetura

### Estrutura de Camadas (DDD)
- **Domain**: Entidades e regras de negócio
- **Application**: Casos de uso e orquestração
- **Infrastructure**: Persistência e configurações
- **Presentation**: API REST e validações

### Stack Tecnológica
- FastAPI (Framework web)
- Pydantic (Validação de dados)
- Motor (MongoDB driver assíncrono)
- Docker (Containerização)
```

**Padrões a seguir:**
- Logging estruturado em JSON
- Health checks implementados
- Graceful shutdown
- Configuração por variáveis de ambiente
- Scripts de automação
- Documentação completa
- Monitoramento básico preparado
- Error tracking configurado

**Estrutura final esperada:**
```
ms-cadastro-funcionario/
├── app/                    # Código da aplicação
├── tests/                  # Estrutura para testes
├── scripts/               # Scripts utilitários
├── docker/               # Arquivos Docker
├── docs/                 # Documentação adicional
├── .env.example          # Variáveis de ambiente
├── docker-compose.yml    # Orquestração
├── Dockerfile           # Build da aplicação
├── requirements.txt     # Dependências
└── README.md           # Documentação principal
```

**Validações finais obrigatórias:**
- Aplicação inicia sem erros
- MongoDB conecta corretamente
- Todos os endpoints respondem adequadamente
- Documentação Swagger acessível
- Logs estruturados funcionando
- Health check retorna status correto

Implemente toda a integração final mantendo foco na robustez, monitoramento e facilidade de operação em diferentes ambientes.
