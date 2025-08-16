# Context Map – ms-cadastro-funcionario

**Data de geração:** 2025-08-10  
**Versão do documento:** 1.0

## Sumário

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Mapa por Camada e Arquivo](#2-mapa-por-camada-e-arquivo)
3. [HTTP API (Swagger snapshot)](#3-http-api-swagger-snapshot)
4. [Persistência (MongoDB/Motor)](#4-persistência-mongodbmotor)
5. [Observabilidade e Erros](#5-observabilidade-e-erros)
6. [Plano de Testes Unitários](#6-plano-de-testes-unitários-por-arquivo)
7. [Riscos e Pontos de Atenção](#7-riscos-e-pontos-de-atenção)
8. [Anexos](#8-anexos)

## 1. Visão Geral do Projeto

**Stack:** FastAPI (async), Pydantic, Motor/MongoDB, Python 3.11+

**Estrutura em camadas:**
- `domain/`: Entidades de negócio (Funcionario), Value Objects (Email, Cargo, Telefone), Exceções de domínio, Interfaces de repositório
- `application/`: Casos de uso (CRUD), DTOs, Validadores, Services, Coordenador de aplicação
- `infrastructure/`: Implementações de repositório (MongoDB), Configurações, Database models, Dependências
- `presentation/`: Controllers, Schemas Pydantic, Routers FastAPI, Dependencies
- `shared/`: Utilitários compartilhados, Logging

**Entrypoints:**
- `app/main.py`: Factory da aplicação FastAPI com middleware CORS e lifespan
- `main.py`: Wrapper para execução local com uvicorn

**Execução:**
```bash
# Docker Compose
docker-compose up

# Local
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Variáveis de ambiente:**

| NOME | DESCRIÇÃO | EXEMPLO/DEFAULT | USO |
|------|-----------|-----------------|-----|
| `MONGODB_URL` | URL de conexão MongoDB | `mongodb://localhost:27017` | `app/infrastructure/config/settings.py` |
| `DATABASE_NAME` | Nome do banco de dados | `funcionarios_db` | `app/infrastructure/config/settings.py` |
| `API_HOST` | Host da API | `0.0.0.0` | `app/infrastructure/config/settings.py` |
| `API_PORT` | Porta da API | `8000` | `app/infrastructure/config/settings.py` |
| `API_VERSION` | Versão da API | `v1` | `app/infrastructure/config/settings.py` |
| `ENVIRONMENT` | Ambiente de execução | `development` | `app/infrastructure/config/settings.py` |
| `LOG_LEVEL` | Nível de log | `INFO` | `app/infrastructure/config/settings.py` |
| `DEBUG` | Modo debug | `false` | `app/infrastructure/config/settings.py` |
| `MONGO_INITDB_ROOT_USERNAME` | Usuário root MongoDB | `admin` | Docker Compose |
| `MONGO_INITDB_ROOT_PASSWORD` | Senha root MongoDB | `password123` | Docker Compose |

## 2. Mapa por Camada e Arquivo

### 2.1 app/main.py
**Papel:** Entrypoint/Factory da aplicação FastAPI  
**Dependências-chaves:** FastAPI, CORSMiddleware, uvicorn, app.infrastructure.config.settings  
**Assinaturas públicas:**

```python
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]
# Raises: Nenhuma específica
# Side effects: Logging de inicialização/finalização

def create_app() -> FastAPI
# Raises: Nenhuma específica
# Side effects: Configuração de logging, criação de middlewares

@app.get("/health", tags=["Health"])
async def health_check() -> dict
# Raises: Nenhuma específica
# Side effects: Nenhum (read-only)
```

**Usado por:** main.py (root), docker containers  
**Observações de domínio/regra:** 
- Configura CORS para desenvolvimento com `allow_origins=["*"]`
- Health check básico sem verificação real de conexão com MongoDB

### 2.2 app/domain/entities/funcionario.py
**Papel:** Entidade principal do domínio  
**Dependências-chaves:** dataclasses, datetime, decimal, value_objects, funcionario_exceptions  
**Assinaturas públicas:**

```python
@dataclass
class Funcionario:
    # Atributos: nome_completo: str, email: Email, cargo: Cargo, data_admissao: date
    # telefone: Optional[Telefone], departamento: Optional[str], salario: Optional[Decimal]
    # ativo: bool, id: Optional[str], created_at: datetime, updated_at: datetime

def __post_init__(self) -> None
# Raises: DadosInvalidosException
# Side effects: Validação e normalização de dados

@classmethod
def criar(cls, nome_completo: str, email: str, cargo: str, data_admissao: date, 
         telefone: Optional[str] = None, departamento: Optional[str] = None,
         salario: Optional[Decimal] = None, ativo: bool = False) -> 'Funcionario'
# Raises: DadosInvalidosException
# Side effects: Criação de value objects

def atualizar(self, nome_completo: Optional[str] = None, cargo: Optional[str] = None,
             telefone: Optional[str] = None, departamento: Optional[str] = None,
             salario: Optional[Decimal] = None, ativo: Optional[bool] = None) -> None
# Raises: DadosInvalidosException
# Side effects: Atualização de timestamp

def validar_exclusao(self) -> None
# Raises: FuncionarioAtivoEmProjetosException
# Side effects: Nenhum (read-only)

def to_dict(self) -> Dict[str, Any]
# Raises: Nenhuma específica
# Side effects: Nenhum (read-only)

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'Funcionario'
# Raises: DadosInvalidosException (inferido)
# Side effects: Parsing de dados
```

**Usado por:** Use cases, Repository implementations, Controllers  
**Observações de domínio/regra:**
- Email e data de admissão são imutáveis após criação
- Funcionários ativos não podem ser excluídos
- Nome deve ter pelo menos 2 palavras de 2+ caracteres
- Data de admissão não pode ser futura nem anterior a 50 anos

### 2.3 app/domain/entities/value_objects.py
**Papel:** Value Objects com validações específicas  
**Dependências-chaves:** re, enum, funcionario_exceptions  
**Assinaturas públicas:**

```python
class Email:
    def __init__(self, value: str)
    # Raises: DadosInvalidosException
    # Side effects: Normalização para lowercase

    @classmethod
    def is_valid(cls, email: str) -> bool
    # Raises: Nenhuma específica
    # Side effects: Nenhum (read-only)

class TiposCargo(Enum):
    # Valores: DESENVOLVEDOR_JUNIOR, DESENVOLVEDOR_PLENO, DESENVOLVEDOR_SENIOR, etc.
    
    @classmethod
    def get_all_values(cls) -> List[str]
    # Raises: Nenhuma específica
    # Side effects: Nenhum (read-only)

class Cargo:
    def __init__(self, value: str, permitir_cargo_personalizado: bool = True)
    # Raises: DadosInvalidosException, CargoInvalidoException
    # Side effects: Normalização para Title Case

class Telefone:
    def __init__(self, value: str)
    # Raises: DadosInvalidosException
    # Side effects: Normalização para formato (XX) XXXXX-XXXX
```

**Usado por:** Entidade Funcionario, Schemas, Use cases  
**Observações de domínio/regra:**
- Email usa regex RFC 5322 simplificado
- Telefone aceita formatos brasileiros (11) 99999-9999 ou (11) 9999-9999
- Cargo permite tipos personalizados além dos pré-definidos

### 2.4 app/domain/exceptions/funcionario_exceptions.py
**Papel:** Exceções de domínio específicas  
**Dependências-chaves:** Nenhuma externa  
**Assinaturas públicas:**

```python
class FuncionarioException(Exception):
    def __init__(self, message: str, error_code: str = None)
    # Raises: Nenhuma específica
    # Side effects: Nenhum

class FuncionarioNaoEncontradoException(FuncionarioException):
    def __init__(self, funcionario_id: str = None, email: str = None)
    # Raises: Nenhuma específica
    # Side effects: Nenhum

class EmailDuplicadoException(FuncionarioException):
    def __init__(self, email: str)
    # Raises: Nenhuma específica
    # Side effects: Nenhum

class DadosInvalidosException(FuncionarioException):
    def __init__(self, campo: str, valor: str = None, regra: str = None)
    # Raises: Nenhuma específica
    # Side effects: Nenhum
```

**Usado por:** Entidades de domínio, Use cases, Repository implementations  
**Observações de domínio/regra:**
- Hierarquia base com FuncionarioException
- Error codes padronizados para tratamento na apresentação

### 2.5 app/application/use_cases/criar_funcionario.py
**Papel:** Caso de uso para criação de funcionário  
**Dependências-chaves:** datetime.date, dto.requests/responses, domain.entities, domain.repositories  
**Assinaturas públicas:**

```python
class CriarFuncionarioUseCase(UseCase[CriarFuncionarioRequest, FuncionarioResponse]):
    def __init__(self, funcionario_repository: AbstractFuncionarioRepository)
    # Raises: Nenhuma específica
    # Side effects: Nenhum

    async def execute(self, request: CriarFuncionarioRequest) -> FuncionarioResponse
    # Raises: ValidationException, DuplicateResourceException
    # Side effects: Persistência no banco, logging
```

**Usado por:** Controllers  
**Observações de domínio/regra:**
- Verifica unicidade de email antes da criação
- Valida dados de entrada antes de criar entidade
- Converte exceptions de domínio para application

### 2.6 app/infrastructure/config/settings.py
**Papel:** Configurações centralizadas com Pydantic Settings  
**Dependências-chaves:** pydantic_settings, functools.lru_cache  
**Assinaturas públicas:**

```python
class Settings(BaseSettings):
    # Atributos: API_HOST, API_PORT, MONGODB_URL, DATABASE_NAME, ENVIRONMENT, etc.
    
    def is_development(self) -> bool
    # Raises: Nenhuma específica
    # Side effects: Nenhum (read-only)

    def get_mongodb_connection_string(self) -> str
    # Raises: Nenhuma específica
    # Side effects: Nenhum (read-only)

    def setup_logging(self) -> None
    # Raises: Nenhuma específica
    # Side effects: Configuração global de logging

@lru_cache()
def get_settings() -> Settings
# Raises: ValidationError (Pydantic)
# Side effects: Carregamento de .env, singleton pattern
```

**Usado por:** main.py, database connections, toda a aplicação  
**Observações de domínio/regra:**
- Singleton pattern via lru_cache
- Validação automática de tipos e valores via Pydantic
- Suporte a autenticação MongoDB opcional

### 2.7 app/presentation/api/v1/funcionarios.py
**Papel:** Endpoints REST para CRUD de funcionários  
**Dependências-chaves:** FastAPI, presentation.schemas, application.exceptions, dependencies  
**Assinaturas públicas:**

```python
@router.post("/", response_model=SuccessResponseSchema[FuncionarioResponseSchema])
async def criar_funcionario(funcionario_data: FuncionarioCreateSchema, 
                           controller: FuncionarioControllerDep) -> SuccessResponseSchema[FuncionarioResponseSchema]
# Raises: HTTPException (409, 422, 400)
# Side effects: HTTP response, logging via controller

@router.get("/", response_model=SuccessResponseSchema[FuncionarioListResponseSchema])
async def listar_funcionarios(controller: FuncionarioControllerDep, page: int = Query(1), 
                              size: int = Query(10), departamento: Optional[str] = None,
                              cargo: Optional[str] = None) -> SuccessResponseSchema[FuncionarioListResponseSchema]
# Raises: HTTPException (400)
# Side effects: HTTP response, database query

@router.get("/{funcionario_id}", response_model=SuccessResponseSchema[FuncionarioResponseSchema])
async def buscar_funcionario(funcionario_id: ValidObjectId, 
                            controller: FuncionarioControllerDep) -> SuccessResponseSchema[FuncionarioResponseSchema]
# Raises: HTTPException (404, 400)
# Side effects: HTTP response, database query

@router.put("/{funcionario_id}", response_model=SuccessResponseSchema[FuncionarioResponseSchema])
async def atualizar_funcionario(funcionario_id: ValidObjectId, funcionario_data: FuncionarioUpdateSchema,
                                controller: FuncionarioControllerDep) -> SuccessResponseSchema[FuncionarioResponseSchema]
# Raises: HTTPException (404, 422, 400)
# Side effects: HTTP response, database update

@router.delete("/{funcionario_id}", status_code=204)
async def excluir_funcionario(funcionario_id: ValidObjectId, 
                             controller: FuncionarioControllerDep) -> None
# Raises: HTTPException (404, 409)
# Side effects: HTTP 204, database deletion
```

**Usado por:** FastAPI router, HTTP clients  
**Observações de domínio/regra:**
- Paginação limitada a 100 itens por página
- Validação de ObjectId via dependency
- Mapeamento de exceptions para status codes HTTP apropriados

### 2.8 app/infrastructure/repositories/funcionario_repository_impl.py
**Papel:** Implementação concreta do repositório MongoDB  
**Dependências-chaves:** motor.motor_asyncio, bson.ObjectId, pymongo.errors, domain.entities, infrastructure.database.models  
**Assinaturas públicas:**

```python
class FuncionarioRepositoryImpl(AbstractFuncionarioRepository):
    def __init__(self, database)
    # Raises: Nenhuma específica
    # Side effects: Referência para coleção MongoDB

    async def salvar(self, funcionario: Funcionario) -> Funcionario
    # Raises: EmailDuplicadoException, DadosInvalidosException, ErroOperacaoException
    # Side effects: Inserção no MongoDB, atribuição de ID

    async def buscar_por_id(self, funcionario_id: str) -> Optional[Funcionario]
    # Raises: ErroOperacaoException
    # Side effects: Query no MongoDB

    async def buscar_por_email(self, email: str) -> Optional[Funcionario]
    # Raises: ErroOperacaoException
    # Side effects: Query no MongoDB usando índice único

    async def listar_por_filtros(self, departamento: Optional[str] = None, cargo: Optional[str] = None,
                                 ativo: Optional[bool] = None, skip: int = 0, limit: int = 100) -> List[Funcionario]
    # Raises: ErroOperacaoException
    # Side effects: Query complexa no MongoDB com filtros

    async def atualizar(self, funcionario: Funcionario) -> Funcionario
    # Raises: FuncionarioNaoEncontradoException, DadosInvalidosException, ErroOperacaoException
    # Side effects: Update no MongoDB, timestamp atualizado

    async def excluir(self, funcionario_id: str) -> bool
    # Raises: DadosInvalidosException, ErroOperacaoException
    # Side effects: Deleção no MongoDB

    async def verificar_email_existe(self, email: str, excluir_id: Optional[str] = None) -> bool
    # Raises: ErroOperacaoException
    # Side effects: Query no MongoDB
```

**Usado por:** Use cases via dependency injection  
**Observações de domínio/regra:**
- Conversão automática entre entidades de domínio e documentos MongoDB
- Tratamento de DuplicateKeyError para emails únicos
- Logging detalhado de operações com emojis para facilitar debugging

### 2.9 app/infrastructure/database/models.py
**Papel:** Mapeamento entre entidades de domínio e documentos MongoDB  
**Dependências-chaves:** bson.ObjectId, datetime, decimal, domain.entities  
**Assinaturas públicas:**

```python
class FuncionarioModel:
    @staticmethod
    def from_entity(funcionario: Funcionario) -> Dict[str, Any]
    # Raises: Nenhuma específica
    # Side effects: Nenhum (pure function)

    @staticmethod
    def to_entity(document: Dict[str, Any]) -> Funcionario
    # Raises: ValueError (documento inválido)
    # Side effects: Parsing de dados, criação de value objects

    @staticmethod
    def to_update_document(funcionario: Funcionario, campos_permitidos: Optional[list] = None) -> Dict[str, Any]
    # Raises: Nenhuma específica
    # Side effects: Nenhum (pure function)

    @staticmethod
    def validate_document(document: Dict[str, Any]) -> bool
    # Raises: Nenhuma específica
    # Side effects: Nenhum (read-only validation)
```

**Usado por:** Repository implementations  
**Observações de domínio/regra:**
- Suporte a backwards compatibility (campo "nome" vs "nome_completo")
- Conversão automática de tipos (Decimal ↔ float, date ↔ datetime)
- Exclusão de campos None em updates usando $unset

### 2.10 app/presentation/schemas/funcionario_schemas.py
**Papel:** Schemas Pydantic para validação de entrada/saída  
**Dependências-chaves:** pydantic, decimal, datetime, presentation.schemas.validators  
**Assinaturas públicas:**

```python
class FuncionarioCreateSchema(BaseSchema):
    # Campos: nome_completo, email, cargo, data_admissao, telefone, cpf, departamento, etc.
    
    @field_validator('nome_completo')
    @classmethod
    def validar_nome_completo(cls, v: str) -> str
    # Raises: ValueError (via Pydantic)
    # Side effects: Normalização

class FuncionarioUpdateSchema(BaseSchema):
    # Campos opcionais: nome_completo, cargo, telefone, departamento, salario, etc.
    
    @model_validator(mode='before')
    @classmethod
    def validar_campos_imutaveis(cls, values)
    # Raises: ValueError
    # Side effects: Validação de regras de negócio

class FuncionarioResponseSchema(BaseSchema, TimestampMixin):
    # Campos de resposta: id, nome_completo, email, cargo, etc. + timestamps
```

**Usado por:** Endpoints FastAPI, Controllers  
**Observações de domínio/regra:**
- Validação rigorosa de tipos e formatos
- Campos imutáveis protegidos em updates
- Normalização automática de dados de entrada

## 3. HTTP API (Swagger snapshot)

**Base URL:** `http://localhost:8000`

### Health Check
```
GET /health → app.main:health_check
Response: {"status": "healthy", "service": "ms-cadastro-funcionario", "version": "1.0.0"}
Status: 200
```

### Funcionários CRUD
```
POST /funcionarios → presentation.api.v1.funcionarios:criar_funcionario
Request model: FuncionarioCreateSchema
Response model: SuccessResponseSchema[FuncionarioResponseSchema]
Status: 201/400/409/422
Dependencies: FuncionarioControllerDep
Headers: Content-Type: application/json
Errors: {"success": false, "error": "DUPLICATE_EMAIL", "message": "...", "field": "email"}

GET /funcionarios → presentation.api.v1.funcionarios:listar_funcionarios  
Query params: page (1+), size (1-100), departamento (optional), cargo (optional)
Response model: SuccessResponseSchema[FuncionarioListResponseSchema]
Status: 200/400
Dependencies: FuncionarioControllerDep

GET /funcionarios/{id} → presentation.api.v1.funcionarios:buscar_funcionario
Path params: funcionario_id (ValidObjectId)
Response model: SuccessResponseSchema[FuncionarioResponseSchema]
Status: 200/400/404
Dependencies: FuncionarioControllerDep

PUT /funcionarios/{id} → presentation.api.v1.funcionarios:atualizar_funcionario
Path params: funcionario_id (ValidObjectId)
Request model: FuncionarioUpdateSchema
Response model: SuccessResponseSchema[FuncionarioResponseSchema]
Status: 200/400/404/422
Dependencies: FuncionarioControllerDep

DELETE /funcionarios/{id} → presentation.api.v1.funcionarios:excluir_funcionario
Path params: funcionario_id (ValidObjectId)
Response: 204 No Content
Status: 204/400/404/409
Dependencies: FuncionarioControllerDep
```

### Utilitários
```
POST /funcionarios/validar/email → presentation.api.v1.funcionarios:validar_email_unico
Query params: email
Response: {"success": true, "email": "...", "disponivel": true}
Status: 200

POST /funcionarios/validar/cpf → presentation.api.v1.funcionarios:validar_cpf
Query params: cpf  
Response: {"success": true, "cpf": "...", "valido": true}
Status: 200
```

## 4. Persistência (MongoDB/Motor)

### Conexão
- **Criação:** `app.infrastructure.database.connection` (NÃO ENCONTRADO - usar connection string de settings)
- **Fechamento:** Lifecycle da aplicação via lifespan
- **Estratégia:** Singleton pattern via dependency injection

### Banco/Coleções
- **Banco:** `funcionarios_db` (configurável via `DATABASE_NAME`)
- **Coleções:** `funcionarios`

### Índices
```javascript
// Índice único para email (previne duplicatas)
db.funcionarios.createIndex({"email": 1}, {"unique": true})

// Índices para consultas frequentes (sugeridos)
db.funcionarios.createIndex({"departamento": 1})
db.funcionarios.createIndex({"cargo": 1})
db.funcionarios.createIndex({"ativo": 1})
db.funcionarios.createIndex({"created_at": -1})
```

### Mapeamento
**Modelo → Documento:**
- `nome_completo` → string (com suporte a "nome" legacy)
- `email` → string (único)
- `cargo` → string
- `data_admissao` → Date/ISOString
- `telefone` → string opcional
- `departamento` → string opcional
- `salario` → number opcional (Decimal → float)
- `ativo` → boolean
- `created_at/updated_at` → Date/ISOString

## 5. Observabilidade e Erros

### Logs
- **Formatação:** `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Configuração:** `app.infrastructure.config.settings:Settings.setup_logging()`
- **Níveis:** Por ambiente (development=INFO, production=WARNING)
- **Request-ID:** NÃO ENCONTRADO (ponto de melhoria)

### Tratamento de Exceções
**Exception Handlers Globais:** NÃO ENCONTRADO

**Mapeamento Domínio → HTTP:**
- `DadosInvalidosException` → 422 Unprocessable Entity
- `EmailDuplicadoException` → 409 Conflict  
- `FuncionarioNaoEncontradoException` → 404 Not Found
- `FuncionarioAtivoEmProjetosException` → 409 Conflict
- `ValidationException` → 400 Bad Request

## 6. Plano de Testes Unitários (por arquivo)

### 6.1 app/domain/entities/funcionario.py

**O que testar:**
- Método `criar()` valida todos os campos obrigatórios
- Método `atualizar()` preserva campos imutáveis (email, data_admissao)
- Método `validar_exclusao()` rejeita funcionários ativos
- Método `_validar_nome_completo()` aplica regras de 2+ palavras
- Método `_validar_data_admissao()` rejeita datas futuras
- Métodos `to_dict()` e `from_dict()` fazem roundtrip correto

**Cenários felizes/tristes:**
1. **Feliz:** Criar funcionário com todos os dados válidos
2. **Triste:** Criar funcionário com nome de uma palavra apenas
3. **Triste:** Criar funcionário com data de admissão futura
4. **Feliz:** Atualizar cargo e salário mantendo email
5. **Triste:** Tentar atualizar email (deve ser ignorado/rejeitado)
6. **Triste:** Validar exclusão de funcionário ativo

**Mocks necessários:**
- Não necessário (entidade pura)

**Fixtures sugeridas:**
```python
@pytest.fixture
def funcionario_valido():
    return Funcionario.criar(
        nome_completo="João Silva Santos",
        email="joao@empresa.com", 
        cargo="Desenvolvedor",
        data_admissao=date(2023, 1, 15)
    )

@pytest.fixture  
def dados_funcionario_dict():
    return {
        "nome_completo": "Maria Santos",
        "email": "maria@empresa.com",
        "cargo": "Analista",
        "data_admissao": "2023-02-01",
        "ativo": False,
        "created_at": "2024-01-01T10:00:00",
        "updated_at": "2024-01-01T10:00:00"
    }
```

**Cobertura alvo:** 95%

### 6.2 app/domain/entities/value_objects.py

**O que testar:**
- `Email.__init__()` valida formato e normaliza para lowercase
- `Email.is_valid()` identifica emails válidos/inválidos
- `Cargo.__init__()` aceita tipos pré-definidos e personalizados
- `Telefone.__init__()` normaliza formato brasileiro
- `TiposCargo.get_all_values()` retorna lista completa

**Cenários felizes/tristes:**
1. **Feliz:** Email válido é normalizado para lowercase
2. **Triste:** Email inválido lança DadosInvalidosException
3. **Feliz:** Cargo pré-definido é aceito
4. **Triste:** Cargo inválido com `permitir_cargo_personalizado=False`
5. **Feliz:** Telefone formatado corretamente
6. **Triste:** Telefone com formato internacional

**Mocks necessários:**
- Não necessário (value objects puros)

**Fixtures sugeridas:**
```python
@pytest.fixture(params=[
    "joao@empresa.com",
    "MARIA@EMPRESA.COM.BR", 
    "teste.email+tag@dominio.co"
])
def emails_validos(request):
    return request.param

@pytest.fixture(params=[
    "email-sem-arroba",
    "@dominio.com",
    "email@"
])
def emails_invalidos(request):
    return request.param
```

**Cobertura alvo:** 95%

### 6.3 app/application/use_cases/criar_funcionario.py

**O que testar:**
- Método `execute()` cria funcionário com dados válidos
- Método `_validate_request()` detecta dados inválidos
- Método `_validate_unique_email()` detecta email duplicado
- Método `_create_funcionario_entity()` converte DTO para entidade

**Cenários felizes/tristes:**
1. **Feliz:** Criar funcionário com todos os dados corretos
2. **Triste:** Tentar criar com email já existente
3. **Triste:** Dados inválidos na requisição (nome muito curto)
4. **Triste:** Salário negativo
5. **Feliz:** Criar funcionário sem campos opcionais

**Mocks necessários:**
```python
@pytest.fixture
def mock_funcionario_repository():
    return AsyncMock(spec=AbstractFuncionarioRepository)

@pytest.fixture  
def mock_email_validator():
    return Mock()
```

**Fixtures sugeridas:**
```python
@pytest.fixture
def request_funcionario_valido():
    return CriarFuncionarioRequest(
        nome_completo="João Silva",
        email="joao@empresa.com",
        cargo="Desenvolvedor", 
        data_admissao=date.today()
    )

@pytest.fixture
def use_case(mock_funcionario_repository):
    return CriarFuncionarioUseCase(mock_funcionario_repository)
```

**Cobertura alvo:** 90%

### 6.4 app/infrastructure/repositories/funcionario_repository_impl.py

**O que testar:**
- Método `salvar()` insere documento e retorna ID
- Método `buscar_por_id()` encontra/não encontra por ObjectId
- Método `buscar_por_email()` usa índice único corretamente
- Método `listar_por_filtros()` aplica filtros e paginação
- Método `atualizar()` modifica apenas campos permitidos
- Método `excluir()` remove documento
- Tratamento de DuplicateKeyError em `salvar()`

**Cenários felizes/tristes:**
1. **Feliz:** Salvar funcionário novo retorna entidade com ID
2. **Triste:** Salvar funcionário com email duplicado lança EmailDuplicadoException
3. **Feliz:** Buscar por ID válido retorna funcionário
4. **Triste:** Buscar por ID inválido retorna None
5. **Feliz:** Filtros aplicam corretamente na consulta
6. **Triste:** Atualizar funcionário inexistente lança FuncionarioNaoEncontradoException

**Mocks necessários:**
```python
@pytest.fixture
def mock_collection():
    return AsyncMock()

@pytest.fixture
def mock_database(mock_collection):
    db = Mock()
    db.__getitem__.return_value = mock_collection
    return db
```

**Fixtures sugeridas:**
```python
@pytest.fixture
def funcionario_document():
    return {
        "_id": ObjectId(),
        "nome_completo": "João Silva",
        "email": "joao@empresa.com",
        "cargo": "Desenvolvedor",
        "data_admissao": datetime(2023, 1, 15),
        "ativo": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

@pytest.fixture
async def repository(mock_database):
    return FuncionarioRepositoryImpl(mock_database)
```

**Cobertura alvo:** 85%

### 6.5 app/presentation/api/v1/funcionarios.py

**O que testar:**
- Endpoint `POST /funcionarios` retorna 201 com dados válidos
- Endpoint `GET /funcionarios/{id}` retorna 404 para ID inválido
- Endpoint `PUT /funcionarios/{id}` retorna 422 para dados inválidos
- Endpoint `DELETE /funcionarios/{id}` retorna 409 para funcionário ativo
- Paginação funciona corretamente em `GET /funcionarios`
- Filtros são aplicados corretamente
- Tratamento correto de exceptions para status codes

**Cenários felizes/tristes:**
1. **Feliz:** POST cria funcionário e retorna 201
2. **Triste:** POST com email duplicado retorna 409
3. **Feliz:** GET com filtros retorna lista paginada
4. **Triste:** GET com ID inválido retorna 400
5. **Feliz:** PUT atualiza dados e retorna funcionário modificado
6. **Triste:** DELETE funcionário ativo retorna 409

**Mocks necessários:**
```python
@pytest.fixture
def mock_controller():
    return AsyncMock()

@pytest.fixture
def client(mock_controller):
    # Configurar dependency override
    app.dependency_overrides[FuncionarioControllerDep] = lambda: mock_controller
    return TestClient(app)
```

**Fixtures sugeridas:**
```python
@pytest.fixture
def funcionario_create_payload():
    return {
        "nome_completo": "João Silva",
        "email": "joao@empresa.com",
        "cargo": "Desenvolvedor",
        "data_admissao": "2023-01-15"
    }

@pytest.fixture
def funcionario_response():
    return FuncionarioResponseSchema(
        id="507f1f77bcf86cd799439011",
        nome_completo="João Silva",
        email="joao@empresa.com",
        cargo="Desenvolvedor",
        data_admissao=date(2023, 1, 15),
        ativo=False,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
```

**Cobertura alvo:** 85%

### 6.6 app/infrastructure/database/models.py

**O que testar:**
- Método `from_entity()` converte entidade para documento
- Método `to_entity()` converte documento para entidade com todos os campos
- Método `to_update_document()` gera operadores MongoDB corretos
- Método `validate_document()` identifica documentos válidos/inválidos
- Compatibilidade com formato legacy (campo "nome" vs "nome_completo")
- Conversão correta de tipos (Decimal ↔ float, date ↔ datetime)

**Cenários felizes/tristes:**
1. **Feliz:** Roundtrip entidade → documento → entidade preserva dados
2. **Feliz:** Documento legacy com campo "nome" é convertido corretamente
3. **Triste:** Documento inválido falha na validação
4. **Feliz:** Update document contém apenas campos modificados
5. **Feliz:** Campos opcionais None são tratados com $unset
6. **Triste:** Conversão de tipo inválido lança exceção

**Mocks necessários:**
- Não necessário (funções puras)

**Fixtures sugeridas:**
```python
@pytest.fixture
def funcionario_entity():
    return Funcionario.criar(
        nome_completo="João Silva",
        email="joao@empresa.com", 
        cargo="Desenvolvedor",
        data_admissao=date(2023, 1, 15),
        salario=Decimal("5000.00")
    )

@pytest.fixture
def funcionario_document():
    return {
        "_id": ObjectId(),
        "nome_completo": "João Silva",
        "email": "joao@empresa.com",
        "cargo": "Desenvolvedor", 
        "data_admissao": datetime(2023, 1, 15),
        "salario": 5000.00,
        "ativo": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

@pytest.fixture
def documento_legacy():
    return {
        "_id": ObjectId(),
        "nome": "João Silva",  # Campo legacy
        "email": "joao@empresa.com",
        "cargo": "Desenvolvedor",
        "data_admissao": "2023-01-15",  # String format
        "ativo": False,
        "created_at": "2024-01-01T10:00:00",
        "updated_at": "2024-01-01T10:00:00"
    }
```

**Cobertura alvo:** 90%

### 6.7 app/presentation/schemas/funcionario_schemas.py

**O que testar:**
- `FuncionarioCreateSchema` valida todos os campos obrigatórios
- `FuncionarioUpdateSchema` rejeita campos imutáveis
- Validadores customizados aplicam regras corretas
- Normalização de dados funciona (email lowercase, título case)
- Validação de tipos Pydantic funciona
- Model validators executam regras de negócio

**Cenários felizes/tristes:**
1. **Feliz:** Schema válido passa em todas as validações
2. **Triste:** Campo obrigatório ausente lança ValidationError
3. **Triste:** Update schema com campo imutável lança ValueError
4. **Feliz:** Dados são normalizados automaticamente
5. **Triste:** Formato de email inválido lança ValidationError
6. **Triste:** Update sem nenhum campo lança ValueError

**Mocks necessários:**
```python
@pytest.fixture
def mock_custom_validators():
    return Mock()
```

**Fixtures sugeridas:**
```python
@pytest.fixture
def dados_create_validos():
    return {
        "nome_completo": "joão SILVA santos",
        "email": "JOAO@EMPRESA.COM", 
        "cargo": "desenvolvedor pleno",
        "data_admissao": "2023-01-15"
    }

@pytest.fixture
def dados_update_validos():
    return {
        "cargo": "desenvolvedor senior",
        "salario": 6000.00
    }

@pytest.fixture  
def dados_update_invalidos():
    return {
        "email": "novo@email.com",  # Campo imutável
        "cargo": "analista"
    }
```

**Cobertura alvo:** 95%

## 7. Riscos e Pontos de Atenção

### Dependências Assíncronas
- **Risco:** Motor/MongoDB requer event loop configurado corretamente
- **Mitigação:** Usar pytest-asyncio e fixtures apropriadas
- **Teste:** Verificar que conexões são abertas/fechadas corretamente

### Consistência de Validações
- **Risco:** Divergência entre validações Pydantic e domínio
- **Mitigação:** Centralizar validações em CustomValidators
- **Teste:** Validar que ambas as camadas rejeitam os mesmos dados inválidos

### Conversão ObjectId
- **Risco:** Strings inválidas causam exceções não tratadas
- **Mitigação:** ValidObjectId dependency e validação no repositório
- **Teste:** Testar todos os cenários de ID inválido

### Índices MongoDB
- **Risco:** Índices ausentes em produção degradam performance
- **Mitigação:** Scripts de migração/setup automático
- **Teste:** Verificar que queries usam índices apropriados

### Campos Legacy
- **Risco:** Dados antigos podem ter formato incompatível
- **Mitigação:** FuncionarioModel suporta ambos os formatos
- **Teste:** Testar roundtrip com dados legacy

### Error Handling
- **Risco:** Exceptions não tratadas vazam detalhes internos
- **Mitigação:** Exception handlers globais (não implementado ainda)
- **Teste:** Verificar que todas as exceptions retornam responses apropriados

## 8. Anexos

### Comandos Úteis
```bash
# Executar aplicação
docker-compose up
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Testes
pytest tests/ -v --cov=app --cov-report=html

# Lint
flake8 app/
black app/
isort app/

# Análise SonarQube  
./scripts/run-sonar.ps1  # Windows
./scripts/run-sonar.sh   # Linux/macOS
```

### Docker Compose
- **Serviços:** app (FastAPI), mongodb (MongoDB 7.0)
- **Volumes:** mongodb_data (persistente), logs, código fonte (dev)
- **Healthcheck:** MongoDB com mongosh ping, FastAPI com HTTP GET /health
- **Networks:** Default bridge network

### Dockerfile
- **Multi-stage:** builder (dev com deps completas), runtime (prod slim)
- **Base:** python:3.11-slim
- **User:** appuser (não-root)
- **Healthcheck:** HTTP GET /health via python http.client

### Glossário de Domínio
- **Funcionário:** Entidade principal representando pessoa física da empresa
- **Email:** Value Object único no sistema, normalizado lowercase
- **Cargo:** Value Object com tipos pré-definidos + personalizados
- **Telefone:** Value Object formato brasileiro (XX) XXXXX-XXXX
- **Ativo:** Boolean indicando participação em projetos (afeta exclusão)
- **Data Admissão:** Campo imutável, não pode ser futura
- **Departamento:** String opcional, normalizada Title Case

---

**Nota:** Este mapa foi gerado automaticamente em 2025-08-10 baseado na análise estática do código. Algumas implementações podem estar incompletas (marcadas como NÃO ENCONTRADO) e requerem verificação manual.
