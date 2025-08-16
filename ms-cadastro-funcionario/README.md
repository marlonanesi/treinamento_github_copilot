# Microserviço de Cadastro de Funcionários

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![DDD](https://img.shields.io/badge/Architecture-DDD-orange)

Sistema de gerenciamento de funcionários da **TechNovaMBA Solutions** desenvolvido com FastAPI, MongoDB e arquitetura DDD simplificada (Domain Driven Design).

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Setup do Zero](#-setup-do-zero)
- [API Endpoints](#-api-endpoints)
- [Configuração](#️-configuração)
- [Desenvolvimento](#-desenvolvimento)
- [Como Implementar Novas Funcionalidades](#-como-implementar-novas-funcionalidades)
- [Testes](#-testes)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contribuição](#-contribuição)

## 🎯 Visão Geral

Este microserviço faz parte da migração do sistema monolítico da TechNovaMBA Solutions para uma arquitetura moderna baseada em microsserviços. Ele gerencia o cadastro, consulta, atualização e remoção de funcionários.

### Funcionalidades Principais

- ✅ Cadastro de funcionários com validação de email único
- ✅ Consulta de funcionários com filtros por departamento e cargo
- ✅ Atualização de dados (exceto email e data de admissão - campos imutáveis)
- ✅ Exclusão controlada (funcionários ativos em projetos não podem ser excluídos)
- ✅ Validações de entrada robustas (CPF, telefone, email, salário)
- ✅ Documentação automática da API (Swagger/OpenAPI)
- ✅ Logging estruturado em JSON
- ✅ Health checks para monitoramento
- ✅ Paginação de resultados
- ✅ Tratamento de exceções padronizado

### Regras de Negócio Implementadas

- **Email único**: Não é possível cadastrar dois funcionários com o mesmo email
- **Campos imutáveis**: Email e data de admissão não podem ser alterados após criação
- **Exclusão controlada**: Funcionários com `ativo: true` não podem ser excluídos
- **Validação de telefone**: Formato brasileiro com validação de celular (9º dígito)
- **Validação de CPF**: Formato e dígitos verificadores válidos
- **Validação de salário**: Deve ser positivo quando informado

## 🏗 Arquitetura

### Estrutura DDD (Domain Driven Design)

```
ms-cadastro-funcionario/
├── app/
│   ├── domain/                 # 🏛️ Camada de Domínio
│   │   ├── entities/           # Entidades de negócio
│   │   │   ├── funcionario.py  # Entidade principal
│   │   │   └── value_objects.py # Email, Cargo, Telefone
│   │   ├── repositories/       # Contratos de repositório
│   │   └── exceptions/         # Exceções de domínio
│   │
│   ├── application/            # 🎯 Camada de Aplicação
│   │   ├── use_cases/          # Casos de uso CRUD
│   │   ├── dto/               # Data Transfer Objects
│   │   ├── services/          # Serviços de aplicação
│   │   └── coordinators/      # Coordenação entre use cases
│   │
│   ├── infrastructure/         # 🔧 Camada de Infraestrutura
│   │   ├── database/          # Configuração MongoDB
│   │   └── repositories/      # Implementação de repositórios
│   │
│   ├── presentation/          # 🌐 Camada de Apresentação
│   │   ├── api/              # Endpoints FastAPI
│   │   │   ├── controllers/   # Controllers REST
│   │   │   └── v1/           # Versionamento da API
│   │   ├── schemas/          # Schemas Pydantic
│   │   └── middleware/       # Middlewares customizados
│   │
│   └── shared/               # 🛠️ Utilitários Compartilhados
│       ├── exceptions/       # Exceções base
│       └── utils/           # Utilities gerais
│
├── scripts/                  # Scripts auxiliares
├── tests/                   # Estrutura de testes (futuro)
├── docs/                    # Documentação adicional
└── requirements/            # Dependências organizadas
```

### Stack Tecnológica

| Componente | Tecnologia | Versão | Propósito |
|------------|------------|--------|-----------|
| Framework Web | FastAPI | 0.104+ | API REST assíncrona de alta performance |
| Validação | Pydantic | 2.5+ | Validação e serialização de dados |
| Banco de Dados | MongoDB | 7.0+ | Persistência NoSQL com flexibilidade |
| Driver BD | Motor | 3.3+ | Cliente MongoDB assíncrono |
| ASGI Server | Uvicorn | 0.24+ | Servidor de aplicação Python |
| Containerização | Docker | 24.0+ | Empacotamento e isolamento |
| Orquestração | Docker Compose | 2.20+ | Ambiente de desenvolvimento |

## 🔧 Pré-requisitos

### Para Desenvolvimento com Docker (Recomendado)
- **Docker** 24.0+
- **Docker Compose** 2.20+
- **Git**
- **Editor/IDE** (VSCode recomendado)

### Para Desenvolvimento Local (Opcional)
- **Python** 3.11+
- **MongoDB** 7.0+
- **pip** 23.0+

## 🚀 Setup do Zero

### 1. Clonar e Preparar o Projeto

```bash
# Clonar o repositório
git clone <repository-url>
cd ms-cadastro-funcionario

# Verificar estrutura do projeto
ls -la
```

### 2. Configuração de Ambiente

```bash
# Copiar arquivo de configuração
cp .env.example .env

# Editar variáveis de ambiente (opcional para desenvolvimento)
nano .env
```

**Arquivo .env padrão:**
```bash
# Database
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=funcionarios_db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_VERSION=v1

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=false

# CORS
ALLOWED_ORIGINS=*
```

### 3. Executar com Docker (Recomendado)

```bash
# Iniciar ambiente completo (API + MongoDB)
docker-compose up -d

# Verificar se os serviços estão rodando
docker-compose ps

# Acompanhar logs da aplicação
docker-compose logs -f app
```

### 4. Executar Localmente (Alternativo)

```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar MongoDB localmente (Ubuntu/Debian)
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update && sudo apt-get install -y mongodb-org

# Iniciar MongoDB
sudo systemctl start mongod

# Executar aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Verificar Instalação

```bash
# Health check da aplicação
curl http://localhost:8000/api/v1/health

# Resposta esperada:
# {
#   "success": true,
#   "message": "Sistema funcionando corretamente",
#   "data": {
#     "status": "healthy",
#     "database": "connected",
#     "timestamp": "2025-08-10T10:30:00Z"
#   }
# }

# Acessar documentação Swagger
open http://localhost:8000/docs

# Acessar documentação ReDoc
open http://localhost:8000/redoc
```

### 6. Dados de Exemplo (Opcional)

```bash
# O sistema já vem com dados de exemplo pré-carregados via mongo-init.js
# Para verificar os dados iniciais:
docker-compose exec mongodb mongosh funcionarios_db --eval "db.funcionarios.find().pretty()"
```

## 📡 API Endpoints

### 🔗 Base URL
```
http://localhost:8000/api/v1
```

### 👥 Funcionários

| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| `POST` | `/funcionarios` | Criar novo funcionário | ✅ |
| `GET` | `/funcionarios` | Listar funcionários com filtros | ✅ |
| `GET` | `/funcionarios/{id}` | Buscar funcionário por ID | ✅ |
| `PUT` | `/funcionarios/{id}` | Atualizar funcionário | ✅ |
| `DELETE` | `/funcionarios/{id}` | Excluir funcionário | ✅ |

### 🏥 Sistema

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Health check da aplicação |
| `GET` | `/docs` | Documentação Swagger UI |
| `GET` | `/redoc` | Documentação ReDoc |

### 📝 Exemplos de Uso

**1. Criar Funcionário:**
```bash
curl -X POST "http://localhost:8000/api/v1/funcionarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_completo": "João Silva Santos",
    "email": "joao.santos@company.com",
    "cargo": "Desenvolvedor Senior",
    "data_admissao": "2024-01-15",
    "telefone": "(11) 99999-9999",
    "departamento": "Tecnologia",
    "salario": 8500.00,
    "data_nascimento": "1985-03-20"
  }'
```

**2. Listar Funcionários com Filtros:**
```bash
# Todos os funcionários (paginado)
curl "http://localhost:8000/api/v1/funcionarios?page=1&size=10"

# Filtrar por departamento
curl "http://localhost:8000/api/v1/funcionarios?departamento=Tecnologia"

# Filtrar por cargo e departamento
curl "http://localhost:8000/api/v1/funcionarios?cargo=Desenvolvedor&departamento=RH&page=1&size=5"
```

**3. Buscar por ID:**
```bash
curl "http://localhost:8000/api/v1/funcionarios/60d5ecb74b24c3b3d8f8e1a2"
```

**4. Atualizar Funcionário:**
```bash
curl -X PUT "http://localhost:8000/api/v1/funcionarios/60d5ecb74b24c3b3d8f8e1a2" \
  -H "Content-Type: application/json" \
  -d '{
    "cargo": "Tech Lead",
    "salario": 12000.00,
    "departamento": "Arquitetura"
  }'
```

**5. Excluir Funcionário:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/funcionarios/60d5ecb74b24c3b3d8f8e1a2"
```

### 📊 Estrutura de Resposta Padrão

**Sucesso:**
```json
{
  "success": true,
  "message": "Operação realizada com sucesso",
  "data": { ... },
  "timestamp": "2025-08-10T10:30:00Z"
}
```

**Erro de Validação:**
```json
{
  "success": false,
  "message": "Dados inválidos",
  "error": {
    "type": "ValidationError",
    "details": [
      {
        "field": "email",
        "message": "Email já existe no sistema"
      }
    ]
  },
  "timestamp": "2025-08-10T10:30:00Z"
}
```

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão | Obrigatória |
|----------|-----------|--------|-------------|
| `MONGODB_URL` | URL de conexão MongoDB | `mongodb://localhost:27017` | ✅ |
| `DATABASE_NAME` | Nome do banco de dados | `funcionarios_db` | ✅ |
| `API_HOST` | Host da aplicação | `0.0.0.0` | ❌ |
| `API_PORT` | Porta da aplicação | `8000` | ❌ |
| `API_VERSION` | Versão da API | `v1` | ❌ |
| `ENVIRONMENT` | Ambiente (dev/prod) | `development` | ❌ |
| `LOG_LEVEL` | Nível de log | `INFO` | ❌ |
| `DEBUG` | Modo debug | `false` | ❌ |
| `ALLOWED_ORIGINS` | CORS origins | `*` | ❌ |

### Estrutura de Configuração

```python
# app/config.py
class Settings:
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "funcionarios_db"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    # ... outras configurações
```

## 🛠 Desenvolvimento

### Comandos Úteis

```bash
# Desenvolvimento com Docker
docker-compose up -d              # Iniciar ambiente
docker-compose down               # Parar ambiente
docker-compose logs -f app        # Ver logs em tempo real
docker-compose exec app bash      # Acessar container da aplicação
docker-compose exec mongodb mongosh # Acessar MongoDB

# Desenvolvimento local
uvicorn app.main:app --reload     # Executar com auto-reload
python -m pytest                 # Executar testes (futuro)
black app/                        # Formatação de código
isort app/                        # Organizar imports
flake8 app/                       # Análise estática
```

### Estrutura de Logs

```json
{
  "timestamp": "2025-08-10T10:30:00Z",
  "level": "INFO",
  "logger": "funcionario_service",
  "message": "Funcionário criado com sucesso",
  "extra": {
    "funcionario_id": "60d5ecb74b24c3b3d8f8e1a2",
    "email": "joao@company.com",
    "operation": "create_funcionario"
  }
}
```

### Debug e Desenvolvimento

```bash
# Habilitar modo debug (mais logs)
export DEBUG=true
export LOG_LEVEL=DEBUG

# Executar com debugger (se usando local)
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn app.main:app --reload
```

## 🔄 Como Implementar Novas Funcionalidades

### 1. Implementando Nova Rota/Endpoint

**Exemplo: Endpoint para listar funcionários por salário**

**a) Criar Schema de Entrada (presentation/schemas/):**
```python
# app/presentation/schemas/funcionario_schemas.py
class FuncionarioPorSalarioQuerySchema(BaseSchema):
    salario_min: Optional[float] = Field(None, ge=0)
    salario_max: Optional[float] = Field(None, ge=0)
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
```

**b) Criar Caso de Uso (application/use_cases/):**
```python
# app/application/use_cases/listar_funcionarios_por_salario.py
from app.application.dto.requests import ListarFuncionariosPorSalarioRequest
from app.application.dto.responses import FuncionarioListResponse

class ListarFuncionariosPorSalarioUseCase:
    def __init__(self, funcionario_repository):
        self.funcionario_repository = funcionario_repository
    
    async def execute(self, request: ListarFuncionariosPorSalarioRequest) -> FuncionarioListResponse:
        # Lógica de negócio aqui
        funcionarios = await self.funcionario_repository.listar_por_faixa_salario(
            salario_min=request.salario_min,
            salario_max=request.salario_max,
            skip=(request.page - 1) * request.size,
            limit=request.size
        )
        
        return FuncionarioListResponse(funcionarios=funcionarios)
```

**c) Implementar no Repositório (infrastructure/repositories/):**
```python
# app/infrastructure/repositories/funcionario_repository_impl.py
async def listar_por_faixa_salario(
    self,
    salario_min: Optional[float] = None,
    salario_max: Optional[float] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Funcionario]:
    query_filters = {}
    
    if salario_min is not None or salario_max is not None:
        salario_filter = {}
        if salario_min is not None:
            salario_filter["$gte"] = salario_min
        if salario_max is not None:
            salario_filter["$lte"] = salario_max
        query_filters["salario"] = salario_filter
    
    cursor = self.collection.find(query_filters).skip(skip).limit(limit)
    documents = await cursor.to_list(length=None)
    
    return [FuncionarioModel.to_entity(doc) for doc in documents]
```

**d) Criar Controller (presentation/api/controllers/):**
```python
# app/presentation/api/controllers/funcionario_controller.py
async def listar_funcionarios_por_salario(
    self, 
    query: FuncionarioPorSalarioQuerySchema
) -> SuccessResponseSchema[FuncionarioListResponseSchema]:
    request = ListarFuncionariosPorSalarioRequest(
        salario_min=query.salario_min,
        salario_max=query.salario_max,
        page=query.page,
        size=query.size
    )
    
    resultado = await self.coordinator.listar_funcionarios_por_salario_use_case.execute(request)
    
    return SuccessResponseSchema(
        message="Funcionários encontrados",
        data=FuncionarioListResponseSchema.from_response(resultado)
    )
```

