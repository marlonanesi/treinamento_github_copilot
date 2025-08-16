# 🧪 Geração de Testes Unitários - ms-cadastro-funcionario

> **📋 Regra Fundamental:** Este documento orienta a criação de **APENAS TESTES UNITÁRIOS**. Para qualquer interação com banco de dados, utilize **MOCKS** - nunca acesse recursos externos reais.

## 🎯 Objetivo

Criar uma suíte completa de **testes unitários isolados** para o ms-cadastro-funcionario, garantindo:

- ✅ **Cobertura por camada** seguindo Clean Architecture
- ✅ **Zero dependências externas** (sem DB, rede, disco)
- ✅ **Mocks obrigatórios** para Motor/MongoDB
- ✅ **Validação de regras de negócio** sem I/O real

## ⚠️ Restrições Importantes

- ❌ **NUNCA** conectar com MongoDB real
- ❌ **NUNCA** subir Uvicorn ou Docker nos testes
- ❌ **NUNCA** fazer I/O (disco, rede, banco)
- ✅ **SEMPRE** usar AsyncMock para operações assíncronas
- ✅ **SEMPRE** mockar repositórios e dependências externas
- ✅ **APENAS** testes unitários isolados

## 📁 Estrutura de Arquivos

```
tests/
├── unit/                     # 🧪 Apenas testes unitários
│   ├── domain/              # 🏗️ Entidades, VOs, exceções
│   ├── application/         # ⚙️ Casos de uso (com mocks)
│   ├── infrastructure/      # 🗄️ Repositórios (com AsyncMock)
│   ├── presentation/        # 🌐 Routers, schemas (dependências mockadas)
│   └── shared/              # 🔧 Utilitários, adapters
├── conftest.py              # ⚙️ Fixtures globais
├── factories.py             # 🏭 Fábricas de dados de teste
├── mocks.py                 # 🎭 Mocks de repositórios e casos de uso
├── pytest.ini               # ⚙️ Configuração do pytest
└── .coveragerc              # 📊 Configuração de cobertura
```

## 🛠️ Stack e Ferramentas

**Ferramentas obrigatórias:**
- `pytest` + `pytest-asyncio` + `pytest-mock`
- `unittest.mock.AsyncMock` para **todos os métodos assíncronos**
- `monkeypatch` para variáveis de ambiente
- **AAA Pattern** (Arrange-Act-Assert)
- **Nomes descritivos** + docstrings curtas
- `@pytest.mark.parametrize` para múltiplos cenários
## ⚙️ Configurações Iniciais

### 📄 pytest.ini
```ini
[pytest]
addopts = -q --maxfail=1 --disable-warnings --strict-markers --cov=app --cov-report=term-missing
markers =
    asyncio: marks tests as needing an asyncio event loop
```

### 📊 .coveragerc
```ini
[report]
omit =
  venv/*
  __pycache__/*
  tests/*
  app/main.py
```

## 🏗️ Arquivos de Suporte

### 🔧 conftest.py
> **Centraliza fixtures globais com foco em MOCKS**

```python

import pytest
from unittest.mock import AsyncMock, patch

# 🔄 Define o backend para testes assíncronos
# pytest-asyncio utiliza esta fixture para gerenciar loops de eventos
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

# 🌍 Simula variáveis de ambiente (OBRIGATÓRIO para Motor)
# NUNCA usar URIs reais de banco em testes unitários
@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv("MONGO_URI", "mongodb://fake-test-uri:27017")
    monkeypatch.setenv("DB_NAME", "fake-test-database")

# 🎭 Mock da coleção do Motor (ESSENCIAL para testes de infraestrutura)
# Substitui COMPLETAMENTE a conexão real com o DB
@pytest.fixture
def motor_collection_mock():
    """
    ⚠️ IMPORTANTE: Este mock substitui TODA interação com MongoDB.
    Nunca permita que testes acessem banco real.
    """
    mock_collection = AsyncMock()
    # Configura todos os métodos assíncronos do Motor
    mock_collection.find_one = AsyncMock(return_value=None)
    mock_collection.insert_one = AsyncMock(return_value=None)
    mock_collection.update_one = AsyncMock(return_value=None)
    mock_collection.delete_one = AsyncMock(return_value=None)
    mock_collection.find = AsyncMock(return_value=[])
    return mock_collection
```

