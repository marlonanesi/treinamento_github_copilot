#!/bin/bash
# Script para iniciar ambiente de produção

set -e  # Sair se algum comando falhar

echo "🚀 Iniciando ambiente de produção do Microserviço de Funcionários..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker primeiro."
    exit 1
fi

echo "✅ Docker verificado com sucesso"

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado. Configure as variáveis de ambiente primeiro."
    echo "💡 Copie .env.example para .env e ajuste as configurações para produção"
    exit 1
fi

# Verificar variáveis críticas de produção
if grep -q "ENVIRONMENT=development" .env; then
    echo "⚠️  ATENÇÃO: ENVIRONMENT ainda está configurado como 'development'"
    echo "   Configure ENVIRONMENT=production no arquivo .env"
    read -p "Continuar mesmo assim? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Criar diretório de logs se não existir
mkdir -p logs

# Usar arquivo docker-compose específico para produção
COMPOSE_FILE="docker-compose.yml"

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose -f $COMPOSE_FILE down

# Construir imagem de produção
echo "🔨 Construindo imagem de produção..."
docker-compose -f $COMPOSE_FILE build app

# Iniciar em modo produção (sem override de desenvolvimento)
echo "🚀 Iniciando containers em modo produção..."
docker-compose -f $COMPOSE_FILE up -d

# Aguardar serviços estarem prontos
echo "⏳ Aguardando serviços estarem prontos..."

# Aguardar MongoDB
echo "  📊 Aguardando MongoDB..."
timeout=60
counter=0
until docker-compose -f $COMPOSE_FILE exec -T mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
    sleep 2
    counter=$((counter + 2))
    if [ $counter -ge $timeout ]; then
        echo "❌ Timeout aguardando MongoDB"
        docker-compose -f $COMPOSE_FILE logs mongodb
        exit 1
    fi
done
echo "  ✅ MongoDB pronto"

# Aguardar aplicação
echo "  🐍 Aguardando aplicação Python..."
timeout=60
counter=0
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
    sleep 2
    counter=$((counter + 2))
    if [ $counter -ge $timeout ]; then
        echo "❌ Timeout aguardando aplicação"
        docker-compose -f $COMPOSE_FILE logs app
        exit 1
    fi
done
echo "  ✅ Aplicação pronta"

echo ""
echo "🎉 Ambiente de produção iniciado com sucesso!"
echo ""
echo "📋 Informações de produção:"
echo "  🌐 Aplicação:     http://localhost:8000"
echo "  📚 Documentação:  http://localhost:8000/docs"
echo "  🔧 Health Check:  http://localhost:8000/health"
echo ""
echo "📖 Comandos de monitoramento:"
echo "  docker-compose -f $COMPOSE_FILE logs -f    # Ver logs em tempo real"
echo "  docker-compose -f $COMPOSE_FILE ps         # Status dos containers"
echo "  docker stats                               # Uso de recursos"
echo ""
