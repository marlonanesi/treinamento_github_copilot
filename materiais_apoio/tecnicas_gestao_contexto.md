# Técnicas práticas de gestão de contexto no GitHub Copilot

Por que gerir contexto? Modelos têm uma “janela de contexto” limitada e geram melhores respostas quando recebem objetivos claros, amostras pequenas e sinais fortes. Menos ruído, mais precisão.

## Princípios

- Foco: passe apenas o necessário para a etapa atual.
- Granularidade: trabalhe em partes pequenas e verificáveis.
- Contratos: explicite entradas, saídas, invariantes e critérios de aceitação.
- Evidência: forneça trechos/regras concretas (não apenas descrições vagas).
- Iteração: refine com deltas (mudanças específicas), não reinvente tudo a cada rodada.

---

## 1) Decomponha atividades complexas em passos modulares

Objetivo: reduzir a ambiguidade e orientar o Copilot com “micro-briefings”.

Passos
1. Descreva o objetivo final em 1–2 frases.
2. Liste subtarefas atômicas (idealmente 10–30 min cada).
3. Defina um contrato simples para cada subtarefa (inputs/outputs/erros/testes).
4. Alimente o Copilot com o contrato + trechos relevantes + pedido específico.

Template de contrato
- Inputs: …
- Outputs: …
- Regras/invariantes: …
- Testes mínimos: …

Prompt exemplo
```
Contexto: Quero implementar a validação de CPF na camada de domínio.
Contrato:
- Input: string cpf
- Output: bool válido, lista de erros
- Regras: remover máscara; checar dígitos verificadores; rejeitar sequências repetidas
- Testes: happy path, CPF inválido, nulo/vazio
Arquivos relevantes: app/domain/…/validators.py
Tarefa: gere apenas a função validar_cpf e 3 testes minimalistas.
```

---

## 2) Contexto mínimo viável + bons prompts

Passe somente:
- Objetivo e definição de pronto (DoD/aceitação)
- Assinaturas/Interfaces/Modelos que a mudança toca
- Regras de negócio essenciais
- 1–2 trechos de código de referência (máximo necessário)

Checklist do prompt
- O que fazer? (verbo claro e escopo)
- Onde? (arquivos/locais)
- Como validar? (testes/linters)
- Restrições? (compatibilidade, estilo, performance)

Mini-templates
- Implementação: “Implemente X em Y, mantendo Z. Entregue apenas o diff mental e os pontos de atenção.”
- Correção: “Investigue falha A. Diga hipótese, experimento, fix e teste.”
- Refatoração: “Refatore para extrair função/serviço. Não mude contrato público. Liste riscos.”

---

## 3) Crie um Mapa de Contexto do repositório (índice de trabalho)

Ideia: produzir um índice leve com módulos, arquivos-chave, modelos, endpoints, eventos e dependências. Use-o como referência em prompts seguintes.

Como gerar (com o próprio Copilot Chat)
1. “Liste as pastas principais e seus propósitos.”
2. “Para cada módulo, extraia arquivos-chave, classes/funções públicas e dependências externas.”
3. “Resuma em YAML/Markdown compacto.”

Template (YAML)
```yaml
modules:
	- name: app/domain/funcionarios
		purpose: regras de negócio de Funcionário
		key_files:
			- validators.py
			- models.py
			- services/atualizar_funcionario.py
		public_api:
			- class Funcionario
			- def validar_cpf(cpf: str) -> bool
		external:
			- lib: pydantic
		invariants:
			- CPF deve ser válido antes de persistir
```

Dica no seu repo: mantenha e evolua `docs/CONTEXT_MAP.md` (já existe em `ms-cadastro-funcionario/docs/CONTEXT_MAP.md`). Ao iniciar uma tarefa, cole o trecho relevante do mapa no prompt para ancorar o Copilot.

---

## 4) Resuma arquivos longos em “fichas” reutilizáveis

Use resumos estruturados para reduzir tokens.

