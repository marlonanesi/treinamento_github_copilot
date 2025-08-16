# Guia SonarQube - MS Cadastro Funcionário

## 🎯 Visão Geral

O SonarQube é uma ferramenta de análise estática de código que ajuda a identificar bugs, vulnerabilidades, code smells e medir cobertura de testes.

## 🚀 Como Executar

### Opção 1: Script Automático (Recomendado)

**Windows PowerShell:**
```powershell
# Executar análise completa
.\scripts\run-sonar.ps1
```

**Linux/Mac/WSL:**
```bash
# Dar permissão e executar
chmod +x scripts/run-sonar.sh
./scripts/run-sonar.sh
```

### Opção 2: Manual

**1. Iniciar SonarQube:**
```bash
# Iniciar SonarQube e PostgreSQL
docker-compose -f docker-compose.sonar.yml up -d

# Aguardar inicialização (pode demorar 1-2 minutos)
# Verificar status
curl http://localhost:9000/api/system/status
```

**2. Executar Testes (opcional, para coverage):**
```bash
# Instalar dependências de teste
pip install pytest pytest-cov coverage

# Executar testes com coverage
python -m pytest tests/ --cov=app --cov-report=xml --cov-report=term
```

**3. Executar Análise:**
```bash
# Via Docker (sem instalar sonar-scanner)
docker run --rm \
    --network host \
    -v "$(pwd):/usr/src" \
    sonarsource/sonar-scanner-cli:latest \
    -Dsonar.projectKey=ms-cadastro-funcionario \
    -Dsonar.sources=app \
    -Dsonar.tests=tests \
    -Dsonar.host.url=http://localhost:9000 \
    -Dsonar.login=admin \
    -Dsonar.password=admin
```

## 🌐 Acessar Dashboard

Após a análise:

1. **Acesse**: http://localhost:9000
2. **Login inicial**: 
   - Username: `admin`
   - Password: `admin`
3. **Será solicitado para alterar a senha na primeira vez**
4. **Projeto**: `ms-cadastro-funcionario`

## 📊 O que o SonarQube Analisa

### 🐛 Bugs
- Erros lógicos no código
- Uso incorreto de APIs
- Problemas de concorrência
- Memory leaks potenciais

### 🔒 Vulnerabilidades
- Problemas de segurança
- Uso de funções inseguras
- Exposição de dados sensíveis
- Injeção de código

### 👃 Code Smells
- Código duplicado
- Métodos muito longos
- Classes muito complexas
- Variáveis não utilizadas
- Imports desnecessários

### 📈 Cobertura de Testes
- Linhas cobertas por testes
- Branches cobertas
- Funções testadas
- Arquivos com baixa cobertura

### 🔢 Métricas
- Linhas de código
- Densidade de comentários
- Complexidade ciclomática
- Duplicação de código

## 🎯 Quality Gates

### Quality Gate Padrão
- **Coverage**: > 80%
- **Duplicated Lines**: < 3%
- **Maintainability Rating**: A
- **Reliability Rating**: A
- **Security Rating**: A

### Configurar Quality Gate Customizado

1. Acesse **Quality Gates** no menu
2. Clique em **Create**
3. Configure métricas:
   - **Coverage**: > 85%
   - **New Coverage**: > 85%
   - **Duplicated Lines (%)**: < 3%
   - **New Duplicated Lines (%)**: < 3%
   - **Security Rating**: A
   - **Maintainability Rating**: A

## 💡 Dicas de Uso

### 1. Interpretando Resultados

**Issues Críticas** (resolver primeiro):
- **Bugs**: Problemas funcionais
- **Vulnerabilities**: Problemas de segurança
- **Code Smells** (Major/Critical): Problemas de manutenibilidade

**Métricas Importantes**:
- **Technical Debt**: Tempo estimado para resolver problemas
- **Coverage**: Porcentagem de código coberta por testes
- **Duplications**: Código duplicado que pode ser refatorado

### 2. Melhorando a Cobertura

```python
# Exemplo: Adicionar testes para aumentar coverage

# Código sem teste
def calcular_bonus(salario, performance):
    if performance == "excellent":
        return salario * 0.2
    elif performance == "good":
        return salario * 0.1
    return 0

# Teste correspondente
def test_calcular_bonus():
    assert calcular_bonus(1000, "excellent") == 200
    assert calcular_bonus(1000, "good") == 100
    assert calcular_bonus(1000, "poor") == 0
```

### 3. Resolvendo Code Smells

