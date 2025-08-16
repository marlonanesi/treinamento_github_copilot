# 📋 Gerenciador de Tarefas Simples

Um aplicativo web simples para gerenciar tarefas diárias, desenvolvido com Python e Streamlit. Este projeto foi criado para demonstrar o uso do GitHub Copilot no desenvolvimento de aplicações Python.

## ✨ Funcionalidades

- ➕ **Adicionar Tarefas**: Crie novas tarefas com facilidade
- 📝 **Visualizar Tarefas**: Liste todas as tarefas de forma organizada
- ✅ **Marcar como Concluída**: Use checkboxes para atualizar o status das tarefas
- 📊 **Estatísticas**: Visualize métricas sobre suas tarefas (total, concluídas, pendentes)
- 🔍 **Filtros**: Filtre tarefas por status (todas, pendentes, concluídas)
- 🗂️ **Ordenação**: Ordene tarefas por data ou status
- 🧹 **Limpeza**: Remova tarefas concluídas ou todas as tarefas

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem de programação principal
- **Streamlit**: Framework para criação da interface web
- **Typing**: Para type hints e melhor documentação do código

## 📋 Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes do Python)

## 🚀 Como Executar

### 1. Clone ou baixe o projeto

```bash
# Se usando git
git clone <url-do-repositorio>

# Ou baixe os arquivos diretamente
```

### 2. Navegue até o diretório do projeto

```bash
cd gerenciador_tarefas
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

**Ou instale diretamente o Streamlit:**

```bash
pip install streamlit
```

### 4. Execute a aplicação

```bash
streamlit run app.py
```

### 5. Acesse a aplicação

O Streamlit automaticamente abrirá seu navegador padrão no endereço:
- **URL Local**: http://localhost:8501

Se o navegador não abrir automaticamente, copie e cole o endereço acima na barra de endereços.

## 📁 Estrutura do Projeto

```
gerenciador_tarefas/
│
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação (este arquivo)
└── gerenciador_tarefas_simples.md  # Especificação do projeto
```

## 💡 Como Usar

1. **Adicionar uma tarefa**: Digite o nome da tarefa no campo de texto e clique em "Adicionar"
2. **Marcar como concluída**: Clique na checkbox ao lado da tarefa
3. **Filtrar tarefas**: Use o dropdown "Filtrar tarefas" para ver apenas pendentes ou concluídas
4. **Ordenar tarefas**: Use o dropdown "Ordenar por" para reorganizar a lista
5. **Limpar tarefas**: Use os botões "Limpar Concluídas" ou "Limpar Todas" conforme necessário

## 🧠 Conceitos Demonstrados

Este projeto demonstra vários conceitos importantes:

- **Session State**: Persistência de dados durante a sessão
- **Type Hints**: Documentação de tipos para melhor legibilidade
- **Docstrings**: Documentação completa de funções
- **Componentização**: Separação de responsabilidades em funções específicas
- **Interface Responsiva**: Layout que se adapta ao conteúdo
- **UX/UI**: Interface intuitiva e amigável

## 🔧 Personalização

Você pode personalizar a aplicação:

- **Cores e Tema**: Modifique os estilos CSS inline ou adicione um arquivo de estilo
- **Funcionalidades**: Adicione novas features como prioridades, categorias ou datas
- **Persistência**: Implemente salvamento em arquivo ou banco de dados
- **Validações**: Adicione validações mais robustas para entrada de dados

## 🚨 Solução de Problemas

### Erro: "Command 'streamlit' not found"
- Certifique-se de que o Streamlit está instalado: `pip install streamlit`
- Verifique se o Python e pip estão no PATH do sistema

### A aplicação não abre no navegador
- Acesse manualmente: http://localhost:8501
- Verifique se a porta 8501 não está em uso por outra aplicação

### Erro de importação do Streamlit
- Reinstale o Streamlit: `pip uninstall streamlit && pip install streamlit`
- Verifique se está usando o ambiente Python correto

## 🤝 Contribuição

Este é um projeto educacional. Sugestões de melhorias são bem-vindas!

## 📄 Licença

Este projeto é de uso educacional e está disponível para modificação e distribuição.

---

**Desenvolvido com ❤️ para demonstrar o poder do GitHub Copilot no desenvolvimento Python**
