#!/bin/bash
# Script para iniciar ambiente de desenvolvimento

set -e  # Sair se algum comando falhar

echo "🚀 Iniciando ambiente de desenvolvimento do Microserviço de Funcionários..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está disponível
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ Docker Compose não está instalado."
    exit 1
fi

echo "✅ Docker verificado com sucesso"

# Copiar arquivo de ambiente se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo de configuração (.env)..."
    cp .env.example .env
    echo "✅ Arquivo .env criado a partir do .env.example"
    echo "💡 Edite o arquivo .env se necessário"
else
    echo "✅ Arquivo .env já existe"
fi

# Criar diretório de logs se não existir
mkdir -p logs
echo "✅ Diretório de logs criado"

# Parar containers existentes se estiverem rodando
echo "🛑 Parando containers existentes..."
docker-compose down > /dev/null 2>&1 || true

# Construir e iniciar containers
echo "🔨 Construindo e iniciando containers..."
docker-compose up -d --build

# Aguardar serviços estarem prontos
echo "⏳ Aguardando serviços estarem prontos..."

# Aguardar MongoDB
echo "  📊 Aguardando MongoDB..."
timeout=60
counter=0
until docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
    sleep 2
    counter=$((counter + 2))
    if [ $counter -ge $timeout ]; then
        echo "❌ Timeout aguardando MongoDB"
        docker-compose logs mongodb
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
        docker-compose logs app
        exit 1
    fi
done
echo "  ✅ Aplicação pronta"

echo ""
echo "🎉 Ambiente de desenvolvimento iniciado com sucesso!"
echo ""
echo "📋 Informações importantes:"
echo "  🌐 Aplicação:     http://localhost:8000"
echo "  📚 Documentação:  http://localhost:8000/docs"
echo "  🔧 Health Check:  http://localhost:8000/health"
echo "  📊 MongoDB:       mongodb://localhost:27017"
echo ""
echo "📖 Comandos úteis:"
echo "  docker-compose logs -f        # Ver logs em tempo real"
echo "  docker-compose logs app       # Ver logs da aplicação"
echo "  docker-compose logs mongodb   # Ver logs do MongoDB"
echo "  ./scripts/clean.sh           # Limpar ambiente"
echo ""
