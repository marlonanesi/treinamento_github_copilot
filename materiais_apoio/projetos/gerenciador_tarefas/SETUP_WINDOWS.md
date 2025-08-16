# 🚀 Instruções de Setup - Windows PowerShell

## Instalação e Execução no Windows

### Opção 1: Script Automático (Mais Fácil)

1. **Abra o PowerShell como Administrador**
2. **Execute o script de setup:**
   ```powershell
   python setup.py
   ```

### Opção 2: Script Batch (Windows)

1. **Clique duas vezes no arquivo `executar.bat`**
2. **O script irá:**
   - Verificar se Python está instalado
   - Instalar as dependências automaticamente
   - Executar a aplicação

### Opção 3: Manual (PowerShell)

1. **Abra o PowerShell na pasta do projeto:**
   ```powershell
   cd "caminho\para\gerenciador_tarefas"
   ```

2. **Instale as dependências:**
   ```powershell
   pip install streamlit
   ```

3. **Execute a aplicação:**
   ```powershell
   streamlit run app.py
   ```

### Opção 4: Com Ambiente Virtual (Recomendado)

1. **Crie um ambiente virtual:**
   ```powershell
   python -m venv venv
   ```

2. **Ative o ambiente virtual:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```powershell
   streamlit run app.py
   ```

## 🔧 Possíveis Problemas e Soluções

### Erro: "Execution of scripts is disabled"
Se aparecer erro de política de execução no PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "streamlit command not found"
1. Reinstale o streamlit:
   ```powershell
   pip uninstall streamlit
   pip install streamlit
   ```

2. Ou execute diretamente:
   ```powershell
   python -m streamlit run app.py
   ```

### Erro: "Python não encontrado"
1. Instale Python do site oficial: https://python.org
2. Certifique-se de marcar "Add to PATH" durante a instalação
3. Reinicie o PowerShell

## 🌐 Acessando a Aplicação

Após executar, a aplicação estará disponível em:
- **URL**: http://localhost:8501
- O navegador deve abrir automaticamente
- Se não abrir, copie e cole a URL no navegador

## ⏹️ Parar a Aplicação

Para parar a aplicação:
- **PowerShell**: Pressione `Ctrl + C`
- **Ou**: Feche a janela do terminal

---

**💡 Dica**: Se estiver usando um ambiente de desenvolvimento como VS Code, você pode abrir o terminal integrado e seguir as mesmas instruções.