**Exemplo 1 - Função muito longa:**
```python
# ❌ Função longa (Code Smell)
def processar_funcionario(dados):
    # validar email
    if not '@' in dados['email']:
        raise ValueError("Email inválido")
    # validar cpf
    if len(dados['cpf']) != 11:
        raise ValueError("CPF inválido")
    # validar telefone
    if not dados['telefone'].startswith('('):
        raise ValueError("Telefone inválido")
    # criar funcionário
    funcionario = Funcionario(**dados)
    # salvar no banco
    repository.save(funcionario)
    return funcionario

# ✅ Refatorado (sem Code Smell)
def processar_funcionario(dados):
    _validar_dados(dados)
    funcionario = _criar_funcionario(dados)
    _salvar_funcionario(funcionario)
    return funcionario

def _validar_dados(dados):
    if not '@' in dados['email']:
        raise ValueError("Email inválido")
    if len(dados['cpf']) != 11:
        raise ValueError("CPF inválido")
    if not dados['telefone'].startswith('('):
        raise ValueError("Telefone inválido")
```

**Exemplo 2 - Código duplicado:**
```python
# ❌ Código duplicado
def validar_email_funcionario(email):
    if not '@' in email:
        return False
    if not '.' in email:
        return False
    return True

def validar_email_cliente(email):
    if not '@' in email:
        return False
    if not '.' in email:
        return False
    return True

# ✅ Refatorado
def validar_email(email):
    return '@' in email and '.' in email

def validar_email_funcionario(email):
    return validar_email(email)

def validar_email_cliente(email):
    return validar_email(email)
```

### 4. Integrando no CI/CD

**GitHub Actions:**
```yaml
name: SonarQube Analysis

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: |
        python -m pytest tests/ --cov=app --cov-report=xml
    - name: SonarQube Scan
      uses: sonarqube-quality-gate-action@master
      with:
        scannerVersion: latest
        projectBaseDir: .
        args: >
          -Dsonar.projectKey=ms-cadastro-funcionario
          -Dsonar.sources=app
          -Dsonar.tests=tests
          -Dsonar.python.coverage.reportPaths=coverage.xml
```

## 🔧 Comandos Úteis

### Gerenciamento do SonarQube

```bash
# Iniciar SonarQube
docker-compose -f docker-compose.sonar.yml up -d

# Parar SonarQube
docker-compose -f docker-compose.sonar.yml down

# Ver logs
docker-compose -f docker-compose.sonar.yml logs -f sonarqube

# Resetar dados (cuidado!)
docker-compose -f docker-compose.sonar.yml down -v

# Status da aplicação
curl http://localhost:9000/api/system/status
```

### Análise

```bash
# Análise rápida (sem testes)
docker run --rm --network host \
    -v "$(pwd):/usr/src" \
    sonarsource/sonar-scanner-cli:latest \
    -Dsonar.projectKey=ms-cadastro-funcionario \
    -Dsonar.sources=app \
    -Dsonar.host.url=http://localhost:9000 \
    -Dsonar.login=admin \
    -Dsonar.password=admin

# Análise com testes específicos
python -m pytest tests/unit/ --cov=app --cov-report=xml
# Depois executar sonar-scanner

# Análise de branch específica
sonar-scanner -Dsonar.branch.name=feature/nova-funcionalidade
```

## 📈 Relatórios e Exportação

### Exportar Resultados

1. **PDF Report**: Project → More → Download PDF
2. **Issues Export**: Issues → Bulk Change → Export
3. **Metrics API**:
   ```bash
   curl "http://localhost:9000/api/measures/component?component=ms-cadastro-funcionario&metricKeys=coverage,bugs,vulnerabilities,code_smells"
   ```

### Configurar Notificações

1. **My Account** → **Notifications**
2. Configurar para:
   - New issues on my favorite projects
   - Quality Gate status changes
   - New coverage less than threshold

## 🚨 Troubleshooting

### Problemas Comuns

**1. SonarQube não inicia:**
```bash
# Verificar logs
docker-compose -f docker-compose.sonar.yml logs sonarqube

# Verificar se PostgreSQL está saudável
docker-compose -f docker-compose.sonar.yml ps

# Aumentar memória do Docker se necessário
```

**2. Erro de permissão:**
```bash
# Linux/Mac - ajustar permissões
sudo chown -R $USER:$USER ./
```

**3. Análise falha:**
```bash
# Verificar se projeto existe
curl http://localhost:9000/api/projects/search

# Verificar conectividade
curl http://localhost:9000/api/system/ping

# Debug verbose
docker run --rm --network host \
    -v "$(pwd):/usr/src" \
    sonarsource/sonar-scanner-cli:latest \
    -X -Dsonar.verbose=true
```

### Limpar Dados

```bash
# Parar tudo e limpar volumes
docker-compose -f docker-compose.sonar.yml down -v

# Remover imagens (opcional)
docker rmi sonarqube:10-community postgres:15-alpine

# Reiniciar do zero
docker-compose -f docker-compose.sonar.yml up -d
```

## 📚 Recursos Adicionais

- [Documentação SonarQube](https://docs.sonarqube.org/)
- [SonarPython Rules](https://rules.sonarsource.com/python)
- [Quality Gates Guide](https://docs.sonarqube.org/latest/user-guide/quality-gates/)
- [Coverage Guide](https://docs.sonarqube.org/latest/analysis/coverage/)

---

**💡 Dica**: Execute análises regularmente e trate issues críticas prioritariamente para manter a qualidade do código alta!
