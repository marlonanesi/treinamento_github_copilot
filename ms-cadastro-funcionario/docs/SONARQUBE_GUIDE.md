# 🔍 Guia SonarQube - Análise de Qualidade de Código

Este guia explica como usar o SonarQube para análise de qualidade de código no projeto MS Cadastro Funcionário.

## 🎯 Visão Geral

O SonarQube é uma plataforma de análise contínua de qualidade de código que detecta bugs, vulnerabilidades de segurança, code smells e mede cobertura de testes.

### 📊 Métricas Analisadas

- **Bugs**: Problemas que podem causar comportamento incorreto
- **Vulnerabilidades**: Problemas de segurança
- **Code Smells**: Problemas de manutenibilidade do código
- **Cobertura**: Percentual do código coberto por testes
- **Duplicação**: Blocos de código duplicados
- **Complexidade**: Complexidade ciclomática do código

## 🚀 Execução Rápida

### Windows (PowerShell)
```powershell
# Executar análise completa
.\scripts\run-sonar.ps1

# Parar SonarQube
docker-compose -f docker-compose.sonar.yml down
```

### Linux/macOS (Bash)
```bash
# Executar análise completa
./scripts/run-sonar.sh

# Parar SonarQube
docker-compose -f docker-compose.sonar.yml down
```

## 🔧 Configuração Manual

### 1. Iniciar SonarQube
```bash
docker-compose -f docker-compose.sonar.yml up -d
```

### 2. Aguardar Inicialização
O SonarQube estará disponível em: http://localhost:9000
- Login padrão: `admin`
- Senha padrão: `admin`

### 3. Executar Análise
```bash
# Com Docker
docker run --rm \
  -e SONAR_HOST_URL=http://host.docker.internal:9000 \
  -e SONAR_LOGIN=admin \
  -e SONAR_PASSWORD=admin \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

## 📁 Estrutura de Configuração

### sonar-project.properties
```properties
# Identificação do projeto
sonar.projectKey=ms-cadastro-funcionario
sonar.projectName=Microserviço de Cadastro de Funcionários
sonar.projectVersion=1.0

# Configuração de código fonte
sonar.sources=app
sonar.tests=tests
sonar.python.version=3.11

# Relatórios de cobertura
sonar.python.coverage.reportPaths=coverage.xml

