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
