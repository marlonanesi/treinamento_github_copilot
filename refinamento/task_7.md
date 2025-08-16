# Task 7 - Endpoints FastAPI e Controllers

## Objetivo
Implementar os endpoints da API REST usando FastAPI, incluindo controllers, roteamento, tratamento de erros e documentação automática completa.

## Principais Entregas
- Endpoints para todas as operações CRUD
- Controllers com separação de responsabilidades
- Roteamento organizado por recursos
- Tratamento de exceções HTTP
- Middleware de logging e CORS
- Documentação automática completa

## Critério de Pronto
- ✅ Todos os endpoints implementados e funcionais
- ✅ Documentação Swagger/OpenAPI completa
- ✅ Tratamento adequado de erros HTTP
- ✅ Middleware configurado corretamente
- ✅ Injeção de dependências funcionando

## Prompt de Execução

Como especialista em FastAPI e APIs REST, implemente os endpoints do microserviço `ms-cadastro-funcionario` seguindo estas especificações:

**Router Principal (app/presentation/api/v1/funcionarios.py):**
```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

# Endpoints a implementar:
@router.post("/", response_model=FuncionarioResponseSchema, status_code=status.HTTP_201_CREATED)
@router.get("/", response_model=FuncionarioListResponseSchema)
@router.get("/{funcionario_id}", response_model=FuncionarioResponseSchema)
@router.put("/{funcionario_id}", response_model=FuncionarioResponseSchema)
@router.delete("/{funcionario_id}", status_code=status.HTTP_204_NO_CONTENT)
```

**Controller de Funcionários (app/presentation/api/controllers/funcionario_controller.py):**
```python
class FuncionarioController:
    def __init__(self, funcionario_coordinator: FuncionarioCoordinator):
        self.funcionario_coordinator = funcionario_coordinator
    
    async def criar_funcionario(self, dados: FuncionarioCreateSchema) -> FuncionarioResponseSchema:
        # Implementar lógica de criação
    
    async def listar_funcionarios(
        self, 
        filtros: FuncionarioListQuerySchema
    ) -> FuncionarioListResponseSchema:
        # Implementar lógica de listagem
    
    async def buscar_funcionario(self, funcionario_id: str) -> FuncionarioResponseSchema:
        # Implementar lógica de busca
    
    async def atualizar_funcionario(
        self, 
        funcionario_id: str, 
        dados: FuncionarioUpdateSchema
    ) -> FuncionarioResponseSchema:
        # Implementar lógica de atualização
    
    async def excluir_funcionario(self, funcionario_id: str) -> None:
        # Implementar lógica de exclusão
```

**Dependências FastAPI (app/presentation/dependencies/dependencies.py):**
```python
async def get_funcionario_controller() -> FuncionarioController:
    # Factory para controller com injeção de dependências
    
async def get_funcionario_coordinator() -> FuncionarioCoordinator:
    # Factory para coordinator
    
async def validate_object_id(funcionario_id: str = Path(...)) -> str:
    # Validar se ID é um ObjectId válido
```

**Tratamento de Exceções (app/presentation/api/middleware/exception_handler.py):**
```python
async def domain_exception_handler(request: Request, exc: DomainException):
    # Tratar exceções de domínio
    
async def validation_exception_handler(request: Request, exc: ValidationError):
    # Tratar erros de validação Pydantic
    
async def mongodb_exception_handler(request: Request, exc: PyMongoError):
    # Tratar erros específicos do MongoDB
    
async def generic_exception_handler(request: Request, exc: Exception):
    # Fallback para exceções não tratadas
```

**Middleware de Logging (app/presentation/api/middleware/logging_middleware.py):**
```python
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log de requests/responses
        # Tempo de processamento
        # Dados de debugging
```

**Configuração da API (app/presentation/api/api_v1.py):**
```python
from fastapi import APIRouter
from .v1.funcionarios import router as funcionarios_router
from .v1.health import router as health_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(funcionarios_router)
api_router.include_router(health_router)
```

**Endpoints Específicos:**

