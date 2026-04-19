# Treinamento GitHub Copilot – Repositório Oficial

Aprenda, na prática, a dominar o GitHub Copilot e acelerar seu fluxo de trabalho com exercícios guiados, boas práticas de prompting e um projeto real construído do zero. 🚀

![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Seu%20par%20de%20programa%C3%A7%C3%A3o-0C8FFF?logo=githubcopilot&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-Ready-007ACC?logo=visual-studio-code&logoColor=white)
![Udemy](https://img.shields.io/badge/Udemy-Curso%20Oficial-A435F0?logo=udemy&logoColor=white)

Conteúdo prático com um microserviço real e arquitetura limpa:

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![DDD](https://img.shields.io/badge/Architecture-DDD-orange)

• Curso na Udemy: https://www.udemy.com/course/curso-github-copilot/?referralCode=43974AB5FC936615A576  
• Promoções e descontos do instrutor: https://cloudforall.com.br

## 📦 O que você encontra aqui

- aulas/ – Slides e materiais de apresentação (HTML) organizados por tópicos: LLMs, contexto, técnicas de prompt e construção modular.
- materiais_apoio/ – Guias práticos (instalação do Copilot, tour da interface, gestão de contexto) e projetos de exemplo.
- refinamento/ – Tarefas incrementais (task_1 a task_10), histórias e prompts para evolução orientada.
- ms-cadastro-funcionario/ – Microserviço completo (FastAPI + MongoDB + Docker) com arquitetura limpa, do design à execução.
- guia_labs_mcp/ – Labs práticos do módulo de MCP (Model Context Protocol): filesystem, GitHub, fetch e SQLite.

## ✅ Atividades principais do curso

- Instalação, configuração e uso eficiente do GitHub Copilot no VS Code.
- Técnicas de prompting (comando + contexto), múltiplas personas e construção modular.
- Prática guiada com tarefas de refinamento para transformar ideias em software.
- Desenvolvimento de um microserviço real com endpoints, validações e documentação.
- Execução com Docker Compose, organização de dependências e boas práticas.
- Integração com servidores MCP (filesystem, GitHub, fetch, SQLite) usando o Copilot em Agent Mode.

## ⭐ Destaque do projeto: Microserviço de Cadastro de Funcionários

- Stack: FastAPI (Python), MongoDB (Motor), Uvicorn, Docker Compose.
- Recursos: CRUD de funcionários, validações, health check e docs automáticas (Swagger/ReDoc).
- Guia completo: veja `ms-cadastro-funcionario/README.md`.

## 🔌 Módulo MCP — Model Context Protocol

O módulo de MCP ensina a conectar o GitHub Copilot (Agent Mode) a ferramentas externas reais via servidores MCP. São 4 labs progressivos:

| Lab | Servidor | O que você aprende |
|-----|----------|--------------------|
| Lab 1 | `filesystem` | Ler e escrever arquivos no sistema via agente |
| Lab 2 | `github` | Buscar repositórios, criar issues e comentários pelo Copilot |
| Lab 3 | `fetch` | Consultar páginas web e APIs externas diretamente no chat |
| Lab 4 | `sqlite` | Explorar schema, consultar e inserir dados em banco real |

- Guia completo com pré-requisitos e passo a passo: `guia_labs_mcp/`
- Pré-requisitos: `guia_labs_mcp/requisitos.md`

## ▶️ Como começar

1) Abra este repositório no VS Code.  
2) Explore as pastas na ordem: `aulas/` → `materiais_apoio/` → `refinamento/`.  
3) Ao chegar no projeto prático, siga `ms-cadastro-funcionario/README.md` para subir a API.  
4) Para o módulo de MCP, comece por `guia_labs_mcp/requisitos.md` e execute os labs em sequência.

Dica: mantenha o Copilot ativo e use o Chat para explicar trechos, gerar testes e refatorar conforme avança.

## 🔗 Links úteis

- Curso na Udemy: https://www.udemy.com/course/curso-github-copilot/?referralCode=43974AB5FC936615A576
- Promoções do instrutor: https://cloudforall.com.br
- Guia do microserviço: `ms-cadastro-funcionario/README.md`
- Guia dos Labs MCP: `guia_labs_mcp/`

Bons estudos e bons prompts! 
