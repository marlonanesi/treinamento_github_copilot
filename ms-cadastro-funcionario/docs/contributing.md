# Guia de Contribuição

## 🎯 Como Contribuir

Agradecemos seu interesse em contribuir com o microserviço de cadastro de funcionários! Este guia vai te ajudar a entender como colaborar efetivamente com o projeto.

## 🏗️ Configuração do Ambiente

### 1. Fork e Clone

```bash
# 1. Fork o repositório no GitHub/GitLab
# 2. Clone seu fork
git clone https://github.com/seu-usuario/ms-cadastro-funcionario.git
cd ms-cadastro-funcionario

# 3. Adicione o repositório original como upstream
git remote add upstream https://github.com/empresa/ms-cadastro-funcionario.git
```

### 2. Setup Local

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Se existir

# Ou usar Docker (recomendado)
docker-compose up -d

# Verificar se tudo funciona
curl http://localhost:8000/api/v1/health
```

### 3. Configuração do Editor

**VS Code** (recomendado):
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.sortImports.provider": "isort",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

**Extensões úteis**:
- Python
- Docker
- GitLens
- REST Client
- MongoDB for VS Code

## 📋 Processo de Desenvolvimento

### Git Flow Simplificado

```bash
# 1. Sempre comece a partir da main atualizada
git checkout main
git pull upstream main

# 2. Crie uma branch para sua feature/fix
git checkout -b feature/nome-da-funcionalidade
# ou
git checkout -b bugfix/corrigir-problema

# 3. Desenvolvimento com commits pequenos
git add .
git commit -m "feat: adiciona validação de CPF"

# 4. Push da branch
git push origin feature/nome-da-funcionalidade

# 5. Abra Pull Request no GitHub/GitLab
```

### Padrão de Branches

| Tipo | Formato | Exemplo | Descrição |
|------|---------|---------|-----------|
| Feature | `feature/descricao` | `feature/validacao-cnpj` | Novas funcionalidades |
| Bug Fix | `bugfix/descricao` | `bugfix/erro-listagem` | Correções de bugs |
| Hot Fix | `hotfix/descricao` | `hotfix/falha-critica` | Correções urgentes |
| Docs | `docs/descricao` | `docs/api-examples` | Documentação apenas |
| Refactor | `refactor/descricao` | `refactor/use-cases` | Refatoração de código |

## 💬 Padrão de Commits

### Conventional Commits

Seguimos o padrão [Conventional Commits](https://conventionalcommits.org/):

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé opcional]
```

**Tipos permitidos**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de código)
- `refactor`: Refatoração
- `test`: Adição/correção de testes
- `chore`: Tarefas de manutenção

**Exemplos**:
```bash
feat: adiciona validação de CNPJ
fix: corrige erro na listagem paginada
docs: atualiza guia de instalação
refactor: melhora estrutura do repositório
test: adiciona testes para validação de email
chore: atualiza dependências do projeto
```

### Mensagens de Commit

**✅ Boas práticas**:
- Use o imperativo ("adiciona" não "adicionei")
- Primeira linha até 50 caracteres
- Seja específico e claro
- Referencie issues quando aplicável

**❌ Evite**:
```bash
git commit -m "fix"
git commit -m "alterações"
git commit -m "mudanças no código"
```

**✅ Prefira**:
```bash
git commit -m "fix: corrige validação de email único"
git commit -m "feat: adiciona filtro por data de admissão"
git commit -m "docs: documenta endpoint de relatórios"
```

## 🏗️ Padrões de Código

### Estrutura de Arquivos

Para novas funcionalidades, siga a estrutura DDD:

```
nova_funcionalidade/
├── domain/entities/nova_entidade.py       # Entidades
├── application/
│   ├── dto/nova_dto.py                   # DTOs
│   └── use_cases/nova_operacao.py        # Casos de uso
├── infrastructure/repositories/          # Implementações
│   └── nova_repository_impl.py
├── presentation/
│   ├── api/controllers/novo_controller.py # Controllers
│   └── schemas/nova_schema.py             # Schemas
```

### Convenções de Naming

```python
# Classes (PascalCase)
class FuncionarioController:
    pass

# Métodos e variáveis (snake_case)
def criar_funcionario(self):
    funcionario_id = "123"

# Constantes (UPPER_CASE)
DEFAULT_PAGE_SIZE = 10
API_VERSION = "v1"

# Arquivos (snake_case.py)
funcionario_controller.py
criar_funcionario_use_case.py
```

### Type Hints Obrigatórios

```python
from typing import Optional, List, Dict, Any
from datetime import datetime

async def criar_funcionario(
    self,
    request: CriarFuncionarioRequest
) -> FuncionarioResponse:
    """Cria um novo funcionário no sistema."""
    pass

async def buscar_por_email(
    self,
    email: str
) -> Optional[Funcionario]:
    """Busca funcionário por email."""
    pass
```

### Docstrings

Use docstrings para classes e métodos públicos:

```python
class FuncionarioService:
    """
    Serviço de negócio para gerenciamento de funcionários.
    
    Este serviço implementa as regras de negócio relacionadas
    ao cadastro, consulta e manutenção de funcionários.
    """
    
    async def criar_funcionario(
        self,
        dados: Dict[str, Any]
    ) -> Funcionario:
        """
        Cria um novo funcionário no sistema.
        
        Args:
            dados: Dicionário com os dados do funcionário
            
        Returns:
            Funcionário criado com ID atribuído
            
        Raises:
            EmailJaExisteException: Quando email já existe
            DadosInvalidosException: Quando dados estão inválidos
        """
        pass
```

## 🧪 Testes

### Estrutura de Testes (Futuro)

