# Lab 4 (Bônus) — MCP SQLite: análise de dados com linguagem natural

**Servidor:** `mcp-server-sqlite` (pacote Python)  
**Pré-requisitos:** VS Code, extensão GitHub Copilot, Python 3.10+

---

## Objetivo

Configurar o servidor MCP SQLite, criar um banco de dados de exemplo e usar o Copilot para consultar, inserir e analisar dados com linguagem natural. O modelo gera e executa o SQL automaticamente — você faz a pergunta de negócio e ele traz a resposta dos dados reais.

---

## Por que este servidor?

- Banco de dados local: nenhuma instalação de servidor, nenhum serviço externo
- O impacto visual é alto: o aluno vê SQL sendo gerado e executado em tempo real
- Demonstra que o MCP não é só para código — é para **dados também**
- Ótimo para perfis de dados, BI e análise que usam VS Code

---

## Estrutura deste lab

```
lab4_sqlite/
├── lab4_sqlite.md    ← este roteiro
└── seed.sql          ← script para criar e popular o banco de exemplo
```

---

## Passo 0 — Instalar o servidor MCP SQLite

O servidor SQLite do MCP é distribuído como pacote Python — **não existe no npm**. Instale via pip:

```powershell
pip install mcp-server-sqlite
```

---

## Configuração do servidor MCP

Crie ou edite o arquivo `.vscode/mcp.json` na raiz do projeto que você abriu no VS Code.  
**Substitua o caminho** pelo caminho real onde você vai salvar o arquivo `.db`:

```json
{
  "servers": {
    "sqlite": {
      "command": "mcp-server-sqlite",
      "args": [
        "--db-path",
        "C:\\Users\\SEU_USUARIO\\labs-mcp\\lab4-workspace\\loja.db"
      ]
    }
  }
}
```

> **macOS/Linux:** substitua o valor de `--db-path` por `/Users/SEU_USUARIO/labs-mcp/lab4-workspace/loja.db`  
> O diretório precisa existir antes de iniciar o servidor.

---

## Passo 1 — Criar a pasta de trabalho

```bash
# bash / zsh (Linux e macOS)
mkdir -p ~/labs-mcp/lab4-workspace
```

```powershell
# PowerShell (Windows)
New-Item -ItemType Directory -Force -Path "$HOME\labs-mcp\lab4-workspace"
```

---

## Passo 2 — Criar e popular o banco de dados

Use o script `seed.sql` que acompanha este lab para criar a estrutura e inserir dados de exemplo. Execute com o SQLite da sua máquina:

```bash
# bash / zsh (Linux e macOS) — com sqlite3 CLI instalado
sqlite3 ~/labs-mcp/lab4-workspace/loja.db < seed.sql
```

```bash
# bash / zsh (Linux e macOS) — alternativa com Python (sem sqlite3 CLI)
python3 -c "
import sqlite3, pathlib
db = sqlite3.connect(pathlib.Path.home() / 'labs-mcp/lab4-workspace/loja.db')
db.executescript(open('seed.sql').read())
db.commit()
print('Banco criado com sucesso!')
"
```

```powershell
# PowerShell (Windows) — com Python
python -c "
import sqlite3, pathlib
db = sqlite3.connect(str(pathlib.Path.home() / 'labs-mcp' / 'lab4-workspace' / 'loja.db'))
db.executescript(open('seed.sql').read())
db.commit()
print('Banco criado com sucesso!')
"
```

---

## Passo 3 — Configurar o servidor MCP e ativar o Agent Mode

1. Crie o `.vscode/mcp.json` conforme a seção "Configuração do servidor MCP" acima
2. Abra o **Copilot Chat** (`Ctrl+Alt+I`)
3. Troque para o modo **"Agent"**
4. Clique no ícone de ferramentas (🔧) e confirme que `sqlite` aparece na lista ✓

---

## Passo 4 — Conhecendo o banco de dados

Antes de fazer perguntas, peça ao Copilot para explorar a estrutura do banco:

```
Quais tabelas existem no banco de dados? Descreva a estrutura de cada uma.
```

**O que observar:** o Copilot invoca tools como `list_tables` e `describe_table` para descobrir o schema. Ele não "sabe" a estrutura — ele consulta o banco real.

