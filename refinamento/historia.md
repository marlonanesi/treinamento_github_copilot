# Projeto de Cadastro de Funcionários

## Contexto da Empresa

A **TechNovaMBA Solutions** é uma empresa de tecnologia com 200 funcionários, que está migrando gradualmente seu sistema interno monolítico para uma arquitetura moderna baseada em microsserviços e APIs.

O monólito atual possui um módulo de cadastro de funcionários antigo, com baixa manutenibilidade, sem testes e com dados misturados em um banco SQL legado.

O objetivo inicial do projeto é criar um novo microserviço para gerenciar o cadastro de funcionários, que será integrado aos poucos aos outros módulos da empresa.

## Objetivo do Projeto

> "Como equipe de RH, quero cadastrar, consultar, atualizar e remover funcionários no novo sistema, para que a empresa possa substituir o módulo antigo e começar a migração para o novo modelo moderno e escalável."

## Requisitos Iniciais

### Cadastro de Funcionário

**Campos obrigatórios:**
- `nome_completo`
- `email` (único)
- `cargo`
- `data_admissao`

**Campos opcionais:**
- `telefone`
- `departamento`

⚠️ O sistema deve validar duplicidade de e-mail.

### Consulta de Funcionários

- Consultar todos ou filtrar por:
  - `departamento`
  - `cargo`

### Atualização de Funcionário

- Permitir atualização de qualquer campo, exceto `email` e `data_admissao`.

### Exclusão de Funcionário

- Somente se o funcionário não estiver marcado como ativo em projetos (fictício, por enquanto apenas um campo booleano `ativo` que impede exclusão).

### Persistência

- Banco **MongoDB** para armazenar os funcionários.

## Detalhes Adicionais

- O microserviço será containerizado com **Docker** e depois orquestrado com **Docker Compose**.