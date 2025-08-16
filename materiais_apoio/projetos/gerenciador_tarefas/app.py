"""
Gerenciador de Tarefas Simples

Aplicativo desenvolvido para demonstrar o uso do GitHub Copilot
em um projeto Python com interface gráfica usando Streamlit.

Autor: Programador Python SR
Data: Agosto 2025
"""

import streamlit as st
from typing import List, Dict
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EstadoTarefas:
    """
    Contêiner simples para permitir testes unitários sem depender
    do st.session_state real do Streamlit.
    """
    tarefas: List[Dict] = field(default_factory=list)
    contador_id: int = 0


def _estado(estado: Optional[object]):
    """
    Retorna o estado passado (mock) ou o st.session_state real.
    """
    return estado if estado is not None else st.session_state


def inicializar_session_state(estado: Optional[object] = None):
    """
    Inicializa o estado (real ou simulado em testes).
    """
    est = _estado(estado)
    if not hasattr(est, 'tarefas'):
        est.tarefas = []
    if not hasattr(est, 'contador_id'):
        est.contador_id = 0


def adicionar_tarefa(nome_tarefa: str, estado: Optional[object] = None) -> bool:
    """
    Adiciona tarefa no estado fornecido ou st.session_state.
    """
    est = _estado(estado)
    if nome_tarefa.strip():
        nova_tarefa = {
            'id': est.contador_id,
            'nome': nome_tarefa.strip(),
            'concluida': False
        }
        est.tarefas.append(nova_tarefa)
        est.contador_id += 1
        return True
    return False


def atualizar_status_tarefa(tarefa_id: int, status: bool, estado: Optional[object] = None) -> None:
    """
    Atualiza status de uma tarefa no estado alvo.
    """
    est = _estado(estado)
    for tarefa in est.tarefas:
        if tarefa['id'] == tarefa_id:
            tarefa['concluida'] = status
            break


def obter_estatisticas(estado: Optional[object] = None) -> Dict[str, int]:
    """
    Calcula estatísticas a partir do estado escolhido.
    """
    est = _estado(estado)
    total = len(est.tarefas)
    concluidas = sum(1 for tarefa in est.tarefas if tarefa['concluida'])
    pendentes = total - concluidas
    
    return {
        'total': total,
        'concluidas': concluidas,
        'pendentes': pendentes
    }


def renderizar_cabecalho():
    """
    Renderiza o cabeçalho da aplicação com título e estatísticas.
    """
    st.title("📋 Gerenciador de Tarefas")
    st.markdown("---")
    
    # Exibir estatísticas
    stats = obter_estatisticas()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Tarefas", stats['total'])
    with col2:
        st.metric("Concluídas", stats['concluidas'])
    with col3:
        st.metric("Pendentes", stats['pendentes'])
    
    st.markdown("---")