**e) Criar Endpoint (presentation/api/v1/):**
```python
# app/presentation/api/v1/funcionarios.py
@router.get(
    "/por-salario",
    response_model=SuccessResponseSchema[FuncionarioListResponseSchema],
    summary="Listar funcionários por faixa salarial"
)
async def listar_funcionarios_por_salario(
    query: Annotated[FuncionarioPorSalarioQuerySchema, Depends()],
    controller: Annotated[FuncionarioController, Depends(get_funcionario_controller)]
):
    return await controller.listar_funcionarios_por_salario(query)
```

### 2. Implementando Novo Filtro

**Exemplo: Filtro por data de admissão**

**a) Atualizar Schema Existente:**
```python
# app/presentation/schemas/funcionario_schemas.py
class FuncionarioListQuerySchema(BaseSchema):
    # ... campos existentes ...
    data_admissao_inicio: Optional[date] = Field(None, description="Data de admissão inicial")
    data_admissao_fim: Optional[date] = Field(None, description="Data de admissão final")
```

**b) Atualizar Repositório:**
```python
# app/infrastructure/repositories/funcionario_repository_impl.py
async def listar_por_filtros(
    self,
    departamento: Optional[str] = None,
    cargo: Optional[str] = None,
    ativo: Optional[bool] = None,
    data_admissao_inicio: Optional[date] = None,
    data_admissao_fim: Optional[date] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Funcionario]:
    query_filters = {}
    
    # ... filtros existentes ...
    
    # Novo filtro por data de admissão
    if data_admissao_inicio or data_admissao_fim:
        data_filter = {}
        if data_admissao_inicio:
            data_filter["$gte"] = datetime.combine(data_admissao_inicio, datetime.min.time())
        if data_admissao_fim:
            data_filter["$lte"] = datetime.combine(data_admissao_fim, datetime.max.time())
        query_filters["data_admissao"] = data_filter
    
    # ... resto da implementação ...
```

