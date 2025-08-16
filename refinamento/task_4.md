# Task 4 - Infraestrutura de Dados e Repositório MongoDB

## Objetivo
Implementar a camada de infraestrutura com configuração do MongoDB, conexão assíncrona usando Motor e implementação concreta do repositório de funcionários.

## Principais Entregas
- Configuração de conexão assíncrona com MongoDB usando Motor
- Implementação concreta do repositório de funcionários
- Modelos de dados para MongoDB (ODM simples)
- Configuração de índices para performance
- Gerenciamento de conexões e pool

## Critério de Pronto
- ✅ Conexão com MongoDB estabelecida e funcional
- ✅ Repositório implementado com todas as operações CRUD
- ✅ Índices criados automaticamente na inicialização (caso não existam)
- ✅ Validações de duplicidade funcionando
- ✅ Operações assíncronas implementadas corretamente

## Prompt de Execução

Como especialista em MongoDB e Python assíncrono, implemente a camada de infraestrutura do microserviço `ms-cadastro-funcionario` seguindo estas especificações:

**Configuração de Database (app/infrastructure/database/connection.py):**
- Classe `MongoDBConnection`:
  - Singleton pattern para conexão única
  - Pool de conexões configurado
  - Método `connect()`: Estabelece conexão
  - Método `disconnect()`: Fecha conexões
  - Método `get_database()`: Retorna instância do banco
  - Configuração de timeout e retry
  - Logging de conexão/desconexão

**Database Manager (app/infrastructure/database/database_manager.py):**
- Classe `DatabaseManager`:
  - Inicialização de índices
  - Criação de coleções se necessário
  - Método `create_indexes()`: Cria índices otimizados
  - Método `health_check()`: Verifica saúde da conexão
  - Configuração de TTL se necessário

**Modelos de Dados (app/infrastructure/database/models.py):**
- Classe `FuncionarioModel`:
  - Mapeamento entre entidade de domínio e documento MongoDB
  - Método `from_entity()`: Converte entidade para documento
  - Método `to_entity()`: Converte documento para entidade
  - Validação de tipos específicos do MongoDB
  - Serialização de datas e ObjectId

**Implementação do Repositório (app/infrastructure/repositories/funcionario_repository_impl.py):**
- Classe `FuncionarioRepositoryImpl(AbstractFuncionarioRepository)`:
  - Implementar todos os métodos da interface
  - `salvar()`: Insert com validação de duplicidade
  - `buscar_por_id()`: Find by ObjectId com conversão
  - `buscar_por_email()`: Query por email com índice
  - `listar_todos()`: Find com paginação
  - `listar_por_filtros()`: Query complexa com filtros opcionais
  - `atualizar()`: Update parcial preservando campos imutáveis
  - `excluir()`: Delete com validação de regras de negócio
  - `verificar_email_existe()`: Existe para validação de duplicidade

**Configurações Específicas:**

**Índices obrigatórios:**
- `email`: unique=True (previne duplicatas)
- `departamento`: para queries de filtro
- `cargo`: para queries de filtro
- `created_at`: para ordenação temporal
- Índice composto: `{departamento: 1, cargo: 1}` para filtros combinados

**Queries Otimizadas:**
- Listar com filtros: usar `$and` para múltiplos filtros
- Paginação: usar `skip` e `limit` eficientemente
- Busca por email: usar índice unique
- Contagem: usar `count_documents()` quando necessário

**Tratamento de Erros:**
- `DuplicateKeyError`: Converter para `EmailDuplicadoException`
- `ValidationError`: Converter para `DadosInvalidosException`
- `ConnectionFailure`: Log e re-raise com contexto
- `DocumentNotFound`: Converter para `FuncionarioNaoEncontradoException`

**Configuração de Conexão (app/infrastructure/config/database.py):**
- Função `get_mongo_client()`: Factory para cliente Motor
- Configurações de conexão:
  - `maxPoolSize`: 10
  - `minPoolSize`: 1
  - `maxIdleTimeMS`: 30000
  - `connectTimeoutMS`: 5000
  - `serverSelectionTimeoutMS`: 5000

**Dependency Injection (app/infrastructure/dependencies.py):**
- Função `get_database()`: Retorna instância do banco
- Função `get_funcionario_repository()`: Factory do repositório
- Configuração para FastAPI dependencies

**Operações Assíncronas Específicas:**
```python
# Exemplo de estrutura esperada para busca com filtros
async def listar_por_filtros(
    self, 
    departamento: Optional[str] = None,
    cargo: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
) -> List[Funcionario]:
    # Construir query dinâmica
    # Usar índices otimizados
    # Aplicar paginação
    # Converter resultados para entidades
```

**Padrões a seguir:**
- Use `motor.motor_asyncio` para operações assíncronas
- Implemente logging adequado para debug
- Use Context Managers quando apropriado
- Valide dados antes de persistir
- Converta exceções de MongoDB para exceções de domínio
- Implemente retry logic para operações críticas
- Use TypeHints em todos os métodos
- Documente queries complexas

**Estrutura de arquivos esperada:**
```
app/infrastructure/
├── database/
│   ├── connection.py        # Configuração de conexão
│   ├── database_manager.py  # Gerenciamento do banco
│   └── models.py           # Modelos de dados
├── repositories/
│   └── funcionario_repository_impl.py  # Implementação do repositório
├── config/
│   └── database.py         # Configurações específicas
└── dependencies.py         # Injeção de dependências
```

**Configuração de Inicialização:**
- Método para criar índices na startup da aplicação
- Verificação de conectividade na inicialização
- Configuração de logging específico para MongoDB

Implemente toda a camada de infraestrutura mantendo foco em performance, confiabilidade e facilidade de manutenção.
