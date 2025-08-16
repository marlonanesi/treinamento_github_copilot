#!/bin/bash
# Script de setup inicial do projeto

set -e

echo "⚙️  Setup inicial do Microserviço de Funcionários"
echo ""

# Verificar pré-requisitos
echo "🔍 Verificando pré-requisitos..."

# Verificar Docker
if ! command -v docker > /dev/null 2>&1; then
    echo "❌ Docker não está instalado"
    echo "   Instale o Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "  ✅ Docker encontrado: $(docker --version)"

# Verificar Docker Compose
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ Docker Compose não está instalado"
    echo "   Instale o Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo "  ✅ Docker Compose encontrado: $(docker-compose --version)"

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon não está rodando"
    echo "   Inicie o Docker e tente novamente"
    exit 1
fi
echo "  ✅ Docker daemon rodando"

# Criar estrutura de diretórios necessários
echo ""
echo "📁 Criando estrutura de diretórios..."
mkdir -p logs
mkdir -p data/mongodb
echo "  ✅ Diretórios criados"

# Configurar arquivo de ambiente
echo ""
echo "⚙️  Configurando ambiente..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  ✅ Arquivo .env criado a partir do .env.example"
    echo "  💡 Edite .env para personalizar as configurações"
else
    echo "  ✅ Arquivo .env já existe"
fi

# Tornar scripts executáveis
echo ""
echo "🔧 Configurando permissões de scripts..."
chmod +x scripts/*.sh
echo "  ✅ Scripts configurados como executáveis"

# Verificar se porta está disponível
echo ""
echo "🔌 Verificando portas..."
if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
    echo "  ⚠️  Porta 8000 já está em uso"
    echo "     Pare o serviço que está usando a porta ou altere API_PORT no .env"
else
    echo "  ✅ Porta 8000 disponível"
fi

if netstat -tuln 2>/dev/null | grep -q ":27017 "; then
    echo "  ⚠️  Porta 27017 (MongoDB) já está em uso"
    echo "     Pare o MongoDB local ou altere a porta no docker-compose.yml"
else
    echo "  ✅ Porta 27017 disponível"
fi

echo ""
echo "🎉 Setup inicial concluído com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "  1. Revise as configurações no arquivo .env"
echo "  2. Execute: ./scripts/start_dev.sh"
echo "  3. Acesse: http://localhost:8000/docs"
echo ""
echo "📖 Scripts disponíveis:"
echo "  ./scripts/start_dev.sh    # Iniciar desenvolvimento"
echo "  ./scripts/start_prod.sh   # Iniciar produção"  
echo "  ./scripts/clean.sh        # Limpar ambiente"
echo ""
