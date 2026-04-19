# Lab 1 — Configurando o primeiro MCP Server no VS Code

**Servidor:** `@modelcontextprotocol/server-filesystem`   
**Pré-requisitos:** VS Code, extensão GitHub Copilot, Node.js 18+

---

## Objetivo

Configurar o primeiro servidor MCP no VS Code usando o servidor oficial de filesystem da Anthropic. Ao final, o Copilot estará listando, lendo e criando arquivos na sua máquina diretamente pelo chat — tudo com permissão explícita antes de cada ação.

---

## Por que este servidor?

- É oficial e mantido pela Anthropic
- Roda 100% local — nenhuma conta externa, nenhum token, nenhuma dependência de rede
- O resultado é imediato e visualmente claro: você vê os arquivos sendo criados/lidos na sua própria máquina
- Demonstra o modelo de confiança do MCP: o Copilot **sempre pede confirmação** antes de escrever ou modificar arquivos

---

## Passo 1 — Verificar pré-requisitos

Abra o terminal integrado do VS Code (`Ctrl + '`) e verifique:

```bash
node --version   # deve ser >= 18
npm --version    # deve aparecer uma versão válida
```

Se Node.js não estiver instalado, baixe em [nodejs.org](https://nodejs.org) (versão LTS).

---

## Passo 2 — Criar a pasta de trabalho do lab

Crie uma pasta dedicada para este laboratório. O servidor de filesystem só terá acesso às pastas que você liberar explicitamente na configuração.

```bash
# bash / zsh (Linux e macOS)
mkdir -p ~/labs-mcp/lab1-workspace
```

```powershell
# PowerShell (Windows)
New-Item -ItemType Directory -Force -Path "$HOME\labs-mcp\lab1-workspace"
```

> **Dica de segurança:** o servidor filesystem opera como um sandbox — ele só enxerga as pastas listadas na configuração. Nunca libere a raiz do sistema (`/` ou `C:\`).

---

## Passo 3 — Configurar o servidor MCP no VS Code

Você tem duas formas de configurar. Escolha a que preferir:

### Opção A — Arquivo `.vscode/mcp.json` (recomendada para projetos)

Na raiz do projeto que você abriu no VS Code, crie o arquivo `.vscode/mcp.json` com o conteúdo abaixo.  
**Substitua o caminho pela pasta que você criou no Passo 2.**

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/SEU_USUARIO/labs-mcp/lab1-workspace"
      ]
    }
  }
}
```

> No Windows, use o formato: `"C:\\Users\\SEU_USUARIO\\labs-mcp\\lab1-workspace"`

### Opção B — Settings do usuário (`settings.json`)

Abra a paleta de comandos (`Ctrl+Shift+P`) → **"Open User Settings (JSON)"** e adicione:

```json
"github.copilot.chat.mcp.servers": {
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "/Users/SEU_USUARIO/labs-mcp/lab1-workspace"
    ]
  }
}
```

---

## Passo 4 — Ativar o Agent Mode no Copilot Chat

1. Abra o **Copilot Chat** (`Ctrl+Alt+I` ou clique no ícone do Copilot na barra lateral)
2. No seletor de modo (canto inferior do chat), troque de **"Ask"** para **"Agent"**
3. Clique no ícone de **ferramentas** (🔧) ao lado do campo de texto para confirmar que o servidor `filesystem` aparece na lista de ferramentas disponíveis

> Se o servidor não aparecer, recarregue o VS Code (`Ctrl+Shift+P` → "Developer: Reload Window").

---

## Passo 5 — Exercícios guiados

Com o Agent Mode ativo, execute cada prompt abaixo no Copilot Chat e observe o comportamento:

### Exercício 5.1 — Listar arquivos

```
Liste os arquivos e pastas que existem na minha pasta de trabalho do lab.
```

**O que observar:** o Copilot vai invocar a tool `list_directory`. Você verá uma caixa de confirmação mostrando exatamente qual ferramenta está sendo chamada e com quais parâmetros. Aprove para continuar.

---

### Exercício 5.2 — Criar um arquivo

```
Crie um arquivo chamado "produtos.txt" na pasta de trabalho com uma lista de 5 produtos fictícios, cada um com nome e preço.
```

**O que observar:** o Copilot vai invocar `write_file`. Antes de escrever, ele exibe o conteúdo que vai gravar e pede sua aprovação. Este é o **modelo de confiança MCP** em ação — o modelo propõe, você decide.

---

### Exercício 5.3 — Ler o arquivo criado

```
Leia o arquivo produtos.txt e me diga qual é o produto mais caro.
```

**O que observar:** o Copilot invoca `read_file`, recebe o conteúdo real do arquivo e usa esse conteúdo como contexto para responder. Ele não "adivinhou" — ele leu.

---

### Exercício 5.4 — Criar estrutura de pastas

```
Crie a seguinte estrutura de pastas dentro da minha pasta de trabalho:
- src/
- src/models/
- src/controllers/
- tests/
E crie um arquivo README.md na raiz com uma descrição básica do projeto.
```

**O que observar:** o Copilot vai encadear múltiplas chamadas de tool (`create_directory`, `write_file`) de forma autônoma, pedindo sua confirmação a cada passo relevante.

---

## Passo 6 — Reflexão

Ao final do lab, observe:

- O Copilot **nunca executou** uma ação sem mostrar o que ia fazer primeiro
- Cada chamada de tool foi **transparente**: você viu o nome da tool, os argumentos e o resultado
- O servidor rodou **totalmente local** — nenhum dado saiu da sua máquina

Isso é o MCP funcionando: o modelo age no mundo real, mas dentro de um modelo de confiança claro e auditável.

---

## Solução de problemas

| Problema | Solução |
|---|---|
| Servidor não aparece na lista de ferramentas | Recarregue o VS Code: `Ctrl+Shift+P` → "Developer: Reload Window" |
| Erro `npx: command not found` | Instale o Node.js e reinicie o terminal |
| Permissão negada ao criar arquivo | Verifique se o caminho configurado existe e você tem permissão de escrita |
| Agent Mode não disponível | Verifique se a extensão GitHub Copilot Chat está atualizada |

---

## Próximo lab

[Lab 2 →](./lab2_github.md) — MCP do GitHub: listar issues, PRs e interagir com repositórios sem sair do VS Code.
