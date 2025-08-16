import pytest
from app import (
    EstadoTarefas,
    inicializar_session_state,
    adicionar_tarefa,
    atualizar_status_tarefa,
    obter_estatisticas
)

def test_inicializar_estado():
    estado = EstadoTarefas()
    # Remove atributos para simular ausência
    del estado.tarefas
    del estado.contador_id
    inicializar_session_state(estado)
    assert estado.tarefas == []
    assert estado.contador_id == 0

def test_adicionar_tarefa_sucesso(estado):
    ok = adicionar_tarefa("Tarefa 1", estado)
    assert ok is True
    assert estado.tarefas[0]['nome'] == "Tarefa 1"
    assert estado.tarefas[0]['concluida'] is False
    assert estado.contador_id == 1

def test_adicionar_tarefa_invalida(estado):
    ok = adicionar_tarefa("   ", estado)
    assert ok is False
    assert estado.tarefas == []
    assert estado.contador_id == 0

def test_atualizar_status_tarefa(estado):
    adicionar_tarefa("Teste", estado)
    atualizar_status_tarefa(0, True, estado)
    assert estado.tarefas[0]['concluida'] is True
    atualizar_status_tarefa(0, False, estado)
    assert estado.tarefas[0]['concluida'] is False

def test_atualizar_status_id_inexistente_nao_quebra(estado):
    adicionar_tarefa("Teste", estado)
    atualizar_status_tarefa(999, True, estado)  # não deve alterar nada
    assert estado.tarefas[0]['concluida'] is False

def test_obter_estatisticas(estado):
    adicionar_tarefa("A", estado)
    adicionar_tarefa("B", estado)
    atualizar_status_tarefa(1, True, estado)
    stats = obter_estatisticas(estado)
    assert stats == {'total': 2, 'concluidas': 1, 'pendentes': 1}

def test_ids_incrementais(estado):
    for i in range(5):
        adicionar_tarefa(f"T{i}", estado)
    assert [t['id'] for t in estado.tarefas] == list(range(5))
    stats = obter_estatisticas(estado)
    assert stats == {'total': 5, 'concluidas': 0, 'pendentes': 5}
