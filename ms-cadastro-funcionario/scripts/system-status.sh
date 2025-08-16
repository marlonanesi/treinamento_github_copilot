#!/bin/bash

# Sistema de Saúde - Script de Diagnóstico Completo
# Para Windows, execute no WSL ou Git Bash

echo "============================================"
echo "🔍 DIAGNÓSTICO COMPLETO DO SISTEMA"
echo "============================================"

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar ferramentas necessárias
echo -e "\n📋 Verificando ferramentas..."
if command_exists docker; then
    echo "✅ Docker: $(docker --version)"
else
    echo "❌ Docker não encontrado"
fi

if command_exists docker-compose; then
    echo "✅ Docker Compose: $(docker-compose --version)"
else
    echo "❌ Docker Compose não encontrado"
fi

if command_exists curl; then
    echo "✅ curl disponível"
else
    echo "❌ curl não encontrado"
fi

if command_exists jq; then
    echo "✅ jq disponível"
else
    echo "⚠️  jq não encontrado (opcional para JSON parsing)"
fi

echo -e "\n🐳 Status dos Containers:"
echo "----------------------------------------"
if command_exists docker-compose; then
    docker-compose ps
else
    echo "❌ Não é possível verificar status dos containers"
fi

echo -e "\n🏥 Health Check da Aplicação:"
echo "----------------------------------------"
if command_exists curl; then
    if curl -s http://localhost:8000/api/v1/health >/dev/null 2>&1; then
        echo "✅ API está respondendo"
        if command_exists jq; then
            curl -s http://localhost:8000/api/v1/health | jq '.'
        else
            curl -s http://localhost:8000/api/v1/health
        fi
    else
        echo "❌ API não está respondendo"
        echo "   Verifique se a aplicação está rodando: docker-compose up -d"
    fi
else
    echo "❌ Não é possível testar API (curl não disponível)"
fi

echo -e "\n📊 Uso de Recursos dos Containers:"
echo "----------------------------------------"
if command_exists docker; then
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" 2>/dev/null || echo "❌ Nenhum container rodando"
else
    echo "❌ Não é possível verificar recursos"
fi

echo -e "\n📝 Logs Recentes da Aplicação:"
echo "----------------------------------------"
if command_exists docker-compose; then
    echo "📋 Últimas 15 linhas:"
    docker-compose logs --tail=15 app 2>/dev/null || echo "❌ Não foi possível obter logs"
    
    echo -e "\n🚨 Erros recentes (últimas 50 linhas):"
    docker-compose logs --tail=50 app 2>/dev/null | grep -i "error\|exception\|critical" | tail -5 || echo "✅ Nenhum erro recente encontrado"
else
    echo "❌ Não é possível verificar logs"
fi

echo -e "\n🗄️  Status do MongoDB:"
echo "----------------------------------------"
if command_exists docker-compose; then
    echo "Testando conectividade..."
    docker-compose exec mongodb mongosh --quiet funcionarios_db --eval "
        try {
            db.adminCommand('ping')
            print('✅ MongoDB conectado e responsivo')
            print('📊 Database:', db.getName())
            print('📋 Collections:', db.getCollectionNames())
            print('👥 Total funcionários:', db.funcionarios.countDocuments())
            print('🔍 Índices criados:', db.funcionarios.getIndexes().length)
        } catch(e) {
            print('❌ Erro ao conectar MongoDB:', e.message)
        }
    " 2>/dev/null || echo "❌ MongoDB indisponível ou não configurado"
else
    echo "❌ Não é possível verificar MongoDB"
fi

echo -e "\n💾 Espaço em Disco:"
echo "----------------------------------------"
if command_exists df; then
    df -h | head -1  # Header
    df -h | grep -E "(/$|docker|mongodb)" | head -5
else
    echo "❌ Não é possível verificar espaço em disco"
fi