### 🏭 factories.py
> **Fábricas para dados de teste consistentes**

```python

import uuid
from datetime import date
from pydantic import ValidationError

from app.domain.entities.funcionario import Funcionario, CargoEnum  # (inferido)
from app.presentation.schemas.funcionario import FuncionarioCreatePayload  # (inferido)

def create_valid_funcionario(**kwargs):
    """🏗️ Cria uma instância válida da entidade Funcionario."""
    data = {
        "id": str(uuid.uuid4()),
        "nome": "João da Silva",
        "email": "joao.silva@exemplo.com",
        "cargo": "ANALISTA",
        "data_nascimento": date(1990, 1, 1),
        **kwargs
    }
    return Funcionario(**data)

def create_valid_create_payload(**kwargs):
    """📝 Cria um payload válido para criação de funcionário."""
    data = {
        "nome": "Maria de Souza",
        "email": "maria.souza@exemplo.com",
        "cargo": "DESENVOLVEDOR",
        "data_nascimento": "1995-05-15",
        **kwargs
    }
    return FuncionarioCreatePayload(**data)
```

### 🎭 mocks.py
> **Mocks de repositórios e casos de uso - SUBSTITUI dependências externas**

```python

import uuid
from unittest.mock import AsyncMock
from typing import Optional

from app.domain.entities.funcionario import Funcionario, FuncionarioUpdate  # (inferido)
from app.application.exceptions import FuncionarioNaoEncontradoError  # (inferido)

class FuncionarioRepositoryMock:
    """🎭 Mock do repositório - SUBSTITUI acesso ao banco real"""
    
    def __init__(self):
        self.db = {}  # Simula banco em memória

    async def get_by_id(self, funcionario_id: str) -> Optional[Funcionario]:
        return self.db.get(funcionario_id)
    
    async def create(self, funcionario: Funcionario) -> Funcionario:
        self.db[funcionario.id] = funcionario
        return funcionario

    async def update(self, funcionario_id: str, update_data: FuncionarioUpdate) -> Funcionario:
        if funcionario_id not in self.db:
            return None
        existing = self.db[funcionario_id]
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        return existing
    
    async def delete(self, funcionario_id: str) -> None:
        self.db.pop(funcionario_id, None)

class FuncionarioUseCaseMock:
    """🎭 Mock do caso de uso - ISOLA lógica de negócio"""
    
    def __init__(self, funcionario: Funcionario = None):
        self.get_by_id = AsyncMock(return_value=funcionario)
        self.create = AsyncMock(return_value=funcionario)
        self.update = AsyncMock(return_value=funcionario)
        self.delete = AsyncMock(return_value=None)
        
        # Simula comportamento de erro quando ID não existe
        self.get_by_id.side_effect = lambda id: funcionario if id == funcionario.id else FuncionarioNaoEncontradoError()
```

---

## 🧪 Exemplos de Testes por Camada

### 🏗️ Domain Layer - `tests/unit/domain/test_funcionario_entity.py`
> **Foco: Validações, regras de negócio, métodos da entidade**

