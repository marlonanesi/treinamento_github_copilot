# Guia do Desenvolvedor - MS Cadastro Funcionário

## 🎯 Objetivo deste Documento

Este guia complementa o README.md principal com informações técnicas detalhadas e exemplos práticos para desenvolvedores que irão trabalhar no projeto.

## 🏗️ Arquitetura Técnica Detalhada

### Padrões Implementados

**Domain Driven Design (DDD)**
- **Domain Layer**: Entidades puras (sem dependências externas)
- **Application Layer**: Casos de uso e DTOs
- **Infrastructure Layer**: Implementações de repositório e BD
- **Presentation Layer**: Controllers, schemas e middlewares

**Repository Pattern**
- Abstração de acesso a dados
- Contratos no domínio, implementação na infraestrutura
- Facilita testes unitários e troca de tecnologia

**Dependency Injection**
- Gerenciado pelo FastAPI
- Inversão de dependências
- Facilita manutenibilidade

### Fluxo de Dados

```
Request → Controller → Use Case → Repository → Database
                     ↓
Response ← Schema ← DTO ← Entity ← Model
```

## 🛠️ Setup Detalhado para Desenvolvimento

### Configuração do Ambiente Local

1. **Clonar e configurar projeto:**
```bash
git clone <repo-url>
cd ms-cadastro-funcionario

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

2. **Configurar VS Code (Recomendado):**
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.sortImports.provider": "isort",
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

3. **Extensões VS Code úteis:**
- Python
- Docker
- REST Client
- MongoDB for VS Code
- GitLens

### Docker Development

```bash
# Build e execução
docker-compose up -d

# Logs em tempo real
docker-compose logs -f app

# Acesso ao container
docker-compose exec app bash

# Restart após mudanças
docker-compose restart app
```

## 📝 Padrões de Código

### Estrutura de Arquivos

```
nova_funcionalidade/
├── domain/entities/nova_entidade.py       # Entidade de domínio
├── application/
│   ├── dto/nova_dto.py                   # Data Transfer Objects
│   └── use_cases/nova_operacao.py        # Lógica de negócio
├── infrastructure/repositories/
│   └── nova_repository_impl.py           # Implementação BD
├── presentation/
│   ├── api/controllers/novo_controller.py # REST Controllers
│   └── schemas/nova_schema.py             # Validação de entrada
```

### Padrão de Naming

```python
# Classes (PascalCase)
class FuncionarioController
class CriarFuncionarioUseCase

# Métodos e variáveis (snake_case)
def criar_funcionario(self):
funcionario_id = "123"

# Constantes (UPPER_CASE)
DEFAULT_PAGE_SIZE = 10
API_VERSION = "v1"

# Arquivos (snake_case)
funcionario_controller.py
criar_funcionario_use_case.py
```

### Type Hints Obrigatórios

```python
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

# Sempre use type hints
async def criar_funcionario(
    self,
    request: CriarFuncionarioRequest
) -> FuncionarioResponse:
    pass

# Para retornos opcionais
async def buscar_por_email(
    self,
    email: str
) -> Optional[Funcionario]:
    pass

# Para listas e dicionários
async def listar_funcionarios(
    self,
    filtros: Dict[str, Any]
) -> List[Funcionario]:
    pass
```

### Docstrings Padrão

```python
class FuncionarioService:
    """
    Serviço de negócio para gerenciamento de funcionários.
    
    Este serviço implementa as regras de negócio relacionadas
    ao cadastro, consulta e manutenção de funcionários.
    """
    
    async def criar_funcionario(
        self,
        dados: Dict[str, Any]
    ) -> Funcionario:
        """
        Cria um novo funcionário no sistema.
        
        Args:
            dados: Dicionário com os dados do funcionário
            
        Returns:
            Funcionário criado com ID atribuído
            
        Raises:
            EmailJaExisteException: Quando email já existe
            DadosInvalidosException: Quando dados estão inválidos
        """
        pass
```

## 🔄 Workflow de Desenvolvimento

### Git Flow Simplificado

```bash
# Criar feature branch
git checkout -b feature/nova-funcionalidade

# Desenvolvimento com commits pequenos
git add .
git commit -m "feat: adiciona validação de CPF"

# Push e Pull Request
git push origin feature/nova-funcionalidade
# Abrir PR no GitHub/GitLab
```

### Testes Locais

```bash
# Executar aplicação local
uvicorn app.main:app --reload

# Testar endpoint
curl -X POST "http://localhost:8000/api/v1/funcionarios" \
  -H "Content-Type: application/json" \
  -d @test_data.json

