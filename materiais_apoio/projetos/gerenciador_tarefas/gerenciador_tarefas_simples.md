# Desafio de Implementação: Gerenciador de Tarefas Simples

---

### 1. Contexto do Negócio

A equipe de desenvolvimento de software precisa de uma ferramenta interna e rápida para gerenciar tarefas diárias. O objetivo é criar uma solução simples que permita aos membros da equipe adicionar, visualizar e marcar tarefas como concluídas, sem a necessidade de um sistema complexo ou banco de dados.

O foco principal desta especificação é a **demonstração em sala de aula do uso do Copilot** para auxiliar na codificação, desde a estrutura básica até a implementação da lógica e da interface visual. O código deve ser intuitivo, bem comentado e refletir as boas práticas de programação.

---

### 2. Problema a ser Resolvido

Desenvolver um aplicativo que:

- Permita a **criação de novas tarefas**, com um campo para o nome da tarefa.
- Exiba uma **lista de todas as tarefas** criadas.
- Ofereça uma maneira de **marcar tarefas como concluídas**, alterando visualmente seu status.

---

### 3. Requisitos de Implementação

#### 3.1. Linguagem de Programação

- **Python** (versão 3.8 ou superior).

#### 3.2. Estrutura do Projeto

O projeto deve ser organizado em um único arquivo chamado `app.py`. A interface visual e a lógica de negócio devem coexistir neste arquivo, facilitando a demonstração.

#### 3.3. Tecnologias

- **Interface Gráfica (GUI):** A interface deve ser implementada usando a biblioteca **Streamlit**. O Streamlit é uma excelente escolha por sua simplicidade e facilidade de uso, o que permite focar na lógica do problema, e não na complexidade da interface.

#### 3.4. Funcionalidades Detalhadas

- **Adicionar Tarefa:** Deve haver um campo de texto (`st.text_input`) e um botão (`st.button`). Ao clicar no botão, a tarefa digitada deve ser adicionada a uma lista.
- **Listar Tarefas:** A lista de tarefas deve ser exibida de forma clara. Cada item da lista deve ser uma tarefa.
- **Marcar como Concluída:** Cada tarefa na lista deve ter uma caixa de seleção (`st.checkbox`). Quando a caixa é marcada, o status da tarefa deve ser atualizado para "concluída".

#### 3.5. Mock-up da Interface

A interface deve ser simples e ter a seguinte estrutura:

1.  Um título principal: "Gerenciador de Tarefas" (`st.title`).
2.  Uma seção para adicionar tarefas, com um campo de texto e um botão.
3.  Uma seção para listar as tarefas, mostrando o nome e um checkbox para cada uma.

---

### 4. Entregas

O projeto final deve consistir em um único arquivo `app.py` que, quando executado, inicie o aplicativo Streamlit.

O código deve incluir comentários para guiar a demonstração, explicando o que cada parte faz e como o Copilot pode ajudar a acelerar o processo.

---

### 5. Como Executar

Para executar o projeto, siga estes passos:

1.  Instale o Streamlit: `pip install streamlit`.
2.  Execute o arquivo `app.py` a partir do terminal: `streamlit run app.py`.