```python

import pytest
from datetime import date
from pydantic import ValidationError

from app.domain.entities.funcionario import Funcionario, CargoEnum  # (inferido)
from app.domain.exceptions import EmailInvalidoError  # (inferido)
from factories import create_valid_funcionario

class TestFuncionario:
    """
    🧪 Testes para a entidade Funcionario
    ✅ Sem dependências externas - apenas validações e regras de negócio
    """

    def test_cria_funcionario_valido_com_sucesso(self):
        """✅ HAPPY PATH: Deve criar uma instância de Funcionario com dados válidos."""
        # ARRANGE
        data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "nome": "Carlos Teste",
            "email": "carlos.teste@teste.com",
            "cargo": CargoEnum.GERENTE,
            "data_nascimento": date(1985, 12, 1)
        }
        
        # ACT
        funcionario = Funcionario(**data)
        
        # ASSERT
        assert funcionario.nome == data["nome"]
        assert funcionario.email == data["email"]
        assert funcionario.cargo == data["cargo"]

    @pytest.mark.parametrize("email, expected_error", [
        ("email_invalido.com", EmailInvalidoError),
        ("email_sem_arroba", EmailInvalidoError),
        ("", ValidationError),
    ])
    def test_cria_funcionario_com_email_invalido(self, email, expected_error):
        """
        ❌ Cenário TRISTE: Deve levantar um erro ao tentar criar um funcionário com email inválido.
        """
        # ARRANGE
        data = create_valid_funcionario()
        data.email = email
        
        # ACT & ASSERT
        with pytest.raises(expected_error):
            Funcionario(**data)

    def test_eq_method(self):
        """✅ Deve retornar True para duas instâncias com o mesmo ID."""
        # ARRANGE
        id_comum = "123e4567-e89b-12d3-a456-426614174000"
        funcionario1 = create_valid_funcionario(id=id_comum, email="um@email.com")
        funcionario2 = create_valid_funcionario(id=id_comum, email="outro@email.com")
        
        # ACT & ASSERT
        assert funcionario1 == funcionario2
```

### ⚙️ Application Layer - `tests/unit/application/test_funcionario_use_case.py`
> **Foco: Orquestração, mocks de repositórios, tratamento de exceções**

```python

import pytest
from unittest.mock import AsyncMock, ANY

from app.application.use_cases.funcionario_use_case import FuncionarioUseCase  # (inferido)
from app.application.exceptions import FuncionarioNaoEncontradoError  # (inferido)
from factories import create_valid_funcionario
from mocks import FuncionarioRepositoryMock

class TestFuncionarioUseCase:
    """
    🧪 Testes para o caso de uso de funcionários
    ⚠️ OBRIGATÓRIO: Repositórios SEMPRE mockados
    """

    @pytest.fixture
    def mock_repo(self):
        return FuncionarioRepositoryMock()

    @pytest.mark.asyncio
    async def test_cria_funcionario_com_sucesso(self, mock_repo):
        """✅ HAPPY PATH: Deve chamar o repositório para criar um funcionário."""
        # ARRANGE
        use_case = FuncionarioUseCase(funcionario_repository=mock_repo)
        novo_funcionario = create_valid_funcionario()
        
        # ACT
        result = await use_case.create(novo_funcionario)
        
        # ASSERT
        assert result == novo_funcionario
        assert mock_repo.db[novo_funcionario.id] == novo_funcionario  # Verifica mock

    @pytest.mark.asyncio
    async def test_busca_funcionario_nao_encontrado(self, mock_repo):
        """❌ Cenário TRISTE: Deve levantar exceção quando o funcionário não é encontrado."""
        # ARRANGE
        use_case = FuncionarioUseCase(funcionario_repository=mock_repo)
        
        # ACT & ASSERT
        with pytest.raises(FuncionarioNaoEncontradoError):
            await use_case.get_by_id("id_nao_existente")

    @pytest.mark.asyncio
    async def test_atualiza_funcionario_com_sucesso(self, mock_repo):
        """✅ HAPPY PATH: Deve atualizar um funcionário existente."""
        # ARRANGE
        funcionario_existente = create_valid_funcionario()
        await mock_repo.create(funcionario_existente)
        use_case = FuncionarioUseCase(funcionario_repository=mock_repo)
        update_data = {"email": "novo.email@exemplo.com"}
        
        # ACT
        await use_case.update(funcionario_existente.id, update_data)
        
        # ASSERT
        funcionario_atualizado = await mock_repo.get_by_id(funcionario_existente.id)
        assert funcionario_atualizado.email == update_data["email"]
```

