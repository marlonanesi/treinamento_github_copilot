# Task 1 - Setup Inicial do Projeto

## Objetivo
Criar a estrutura base do projeto `ms-cadastro-funcionario` com organização de diretórios seguindo DDD simplificado e configuração inicial das dependências.

## Principais Entregas
- Estrutura de diretórios completa seguindo padrões DDD
- Arquivo `requirements.txt` com todas as dependências necessárias
- Arquivo `.env.example` com variáveis de ambiente
- Arquivo `.gitignore` configurado para Python
- Arquivo `README.md` básico do projeto
- Arquivo `main.py` como ponto de entrada da aplicação

## Critério de Pronto
- ✅ Estrutura de diretórios criada conforme especificação DDD
- ✅ Dependências listadas no requirements.txt
- ✅ Arquivos de configuração básicos criados
- ✅ Projeto pode ser inicializado sem erros

## Prompt de Execução

Como especialista em Python e arquitetura de software, crie a estrutura inicial do microserviço `ms-cadastro-funcionario` seguindo estas especificações:

**Estrutura de Diretórios (DDD Simplificado):**
```
ms-cadastro-funcionario/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Ponto de entrada FastAPI
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/              # Entidades de domínio
│   │   │   └── __init__.py
│   │   ├── repositories/          # Interfaces de repositório
│   │   │   └── __init__.py
│   │   └── exceptions/            # Exceções de domínio
│   │       └── __init__.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/              # Configurações de banco
│   │   │   └── __init__.py
│   │   ├── repositories/          # Implementações de repositório
│   │   │   └── __init__.py
│   │   └── config/                # Configurações gerais
│   │       └── __init__.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── use_cases/             # Casos de uso
│   │   │   └── __init__.py
│   │   └── services/              # Serviços de aplicação
│   │       └── __init__.py
│   ├── presentation/
│   │   ├── __init__.py
│   │   ├── api/                   # Endpoints FastAPI
│   │   │   └── __init__.py
│   │   ├── schemas/               # DTOs Pydantic
│   │   │   └── __init__.py
│   │   └── dependencies/          # Injeção de dependências
│   │       └── __init__.py
│   └── shared/
│       ├── __init__.py
│       └── utils/                 # Utilitários compartilhados
│           └── __init__.py
├── tests/                         # Estrutura para testes futuros
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   ├── integration/
│   │   └── __init__.py
│   └── fixtures/
│       └── __init__.py
├── docker/                        # Arquivos Docker
├── requirements/
│   ├── base.txt                  # Dependências base
│   ├── dev.txt                   # Dependências de desenvolvimento
│   └── prod.txt                  # Dependências de produção
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt              # Link para requirements/base.txt
```

**Dependências Principais (requirements/base.txt):**
- FastAPI (framework web)
- Pydantic (validação de dados)
- Motor (driver assíncrono MongoDB)
- Uvicorn (servidor ASGI)
- Python-dotenv (variáveis de ambiente)
- PyMongo (driver MongoDB)

**Dependências de Desenvolvimento (requirements/dev.txt):**
- Pytest e pytest-asyncio (para testes futuros)
- Black (formatação de código)
- Isort (ordenação de imports)
- Flake8 (linting)

**Configurações:**
- `.env.example` com variáveis: `MONGODB_URL`, `DATABASE_NAME`, `API_HOST`, `API_PORT`
- `.gitignore` incluindo: `__pycache__/`, `.env`, `.venv/`, `*.pyc`, `.pytest_cache/`
- `main.py` básico importando FastAPI sem implementar endpoints ainda

**Padrões a seguir:**
- Nomenclatura em snake_case para arquivos e funções
- Nomenclatura em PascalCase para classes
- Todos os diretórios devem ter `__init__.py`
- Comentários explicativos nos arquivos principais
- Documentação clara no README.md explicando o propósito e estrutura

**README.md deve conter:**
- Descrição do microserviço
- Stack tecnológica utilizada
- Estrutura do projeto
- Instruções básicas de setup (a ser expandido nas próximas tasks)

Crie todos os arquivos e diretórios conforme especificado, mantendo organização limpa e preparando a base para as próximas etapas de desenvolvimento.
