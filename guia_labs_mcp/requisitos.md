# Requisitos — Guia de Labs MCP

Antes de iniciar qualquer lab, verifique se todos os itens abaixo estão instalados e configurados corretamente.

---

## 1. VS Code

Baixe em: https://code.visualstudio.com

```bash
# Verificar versão instalada
code --version
```

> Versão mínima recomendada: **1.90+** (suporte completo ao Agent Mode e MCP)

---

## 2. Extensão GitHub Copilot + Copilot Chat

Instale direto no VS Code:

1. Abra a aba de extensões (`Ctrl+Shift+X`)
2. Busque por **"GitHub Copilot"** e instale
3. Busque por **"GitHub Copilot Chat"** e instale
4. Faça login com sua conta GitHub quando solicitado

> Ambas as extensões são necessárias. O **Agent Mode** (usado em todos os labs) está na extensão Copilot Chat.

---

## 3. Node.js e npm/npx

Todos os servidores MCP deste guia são executados via `npx`, que vem junto com o Node.js.

Baixe em: https://nodejs.org (escolha a versão **LTS**)

```bash
# Verificar após instalação
node --version   # deve ser >= 18
npm --version
npx --version
```

> Se já tiver o Node.js instalado mas em versão antiga (< 18), atualize pelo site ou use um gerenciador como `nvm` (Linux/macOS) ou `nvm-windows`.

**Instalação via gerenciador de versões (opcional mas recomendado):**

```bash
# macOS/Linux — nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
nvm use --lts

# Windows — via winget
winget install OpenJS.NodeJS.LTS
```

---

## 4. Git

Necessário para clonar repositórios e para o Lab 2 (MCP GitHub).

Baixe em: https://git-scm.com

```bash
git --version
```

---

## 5. Python 3 (necessário para Lab 3 — Fetch e Lab 4 — SQLite)

Usado para executar o servidor MCP Fetch (Lab 3) e para criar e popular o banco de dados de exemplo (Lab 4).

Baixe em: https://python.org (versão **3.8+**)

```bash
# Linux/macOS
python3 --version

# Windows
python --version
```

> O Python já vem com o módulo `sqlite3` embutido — nenhuma instalação adicional de pacote é necessária para o Lab 4.

**Instalação rápida:**

```bash
# macOS (Homebrew)
brew install python

# Windows (winget)
winget install Python.Python.3
```

### 5.1 — Pacote mcp-server-fetch (Lab 3)

Após instalar o Python, instale o servidor MCP Fetch:

```bash
pip install mcp-server-fetch
```

Valide:

```bash
python -m mcp_server_fetch --help
# Saída esperada: usage: __main__.py [-h] [--user-agent ...] ...
```

> **Atenção (Windows):** o `mcp.json` deve usar o caminho **absoluto** do executável Python. Execute `where python` no PowerShell para descobrir o caminho e use-o na configuração do servidor.

---

## 6. SQLite CLI (opcional — Lab 4)

O CLI do SQLite permite rodar o `seed.sql` diretamente, sem precisar do Python.

```bash
sqlite3 --version
```

**Instalação:**

```bash
# macOS (Homebrew)
brew install sqlite

# Ubuntu/Debian
sudo apt install sqlite3

# Windows — baixe o executável em: https://sqlite.org/download.html
# Extraia e adicione ao PATH do sistema
```

> Se não quiser instalar o SQLite CLI, use o Python para criar o banco (instrução no roteiro do Lab 4).

---

## 7. Token do GitHub (necessário apenas no Lab 2)

O Lab 2 exige um Personal Access Token com escopo `repo`.

1. Acesse: **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Gere um token com os escopos: `repo` e `read:org`
3. Salve o token — ele só é exibido uma vez

> Guarde o token em local seguro. Nunca o commite em código. O Lab 2 mostra como usá-lo via variável de ambiente.

---

## Resumo rápido — checklist

| Requisito | Labs | Verificação rápida |
|---|---|---|
| VS Code >= 1.90 | Todos | `code --version` |
| Extensão GitHub Copilot + Chat | Todos | Verificar em Extensions |
| Node.js >= 18 + npx | Todos | `node --version` |
| Git | Lab 2 | `git --version` |
| Python 3 + pip | Labs 3 e 4 | `python3 --version` |
| SQLite CLI | Lab 4 (opcional) | `sqlite3 --version` |
| GitHub Token | Lab 2 | Gerado em github.com |

---

## Dica: validar tudo de uma vez

### bash / zsh (Linux e macOS)

```bash
echo "=== Verificando requisitos ===" && \
echo "Node:   $(node --version 2>/dev/null || echo 'NÃO ENCONTRADO')" && \
echo "npm:    $(npm --version 2>/dev/null || echo 'NÃO ENCONTRADO')" && \
echo "npx:    $(npx --version 2>/dev/null || echo 'NÃO ENCONTRADO')" && \
echo "Git:    $(git --version 2>/dev/null || echo 'NÃO ENCONTRADO')" && \
echo "Python: $(python3 --version 2>/dev/null || python --version 2>/dev/null || echo 'NÃO ENCONTRADO')" && \
echo "mcp-server-fetch: $(python3 -m mcp_server_fetch --help 2>/dev/null | head -1 || echo 'NÃO INSTALADO — rode: pip install mcp-server-fetch')" && \
echo "SQLite: $(sqlite3 --version 2>/dev/null || echo 'não instalado (opcional)')"
```

### PowerShell (Windows)

```powershell
Write-Host "=== Verificando requisitos ==="

$checks = @(
    @{ Nome = "Node";           Cmd = "node";             Args = "--version" },
    @{ Nome = "npm";            Cmd = "npm";              Args = "--version" },
    @{ Nome = "npx";            Cmd = "npx";              Args = "--version" },
    @{ Nome = "Git";            Cmd = "git";              Args = "--version" },
    @{ Nome = "Python";         Cmd = "python";           Args = "--version" },
    @{ Nome = "mcp-server-fetch"; Cmd = "python";         Args = "-m mcp_server_fetch --help" },
    @{ Nome = "SQLite";         Cmd = "sqlite3";          Args = "--version" }
)

foreach ($item in $checks) {
    $resultado = & $item.Cmd $item.Args 2>$null
    if ($resultado) { Write-Host "$($item.Nome): $resultado" }
    else            { Write-Host "$($item.Nome): NÃO ENCONTRADO" }
}
```