### 3. Implementando Nova Camada/Serviço

**Exemplo: Serviço de Relatórios**

**a) Criar Interface no Domínio:**
```python
# app/domain/repositories/relatorio_repository.py
from abc import ABC, abstractmethod

class AbstractRelatorioRepository(ABC):
    @abstractmethod
    async def gerar_relatorio_departamental(self) -> Dict[str, Any]:
        pass
```

**b) Implementar na Infraestrutura:**
```python
# app/infrastructure/repositories/relatorio_repository_impl.py
class RelatorioRepositoryImpl(AbstractRelatorioRepository):
    def __init__(self, collection):
        self.collection = collection
    
    async def gerar_relatorio_departamental(self) -> Dict[str, Any]:
        pipeline = [
            {"$group": {
                "_id": "$departamento",
                "total_funcionarios": {"$sum": 1},
                "salario_medio": {"$avg": "$salario"}
            }}
        ]
        
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=None)
```

**c) Criar Caso de Uso:**
```python
# app/application/use_cases/gerar_relatorio.py
class GerarRelatorioUseCase:
    def __init__(self, relatorio_repository: AbstractRelatorioRepository):
        self.relatorio_repository = relatorio_repository
    
    async def execute(self) -> RelatorioResponse:
        dados = await self.relatorio_repository.gerar_relatorio_departamental()
        return RelatorioResponse(dados=dados)
```