echo -e "\n🌐 Conectividade de Rede:"
echo "----------------------------------------"
if command_exists docker-compose; then
    echo "Testando conectividade entre containers..."
    if docker-compose exec app ping -c 2 mongodb >/dev/null 2>&1; then
        echo "✅ app -> mongodb: OK"
    else
        echo "❌ app -> mongodb: FALHA"
    fi
    
    echo "Testando conectividade externa..."
    if docker-compose exec app ping -c 2 8.8.8.8 >/dev/null 2>&1; then
        echo "✅ Acesso à internet: OK"
    else
        echo "❌ Acesso à internet: FALHA"
    fi
else
    echo "❌ Não é possível testar conectividade"
fi

echo -e "\n🔍 Verificação de Configuração:"
echo "----------------------------------------"
if [ -f ".env" ]; then
    echo "✅ Arquivo .env encontrado"
    echo "📋 Principais variáveis:"
    grep -E "^(MONGODB_URL|DATABASE_NAME|API_PORT|ENVIRONMENT)" .env 2>/dev/null || echo "   (Variáveis principais não encontradas)"
else
    echo "⚠️  Arquivo .env não encontrado - usando configurações padrão"
fi

if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml encontrado"
else
    echo "❌ docker-compose.yml não encontrado"
fi

echo -e "\n🚀 Endpoints Principais:"
echo "----------------------------------------"
if command_exists curl; then
    echo "Testando endpoints principais..."
    
    endpoints=(
        "GET /health"
        "GET /docs"
        "GET /funcionarios"
    )
    
    for endpoint in "${endpoints[@]}"; do
        method=$(echo $endpoint | cut -d' ' -f1)
        path=$(echo $endpoint | cut -d' ' -f2)
        
        if curl -s -o /dev/null -w "%{http_code}" -X $method "http://localhost:8000/api/v1$path" | grep -q "200\|404"; then
            echo "✅ $endpoint: OK"
        else
            echo "❌ $endpoint: FALHA"
        fi
    done
else
    echo "❌ Não é possível testar endpoints"
fi

echo -e "\n💡 Recomendações:"
echo "----------------------------------------"

# Verificar problemas comuns e dar sugestões
has_issues=false

# Verificar se containers estão rodando
if ! docker-compose ps 2>/dev/null | grep -q "Up"; then
    echo "🔧 Containers não estão rodando: execute 'docker-compose up -d'"
    has_issues=true
fi

# Verificar conectividade API
if ! curl -s http://localhost:8000/api/v1/health >/dev/null 2>&1; then
    echo "🔧 API não responde: verifique logs com 'docker-compose logs app'"
    has_issues=true
fi

# Verificar espaço em disco baixo
if command_exists df; then
    disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 90 ]; then
        echo "⚠️  Espaço em disco baixo ($disk_usage%): considere limpeza"
        has_issues=true
    fi
fi

if [ "$has_issues" = false ]; then
    echo "✅ Sistema parece estar funcionando corretamente!"
    echo "📍 API disponível em: http://localhost:8000"
    echo "📚 Documentação em: http://localhost:8000/docs"
fi

echo -e "\n============================================"
echo "📊 RELATÓRIO DE DIAGNÓSTICO COMPLETO"
echo "⏰ Gerado em: $(date)"
echo "============================================"

# Salvar relatório em arquivo
REPORT_FILE="diagnostic-report-$(date +%Y%m%d-%H%M%S).txt"
echo "💾 Salvando relatório em: $REPORT_FILE"
{
    echo "Sistema de Diagnóstico - Relatório"
    echo "=================================="
    echo "Data: $(date)"
    echo "Usuário: $(whoami)"
    echo "Diretório: $(pwd)"
    echo ""
    
    # Re-executar verificações principais para o arquivo
    echo "Status Containers:"
    docker-compose ps 2>/dev/null
    
    echo -e "\nHealth Check:"
    curl -s http://localhost:8000/api/v1/health 2>/dev/null || echo "API indisponível"
    
    echo -e "\nLogs recentes:"
    docker-compose logs --tail=20 app 2>/dev/null
    
} > "$REPORT_FILE" 2>/dev/null || echo "⚠️  Não foi possível salvar relatório em arquivo"

echo "✅ Diagnóstico concluído!"
