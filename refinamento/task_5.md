# Task 5 - Camada de Aplicação e Casos de Uso

## Objetivo
Implementar a camada de aplicação com casos de uso (use cases) e serviços que orquestram as operações de negócio do microserviço de funcionários.

## Principais Entregas
- Casos de uso para todas as operações CRUD
- Serviços de aplicação com validações de negócio
- DTOs internos para transferência de dados
- Coordenação entre domínio e infraestrutura
- Tratamento de exceções da aplicação

## Critério de Pronto
- ✅ Todos os casos de uso implementados e funcionais
- ✅ Validações de negócio aplicadas corretamente
- ✅ Exceções tratadas adequadamente
- ✅ Separação clara entre lógica de aplicação e domínio
- ✅ Injeção de dependências configurada

## Prompt de Execução

Como especialista em arquitetura de software e casos de uso, implemente a camada de aplicação do microserviço `ms-cadastro-funcionario` seguindo estas especificações:

**Casos de Uso - Estrutura Base (app/application/use_cases/base.py):**
- Classe abstrata `BaseUseCase[TRequest, TResponse]`:
  - Método abstrato `execute(request: TRequest) -> TResponse`
  - Logging básico de entrada e saída
  - Tratamento de exceções genérico
  - Validação de entrada

**Caso de Uso - Criar Funcionário (app/application/use_cases/criar_funcionario.py):**
- Classe `CriarFuncionarioUseCase`:
  - Request: `CriarFuncionarioRequest` (DTO)
  - Response: `FuncionarioResponse` (DTO)
  - Validações:
    - Email único no sistema
    - Dados obrigatórios presentes
    - Formato de campos válidos
  - Fluxo: validar → criar entidade → salvar → retornar DTO

**Caso de Uso - Buscar Funcionário (app/application/use_cases/buscar_funcionario.py):**
- Classe `BuscarFuncionarioPorIdUseCase`:
  - Request: `BuscarFuncionarioRequest` (ID)
  - Response: `FuncionarioResponse` ou None
  - Validação de ID válido
  - Tratamento de funcionário não encontrado

**Caso de Uso - Listar Funcionários (app/application/use_cases/listar_funcionarios.py):**
- Classe `ListarFuncionariosUseCase`:
  - Request: `ListarFuncionariosRequest` (filtros, paginação)
  - Response: `ListarFuncionariosResponse` (lista + metadados)
  - Suporte a filtros opcionais (departamento, cargo)
  - Paginação com skip/limit
  - Metadados de paginação (total, páginas)

**Caso de Uso - Atualizar Funcionário (app/application/use_cases/atualizar_funcionario.py):**
- Classe `AtualizarFuncionarioUseCase`:
  - Request: `AtualizarFuncionarioRequest` (ID + dados)
  - Response: `FuncionarioResponse`
  - Validações:
    - Funcionário existe
    - Campos imutáveis não alterados (email, data_admissao)
    - Dados válidos para atualização
  - Preservação de campos não informados

**Caso de Uso - Excluir Funcionário (app/application/use_cases/excluir_funcionario.py):**
- Classe `ExcluirFuncionarioUseCase`:
  - Request: `ExcluirFuncionarioRequest` (ID)
  - Response: `bool` (sucesso/falha)
  - Validações:
    - Funcionário existe
    - Não está ativo em projetos
  - Exclusão lógica ou física conforme regra

**DTOs de Request (app/application/dto/requests.py):**
```python
@dataclass
class CriarFuncionarioRequest:
    nome_completo: str
    email: str
    cargo: str
    data_admissao: date
    telefone: Optional[str] = None
    departamento: Optional[str] = None

@dataclass
class ListarFuncionariosRequest:
    departamento: Optional[str] = None
    cargo: Optional[str] = None
    skip: int = 0
    limit: int = 10

@dataclass
class AtualizarFuncionarioRequest:
    id: str
    nome_completo: Optional[str] = None
    cargo: Optional[str] = None
    telefone: Optional[str] = None
    departamento: Optional[str] = None
```

**DTOs de Response (app/application/dto/responses.py):**
```python
@dataclass
class FuncionarioResponse:
    id: str
    nome_completo: str
    email: str
    cargo: str
    data_admissao: date
    telefone: Optional[str]
    departamento: Optional[str]
    ativo: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class ListarFuncionariosResponse:
    funcionarios: List[FuncionarioResponse]
    total: int
    skip: int
    limit: int
    has_next: bool
```

**Serviço de Aplicação (app/application/services/funcionario_service.py):**
- Classe `FuncionarioService`:
  - Orquestra múltiplos casos de uso
  - Validações cross-cutting
  - Logging de operações
  - Métricas de performance (se necessário)

**Coordenador de Casos de Uso (app/application/coordinators/funcionario_coordinator.py):**
- Classe `FuncionarioCoordinator`:
  - Facade para todos os casos de uso
  - Injeção de dependências centralizada
  - Configuração de logging específico
  - Factory methods para casos de uso

**Exceções de Aplicação (app/application/exceptions.py):**
- `ApplicationException`: Base para exceções de aplicação
- `ValidationException`: Erros de validação de entrada
- `BusinessRuleException`: Regras de negócio violadas
- `ResourceNotFoundException`: Recurso não encontrado
- `DuplicateResourceException`: Recurso duplicado

**Validadores (app/application/validators/funcionario_validator.py):**
- Classe `FuncionarioValidator`:
  - `validate_create_request()`: Validação para criação
  - `validate_update_request()`: Validação para atualização
  - `validate_email_format()`: Validação de email
  - `validate_phone_format()`: Validação de telefone
  - `validate_business_rules()`: Regras de negócio específicas

**Padrões a seguir:**
- Use casos de uso únicos e focados (Single Responsibility)
- DTOs imutáveis para transferência de dados
- Validação em múltiplas camadas (entrada, negócio, persistência)
- Logging estruturado com contexto
- Exceções específicas com mensagens claras
- Type Hints em todos os métodos e classes
- Documentação clara dos fluxos de negócio
- Injeção de dependências via construtor

**Estrutura de arquivos esperada:**
```
app/application/
├── use_cases/
│   ├── base.py                    # Classe base
│   ├── criar_funcionario.py       # Criar funcionário
│   ├── buscar_funcionario.py      # Buscar por ID
│   ├── listar_funcionarios.py     # Listar com filtros
│   ├── atualizar_funcionario.py   # Atualizar dados
│   └── excluir_funcionario.py     # Excluir funcionário
├── services/
│   └── funcionario_service.py     # Serviços de aplicação
├── dto/
│   ├── requests.py               # DTOs de entrada
│   └── responses.py              # DTOs de saída
├── validators/
│   └── funcionario_validator.py  # Validadores
├── coordinators/
│   └── funcionario_coordinator.py # Coordenador
└── exceptions.py                 # Exceções de aplicação
```

**Fluxos de Validação:**
1. Validação de entrada (formato, tipos)
2. Validação de negócio (regras específicas)
3. Validação de consistência (banco de dados)
4. Executar operação
5. Retornar resultado ou exceção

Implemente toda a camada de aplicação mantendo foco na orquestração clara dos casos de uso e separação adequada de responsabilidades.