### 4. Adicionando Validação Customizada

**Exemplo: Validar CNPJ da empresa**

```python
# app/presentation/schemas/validators.py
class CustomValidators:
    @staticmethod
    def validar_cnpj(v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        
        # Remover formatação
        cnpj = re.sub(r'[^0-9]', '', v)
        
        if len(cnpj) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        
        # Validação dos dígitos verificadores (implementar algoritmo)
        # ... lógica de validação ...
        
        return cnpj

# Usar no schema
class EmpresaSchema(BaseSchema):
    cnpj: Optional[str] = Field(None)
    
    @field_validator('cnpj')
    @classmethod
    def validar_cnpj(cls, v: Optional[str]) -> Optional[str]:
        return CustomValidators.validar_cnpj(v)
```

## 🧪 Testes

### Estrutura Preparada para Testes

```
tests/
├── unit/                    # Testes unitários (futuro)
│   ├── domain/             # Testes das entidades e value objects
│   ├── application/        # Testes dos casos de uso
│   └── infrastructure/     # Testes dos repositórios
├── integration/            # Testes de integração (futuro)
│   ├── api/               # Testes dos endpoints
│   └── database/          # Testes com banco de dados
├── fixtures/              # Dados para testes (futuro)
├── conftest.py           # Configurações pytest
└── README.md             # Guia de testes
```

