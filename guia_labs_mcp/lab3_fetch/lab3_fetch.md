# Lab 3 — MCP Fetch: buscando conteúdo real da web

**Servidor:** `mcp-server-fetch` (pacote Python)  
**Pré-requisitos:** VS Code, extensão GitHub Copilot, Python 3.8+

---

## Objetivo

Configurar o servidor MCP Fetch e usar o Copilot para buscar conteúdo real da web em tempo real — documentações, páginas, exemplos — e usar esse conteúdo como contexto para gerar código. Este lab demonstra de forma clara o conceito de **contexto dinâmico** versus o conhecimento estático do modelo.

---

## Por que este servidor?

- Zero configuração: nenhuma conta, nenhum token, nenhuma autenticação
- O impacto é imediato e visualmente claro
- Demonstra uma limitação real dos LLMs (knowledge cutoff) e como o MCP a resolve
- Qualquer URL pública é acessível — o aluno pode testar com qualquer documentação

---

## Passo 1 — Verificar pré-requisitos

Abra o terminal integrado do VS Code (`Ctrl + '`) e verifique:

```bash
python --version   # deve ser >= 3.8
pip --version
```

> **Atenção:** diferente dos outros labs, o servidor fetch **não é um pacote npm**. Ele é publicado no PyPI e precisa ser instalado via `pip` antes de usar.

---

## Passo 2 — Instalar o servidor MCP

Instale o pacote Python antes de configurar:

```bash
# Linux/macOS
pip install mcp-server-fetch

# Windows
pip install mcp-server-fetch
```

Valide a instalação:

```bash
python -m mcp_server_fetch --help
# Saída esperada: usage: __main__.py [-h] [--user-agent ...] ...
```

---

## Passo 3 — Configurar o servidor MCP

Atualize o arquivo `.vscode/mcp.json` com a configuração correta.

**Linux/macOS:**

```json
{
  "servers": {
    "fetch": {
      "command": "python",
      "args": ["-m", "mcp_server_fetch"]
    }
  }
}
```

**Windows** (use o caminho completo do executável Python):

```json
{
  "servers": {
    "fetch": {
      "command": "C:\\python\\312\\python.exe",
      "args": ["-m", "mcp_server_fetch"]
    }
  }
}
```

> Para descobrir o caminho do seu Python no Windows, execute `where python` no PowerShell.

> **Por que caminho completo no Windows?** O VS Code ao iniciar servidores MCP pode não herdar o PATH completo do sistema. Usar o caminho absoluto garante que o executável correto seja encontrado.

---

## Passo 4 — Ativar o Agent Mode no Copilot Chat

1. Abra a pasta `lab3_fetch` no VS Code
2. Abra o **Copilot Chat** (`Ctrl+Alt+I`)
3. Troque para o modo **"Agent"**
4. Clique no ícone de ferramentas (🔧) e confirme que `fetch` aparece na lista ✓

---

## Passo 5 — Entendendo o problema que vamos resolver

Antes dos exercícios, faça este teste rápido no modo **"Ask"** (não Agent):

```
O que é o hook useActionState do React? Mostre um exemplo de uso.
```

Observe a resposta. O modelo responde com o conhecimento que tem até a data de corte (agosto de 2025 para este modelo). A resposta pode estar desatualizada ou incompleta para versões muito recentes.

Agora troque para o modo **"Agent"** e compare os próximos exercícios.

---

## Passo 6 — Exercícios guiados

### Exercício 5.1 — Buscar documentação e gerar código

```
Acesse https://react.dev/reference/react/useActionState e me explique
o que este hook faz. Depois gere um exemplo prático de formulário
usando este hook com validação de campos.
```

**O que observar:**
1. O Copilot invoca a tool `fetch` com a URL fornecida
2. O servidor busca o conteúdo real da página em tempo real
3. O conteúdo HTML é convertido para texto e entregue ao modelo como contexto
4. O Copilot usa o conteúdo **real e atual** da documentação para gerar o código
5. O exemplo gerado reflete a API atual, não o conhecimento treinado