# Verificar no banco
docker-compose exec mongodb mongosh funcionarios_db
```

### Debug e Troubleshooting

```python
# Adicionar logs de debug
import logging

logger = logging.getLogger(__name__)

async def minha_funcao():
    logger.debug("Iniciando operação")
    logger.info(f"Processando dados: {dados}")
    logger.error(f"Erro encontrado: {erro}")
```

## 📊 Exemplos Práticos

### Implementar Nova Validação

```python
# 1. Criar validador na camada de domínio
# app/domain/value_objects.py
class CNPJ:
    def __init__(self, valor: str):
        self.valor = self._validar(valor)
    
    def _validar(self, cnpj: str) -> str:
        # Lógica de validação CNPJ
        if not self._is_valid_cnpj(cnpj):
            raise ValueError("CNPJ inválido")
        return cnpj

# 2. Usar no schema
# app/presentation/schemas/empresa_schema.py
class EmpresaCreateSchema(BaseSchema):
    cnpj: str = Field(..., description="CNPJ da empresa")
    
    @field_validator('cnpj')
    @classmethod
    def validar_cnpj(cls, v):
        return CNPJ(v).valor
```

### Implementar Novo Endpoint

```python
# 1. Schema de entrada
class FuncionarioPorDepartamentoQuery(BaseSchema):
    departamento: str
    page: int = 1
    size: int = 10

# 2. Caso de uso
class ListarPorDepartamentoUseCase:
    async def execute(self, request):
        # Lógica de negócio
        return resultado

# 3. Controller
class FuncionarioController:
    async def listar_por_departamento(self, query):
        # Converter query em request
        # Chamar use case
        # Retornar response

# 4. Route
@router.get("/por-departamento")
async def listar_funcionarios_por_departamento(
    query: Annotated[FuncionarioPorDepartamentoQuery, Depends()],
    controller: Annotated[FuncionarioController, Depends()]
):
    return await controller.listar_por_departamento(query)
```

### Implementar Novo Repository Method

```python
# 1. Adicionar no contrato
class AbstractFuncionarioRepository(ABC):
    @abstractmethod
    async def buscar_por_departamento(
        self,
        departamento: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Funcionario]:
        pass

# 2. Implementar
class FuncionarioRepositoryImpl(AbstractFuncionarioRepository):
    async def buscar_por_departamento(
        self,
        departamento: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Funcionario]:
        cursor = self.collection.find(
            {"departamento": departamento}
        ).skip(skip).limit(limit)
        
        documents = await cursor.to_list(length=None)
        return [FuncionarioModel.to_entity(doc) for doc in documents]
```

## 🚀 Deploy e CI/CD

### Build Local

```bash
# Build da imagem
docker build -t funcionarios-api:dev .

# Test da imagem
docker run -p 8000:8000 funcionarios-api:dev

# Push para registry
docker tag funcionarios-api:dev registry.com/funcionarios-api:latest
docker push registry.com/funcionarios-api:latest
```

### GitHub Actions (Exemplo)

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest
      - name: Build Docker image
        run: |
          docker build -t funcionarios-api:${{ github.sha }} .
```

## 📚 Recursos para Estudo

### FastAPI
- [Tutorial Oficial](https://fastapi.tiangolo.com/tutorial/)
- [Async/Await em Python](https://docs.python.org/3/library/asyncio.html)
- [Pydantic Validation](https://docs.pydantic.dev/latest/)

### MongoDB
- [PyMongo Tutorial](https://pymongo.readthedocs.io/en/stable/tutorial.html)
- [Motor (Async MongoDB)](https://motor.readthedocs.io/en/stable/)
- [MongoDB Query Operators](https://docs.mongodb.com/manual/reference/operator/query/)

### Arquitetura
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

## 🤝 Contribuição e Code Review

### Checklist PR

- [ ] Código segue os padrões estabelecidos
- [ ] Type hints em todas as funções
- [ ] Docstrings nas classes e métodos principais
- [ ] Testes unitários implementados (futuro)
- [ ] Logs adequados adicionados
- [ ] Documentação atualizada se necessário
- [ ] Performance impact considerado
- [ ] Segurança verificada
- [ ] Backward compatibility mantida

### Code Review Points

1. **Arquitetura**: Respeita as camadas DDD?
2. **Performance**: Queries otimizadas?
3. **Segurança**: Validações adequadas?
4. **Manutenibilidade**: Código claro e testável?
5. **Padrões**: Segue convenções do projeto?

---

**Lembre-se**: Este é um projeto em constante evolução. Sugestões de melhorias são sempre bem-vindas! 🚀
