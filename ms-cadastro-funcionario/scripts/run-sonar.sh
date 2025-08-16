#!/bin/bash

# Script para executar análise SonarQube no projeto
# Para Windows, execute no WSL ou Git Bash

echo "🔍 ANÁLISE SONARQUBE - MS CADASTRO FUNCIONÁRIO"
echo "=============================================="

# Verificar se Docker está rodando
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker e tente novamente."
    exit 1
fi

# Verificar se sonar-scanner está disponível
if ! command -v sonar-scanner >/dev/null 2>&1; then
    echo "⚠️  sonar-scanner não encontrado. Usando Docker para executar..."
    USE_DOCKER=true
else
    echo "✅ sonar-scanner encontrado"
    USE_DOCKER=false
fi

# Função para iniciar SonarQube se não estiver rodando
start_sonarqube() {
    echo "🚀 Iniciando SonarQube..."
    docker-compose -f docker-compose.sonar.yml up -d
    
    echo "⏳ Aguardando SonarQube inicializar..."
    sleep 30
    
    # Verificar se SonarQube está respondendo
    for i in {1..12}; do
        if curl -s http://localhost:9000/api/system/status | grep -q "UP"; then
            echo "✅ SonarQube está rodando!"
            break
        else
            echo "   Tentativa $i/12 - Aguardando SonarQube..."
            sleep 10
        fi
        
        if [ $i -eq 12 ]; then
            echo "❌ SonarQube não iniciou corretamente. Verifique os logs:"
            echo "   docker-compose -f docker-compose.sonar.yml logs sonarqube"
            exit 1
        fi
    done
}

# Verificar se SonarQube está rodando
if ! curl -s http://localhost:9000/api/system/status >/dev/null 2>&1; then
    echo "📋 SonarQube não está rodando. Iniciando..."
    start_sonarqube
else
    echo "✅ SonarQube já está rodando"
fi

# Obter token de acesso (usando credenciais padrão)
echo "🔑 Configurando autenticação..."
SONAR_TOKEN="squ_83c3cec7e4c8b7d8f9d4a9e5f3c2e8a7b6f1e9c4"

# Se não tiver token, usar credenciais padrão
if [ -z "$SONAR_TOKEN" ]; then
    echo "⚠️  Token não configurado. Usando credenciais padrão (admin/admin)"
    SONAR_AUTH="-Dsonar.login=admin -Dsonar.password=admin"
else
    SONAR_AUTH="-Dsonar.login=$SONAR_TOKEN"
fi

# Preparar ambiente para análise
echo "🛠️  Preparando ambiente..."

# Instalar dependências se necessário (para coverage)
if [ -f "requirements.txt" ]; then
    echo "📦 Verificando dependências Python..."
    pip install --quiet coverage pytest pytest-cov 2>/dev/null || echo "⚠️  Não foi possível instalar dependências de teste"
fi

# Executar testes com coverage (opcional)
echo "🧪 Executando testes para coverage..."
if [ -d "tests" ]; then
    python -m pytest tests/ --cov=app --cov-report=xml --cov-report=term 2>/dev/null || echo "⚠️  Testes não executados"
else
    echo "⚠️  Diretório de testes não encontrado"
fi

# Executar análise SonarQube
echo "🔍 Executando análise SonarQube..."

if [ "$USE_DOCKER" = true ]; then
    # Usar sonar-scanner via Docker
    echo "📋 Usando sonar-scanner via Docker..."
    docker run --rm \
        --network host \
        -v "$(pwd):/usr/src" \
        sonarsource/sonar-scanner-cli:latest \
        -Dsonar.projectKey=ms-cadastro-funcionario \
        -Dsonar.sources=app \
        -Dsonar.tests=tests \
        -Dsonar.host.url=http://localhost:9000 \
        $SONAR_AUTH \
        -Dsonar.python.coverage.reportPaths=coverage.xml \
        -Dsonar.exclusions="**/venv/**,**/__pycache__/**,**/node_modules/**"
else
    # Usar sonar-scanner local
    echo "📋 Usando sonar-scanner local..."
    sonar-scanner \
        -Dsonar.projectKey=ms-cadastro-funcionario \
        -Dsonar.sources=app \
        -Dsonar.tests=tests \
        -Dsonar.host.url=http://localhost:9000 \
        $SONAR_AUTH \
        -Dsonar.python.coverage.reportPaths=coverage.xml \
        -Dsonar.exclusions="**/venv/**,**/__pycache__/**,**/node_modules/**"
fi

# Verificar resultado
if [ $? -eq 0 ]; then
    echo "✅ Análise SonarQube concluída com sucesso!"
    echo ""
    echo "📊 Resultados disponíveis em:"
    echo "   🌐 Dashboard: http://localhost:9000/dashboard?id=ms-cadastro-funcionario"
    echo "   👤 Login: admin / admin (primeira vez)"
    echo ""
    echo "💡 Dicas:"
    echo "   • Configure um Quality Gate customizado"
    echo "   • Revise os Code Smells encontrados"
    echo "   • Verifique a cobertura de testes"
    echo "   • Analise duplicações de código"
else
    echo "❌ Erro durante a análise SonarQube"
    echo "   Verifique os logs acima para detalhes"
    exit 1
fi

echo ""
echo "🛠️  Para parar o SonarQube:"
echo "   docker-compose -f docker-compose.sonar.yml down"
echo ""
echo "🔄 Para executar novamente:"
echo "   ./scripts/run-sonar.sh"