### Configuração para Testes (Futuro)

```python
# tests/conftest.py
import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import create_app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_app():
    app = create_app()
    return app

@pytest.fixture
async def test_client(test_app):
    from httpx import AsyncClient
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client
```

### Testes Manuais Atuais

```bash
# Testar criação de funcionário
curl -X POST "http://localhost:8000/api/v1/funcionarios" \
  -H "Content-Type: application/json" \
  -d @test_payload.json

# Testar health check
curl "http://localhost:8000/api/v1/health"

# Verificar dados no banco
docker-compose exec mongodb mongosh funcionarios_db --eval "db.funcionarios.find().pretty()"
```

## 🚀 Deployment

### Desenvolvimento (Docker Compose)

```bash
# Ambiente de desenvolvimento
docker-compose up -d

# Verificar serviços
docker-compose ps

# Parar ambiente
docker-compose down
```

### Produção (Docker)

**1. Build da Imagem:**
```bash
# Build para produção
docker build -t ms-cadastro-funcionario:latest .

# Tag para registry (exemplo)
docker tag ms-cadastro-funcionario:latest registry.company.com/ms-cadastro-funcionario:v1.0.0
```

**2. Deploy com Docker:**
```bash
# Executar container de produção
docker run -d \
  --name funcionarios-api \
  --restart unless-stopped \
  -p 8000:8000 \
  -e MONGODB_URL=mongodb://prod-mongo-cluster:27017 \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=INFO \
  ms-cadastro-funcionario:latest
```

**3. Deploy com Docker Compose (Produção):**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  app:
    image: ms-cadastro-funcionario:latest
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://external-mongo:27017
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    restart: unless-stopped
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

### Checklist de Produção

- [ ] Variáveis de ambiente configuradas para produção
- [ ] Banco MongoDB externo configurado
- [ ] Logs centralizados (ELK Stack ou similar)
- [ ] Health checks monitorados
- [ ] Backup automático do MongoDB
- [ ] Certificados SSL/TLS configurados
- [ ] Rate limiting implementado (futuro)
- [ ] Monitoramento de métricas (Prometheus + Grafana)
- [ ] Alertas configurados

