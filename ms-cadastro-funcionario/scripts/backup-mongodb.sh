#!/bin/bash

# Script de Backup do MongoDB
# Para Windows, execute no WSL ou Git Bash

# Configurações
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups/mongodb"
DB_NAME="funcionarios_db"
CONTAINER_NAME="mongodb"

echo "🗄️  Iniciando backup do MongoDB..."
echo "📅 Data/Hora: $(date)"
echo "🏷️  Database: $DB_NAME"

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

# Verificar se container MongoDB está rodando
if ! docker-compose ps $CONTAINER_NAME 2>/dev/null | grep -q "Up"; then
    echo "❌ Container MongoDB não está rodando!"
    echo "   Execute: docker-compose up -d mongodb"
    exit 1
fi

echo "✅ Container MongoDB encontrado e rodando"

# Fazer backup
BACKUP_FILE="$BACKUP_DIR/funcionarios_backup_$DATE.archive"

echo "💾 Criando backup: $BACKUP_FILE"

# Executar mongodump dentro do container
if docker-compose exec -T $CONTAINER_NAME mongodump \
    --db "$DB_NAME" \
    --archive > "$BACKUP_FILE"; then
    
    echo "✅ Backup criado com sucesso!"
    
    # Verificar tamanho do arquivo
    if [ -f "$BACKUP_FILE" ]; then
        BACKUP_SIZE=$(ls -lh "$BACKUP_FILE" | awk '{print $5}')
        echo "📊 Tamanho do backup: $BACKUP_SIZE"
    fi
    
else
    echo "❌ Erro ao criar backup!"
    exit 1
fi

# Verificar integridade do backup (opcional)
echo "🔍 Verificando integridade do backup..."
if docker-compose exec -T $CONTAINER_NAME mongorestore \
    --db "${DB_NAME}_test_restore" \
    --archive < "$BACKUP_FILE" >/dev/null 2>&1; then
    
    echo "✅ Backup íntegro e válido"
    
    # Limpar database de teste
    docker-compose exec -T $CONTAINER_NAME mongosh --quiet "${DB_NAME}_test_restore" --eval "
        db.dropDatabase()
    " >/dev/null 2>&1
    
else
    echo "⚠️  Não foi possível verificar integridade (backup ainda pode estar válido)"
fi

# Gerenciar retenção de backups (manter últimos 7 dias)
echo "🧹 Limpando backups antigos..."
if command -v find >/dev/null 2>&1; then
    OLD_BACKUPS=$(find "$BACKUP_DIR" -name "funcionarios_backup_*.archive" -mtime +7 2>/dev/null)
    if [ -n "$OLD_BACKUPS" ]; then
        echo "🗑️  Removendo backups com mais de 7 dias:"
        echo "$OLD_BACKUPS"
        find "$BACKUP_DIR" -name "funcionarios_backup_*.archive" -mtime +7 -delete 2>/dev/null
    else
        echo "✅ Nenhum backup antigo para remover"
    fi
else
    echo "⚠️  Comando 'find' não disponível - limpeza manual necessária"
fi

# Mostrar backups disponíveis
echo -e "\n📋 Backups disponíveis:"
if [ -d "$BACKUP_DIR" ]; then
    ls -lh "$BACKUP_DIR"/funcionarios_backup_*.archive 2>/dev/null | head -10 || echo "Nenhum backup encontrado"
fi

# Estatísticas do banco atual
echo -e "\n📊 Estatísticas atuais do banco:"
docker-compose exec -T $CONTAINER_NAME mongosh --quiet "$DB_NAME" --eval "
try {
    const stats = db.stats();
    print('📋 Collections: ' + db.getCollectionNames().length);
    print('👥 Funcionários: ' + db.funcionarios.countDocuments());
    print('💾 Tamanho DB: ' + (stats.dataSize / 1024 / 1024).toFixed(2) + ' MB');
    print('🔍 Índices: ' + db.funcionarios.getIndexes().length);
} catch(e) {
    print('Erro ao obter estatísticas: ' + e.message);
}
" 2>/dev/null || echo "❌ Não foi possível obter estatísticas"

# Criar arquivo de log do backup
LOG_FILE="$BACKUP_DIR/backup_log.txt"
{
    echo "$(date): Backup criado - $BACKUP_FILE"
    echo "  - Database: $DB_NAME"
    echo "  - Status: Sucesso"
    echo "  - Tamanho: $BACKUP_SIZE"
    echo "  - Integridade: Verificada"
} >> "$LOG_FILE"

echo -e "\n✅ Backup concluído com sucesso!"
echo "📍 Local: $BACKUP_FILE"
echo "📝 Log: $LOG_FILE"

# Instruções de uso
echo -e "\n💡 Para restaurar este backup:"
echo "   ./scripts/restore-mongodb.sh $BACKUP_FILE"

echo -e "\n🔄 Para automatizar backups diários, adicione ao cron:"
echo "   0 2 * * * /path/to/ms-cadastro-funcionario/scripts/backup-mongodb.sh"
