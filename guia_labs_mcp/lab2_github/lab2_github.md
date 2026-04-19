# Lab 2 — MCP do GitHub: casos reais de desenvolvimento

**Servidor:** `@modelcontextprotocol/server-github`    
**Pré-requisitos:** VS Code, extensão GitHub Copilot, Node.js 18+, conta no GitHub

---

## Objetivo

Configurar o servidor MCP oficial do GitHub e usar o Copilot para interagir com repositórios, issues e pull requests em linguagem natural — sem abrir o navegador, sem usar o CLI do GitHub separadamente. Este é o **"wow moment"** do módulo MCP.

---

## Por que este servidor?

- Qualquer desenvolvedor já tem uma conta no GitHub
- O token é simples de gerar (escopo mínimo necessário)
- O impacto é imediato: o Copilot age no GitHub real, não em simulações
- Demonstra perfeitamente o ciclo MCP: pergunta natural → tool call → resultado real

---

## Passo 1 — Gerar o GitHub Personal Access Token

1. Acesse: **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Clique em **"Generate new token (classic)"**
3. Dê um nome descritivo: `mcp-lab-copilot`
4. Defina a expiração: `30 days` (suficiente para o curso)
5. Selecione os escopos mínimos necessários:
   - ✅ `repo` — acesso a repositórios (público e privado)
   - ✅ `read:org` — leitura de organizações (opcional, para repos de org)
6. Clique em **"Generate token"** e **copie o token agora** — ele não será exibido novamente

> **Segurança:** nunca commite o token em código. Este lab usa variável de ambiente para isso.

---

## Passo 2 — Configurar a variável de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com o seu token:

```bash
# bash / zsh (Linux e macOS)
cp .env.example .env
```

```powershell
# PowerShell (Windows)
Copy-Item .env.example .env
```

Edite o `.env`:

```
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_SEU_TOKEN_AQUI
```

> O arquivo `.env` está no `.gitignore` por padrão nos projetos gerados pelo Copilot. Se não estiver, adicione manualmente para não subir o token acidentalmente.

**Alternativa — variável de ambiente no sistema operacional:**

```bash
# bash / zsh (Linux e macOS) — adicione ao ~/.bashrc ou ~/.zshrc para persistir
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_SEU_TOKEN_AQUI
```

```powershell
# PowerShell (Windows) — apenas para a sessão atual
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "ghp_SEU_TOKEN_AQUI"

# PowerShell (Windows) — persistir para todas as sessões
[System.Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", "ghp_SEU_TOKEN_AQUI", "User")
```

---

## Passo 3 — Configurar o servidor MCP

O arquivo `.vscode/mcp.json` já está pronto neste lab. Ele lê o token da variável de ambiente, então nenhuma edição adicional é necessária se você configurou o `.env` ou a variável de sistema.

Abra `.vscode/mcp.json` e confirme que está assim:

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

---

## Passo 4 — Abrir no VS Code e ativar o Agent Mode

1. Abra a pasta `lab2_github` no VS Code (ou copie o `.vscode/mcp.json` para o projeto já aberto)
2. Abra o **Copilot Chat** (`Ctrl+Alt+I`)
3. Troque para o modo **"Agent"**
4. Clique no ícone de ferramentas (🔧) e confirme que `github` aparece na lista ✓

> Se o servidor não aparecer, verifique se a variável de ambiente está definida e recarregue o VS Code.

---

## Passo 5 — Exercícios guiados

Para os exercícios abaixo, substitua `DONO/REPOSITORIO` por um repositório real. Você pode usar:
- Um repositório público seu
- `microsoft/vscode` (repositório público grande, ótimo para demonstração)
- `anthropics/anthropic-cookbook` (repositório de exemplos da Anthropic)

---

### Exercício 5.1 — Listar issues abertas

```
Liste as 5 issues abertas mais recentes do repositório microsoft/vscode
e me dê um resumo de cada uma.
```

**O que observar:** o Copilot invoca a tool `list_issues` com os parâmetros `owner`, `repo` e `state`. O resultado retorna JSON estruturado com título, número, autor e data. O Copilot formata tudo em linguagem natural para você.

---

### Exercício 5.2 — Buscar issues por tema

```
Quais issues abertas no repositório microsoft/vscode mencionam "performance" no título?
```

**O que observar:** o Copilot usa a tool `search_issues` com filtros. Perceba como ele traduz sua intenção em linguagem natural para parâmetros técnicos da API do GitHub — tudo transparente no painel de ferramentas.

---

### Exercício 5.3 — Listar pull requests

```
Mostre os últimos 3 pull requests mergeados no repositório anthropics/anthropic-cookbook,
com o título e uma breve descrição do que foi alterado.
```

**O que observar:** o Copilot chama `list_pull_requests` com `state: merged`. Depois pode fazer chamadas adicionais para buscar os detalhes de cada PR.

---

### Exercício 5.4 — Detalhes de uma issue específica

```
Me dê os detalhes completos da issue #1 do repositório SEU_USUARIO/SEU_REPOSITORIO,
incluindo todos os comentários.
```

**O que observar:** o Copilot pode encadear múltiplas tools — primeiro `get_issue`, depois `list_issue_comments` — para montar uma resposta completa.

---

### Exercício 5.5 — Criar um comentário (use com cautela)

> ⚠️ **Este exercício modifica dados reais no GitHub.** Use um repositório seu de testes.

```
No repositório SEU_USUARIO/SEU_REPOSITORIO, adicione um comentário na issue #1
dizendo: "Testando o MCP do GitHub com o GitHub Copilot - Lab 2 do curso."
```

**O que observar:**
1. O Copilot exibe exatamente o comentário que vai postar e pede confirmação
2. Após aprovação, a tool `add_issue_comment` é invocada
3. Acesse o GitHub no navegador e veja o comentário criado em tempo real

Este é o **momento mais impactante do lab**: você viu o Copilot agir no GitHub sem sair do VS Code.

---

## Passo 6 — Visualizando o ciclo completo

Abra o painel de detalhes de uma tool call no Copilot Chat e observe:

```
Pergunta em linguagem natural
        ↓
Copilot decide qual tool usar
        ↓
Tool call: { "name": "list_issues", "arguments": { "owner": "...", "repo": "..." } }
        ↓
Servidor MCP chama a API do GitHub com seu token
        ↓
Resultado JSON retorna para o modelo
        ↓
Copilot formata e apresenta em linguagem natural
```

Este é o ciclo MCP completo. O modelo nunca tocou diretamente na API do GitHub — o servidor MCP fez a ponte.

---

## Solução de problemas

| Problema | Solução |
|---|---|
| Servidor `github` não aparece nas ferramentas | Verifique se a variável `GITHUB_PERSONAL_ACCESS_TOKEN` está definida no ambiente atual do VS Code |
| Erro `401 Unauthorized` | Token inválido ou expirado — gere um novo no GitHub |
| Erro `403 Forbidden` | O escopo do token não inclui a ação solicitada — verifique os escopos no Passo 1 |
| Repositório privado não acessível | Confirme que o token tem escopo `repo` (não só `public_repo`) |
| VS Code não lê o `.env` automaticamente | Use variável de ambiente no sistema operacional (Passo 2, opção alternativa) |

---

## Próximo lab

[Lab 3 →](../lab3_fetch/lab3_fetch.md) — MCP Fetch: buscar conteúdo real da web e usar no contexto do Copilot.