### 🗄️ Infrastructure Layer - `tests/unit/infrastructure/test_funcionario_repository.py`
> **⚠️ CRÍTICO: AsyncMock OBRIGATÓRIO para Motor - NUNCA acesse DB real**

```python

import pytest
from unittest.mock import ANY

from app.infrastructure.repositories.funcionario_repository import FuncionarioRepository  # (inferido)
from factories import create_valid_funcionario

class TestFuncionarioRepository:
    """
    🧪 Testes para a camada de infraestrutura
    🚨 ATENÇÃO: Motor Collection SEMPRE mockada via AsyncMock
    ❌ NUNCA conectar com MongoDB real
    """
    
    @pytest.mark.asyncio
    async def test_create_chama_insert_one_do_motor_com_doc_correto(self, motor_collection_mock):
        """
        ✅ HAPPY PATH: Deve chamar `insert_one` do Motor com o documento mapeado corretamente.
        🎭 Mock verifica chamada sem executar operação real
        """
        # ARRANGE
        repo = FuncionarioRepository(motor_collection=motor_collection_mock)
        novo_funcionario = create_valid_funcionario()
        expected_doc = novo_funcionario.model_dump()
        expected_doc["_id"] = expected_doc.pop("id")  # Mapeamento para Mongo
        
        # ACT
        await repo.create(novo_funcionario)
        
        # ASSERT - Verifica se Motor foi chamado corretamente
        motor_collection_mock.insert_one.assert_awaited_once_with(expected_doc)

    @pytest.mark.asyncio
    async def test_get_by_id_chama_find_one_com_filtro_correto(self, motor_collection_mock):
        """
        ✅ HAPPY PATH: Deve chamar `find_one` do Motor com o filtro "_id" correto.
        """
        # ARRANGE
        repo = FuncionarioRepository(motor_collection=motor_collection_mock)
        funcionario_id = "123e4567-e89b-12d3-a456-426614174000"
        
        # ACT
        await repo.get_by_id(funcionario_id)
        
        # ASSERT - Verifica filtro correto
        motor_collection_mock.find_one.assert_awaited_once_with({"_id": funcionario_id})

    @pytest.mark.asyncio
    async def test_update_chama_update_one_com_filtro_e_doc_corretos(self, motor_collection_mock):
        """
        ✅ HAPPY PATH: Deve chamar `update_one` com filtro e documento de atualização corretos.
        """
        # ARRANGE
        repo = FuncionarioRepository(motor_collection=motor_collection_mock)
        funcionario_id = "123e4567-e89b-12d3-a456-426614174000"
        update_payload = {"email": "novo@email.com"}
        expected_update_doc = {"$set": update_payload}
        
        # ACT
        await repo.update(funcionario_id, update_payload)
        
        # ASSERT - Verifica parâmetros do MongoDB
        motor_collection_mock.update_one.assert_awaited_once_with(
            {"_id": funcionario_id}, 
            expected_update_doc
        )

    @pytest.mark.asyncio
    async def test_delete_chama_delete_one_com_filtro_correto(self, motor_collection_mock):
        """
        ✅ HAPPY PATH: Deve chamar `delete_one` com o filtro "_id" correto.
        """
        # ARRANGE
        repo = FuncionarioRepository(motor_collection=motor_collection_mock)
        funcionario_id = "123e4567-e89b-12d3-a456-426614174000"
        
        # ACT
        await repo.delete(funcionario_id)
        
        # ASSERT
        motor_collection_mock.delete_one.assert_awaited_once_with({"_id": funcionario_id})
```

### 🌐 Presentation Layer - `tests/unit/presentation/test_funcionario_router.py`
> **Foco: FastAPI com dependências mockadas via dependency_overrides**

