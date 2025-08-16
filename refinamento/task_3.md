# Task 3 - Modelagem de Domínio e Entidades

## Objetivo
Implementar a camada de domínio com a entidade `Funcionario`, regras de negócio e interfaces de repositório seguindo princípios DDD.

## Principais Entregas
- Entidade `Funcionario` com validações de domínio
- Value Objects para dados específicos (Email, Cargo)
- Interfaces de repositório (contratos)
- Exceções customizadas de domínio
- Regras de negócio incorporadas na entidade

## Critério de Pronto
- ✅ Entidade `Funcionario` implementada com todas as propriedades
- ✅ Validações de negócio funcionando
- ✅ Interfaces de repositório definidas
- ✅ Exceções de domínio criadas e testáveis
- ✅ Value Objects implementados adequadamente

## Prompt de Execução

Como especialista em Domain Driven Design e Python, implemente a camada de domínio do microserviço `ms-cadastro-funcionario` seguindo estas especificações:

**Entidade Funcionario (app/domain/entities/funcionario.py):**
- Classe `Funcionario` com properties:
  - `id`: Optional[str] (ObjectId do MongoDB)
  - `nome_completo`: str (obrigatório, min 2 palavras)
  - `email`: str (obrigatório, único, validação de formato)
  - `cargo`: str (obrigatório, não vazio)
  - `data_admissao`: date (obrigatório)
  - `telefone`: Optional[str] (formato brasileiro validado)
  - `departamento`: Optional[str]
  - `ativo`: bool (default False)
  - `created_at`: datetime (auto-preenchido)
  - `updated_at`: datetime (auto-atualizado)

**Métodos da Entidade:**
- `__init__()`: Construtor com validações
- `atualizar()`: Método para atualização controlada
- `pode_ser_excluido()`: Regra de negócio para exclusão
- `marcar_ativo()`: Controle do status
- `desmarcar_ativo()`: Controle do status
- `to_dict()`: Serialização para MongoDB
- `from_dict()`: Deserialização do MongoDB

**Value Objects (app/domain/entities/value_objects.py):**
- `Email`: Validação de formato e unicidade
  - Método `is_valid()`: Validação de formato
  - Propriedade `value`: Acesso ao valor
  - Método `__str__()` e `__eq__()`
- `Cargo`: Validação de cargo válido
  - Lista de cargos permitidos (enum-like)
  - Validação de cargo existente
  - Normalização de texto

**Interfaces de Repositório (app/domain/repositories/funcionario_repository.py):**
- `AbstractFuncionarioRepository` (ABC):
  - `async def salvar(funcionario: Funcionario) -> Funcionario`
  - `async def buscar_por_id(id: str) -> Optional[Funcionario]`
  - `async def buscar_por_email(email: str) -> Optional[Funcionario]`
  - `async def listar_todos(skip: int, limit: int) -> List[Funcionario]`
  - `async def listar_por_filtros(departamento: str, cargo: str, skip: int, limit: int) -> List[Funcionario]`
  - `async def atualizar(funcionario: Funcionario) -> Funcionario`
  - `async def excluir(id: str) -> bool`
  - `async def verificar_email_existe(email: str, excluir_id: Optional[str]) -> bool`

**Exceções de Domínio (app/domain/exceptions/funcionario_exceptions.py):**
- `FuncionarioException`: Base para exceções de domínio
- `FuncionarioNaoEncontradoException`: Quando funcionário não existe
- `EmailDuplicadoException`: Email já existe no sistema
- `FuncionarioAtivoEmProjetosException`: Não pode excluir funcionário ativo
- `DadosInvalidosException`: Dados de entrada inválidos
- `CargoInvalidoException`: Cargo não permitido

**Regras de Negócio (implementar na entidade):**
1. Email deve ser único no sistema
2. Nome completo deve ter pelo menos 2 palavras
3. Cargo deve ser de lista pré-definida ou livre (conforme regra de negócio)
4. Funcionário ativo em projetos não pode ser excluído
5. Data de admissão não pode ser futura
6. Telefone deve seguir formato brasileiro (se informado)
7. Email e data_admissao não podem ser alterados após criação

**Validações Específicas:**
- Email: regex para formato válido
- Telefone: regex para formato brasileiro (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
- Nome completo: verificação de múltiplas palavras
- Data admissão: não pode ser maior que hoje

**Padrões a seguir:**
- Use `dataclasses` ou propriedades Python para encapsulamento
- Implemente `__str__` e `__repr__` adequadamente
- Use Type Hints em todos os métodos
- Valide dados no construtor e métodos de atualização
- Separe regras de negócio da lógica de persistência
- Use ABC (Abstract Base Class) para interfaces
- Docstrings em classes e métodos principais
- Exceptions com mensagens claras e informativas

**Estrutura de arquivos esperada:**
```
app/domain/
├── entities/
│   ├── funcionario.py       # Entidade principal
│   └── value_objects.py     # Value objects
├── repositories/
│   └── funcionario_repository.py  # Interface do repositório
└── exceptions/
    └── funcionario_exceptions.py  # Exceções de domínio
```

Implemente toda a camada de domínio seguindo princípios de DDD, mantendo a lógica de negócio isolada e facilmente testável.
