#!/bin/bash
# Script de limpeza do ambiente

set -e

echo "🧹 Limpando ambiente do Microserviço de Funcionários..."

# Parar todos os containers relacionados
echo "🛑 Parando containers..."
docker-compose down 2>/dev/null || true

# Remover containers órfãos
echo "🗑️  Removendo containers órfãos..."
docker-compose down --remove-orphans 2>/dev/null || true

# Opção para remover volumes (dados persistentes)
read -p "Remover volumes de dados (ATENÇÃO: isso apagará todos os dados do banco)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗃️  Removendo volumes de dados..."
    docker-compose down -v 2>/dev/null || true
    
    # Remover volumes nomeados específicos
    docker volume rm ms-cadastro-funcionario_mongodb_data 2>/dev/null || true
    docker volume rm ms-cadastro-funcionario_mongodb_dev_data 2>/dev/null || true
    docker volume rm ms-cadastro-funcionario_dev_cache 2>/dev/null || true
    
    echo "✅ Volumes removidos"
else
    echo "✅ Volumes de dados preservados"
fi

# Remover imagens não utilizadas do projeto
read -p "Remover imagens não utilizadas? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🖼️  Removendo imagens não utilizadas..."
    docker image prune -f
    
    # Tentar remover imagem específica do projeto
    docker image rm ms-cadastro-funcionario-app 2>/dev/null || true
    docker image rm ms-cadastro-funcionario_app 2>/dev/null || true
    
    echo "✅ Imagens limpas"
fi

# Remover rede se existir
echo "🌐 Removendo rede personalizada..."
docker network rm funcionarios-network 2>/dev/null || true

# Limpar logs locais
if [ -d "logs" ]; then
    read -p "Limpar logs locais? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📝 Limpando logs..."
        rm -rf logs/*
        echo "✅ Logs limpos"
    fi
fi

echo ""
echo "🎉 Limpeza concluída!"
echo ""
echo "💡 Para iniciar novamente:"
echo "  ./scripts/start_dev.sh    # Ambiente de desenvolvimento"
echo "  ./scripts/start_prod.sh   # Ambiente de produção"
echo ""
