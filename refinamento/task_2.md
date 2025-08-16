# Task 2 - Configuração e Containerização

## Objetivo
Implementar a containerização do projeto com Docker e Docker Compose, incluindo configurações de ambiente e setup para desenvolvimento.

## Principais Entregas
- `Dockerfile` otimizado para Python com FasAPI
- `docker-compose.yml` com serviços da aplicação e MongoDB
- Scripts de inicialização e utilitários
- Configurações de ambiente para desenvolvimento e produção
- Classe de configurações centralizadas

## Critério de Pronto
- ✅ Aplicação executa corretamente em containers
- ✅ MongoDB inicializa junto com a aplicação via Docker Compose
- ✅ Configurações flexíveis entre ambientes
- ✅ Hot reload funcionando no ambiente de desenvolvimento

## Prompt de Execução

Como especialista em containerização e Python, implemente a containerização completa do microserviço `ms-cadastro-funcionario` seguindo estas especificações:

**Dockerfile (multi-stage para otimização):**
- Base: `python:3.11-slim`
- Stage 1: Build dependencies
- Stage 2: Runtime otimizado
- Usuário não-root para segurança
- Exposição da porta 8000
- Comando para iniciar com Uvicorn
- Otimizações: cache de dependências, minimal layers

**Docker Compose (docker-compose.yml):**
- Serviço `app`:
  - Build do Dockerfile local
  - Porta 8000:8000
  - Volume para hot reload em desenvolvimento
  - Variáveis de ambiente do arquivo .env
  - Dependência do serviço MongoDB
- Serviço `mongodb`:
  - Imagem oficial MongoDB 7.0
  - Porta 27017:27017
  - Volume persistente para dados
  - Variáveis de ambiente para autenticação
  - Healthcheck configurado
- Rede customizada para comunicação entre serviços

**Arquivo de Configurações (app/infrastructure/config/settings.py):**
- Classe `Settings` usando Pydantic BaseSettings
- Configurações de banco: `MONGODB_URL`, `DATABASE_NAME`
- Configurações da API: `API_HOST`, `API_PORT`, `API_VERSION`
- Configurações de ambiente: `ENVIRONMENT` (dev/prod)
- Configurações de logging: `LOG_LEVEL`
- Validação de variáveis obrigatórias
- Singleton pattern para instância única

**Scripts Utilitários (criar pasta scripts/):**
- `start_dev.sh`: Inicia ambiente de desenvolvimento
- `start_prod.sh`: Inicia ambiente de produção
- `setup.sh`: Setup inicial do projeto
- `clean.sh`: Limpeza de containers e volumes

**Configuração do Main (app/main.py):**
- Importar configurações centralizadas
- Configuração básica do FastAPI com título, descrição, versão
- Configuração de CORS para desenvolvimento
- Endpoint de health check (`/health`)
- Configuração de logging básico

**Docker Compose Override (docker-compose.override.yml):**
- Configurações específicas para desenvolvimento
- Hot reload habilitado
- Debug mode ativo
- Volumes adicionais para desenvolvimento

**Variáveis de Ambiente (.env.example atualizado):**
```
# Database
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=funcionarios_db

# API
API_HOST=0.0.0.0
API_PORT=8000
API_VERSION=v1

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO

# MongoDB (for Docker Compose)
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password123
```

**Padrões a seguir:**
- Dockerfile com boas práticas de segurança e performance
- Docker Compose com healthchecks e restart policies
- Configurações usando variáveis de ambiente
- Separação clara entre desenvolvimento e produção
- Logs estruturados e configuráveis
- Validation de configurações na inicialização

**Funcionalidades obrigatórias:**
- Container da aplicação deve iniciar sem erros
- MongoDB deve estar acessível da aplicação
- Endpoint `/health` deve retornar status 200
- Hot reload deve funcionar alterando arquivos Python
- Logs devem aparecer no console do Docker Compose

Implemente todos os arquivos de containerização mantendo foco em facilidade de desenvolvimento e preparação para produção.