Template de resumo
- Propósito do arquivo
- Principais símbolos (classes/funções) e contratos
- Dependências externas/side effects (I/O, rede, DB)
- Invariantes e validações
- Riscos conhecidos/edge cases

Prompt para gerar a ficha
```
Gere um resumo estruturado do arquivo X com: propósito, símbolos públicos e assinaturas,
dependências externas, invariantes principais e edge cases. Seja conciso.
```

---

## 5) Use testes e critérios de aceitação como âncoras

- Escreva 1–2 testes mínimos ou requisitos minimos de aceite antes da implementação. Peça ao Copilot para fazer a implementação passar neles.
- Em bugs, forneça stack trace, trecho mínimo que reproduz e o comportamento esperado.

Prompt
```
Aqui estão 2 testes ou requisitos mínimos que devem passar. Não altere os testes. Faça a implementação mínima
para passar. Explique as invariantes que você adotou.
```

---

## 6) Itere com “delta prompts” (mude só o necessário)

Delta prompts são pedidos incrementais que descrevem apenas o delta (as mudanças específicas) sobre um código já existente — pense em “aplicar um patch/diff”, não “reescrever o arquivo”.

- Evite recomeçar do zero: peça ajustes incrementais.
- Modele o pedido como patch lógico: “adicione parâmetro”, “extraia função”, “troque estratégia X por Y”.
- Benefícios: menos uso de contexto, menor risco de regressão e maior controle sobre o resultado.

Prompt
```
Não reescreva tudo. Aplique APENAS:
- extraia função validar_documento()
- injete o repositório via construtor
- atualize o teste A para cobrir erro de permissão
Liste riscos/regressões.
```

---

## 7) Ferramentas do editor para limitar o contexto prático

- Chat sobre uma seleção: selecione o trecho e acione o chat/inline chat para focar no bloco.
- Anexar/colar apenas o que importa: evite colar arquivos inteiros.
- Pesquisar no workspace e levar só o trecho da definição/uso relevante.
- Ambientes remotos (WSL/containers/SSH): garanta que o Copilot esteja habilitado “no lado remoto”.

---

## 8) Trabalhando em equipes/monorepos

- Padronize contratos (inputs/outputs/erros) e estilo.
- Mantenha um CONTEXT_MAP.md por pacote/módulo.
- Tenha READMEs curtos por pasta com propósito e pontos de extensão.
- Use labels nos PRs (“scope:domínio”, “tipo:bug/refactor/feat”) e links para os resumos/fichas.

---

## Anti‑padrões (evite)

- Pedir “faça tudo”: grande demais, gera ruído.
- Colar arquivos enormes sem recorte: estoura o contexto e confunde.
- Prompt vago: sem objetivo, local e critério de pronto.
- Ignorar testes e linters: sem feedback objetivo, piora a qualidade.

---

## Exemplos rápidos de prompts

1) Leitura guiada de módulo
```
Explique este módulo em 7 bullets: propósito, APIs públicas, dependências externas,
invariantes, principais fluxos, principais erros, TODOs implícitos. Sugira 2 testes.
```

2) Implementação orientada a contrato
```
Objetivo: criar endpoint POST /funcionarios.
Contrato: input JSON {nome, cpf}, validações de CPF e unicidade, output 201 {id}.
Arquivos: presentation/funcionario_controller.py, domain/validators.py.
Tarefa: gere somente o handler + validação + teste de integração mínimo.
```

3) Refatoração incremental
```
Refatore para separar validação de persistência. Extraia serviço de domínio.
Não mude contratos públicos. Indique riscos e migração de testes.
```

---

## Checklist de execução

- Objetivo e DoD definidos em 1–2 frases
- Subtarefas listadas (10–30 min cada) e contratos por subtarefa
- Mapa de contexto atualizado e colado no prompt (trecho relevante)
- Trechos mínimos de código anexados (somente o necessário)
- Testes/aceitação preparados (ao menos 1 feliz + 1 erro)
- Pedidos incrementais (delta) a cada iteração
- Verificação final: linter, testes, riscos e regressões

---