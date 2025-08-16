# Task 6 - Schemas Pydantic e DTOs da API

## Objetivo
Implementar schemas Pydantic para validação, serialização e documentação automática da API, incluindo modelos de entrada, saída e validações específicas.

## Principais Entregas
- Schemas Pydantic para todos os endpoints
- Validações customizadas usando Pydantic validators
- Modelos de resposta padronizados
- Schemas para diferentes operações (create, update, response)
- Documentação automática aprimorada

## Critério de Pronto
- ✅ Todos os schemas Pydantic implementados
- ✅ Validações customizadas funcionando
- ✅ Documentação automática gerada corretamente
- ✅ Padronização de respostas da API
- ✅ Tratamento de erros de validação

## Prompt de Execução

Como especialista em FastAPI e Pydantic, implemente os schemas de validação do microserviço `ms-cadastro-funcionario` seguindo estas especificações:

**Schema Base (app/presentation/schemas/base.py):**
- Classe `BaseSchema` (Pydantic BaseModel):
  - Configuração comum para todos os schemas
  - `Config` com `from_attributes=True` para ORMs
  - Método `model_dump_json()` customizado para datas
  - Validadores comuns (strip strings, normalize)

**Schema de Funcionário - Criação (app/presentation/schemas/funcionario_schemas.py):**
```python
class FuncionarioCreateSchema(BaseSchema):
    nome_completo: str = Field(..., min_length=2, description="Nome completo do funcionário")
    email: EmailStr = Field(..., description="Email único do funcionário")
    cargo: str = Field(..., min_length=1, description="Cargo do funcionário")
    data_admissao: date = Field(..., description="Data de admissão")
    telefone: Optional[str] = Field(None, description="Telefone no formato brasileiro")
    departamento: Optional[str] = Field(None, description="Departamento do funcionário")

    # Validators customizados
    @validator('nome_completo')
    def validar_nome_completo(cls, v):
        # Validar que tem pelo menos 2 palavras
    
    @validator('telefone')
    def validar_telefone(cls, v):
        # Validar formato brasileiro
    
    @validator('data_admissao')
    def validar_data_admissao(cls, v):
        # Não pode ser futura
```

**Schema de Funcionário - Atualização (app/presentation/schemas/funcionario_schemas.py):**
```python
class FuncionarioUpdateSchema(BaseSchema):
    nome_completo: Optional[str] = Field(None, min_length=2)
    cargo: Optional[str] = Field(None, min_length=1)
    telefone: Optional[str] = Field(None)
    departamento: Optional[str] = Field(None)
    
    # Validação para impedir campos imutáveis
    @model_validator(mode='before')
    def validar_campos_imutaveis(cls, values):
        # Verificar se email ou data_admissao estão sendo alterados
```

**Schema de Funcionário - Resposta (app/presentation/schemas/funcionario_schemas.py):**
```python
class FuncionarioResponseSchema(BaseSchema):
    id: str = Field(..., description="ID único do funcionário")
    nome_completo: str
    email: str
    cargo: str
    data_admissao: date
    telefone: Optional[str]
    departamento: Optional[str]
    ativo: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        # Configuração para documentação
        json_schema_extra = {
            "example": {
                "id": "60d5ecb74b24c3b3d8f8e1a2",
                "nome_completo": "João Silva Santos",
                "email": "joao.santos@company.com",
                "cargo": "Desenvolvedor Senior",
                "data_admissao": "2023-01-15",
                "telefone": "(11) 99999-9999",
                "departamento": "Tecnologia",
                "ativo": false,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            }
        }
```

**Schema de Listagem (app/presentation/schemas/funcionario_schemas.py):**
```python
class FuncionarioListQuerySchema(BaseSchema):
    departamento: Optional[str] = Field(None, description="Filtrar por departamento")
    cargo: Optional[str] = Field(None, description="Filtrar por cargo")
    skip: int = Field(0, ge=0, description="Número de registros para pular")
    limit: int = Field(10, ge=1, le=100, description="Limite de registros por página")

class FuncionarioListResponseSchema(BaseSchema):
    funcionarios: List[FuncionarioResponseSchema] = Field(..., description="Lista de funcionários")
    total: int = Field(..., description="Total de funcionários encontrados")
    skip: int = Field(..., description="Registros pulados")
    limit: int = Field(..., description="Limite aplicado")
    has_next: bool = Field(..., description="Indica se há próxima página")
```

