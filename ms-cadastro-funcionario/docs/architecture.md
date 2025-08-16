# Arquitetura do Microserviço de Funcionários

## Visão Geral

Este documento detalha a arquitetura do microserviço de cadastro de funcionários, baseada em princípios de Domain Driven Design (DDD) simplificado.

## Camadas da Aplicação

### 1. Domain Layer (Domínio)
**Responsabilidade**: Regras de negócio puras e entidades do domínio.

**Componentes:**
- `Funcionario`: Entidade principal com validações
- `Email`, `Cargo`, `Telefone`: Value Objects
- `AbstractFuncionarioRepository`: Interface do repositório
- Exceções de domínio específicas

**Características:**
- Sem dependências externas
- Regras de negócio centralizadas
- Validações de domínio
- Imutabilidade onde aplicável

### 2. Application Layer (Aplicação)
**Responsabilidade**: Orquestração de casos de uso e coordenação.

**Componentes:**
- Casos de uso CRUD (Create, Read, Update, Delete)
- DTOs para transferência de dados
- Validadores de entrada
- Coordenadores de operações

**Padrões implementados:**
- Use Case Pattern
- DTO Pattern
- Coordinator Pattern

### 3. Infrastructure Layer (Infraestrutura)
**Responsabilidade**: Persistência, configurações e detalhes técnicos.

**Componentes:**
- Implementação do repositório MongoDB
- Configuração de conexão assíncrona
- Gerenciamento de índices
- Configurações de ambiente

**Tecnologias:**
- Motor (MongoDB async driver)
- Pydantic Settings
- Configuration management

### 4. Presentation Layer (Apresentação)
**Responsabilidade**: Interface HTTP e validações de entrada.

**Componentes:**
- Endpoints FastAPI
- Schemas Pydantic
- Controllers
- Middleware personalizado

**Features:**
- Documentação automática
- Validação de entrada
- Serialização de resposta
- Tratamento de erros

## Fluxo de Dados

```
HTTP Request → FastAPI → Controller → Use Case → Repository → MongoDB
     ↓             ↓          ↓           ↓          ↓
 Validation → Schemas → Business → Domain → Infrastructure
     ↓             ↓          ↓           ↓          ↓
Response ← JSON ← DTO ← Entity ← Model ← Document
```

### Fluxo Detalhado

1. **Entrada (Request)**:
   - HTTP request recebido pelo FastAPI
   - Validação inicial via Pydantic schemas
   - Conversão para DTOs

2. **Processamento**:
   - Controller invoca caso de uso apropriado
   - Caso de uso aplica regras de negócio
   - Entidade do domínio é criada/modificada

3. **Persistência**:
   - Repository converte entidade para modelo
   - Operação executada no MongoDB
   - Resultado retornado

4. **Saída (Response)**:
   - Entidade convertida para DTO de resposta
   - Schema de resposta serializa para JSON
   - HTTP response enviado

## Padrões Implementados

### Repository Pattern
**Propósito**: Abstração do acesso a dados

**Implementação:**
```python
# Interface no domínio
class AbstractFuncionarioRepository(ABC):
    @abstractmethod
    async def criar(self, funcionario: Funcionario) -> Funcionario:
        pass

# Implementação na infraestrutura
class FuncionarioRepositoryImpl(AbstractFuncionarioRepository):
    async def criar(self, funcionario: Funcionario) -> Funcionario:
        # Implementação específica do MongoDB
        pass
```

**Benefícios:**
- Testabilidade
- Flexibilidade para mudanças de tecnologia
- Separação de responsabilidades

### Use Case Pattern
**Propósito**: Isolamento da lógica de negócio

**Implementação:**
```python
class CriarFuncionarioUseCase:
    def __init__(self, repository: AbstractFuncionarioRepository):
        self.repository = repository
    
    async def execute(self, request: CriarFuncionarioRequest) -> FuncionarioResponse:
        # Validações de negócio
        # Criação da entidade
        # Persistência
        # Retorno padronizado
```

**Benefícios:**
- Lógica de negócio centralizada
- Reusabilidade
- Testabilidade isolada

### Dependency Injection
**Propósito**: Inversão de controle

**Implementação:**
```python
# FastAPI dependency system
def get_funcionario_controller() -> FuncionarioController:
    repository = FuncionarioRepositoryImpl(get_database())
    use_case = CriarFuncionarioUseCase(repository)
    return FuncionarioController(use_case)
```

**Benefícios:**
- Acoplamento reduzido
- Configuração centralizada
- Testabilidade aumentada

### Value Objects Pattern
**Propósito**: Encapsulamento de validações

**Implementação:**
```python
class Email:
    def __init__(self, valor: str):
        self.valor = self._validar(valor)
    
    def _validar(self, email: str) -> str:
        # Validação específica
        return email
```