---

### Exercício 5.2 — Comparar comportamentos (sem vs. com MCP)

Primeiro, no modo **"Ask"** (sem MCP):
```
Quais são as novidades do Python 3.13? Liste as principais.
```

Depois, no modo **"Agent"** (com MCP):
```
Acesse https://docs.python.org/3/whatsnew/3.13.html e liste as
principais novidades do Python 3.13 com uma breve descrição de cada.
```

**O que observar:** a diferença entre o conhecimento estático do modelo e o conteúdo real e atual da documentação oficial. Esta é a demonstração mais clara do valor do MCP para contexto dinâmico.

---

### Exercício 5.3 — Gerar código a partir de documentação de uma lib

```
Acesse https://docs.pydantic.dev/latest/concepts/models/ e crie um
exemplo de modelo Pydantic para representar um Pedido de e-commerce
com: id, cliente, lista de itens (produto + quantidade + preço),
status e data de criação. Use os recursos da versão atual documentada.
```

**O que observar:** o Copilot lê a documentação atual e gera código compatível com a versão mais recente da biblioteca, incluindo features que podem não estar no seu treinamento.

---

### Exercício 5.4 — Buscar e resumir uma RFC ou especificação

```
Acesse https://modelcontextprotocol.io/introduction e me faça um
resumo executivo do que é o MCP, seus componentes principais e
casos de uso, em no máximo 10 bullets.
```

**O que observar:** o Copilot busca a spec oficial do MCP em tempo real e resume para você. Isso é útil para criar documentação, resumos técnicos ou preparar apresentações a partir de fontes primárias.

---

### Exercício 5.5 — Usar múltiplas fontes

```
Compare as abordagens de tratamento de erros em TypeScript documentadas em:
1. https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html
2. https://typescript-error-handling.netlify.app (ou outra referência pública)

Gere um guia rápido com as melhores práticas consolidadas.
```

**O que observar:** o Copilot pode fazer múltiplas chamadas de fetch para fontes diferentes e consolidar o conteúdo em uma única resposta coerente.

---

## Passo 6 — Reflexão: contexto estático vs. dinâmico

| | Sem MCP (modo Ask) | Com MCP Fetch (modo Agent) |
|---|---|---|
| **Fonte do conhecimento** | Treinamento do modelo (data de corte) | Web em tempo real |
| **Atualidade** | Limitada ao knowledge cutoff | Sempre atual |
| **Confiabilidade da API** | Pode estar desatualizada | Reflete a versão real documentada |
| **Transparência** | O modelo "sabe" — fonte opaca | Você vê a URL acessada e o conteúdo retornado |
| **Casos de uso ideais** | Conceitos estáveis, fundamentos | Docs recentes, versões novas, specs em evolução |

---

## Boas práticas ao usar o MCP Fetch

- **Prefira URLs de documentação oficial** — resultados mais confiáveis e estruturados
- **URLs públicas apenas** — o servidor não tem acesso a páginas que exigem login
- **Páginas muito pesadas** — o servidor extrai o texto principal, mas páginas com muito JavaScript dinâmico podem retornar conteúdo incompleto
- **Combine com o filesystem** — busque a doc e peça para salvar o exemplo gerado num arquivo local

---

## Solução de problemas

| Problema | Solução |
|---|---|
| Servidor `fetch` não aparece nas ferramentas | Recarregue o VS Code: `Ctrl+Shift+P` → "Developer: Reload Window" |
| Erro de timeout ao buscar URL | A página pode ser pesada — tente uma URL mais específica (âncora da seção) |
| Conteúdo retornado incompleto | A página usa JavaScript para renderizar — tente uma URL de versão `.txt` ou espelho estático |
| Erro de SSL/certificado | URL usa certificado inválido — use apenas URLs com HTTPS válido |

---

## Próximo lab

[Lab 4 →](../lab4_sqlite/lab4_sqlite.md) — MCP SQLite: consultar e analisar banco de dados com linguagem natural.
