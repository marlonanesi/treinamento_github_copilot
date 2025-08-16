# Tour da interface do GitHub Copilot e principais comandos

Guia rápido para se orientar na interface do Copilot (VS Code) e usar os modos Ask, Edit e Agent de forma eficaz.

---

## Visão geral da interface (VS Code)

- Barra lateral “Copilot”
	- Chat: conversa geral (Ask) com histórico por workspace
	- Notebooks, Examples e Quick Actions (varia por versão)
	- Botões de limpar, exportar e copiar

- Inline Chat (Editor)
	- Abrir com Ctrl+I (Windows/Linux) ou Cmd+I (macOS)
	- Aparece sobre o arquivo atual para pedir mudanças contextuais

- Painel de Diferenças (Diff)
	- Exibe sugestões de edição lado a lado antes de aplicar
	- Aceitar tudo, aceitar por hunk, ou descartar

- Status bar
	- Indicador do Copilot (on/off, conta logada)
	- Acesso rápido às configurações

---

## Atalhos e comandos úteis

- Abrir Copilot Chat (painel lateral)
	- Command Palette: “Copilot: Open Chat View”
	- Atalho típico: Ctrl+Alt+I (Windows/Linux) | Cmd+Option+I (macOS) [pode variar]

- Abrir Inline Chat (no editor)
	- Ctrl+I (Windows/Linux) | Cmd+I (macOS)

- Aceitar sugestão inline
	- Tab (padrão) | Shift+Tab para alternativas

- Repetir pergunta/ajuste (Rerun)
	- Botão “Regenerate” no chat/inline

- Comentários estruturados para guiar sugestões
	- Comece linhas com // TODO: …, # objetivo: …, ou docstrings explicativas

---

## Modos: Ask vs Edit vs Agent

### Ask (perguntar/explicar)
Para entender, explorar, gerar snippets e pedir ajuda conceitual. Não altera arquivos automaticamente.

- Quando usar
	- Explicar um trecho, arquitetura ou erro
	- Gerar exemplo, regex, consulta SQL
	- Criar um plano de implementação/testes

- Dicas
	- Forneça contexto mínimo: objetivo, arquivo(s), linguagem
	- Cole trechos pequenos (não o arquivo todo)
	- Peça formato específico: “resuma em 5 bullets”, “mostre só o SQL”

### Edit (aplicar mudanças no código)
Para pedir alterações diretas em arquivo(s) com preview de diff antes de aplicar.

- Como acionar
	- Inline Chat no editor (Ctrl/Cmd+I)
	- Selecione um trecho e peça “Refatore…”, “Extraia função…”, “Corrija…”

- Quando usar
	- Refatorações locais, correções pontuais
	- Implementar função/endpoint com contrato definido

- Dicas
	- Selecione somente o bloco relevante para foco
	- Use “delta prompts”: descreva apenas as mudanças
	- Revise o diff por partes (hunks) antes de aceitar

### Agent (tarefas guiadas e multi-passos)
Para pedidos mais amplos, envolvendo múltiplos arquivos/etapas; o agente orquestra análises e edições com checkpoints.

- Quando usar
	- Criar uma feature com várias alterações coordenadas
	- Aplicar um padrão em vários arquivos (ex.: migrar API, padronizar logs)

- Dicas
	- Comece com um plano: objetivos, subtarefas e critérios de sucesso
	- Estabeleça limites: diretórios afetados, arquivos fora de escopo
	- Peça checkpoints e resumos a cada bloco de mudanças

---

## Exemplos de uso

- Ask
	- “Explique em 5 bullets o que faz a função validar_cpf() e liste 2 casos de borda.”
	- “Escreva uma consulta SQL para contar funcionários por departamento com salário > X.”

- Edit
	- “Extraia a função calcular_bonus() deste bloco, adicione docstring e teste unitário mínimo.”
	- “Corrija o N+1 neste repository usando prefetch/joins sem mudar a assinatura pública.”

- Agent
	- “Implemente POST /funcionarios; contratos: input {nome, cpf}, validação de CPF, output 201 {id}. Atualize controller, service e teste de integração mínimo.”
	- “Migre logs para o formato JSON estruturado em todo o projeto, mantendo níveis e campos existentes.”
---

## Boas práticas rápidas

- Diga onde mexer: cite arquivos/pastas
- Trabalhe por deltas; evite “reescrever tudo”
- Cole contratos e testes mínimos para orientar a implementação
- Confirme no diff e rode testes antes de commitar

---