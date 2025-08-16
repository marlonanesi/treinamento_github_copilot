import pytest
from app import EstadoTarefas, inicializar_session_state, adicionar_tarefa

@pytest.fixture
def estado():
    est = EstadoTarefas()
    inicializar_session_state(est)
    return est