**1. POST /api/v1/funcionarios - Criar Funcionário:**
- Request Body: `FuncionarioCreateSchema`
- Response: `FuncionarioResponseSchema` (201)
- Errors: 400 (dados inválidos), 409 (email duplicado)
- Documentação: "Cadastra um novo funcionário no sistema"

**2. GET /api/v1/funcionarios - Listar Funcionários:**
- Query Parameters: departamento, cargo, skip, limit
- Response: `FuncionarioListResponseSchema` (200)
- Errors: 400 (parâmetros inválidos)
- Documentação: "Lista funcionários com filtros opcionais e paginação"

**3. GET /api/v1/funcionarios/{id} - Buscar Funcionário:**
- Path Parameter: funcionario_id (ObjectId)
- Response: `FuncionarioResponseSchema` (200)
- Errors: 400 (ID inválido), 404 (não encontrado)
- Documentação: "Busca funcionário específico por ID"

**4. PUT /api/v1/funcionarios/{id} - Atualizar Funcionário:**
- Path Parameter: funcionario_id
- Request Body: `FuncionarioUpdateSchema`
- Response: `FuncionarioResponseSchema` (200)
- Errors: 400 (dados inválidos), 404 (não encontrado), 422 (campos imutáveis)

**5. DELETE /api/v1/funcionarios/{id} - Excluir Funcionário:**
- Path Parameter: funcionario_id
- Response: 204 (sem conteúdo)
- Errors: 404 (não encontrado), 409 (ativo em projetos)

**Health Check Endpoint (app/presentation/api/v1/health.py):**
```python
@router.get("/health", response_model=HealthCheckResponseSchema, tags=["Health"])
async def health_check():
    # Verificar status da aplicação
    # Verificar conectividade com MongoDB
    # Retornar informações de versão
```

**Configuração do FastAPI (atualizar app/main.py):**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: conectar banco, criar índices
    yield
    # Shutdown: fechar conexões

app = FastAPI(
    title="Microserviço de Cadastro de Funcionários",
    description="API para gerenciamento de funcionários da TechNovaMBA Solutions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Middleware
app.add_middleware(CORSMiddleware, ...)
app.add_middleware(LoggingMiddleware)

# Exception handlers
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)

# Routers
app.include_router(api_router)
```

**Documentação OpenAPI Customizada:**
- Tags organizadas por recursos
- Descrições detalhadas para cada endpoint
- Exemplos de request/response
- Códigos de status documentados
- Schemas de erro específicos

**Padrões de Resposta:**
```python
# Sucesso com dados
{
    "success": true,
    "data": { ... },
    "message": "Funcionário criado com sucesso"
}

# Erro de validação
{
    "success": false,
    "error": "VALIDATION_ERROR",
    "message": "Dados inválidos fornecidos",
    "details": {
        "field": "email",
        "message": "Email já existe no sistema"
    }
}
```

**Padrões a seguir:**
- Use status codes HTTP adequados
- Implemente logging estruturado
- Valide IDs de entrada (ObjectId)
- Use injeção de dependências do FastAPI
- Trate todas as exceções conhecidas
- Configure CORS apropriadamente
- Documente todos os endpoints
- Use response_model em todos os endpoints
- Implemente paginação consistente
- Configure timeouts adequados

**Estrutura de arquivos esperada:**
```
app/presentation/api/
├── __init__.py
├── api_v1.py                    # Configuração principal da API
├── v1/
│   ├── __init__.py
│   ├── funcionarios.py          # Endpoints de funcionários
│   └── health.py               # Health check
├── controllers/
│   ├── __init__.py
│   └── funcionario_controller.py # Controller principal
├── middleware/
│   ├── __init__.py
│   ├── exception_handler.py     # Tratamento de exceções
│   └── logging_middleware.py    # Middleware de logging
└── dependencies/
    ├── __init__.py
    └── dependencies.py          # Dependências FastAPI
```

**Configurações de Produção:**
- Rate limiting configurado
- Timeouts de request apropriados
- Logging estruturado com correlationId
- Middleware de segurança básico
- Headers de segurança configurados

Implemente todos os endpoints mantendo foco na padronização, documentação clara e tratamento robusto de erros.