## 🔧 Troubleshooting

### Problemas Comuns

**1. Erro de Conexão MongoDB**
```bash
# Verificar se MongoDB está rodando
docker-compose ps mongodb

# Verificar logs do MongoDB
docker-compose logs mongodb

# Testar conectividade
docker-compose exec app python -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test():
    client = AsyncIOMotorClient('mongodb://mongodb:27017')
    await client.admin.command('ping')
    print('MongoDB conectado com sucesso!')

asyncio.run(test())
"
```

**2. Aplicação Não Inicia**
```bash
# Verificar logs da aplicação
docker-compose logs app

# Verificar variáveis de ambiente
docker-compose exec app env | grep MONGODB

# Verificar portas em uso
netstat -tulpn | grep 8000
```

**3. Erro 500 na API**
```bash
# Logs estruturados com filtro
docker-compose logs app | grep "ERROR"

# Verificar health check
curl -v http://localhost:8000/api/v1/health

# Debug mode (desenvolvimento apenas)
export DEBUG=true
export LOG_LEVEL=DEBUG
docker-compose restart app
```

**4. Problemas de Performance**
```bash
# Verificar índices MongoDB
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.getIndexes()
"

# Verificar stats da collection
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.stats()
"

# Monitor de queries lentas
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.setProfilingLevel(1, { slowms: 100 })
"
```

### Logs e Monitoramento

```bash
# Logs em tempo real
docker-compose logs -f app

# Logs estruturados (se jq instalado)
docker-compose logs app --since 1h | grep ERROR

# Health check automático
watch -n 30 'curl -s http://localhost:8000/api/v1/health | jq .'

# Estatísticas do banco
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.runCommand({dbStats: 1})
"
```

### Performance e Otimização

```bash
# Verificar pool de conexões
docker-compose logs app | grep "connection"

# Monitor de memória
docker stats ms-cadastro-funcionario-app-1

# Profiling de requests (desenvolvimento)
pip install py-spy
py-spy record -o profile.svg -- python -m uvicorn app.main:app
```

## 🤝 Contribuição

### Processo de Contribuição

1. **Fork** o projeto
2. **Clone** seu fork: `git clone <your-fork-url>`
3. **Crie** uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
4. **Desenvolva** seguindo os padrões estabelecidos
5. **Teste** suas mudanças localmente
6. **Commit** suas mudanças: `git commit -am 'Adiciona nova funcionalidade'`
7. **Push** para a branch: `git push origin feature/nova-funcionalidade`
8. **Abra** um Pull Request

### Padrões de Desenvolvimento

**Código:**
- Seguir PEP 8 para formatação Python
- Usar type hints em todas as funções
- Documentar funções e classes com docstrings
- Manter cobertura de testes acima de 80% (futuro)

**Commits:**
- Usar Conventional Commits: `feat: adiciona endpoint de relatórios`
- Commits pequenos e atômicos
- Mensagens descritivas em português

**Pull Requests:**
- Título descritivo
- Descrição detalhada das mudanças
- Screenshots/exemplos quando aplicável
- Verificar se passa em todos os checks

### Estrutura de Branches

```
main              # Produção estável
├── develop       # Desenvolvimento integrado
├── feature/      # Novas funcionalidades
├── bugfix/       # Correções de bugs
└── hotfix/       # Correções urgentes para produção
```

## 📚 Recursos Adicionais

### Documentação

- [Documentação da API - Swagger](http://localhost:8000/docs)
- [Documentação da API - ReDoc](http://localhost:8000/redoc)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Motor Documentation](https://motor.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Ferramentas Recomendadas

- **IDE**: VSCode com extensões Python e Docker
- **API Testing**: Postman ou Insomnia
- **Database**: MongoDB Compass
- **Containers**: Docker Desktop
- **Version Control**: Git com GitKraken/SourceTree

### Links Úteis

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [MongoDB Query Guide](https://docs.mongodb.com/manual/tutorial/query-documents/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 📞 Contato e Suporte

**Equipe de Desenvolvimento TechNovaMBA Solutions**

- **Email**: dev-team@technova.com
- **Slack**: #microservicos-funcionarios
- **Issues**: Use o sistema de Issues do GitHub para reportar bugs ou solicitar features

---

**TechNovaMBA Solutions** - Transformando o futuro através da tecnologia 🚀
