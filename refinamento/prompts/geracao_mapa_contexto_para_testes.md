# Prompt para gerar CONTEXT_MAP.md (mapa de contexto e guia de testes)

## Instrução Geral
Você é um Engenheiro de Software Sênior responsável por criar um mapa de contexto do repositório ms-cadastro-funcionario em formato Markdown.  
Seu output deve ser um único arquivo chamado CONTEXT_MAP.md (no diretório raiz ou em /docs) que servirá como guia para criação de testes unitários.

## Objetivo do arquivo
- Mapear camadas e limites (domain, application, infrastructure, presentation, shared).
- Listar assinaturas públicas de classes, funções, routers e middlewares (nome, parâmetros com tipos, retorno, exceções relevantes e efeitos colaterais).
- Descrever fluxos principais (CRUD de Funcionário), dependências externas (Mongo/Motor, Pydantic, FastAPI), variáveis de ambiente e índices/coleções.
- Propor um plano de testes unitários por arquivo/módulo, incluindo mocks/fixtures necessários.

## Escopo (inclua)
- Diretórios: app/ (domain, application, infrastructure, presentation, shared), scripts/, tests/ (se existir), debug_routes.py, config.py, main.py, docker-compose*.yml, Dockerfile, .env.example.
- Ignore: __pycache__/, .pytest_cache/, venv/, logs/ (exceto mencionar diretório), binários gerados.

## Definição de “assinatura”
Para cada elemento público, documente:

- Função/Método: nome(parâmetro: tipo = default, ... ) -> tipo_retorno + “Raises: …” + “Side effects: … (ex.: I/O, DB, rede)"
- Classe: propósito, atributos públicos, métodos públicos (assinaturas).
- Router/Endpoint: HTTP {método} {caminho} -> handler + modelos de request/response (Pydantic) + principais status codes.
- Repositório/DAO: interface (métodos) + coleções e índices usados.
- Middleware/Dep: o que injeta/intercepta.
- Se faltarem type hints, inferir pelo uso e marcar como (inferido).

## Formato do Markdown (siga fielmente)

Context Map – ms-cadastro-funcionario  
Data de geração: YYYY-MM-DD

Versão do documento: 1.0

### 1. Visão Geral do Projeto
- Stack: FastAPI (async), Pydantic, Motor/MongoDB, Python 3.x
- Estrutura em camadas: breve descrição de domain/, application/, infrastructure/, presentation/, shared/.
- Entrypoints: app/main.py, debug_routes.py
- Execução: comandos (uvicorn, docker-compose) encontrados.
- Variáveis de ambiente (a partir de .env.example): tabela com NOME, DESCRIÇÃO, EXEMPLO/DEFAULT, USO (arquivo/módulo que lê).

Tabela de variáveis (exemplo de cabeçalho):
| NOME | DESCRIÇÃO | EXEMPLO/DEFAULT | USO (arquivo/módulo que lê) |
|------|-----------|------------------|------------------------------|

### 2. Mapa por Camada e Arquivo
Para cada arquivo importante, use o bloco abaixo.

#### 2.x Caminho do arquivo (ex.: app/domain/funcionario.py)
- Papel: (Entidade/VO/Exceção/Caso de uso/Router/Repo/Middleware/Util)
- Dependências-chaves: (internas e externas)
- Assinaturas públicas:
  - Classe|Função: assinatura completa
  - Raises: …
  - Side effects: …
- Usado por: (módulos chamadores diretos, se identificável)
- Observações de domínio/regra: bullets curtos

Repita para todos os arquivos de domain, application, infrastructure, presentation, shared, config.py, main.py, debug_routes.py, scripts/ relevantes.

### 3. HTTP API (Swagger snapshot)
Liste todas as rotas detectadas, por exemplo:
- GET /health → presentation/... handler; Response: …; Status: 200/…
- POST /funcionarios → handler; Request model: …; Response model: …; Status: 201/400/422
- GET /funcionarios/{id} …
- GET /funcionarios (paginação/filtros) …
- PUT /funcionarios/{id} …
- DELETE /funcionarios/{id} …

Para cada rota, inclua:
- Dependências FastAPI (Depends), middlewares aplicáveis, headers esperados (ex.: X-Request-ID), e mensagens de erro padrão.

### 4. Persistência (MongoDB/Motor)
- Conexão: onde é criada/fechada; estratégia de lifecycle.
- Banco/Coleções: nomes das coleções usadas (ex.: funcionarios).
- Índices: únicos/compostos/TTL com campos e justificativa (ex.: email único).
- Mapeamento: modelo → documento (campos obrigatórios/opcionais, normalização).

### 5. Observabilidade e Erros
- Logs: formatação (request-id, latency), níveis, onde é configurado.
- Tratamento de exceções: exception handlers globais; mapeamento domínio → HTTP status.

### 6. Plano de Testes Unitários (por arquivo)
Para cada arquivo mapeado, crie uma subseção com:
- O que testar (unidade): lista objetiva (método X valida Y; VO de Email rejeita Z; repo traduz exceção do Motor etc.).
- Cenários felizes/tristes (mín. 3 por unidade).
- Mocks necessários: Motor/Mongo (cliente/collection), relógio/UUID, variáveis de ambiente, logger.
- Fixtures sugeridas: event_loop, client (httpx.AsyncClient), mongo_mock (ex.: mongomock ou pytest-asyncio + patchs).
- Dados de exemplo: payloads JSON pequenos para criar/atualizar Funcionário.
- Cobertura alvo: % recomendado.