```python

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app  # (inferido: assumindo que o router está montado aqui)
from app.presentation.routers.funcionario import router  # (inferido)
from app.application.exceptions import FuncionarioNaoEncontradoError  # (inferido)
from mocks import FuncionarioUseCaseMock
from factories import create_valid_funcionario, create_valid_create_payload

# TestClient configurado, mas com dependências TOTALMENTE mockadas
client = TestClient(app)

class TestFuncionarioRouter:
    """
    🧪 Testes para a camada de apresentação
    ⚠️ IMPORTANTE: Usar dependency_overrides para substituir casos de uso
    ❌ NUNCA fazer requisições que cheguem ao banco real
    """

    def test_create_funcionario_retorna_201_com_sucesso(self):
        """✅ HAPPY PATH: Deve retornar 201 ao criar funcionário com sucesso."""
        # ARRANGE
        novo_funcionario = create_valid_funcionario()
        mock_use_case = FuncionarioUseCaseMock(novo_funcionario)
        
        # 🎭 CRÍTICO: Substitui dependência real pelo mock
        app.dependency_overrides[router.create_funcionario] = lambda: mock_use_case
        
        payload = create_valid_create_payload()
        
        # ACT
        response = client.post("/funcionarios", json=payload.model_dump())
        
        # ASSERT
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["id"] == novo_funcionario.id

    def test_create_funcionario_com_payload_invalido_retorna_422(self):
        """
        ❌ Cenário TRISTE: Deve retornar 422 (Unprocessable Entity) com payload inválido.
        """
        # ARRANGE
        invalid_payload = {"nome": 123}  # Nome não é string - erro de validação Pydantic
        
        # ACT
        response = client.post("/funcionarios", json=invalid_payload)
        
        # ASSERT
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_funcionario_nao_encontrado_retorna_404(self):
        """
        ❌ Cenário TRISTE: Deve retornar 404 quando funcionário não é encontrado.
        """
        # ARRANGE
        mock_use_case = FuncionarioUseCaseMock()  # Mock sem funcionário
        app.dependency_overrides[router.get_funcionario] = lambda: mock_use_case
        
        # ACT
        response = client.get("/funcionarios/id_que_nao_existe")
        
        # ASSERT
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Funcionário não encontrado."
```

---

## ✅ Resumo e Próximos Passos

### 📊 Cobertura Implementada
- ✅ **Configurações**: pytest.ini, .coveragerc, conftest.py
- ✅ **Suporte**: factories.py, mocks.py  
- ✅ **Domain**: Testes de entidades e validações
- ✅ **Application**: Casos de uso com repositórios mockados
- ✅ **Infrastructure**: Repositórios com AsyncMock para Motor
- ✅ **Presentation**: Routers com dependency_overrides

### 🚨 Lembretes Críticos
- ❌ **NUNCA** conectar com MongoDB real nos testes
- ❌ **NUNCA** subir Uvicorn ou Docker durante testes
- ✅ **SEMPRE** usar AsyncMock para métodos assíncronos
- ✅ **SEMPRE** mockar repositórios na camada de aplicação
- ✅ **SEMPRE** usar dependency_overrides na camada de apresentação

### 🎯 Execução
```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio pytest-mock pytest-cov

# Executar testes
pytest tests/unit/ -v --cov=app

# Verificar cobertura
pytest tests/unit/ --cov=app --cov-report=html
```

### 📝 Próximos Passos
1. **Copie o conteúdo** para os arquivos correspondentes
2. **Execute pytest** para validar implementação
3. **Ajuste imports** conforme estrutura real do projeto
4. **Adicione mais cenários** baseados no `CONTEXT_MAP.md`
5. **Mantenha cobertura** acima de 80% com testes unitários

> **💡 Lembre-se:** Testes unitários devem ser **rápidos**, **isolados** e **determinísticos**. Use mocks para tudo que envolva I/O!