def renderizar_formulario_adicionar():
    """
    Renderiza o formulário para adicionar novas tarefas.
    """
    st.subheader("➕ Adicionar Nova Tarefa")
    
    # Criar formulário
    with st.form(key="form_adicionar_tarefa", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            nome_tarefa = st.text_input(
                "Nome da Tarefa",
                placeholder="Digite o nome da tarefa...",
                help="Insira uma descrição clara da tarefa que deseja adicionar"
            )
        
        with col2:
            submit_button = st.form_submit_button("Adicionar", type="primary")
        
        # Processar envio do formulário
        if submit_button:
            if adicionar_tarefa(nome_tarefa):
                st.success(f"✅ Tarefa '{nome_tarefa}' adicionada com sucesso!")
                st.rerun()
            else:
                st.error("❌ Por favor, insira um nome válido para a tarefa.")


def renderizar_lista_tarefas():
    """
    Renderiza a lista de tarefas com checkboxes para marcar como concluídas.
    """
    st.subheader("📝 Lista de Tarefas")
    
    if not st.session_state.tarefas:
        st.info("🎯 Nenhuma tarefa cadastrada ainda. Adicione sua primeira tarefa acima!")
        return
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        filtro = st.selectbox(
            "Filtrar tarefas:",
            ["Todas", "Pendentes", "Concluídas"]
        )
    
    with col2:
        ordenar_por = st.selectbox(
            "Ordenar por:",
            ["Mais recentes", "Mais antigas", "Concluídas primeiro", "Pendentes primeiro"]
        )
    
    # Aplicar filtros
    tarefas_filtradas = list(st.session_state.tarefas)
    
    if filtro == "Pendentes":
        tarefas_filtradas = [t for t in tarefas_filtradas if not t['concluida']]
    elif filtro == "Concluídas":
        tarefas_filtradas = [t for t in tarefas_filtradas if t['concluida']]
    
    # Aplicar ordenação
    if ordenar_por == "Mais antigas":
        tarefas_filtradas.sort(key=lambda x: x['id'])
    elif ordenar_por == "Mais recentes":
        tarefas_filtradas.sort(key=lambda x: x['id'], reverse=True)
    elif ordenar_por == "Concluídas primeiro":
        tarefas_filtradas.sort(key=lambda x: x['concluida'], reverse=True)
    elif ordenar_por == "Pendentes primeiro":
        tarefas_filtradas.sort(key=lambda x: x['concluida'])
    
    # Exibir tarefas
    st.markdown("---")
    
    for tarefa in tarefas_filtradas:
        col1, col2 = st.columns([0.1, 0.9])
        
        with col1:
            # Checkbox para marcar como concluída
            status_atual = tarefa['concluida']
            novo_status = st.checkbox(
                "",
                value=status_atual,
                key=f"checkbox_{tarefa['id']}",
                help="Marque para concluir a tarefa"
            )
            
            # Atualizar status se houve mudança
            if novo_status != status_atual:
                atualizar_status_tarefa(tarefa['id'], novo_status)
                st.rerun()
        
        with col2:
            # Exibir nome da tarefa com formatação baseada no status
            if tarefa['concluida']:
                st.markdown(f"~~{tarefa['nome']}~~ ✅", unsafe_allow_html=True)
            else:
                st.markdown(f"**{tarefa['nome']}** ⏳")
        
        st.markdown("---")


def renderizar_acoes_extras():
    """
    Renderiza ações extras como limpar tarefas concluídas.
    """
    if st.session_state.tarefas:
        st.subheader("⚙️ Ações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧹 Limpar Concluídas", help="Remove todas as tarefas marcadas como concluídas"):
                tarefas_concluidas = sum(1 for t in st.session_state.tarefas if t['concluida'])
                st.session_state.tarefas = [t for t in st.session_state.tarefas if not t['concluida']]
                if tarefas_concluidas > 0:
                    st.success(f"✅ {tarefas_concluidas} tarefa(s) concluída(s) removida(s)!")
                    st.rerun()
                else:
                    st.info("ℹ️ Não há tarefas concluídas para remover.")
        
        with col2:
            if st.button("🗑️ Limpar Todas", help="Remove todas as tarefas da lista"):
                total_tarefas = len(st.session_state.tarefas)
                if total_tarefas > 0:
                    st.session_state.tarefas = []
                    st.success(f"✅ {total_tarefas} tarefa(s) removida(s)!")
                    st.rerun()
                else:
                    st.info("ℹ️ Não há tarefas para remover.")


def main():
    """
    Função principal da aplicação.
    
    Configura a página do Streamlit e renderiza todos os componentes
    da interface do usuário.
    """
    # Configuração da página
    st.set_page_config(
        page_title="Gerenciador de Tarefas",
        page_icon="📋",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Inicializar estado da sessão
    inicializar_session_state()
    
    # Renderizar componentes da interface
    renderizar_cabecalho()
    renderizar_formulario_adicionar()
    st.markdown("---")
    renderizar_lista_tarefas()
    st.markdown("---")
    renderizar_acoes_extras()
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Desenvolvido com ❤️ usando Python e Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


# Executar a aplicação
if __name__ == "__main__":
    main()