# Exclusões
sonar.exclusions=**/venv/**,**/__pycache__/**,**/node_modules/**,**/.pytest_cache/**

# Configurações de análise
sonar.sourceEncoding=UTF-8
```

### docker-compose.sonar.yml
- **SonarQube Server**: Porta 9000
- **PostgreSQL Database**: Porta 5432 (interna)
- **Volumes persistentes**: Para dados e configurações

## 🎯 Interpretando Resultados

### Quality Gate Status
- ✅ **PASSED**: Projeto atende aos critérios de qualidade
- ❌ **FAILED**: Projeto não atende aos critérios mínimos

### Métricas Principais

#### Reliability (Confiabilidade)
- **A**: 0 bugs
- **B**: <= 1% da base de código
- **C**: <= 3% da base de código
- **D**: <= 5% da base de código
- **E**: > 5% da base de código

#### Security (Segurança)
- **A**: 0 vulnerabilidades
- **B**: <= 1% da base de código
- **C**: <= 3% da base de código
- **D**: <= 5% da base de código
- **E**: > 5% da base de código

#### Maintainability (Manutenibilidade)
- **A**: 0-5% code smells
- **B**: 6-10% code smells
- **C**: 11-20% code smells
- **D**: 21-50% code smells
- **E**: > 50% code smells

### Cobertura de Testes
- **🟢 Verde**: > 80% cobertura
- **🟡 Amarelo**: 50-80% cobertura
- **🔴 Vermelho**: < 50% cobertura

## 🛠️ Melhorando a Qualidade

### 1. Corrigindo Bugs
```python
# ❌ Problema: Variável não utilizada
def processar_dados():
    dados = obter_dados()  # Bug: variável não utilizada
    return True

# ✅ Solução: Usar ou remover variável
def processar_dados():
    dados = obter_dados()
    return len(dados) > 0
```

### 2. Resolvendo Code Smells
```python
# ❌ Code Smell: Função muito complexa
def validar_funcionario(funcionario):
    if funcionario.nome:
        if len(funcionario.nome) > 2:
            if funcionario.email:
                if '@' in funcionario.email:
                    return True
    return False

# ✅ Solução: Simplificar lógica
def validar_funcionario(funcionario):
    return (
        funcionario.nome and 
        len(funcionario.nome) > 2 and
        funcionario.email and 
        '@' in funcionario.email
    )
```

### 3. Aumentando Cobertura de Testes
```python
# Executar testes com coverage
pytest tests/ --cov=app --cov-report=xml

# Identificar código não coberto
coverage report --show-missing
```

## 🔐 Configurações de Segurança

### Autenticação
1. Acesse: http://localhost:9000
2. Login: `admin` / `admin`
3. Vá em **My Account > Security**
4. Gere um token de acesso
5. Use o token em vez de login/senha

### Tokens de Acesso
```bash
# Usando token
docker run --rm \
  -e SONAR_HOST_URL=http://host.docker.internal:9000 \
  -e SONAR_TOKEN=seu_token_aqui \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

## 📊 Integração CI/CD

### GitHub Actions
```yaml
name: SonarQube Analysis
on: [push, pull_request]
jobs:
  sonar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: SonarQube Scan
        uses: sonarqube-quality-gate-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Azure DevOps
```yaml
- task: SonarQubePrepare@4
  inputs:
    SonarQube: 'SonarQube-Server'
    scannerMode: 'CLI'
    configMode: 'file'
```

## 🎯 Quality Gates Customizados

### Condições Recomendadas
- **Coverage**: >= 80%
- **Duplicated Lines**: <= 3%
- **Maintainability Rating**: A
- **Reliability Rating**: A
- **Security Rating**: A

### Configurando Quality Gate
1. Acesse **Quality Gates** no menu
2. Clique em **Create**
3. Defina condições personalizadas
4. Associe ao projeto

## 🔍 Análise de Código

### Hotspots de Segurança
```python
# ❌ Problema: Uso de random inseguro
import random
token = random.randint(1000, 9999)

# ✅ Solução: Usar secrets
import secrets
token = secrets.randbelow(9000) + 1000
```

### Complexidade Ciclomática
```python
# ❌ Problema: Função muito complexa (CC > 10)
def processar_pedido(pedido):
    if pedido.tipo == 'A':
        if pedido.urgente:
            if pedido.valor > 1000:
                return processar_tipo_a_urgente_alto()
            else:
                return processar_tipo_a_urgente_baixo()
        else:
            if pedido.valor > 1000:
                return processar_tipo_a_normal_alto()
            else:
                return processar_tipo_a_normal_baixo()
    # ... mais condições

# ✅ Solução: Quebrar em funções menores
def processar_pedido(pedido):
    processadores = {
        ('A', True, True): processar_tipo_a_urgente_alto,
        ('A', True, False): processar_tipo_a_urgente_baixo,
        ('A', False, True): processar_tipo_a_normal_alto,
        ('A', False, False): processar_tipo_a_normal_baixo,
    }
    
    key = (pedido.tipo, pedido.urgente, pedido.valor > 1000)
    return processadores.get(key, processar_padrao)()
```

## 📈 Monitoramento Contínuo

### Histórico de Qualidade
- Acompanhe tendências no dashboard
- Configure alertas para degradação
- Monitore cobertura de testes

### Relatórios Periódicos
- Análise semanal de métricas
- Comparação entre versões
- Identificação de hotspots

## 🛑 Troubleshooting

### Problemas Comuns

#### SonarQube não inicia
```bash
# Verificar logs
docker-compose -f docker-compose.sonar.yml logs sonarqube

# Limpar volumes (ATENÇÃO: apaga dados)
docker-compose -f docker-compose.sonar.yml down -v
```

#### Erro de autenticação
```bash
# Verificar status do servidor
curl -u admin:admin http://localhost:9000/api/system/status

# Resetar senha (primeiro acesso)
# Use admin/admin e será solicitado nova senha
```

#### Análise falha
```bash
# Verificar configuração
cat sonar-project.properties

# Verificar conectividade
docker run --rm sonarsource/sonar-scanner-cli \
  -Dsonar.host.url=http://host.docker.internal:9000 \
  -Dsonar.projectKey=test \
  -Dsonar.sources=/opt/sonar-scanner
```

### Logs Úteis
```bash
# Logs do SonarQube
docker-compose -f docker-compose.sonar.yml logs -f sonarqube

# Logs do PostgreSQL
docker-compose -f docker-compose.sonar.yml logs -f sonar-postgres

# Status dos containers
docker-compose -f docker-compose.sonar.yml ps
```

## 📚 Recursos Adicionais

### Documentação Oficial
- [SonarQube Documentation](https://docs.sonarqube.org/latest/)
- [Python Plugin](https://docs.sonarqube.org/latest/analysis/languages/python/)
- [Quality Gates](https://docs.sonarqube.org/latest/user-guide/quality-gates/)

### Boas Práticas
- Execute análises em cada commit
- Configure Quality Gates rigorosos
- Monitore tendências de qualidade
- Treine a equipe nas métricas
- Integre com pipeline CI/CD

### Comunidade
- [SonarQube Community Forum](https://community.sonarsource.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/sonarqube)
- [GitHub Issues](https://github.com/SonarSource/sonarqube)

---

## 📊 Dashboard URLs

- **SonarQube Server**: http://localhost:9000
- **Projeto Dashboard**: http://localhost:9000/dashboard?id=ms-cadastro-funcionario
- **Issues**: http://localhost:9000/project/issues?id=ms-cadastro-funcionario
- **Coverage**: http://localhost:9000/component_measures?id=ms-cadastro-funcionario&metric=coverage
- **Duplications**: http://localhost:9000/component_measures?id=ms-cadastro-funcionario&metric=duplicated_lines_density

---

**📝 Nota**: Este guia é específico para o projeto MS Cadastro Funcionário. Adapte as configurações conforme necessário para outros projetos.