---

## Passo 5 — Exercícios guiados

### Exercício 5.1 — Consulta simples

```
Quais são os 5 produtos mais caros do catálogo?
```

**O que observar:** o Copilot gera um `SELECT ... ORDER BY preco DESC LIMIT 5`, executa via tool `execute_query` e formata o resultado para você.

---

### Exercício 5.2 — Análise de vendas

```
Qual foi o mês com maior faturamento total? Mostre o valor em reais.
```

**O que observar:** o Copilot precisa fazer um `GROUP BY` com `SUM` e talvez um `JOIN` entre as tabelas de pedidos e itens. Observe como ele constrói a query progressivamente se não conseguir de primeira.

---

### Exercício 5.3 — Ranking de clientes

```
Quais são os 3 clientes que mais gastaram? Mostre o nome, o número de pedidos
e o total gasto por cada um.
```

**O que observar:** query mais complexa com `JOIN`, `GROUP BY`, `COUNT` e `SUM`. O Copilot gera SQL correto a partir de uma pergunta de negócio em português.

---

### Exercício 5.4 — Análise de estoque

```
Quais produtos estão com estoque abaixo de 10 unidades?
Liste por ordem de urgência (menor estoque primeiro).
```

---

### Exercício 5.5 — Inserção de dados

```
Adicione um novo produto chamado "Teclado Mecânico RGB" na categoria "Periféricos",
com preço de R$ 349,90 e estoque inicial de 25 unidades.
```

**O que observar:** o Copilot gera um `INSERT INTO`, mostra o statement antes de executar e pede confirmação. Após aprovação, o dado está no banco — você pode verificar com a query do Exercício 5.1.

---

### Exercício 5.6 — Relatório consolidado

```
Gere um relatório completo de vendas com:
1. Total de pedidos realizados
2. Faturamento total
3. Ticket médio por pedido
4. Produto mais vendido (em quantidade)
5. Categoria com maior receita
```

**O que observar:** o Copilot pode fazer múltiplas queries para montar o relatório — uma para cada métrica — e consolida tudo em uma resposta estruturada.

---

## Passo 6 — Reflexão

| O que aconteceu | O que isso significa |
|---|---|
| Você fez perguntas em português | Nenhum conhecimento de SQL foi necessário |
| O Copilot gerou e executou SQL correto | O modelo entende o schema e o contexto de negócio |
| Cada query foi visível antes de executar | Você pode aprender SQL observando o que o modelo gera |
| Os dados retornados são reais | Não é simulação — é o banco consultado em tempo real |

---

## Boas práticas

- **Sempre revise queries de UPDATE/DELETE** antes de aprovar — diferente de SELECT, essas modificam dados
- **Use backups** antes de exercícios de inserção/atualização em bancos com dados reais
- **O servidor SQLite tem permissão total** sobre o arquivo `.db` — use arquivos de teste, não bancos de produção

---

## Solução de problemas

| Problema | Solução |
|---|---|
| `npm error 404 @modelcontextprotocol/server-sqlite` | O pacote não existe no npm — use `python -m mcp_server_sqlite` conforme este roteiro |
| `No module named mcp_server_sqlite` | Execute `pip install mcp-server-sqlite` — o executável `mcp-server-sqlite.exe` será criado em `Scripts/` |
| Servidor `sqlite` não aparece nas ferramentas | Verifique o caminho do `.db` no `mcp.json` (`--db-path`) e recarregue: `Ctrl+Shift+P` → "Developer: Reload Window" |
| Banco não encontrado | Confirme que o diretório do `.db` existe e rode o `seed.sql` |
| Erro ao executar `seed.sql` com Python | Verifique se o Python 3 está instalado: `python --version` |
| Query retorna vazia | Execute o Passo 4 para confirmar que o banco foi populado corretamente |
| Erro de permissão no arquivo `.db` | Verifique se o usuário atual tem permissão de leitura/escrita no diretório |

---

## Voltar ao início

[← Lab 3](../lab3_fetch/lab3_fetch.md) | [← Lab 1](../lab1_filesystem/lab1_filesystem.md)