```
tests/
├── unit/                    # Testes unitários
│   ├── domain/             # Entidades e value objects
│   ├── application/        # Casos de uso
│   └── infrastructure/     # Repositórios
├── integration/            # Testes de integração
│   ├── api/               # Endpoints
│   └── database/          # Database tests
└── fixtures/              # Dados para testes
```

### Testes Manuais (Atual)

Por enquanto, teste manualmente suas mudanças:

```bash
# 1. Subir ambiente
docker-compose up -d

# 2. Testar health check
curl http://localhost:8000/api/v1/health

# 3. Testar funcionalidade específica
curl -X POST "http://localhost:8000/api/v1/funcionarios" \
  -H "Content-Type: application/json" \
  -d @test_data.json

# 4. Verificar logs
docker-compose logs app
```

## 📝 Pull Request

### Checklist do PR

- [ ] **Código**
  - [ ] Segue padrões de naming
  - [ ] Type hints em todas as funções
  - [ ] Docstrings em classes/métodos públicos
  - [ ] Sem código comentado/debug
  
- [ ] **Funcionalidade**
  - [ ] Funciona como esperado
  - [ ] Não quebra funcionalidades existentes
  - [ ] Tratamento de erros adequado
  - [ ] Performance considerada
  
- [ ] **Documentação**
  - [ ] README.md atualizado (se necessário)
  - [ ] Documentação da API atualizada
  - [ ] Exemplos de uso fornecidos
  
- [ ] **Git**
  - [ ] Branch criada a partir da main atualizada
  - [ ] Commits pequenos e atômicos
  - [ ] Mensagens de commit claras
  - [ ] Sem merge conflicts

### Template do PR

```markdown
## 📋 Descrição
Breve descrição do que foi implementado/corrigido.

## 🎯 Tipo de Mudança
- [ ] Bug fix (correção que resolve um problema)
- [ ] Nova funcionalidade (adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação (apenas documentação)

## 🧪 Como Testar
1. Faça checkout da branch
2. Execute `docker-compose up -d`
3. Teste o endpoint: `curl -X GET http://localhost:8000/api/v1/funcionarios`
4. Verifique se o resultado está correto

## 📸 Screenshots (se aplicável)
Cole screenshots da funcionalidade funcionando.

## ✅ Checklist
- [ ] Testei localmente
- [ ] Segue padrões do projeto
- [ ] Documentação atualizada
- [ ] Sem conflitos com main

## 📋 Issues Relacionadas
Closes #123
Related to #456
```

## 🔍 Code Review

### Como Revisor

**Pontos a verificar**:
- Arquitetura: Respeitou as camadas DDD?
- Performance: Queries eficientes? N+1 avoided?
- Segurança: Validações adequadas? Dados sensíveis protegidos?
- Manutenibilidade: Código limpo e testável?
- Padrões: Seguiu convenções do projeto?

**Feedback construtivo**:
```markdown
# ✅ Bom feedback
Sugestão: Considere usar `Optional[str]` aqui para deixar mais claro que pode ser None.

Questão: Esta query pode ser pesada com muitos registros. Que tal adicionar um índice?

Elogio: Excelente tratamento de erro! Muito claro e informativo.

# ❌ Feedback pouco útil
"Está errado"
"Mude isso"
"Não está bom"
```

### Como Autor

**Respondendo ao feedback**:
- Seja receptivo a sugestões
- Faça perguntas se não entender
- Implemente as correções rapidamente
- Marque como resolvido quando corrigir

## 🐛 Reportando Bugs

### Template de Bug Report

```markdown
## 🐛 Descrição do Bug
Descrição clara do que está acontecendo.

## 🔄 Reproduzir
Passos para reproduzir:
1. Vá para '...'
2. Clique em '....'
3. Faça scroll até '....'
4. Veja o erro

## ✅ Comportamento Esperado
O que deveria acontecer.

## 📸 Screenshots
Se aplicável, adicione screenshots.

## 🖥️ Ambiente
- OS: [ex: Ubuntu 20.04]
- Docker: [ex: 20.10.8]
- Browser: [ex: Chrome 95.0]

## 📋 Contexto Adicional
Qualquer outra informação relevante.
```

## 💡 Sugerindo Melhorias

### Template de Feature Request

```markdown
## 🚀 Feature Request

### Problema
Qual problema esta feature resolveria?

### Solução Proposta
Descrição da solução que você gostaria.

### Alternativas
Outras soluções consideradas.

### Contexto Adicional
Informações adicionais ou screenshots.
```

## 🤝 Comunidade

### Comunicação

**Channels**:
- **GitHub Issues**: Para bugs e feature requests
- **Pull Requests**: Para discussões de código
- **Slack** (se disponível): Para discussões rápidas
- **Email**: Para questões sensíveis

### Código de Conduta

**Esperamos que todos**:
- Sejam respeitosos e inclusivos
- Foquem no problema, não na pessoa
- Sejam pacientes com iniciantes
- Colaborem de forma construtiva
- Mantenham profissionalismo

## 📚 Recursos para Aprender

### FastAPI
- [Tutorial Oficial](https://fastapi.tiangolo.com/tutorial/)
- [Advanced User Guide](https://fastapi.tiangolo.com/advanced/)

### MongoDB
- [MongoDB University](https://university.mongodb.com/)
- [PyMongo Tutorial](https://pymongo.readthedocs.io/en/stable/tutorial.html)

### Python
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [PEP 8 Style Guide](https://pep8.org/)

### Arquitetura
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)

---

## 🙏 Agradecimentos

Obrigado por dedicar seu tempo para melhorar este projeto! Sua contribuição é muito valiosa para a comunidade.

**Primeira vez contribuindo?** Não se preocupe! Todo mundo começou em algum lugar. Estamos aqui para ajudar! 🚀