## Decisões Arquiteturais

### Por que MongoDB?
**Vantagens:**
- Flexibilidade de schema para evolução
- Escalabilidade horizontal nativa
- Performance otimizada para leitura
- Suporte nativo a JSON/BSON
- Consultas expressivas

**Trade-offs:**
- Eventual consistency (vs ACID completo)
- Maior uso de espaço
- Curva de aprendizado específica

### Por que FastAPI?
**Vantagens:**
- Performance superior (baseado em Starlette)
- Documentação automática (OpenAPI/Swagger)
- Suporte nativo a async/await
- Validação automática com Pydantic
- Type hints nativos
- Ecosystem moderno

**Trade-offs:**
- Framework mais novo (menos community)
- Alguns recursos ainda em evolução

### Por que DDD Simplificado?
**Justificativa:**
- Projeto de tamanho médio
- Equipe pequena (1-3 desenvolvedores)
- Complexidade de negócio controlada
- Preparação para crescimento futuro

**Adaptações:**
- Agregados simplificados
- Sem Event Sourcing
- CQRS implícito (não explícito)
- Focus em separação de responsabilidades

## Estrutura de Pastas

```
app/
├── domain/                    # 🏛️ Núcleo do negócio
│   ├── entities/             # Entidades de domínio
│   ├── repositories/         # Contratos de persistência
│   ├── value_objects/        # Objetos de valor
│   └── exceptions/           # Exceções de domínio
│
├── application/              # 🎯 Orquestração
│   ├── use_cases/           # Casos de uso (CRUD)
│   ├── dto/                 # Transferência de dados
│   ├── services/            # Serviços de aplicação
│   └── coordinators/        # Coordenação entre use cases
│
├── infrastructure/          # 🔧 Implementações técnicas
│   ├── database/           # Configuração MongoDB
│   └── repositories/       # Implementações de repositório
│
├── presentation/           # 🌐 Interface externa
│   ├── api/               # Endpoints e controllers
│   ├── schemas/           # Validação de entrada/saída
│   └── middleware/        # Middleware personalizado
│
└── shared/                # 🛠️ Utilitários compartilhados
    ├── exceptions/        # Exceções base
    └── utils/            # Utilities gerais
```

## Configuração e Inicialização

### Sequência de Startup

1. **Carregamento de Configurações**:
   - Variáveis de ambiente
   - Configurações padrão
   - Validação de configuração

2. **Inicialização de Infraestrutura**:
   - Conexão com MongoDB
   - Criação de índices
   - Health checks iniciais

3. **Configuração da Aplicação**:
   - Dependency injection
   - Middleware setup
   - Route registration

4. **Verificações Finais**:
   - Database connectivity
   - Index verification
   - API documentation generation

### Injeção de Dependência

```python
# Hierarchy de dependências
Database Connection → Repository → Use Case → Controller → Endpoint
```

## Escalabilidade e Performance

### Estratégias Implementadas

**Database Level:**
- Índices otimizados (email único, queries frequentes)
- Connection pooling com Motor
- Queries assíncronas

**Application Level:**
- Processamento assíncrono
- Paginação automática
- Cache de conexões

**API Level:**
- Response streaming
- Validação eficiente
- Serialização otimizada

### Pontos de Monitoramento

**Métricas importantes:**
- Response time por endpoint
- Database connection pool usage
- Memory usage
- CPU utilization
- Error rates

**Health Checks:**
- Database connectivity
- Application health
- External dependencies (futuro)

## Considerações de Segurança

### Implementadas

- Validação rigorosa de entrada
- Sanitização de dados
- Type safety com Pydantic
- Logs estruturados (sem dados sensíveis)

### Recomendadas para Produção

- Authentication/Authorization (JWT)
- Rate limiting
- HTTPS obrigatório
- Input sanitization adicional
- Audit logs
- Secrets management

## Evolução Futura

### Próximos Passos

**Testes:**
- Testes unitários (por camada)
- Testes de integração
- Testes de performance
- Testes de contract (API)

**Observabilidade:**
- Tracing distribuído
- Métricas customizadas
- Alerting
- Dashboard de monitoramento

**Funcionalidades:**
- Event-driven architecture
- CQRS explícito
- Cache distribuído
- Background jobs

### Preparação para Microserviços

**Patterns a considerar:**
- API Gateway
- Service mesh
- Event sourcing
- Saga pattern
- Circuit breaker

**Infrastructure as Code:**
- Kubernetes deployment
- Helm charts
- CI/CD pipelines
- Infrastructure monitoring

---

Esta arquitetura foi projetada para ser **simples de entender**, **fácil de manter** e **preparada para crescer** conforme as necessidades do negócio evoluem.