**Schemas de Resposta Padronizada (app/presentation/schemas/response_schemas.py):**
```python
class SuccessResponseSchema(BaseSchema):
    success: bool = Field(True)
    message: str = Field(..., description="Mensagem de sucesso")
    data: Optional[Any] = Field(None, description="Dados da resposta")

class ErrorResponseSchema(BaseSchema):
    success: bool = Field(False)
    error: str = Field(..., description="Tipo do erro")
    message: str = Field(..., description="Mensagem de erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes adicionais")

class ValidationErrorSchema(BaseSchema):
    field: str = Field(..., description="Campo com erro")
    message: str = Field(..., description="Mensagem do erro")
    value: Optional[Any] = Field(None, description="Valor que causou erro")
```

**Validadores Customizados (app/presentation/schemas/validators.py):**
```python
class CustomValidators:
    @staticmethod
    def validar_nome_completo(nome: str) -> str:
        # Implementar validação de nome completo
    
    @staticmethod
    def validar_telefone_brasileiro(telefone: str) -> str:
        # Implementar validação de telefone brasileiro
    
    @staticmethod
    def validar_email_corporativo(email: str) -> str:
        # Validações específicas se necessário
    
    @staticmethod
    def normalizar_cargo(cargo: str) -> str:
        # Normalização de cargo
```

**Schema de Health Check (app/presentation/schemas/health_schemas.py):**
```python
class HealthCheckResponseSchema(BaseSchema):
    status: str = Field(..., description="Status da aplicação")
    timestamp: datetime = Field(..., description="Timestamp da verificação")
    version: str = Field(..., description="Versão da aplicação")
    database_status: str = Field(..., description="Status do banco de dados")
```

**Configurações de Schemas (app/presentation/schemas/config.py):**
- Configurações globais para Pydantic
- Custom JSON encoders para tipos específicos
- Configuração de aliases para campos
- Tratamento de timezone para datetime

**Middlewares de Validação (app/presentation/schemas/middleware.py):**
- Middleware para tratamento de erros de validação
- Formatação padronizada de erros Pydantic
- Logging de erros de validação
- Customização de mensagens de erro

**Exemplos e Documentação (app/presentation/schemas/examples.py):**
- Exemplos para documentação automática
- Dados de teste para schemas
- Factories para criação de dados de exemplo

**Padrões a seguir:**
- Use `Field()` com validações e descrições claras
- Implemente validators customizados quando necessário
- Use `EmailStr` do Pydantic para emails
- Configure exemplos para documentação automática
- Separar schemas por responsabilidade (Create/Update/Response)
- Use Type Hints adequados
- Validações devem ser informativas e específicas
- Configuração de serialização de datas padronizada

**Estrutura de arquivos esperada:**
```
app/presentation/schemas/
├── base.py                     # Schema base
├── funcionario_schemas.py      # Schemas do funcionário
├── response_schemas.py         # Schemas de resposta padrão
├── health_schemas.py          # Schemas de health check
├── validators.py              # Validadores customizados
├── middleware.py              # Middlewares de validação
├── config.py                  # Configurações
└── examples.py                # Exemplos para documentação
```

**Validações Específicas Obrigatórias:**
1. Nome completo: mínimo 2 palavras, sem números
2. Email: formato válido, único no sistema
3. Telefone: formato brasileiro (xx) xxxxx-xxxx ou (xx) xxxx-xxxx
4. Data admissão: não pode ser futura
5. Cargo: não pode ser vazio após strip
6. Campos de atualização: email e data_admissao são imutáveis

**Documentação API:**
- Todos os schemas devem ter descrições claras
- Exemplos realistas nos schemas
- Documentação de códigos de erro
- Schemas de resposta para diferentes status HTTP

Implemente todos os schemas mantendo foco na validação robusta, documentação clara e padronização das respostas da API.
