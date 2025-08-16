# Guia de Operação

## Monitoramento

### Health Checks

**Endpoint Principal**: `GET /api/v1/health`

**Verifica**:
- Status da aplicação FastAPI
- Conectividade com MongoDB
- Timestamp da verificação

**Respostas**:
```json
// Sucesso
{
  "success": true,
  "message": "Sistema funcionando corretamente",
  "data": {
    "status": "healthy",
    "database": "connected",
    "timestamp": "2025-01-10T10:30:00Z"
  }
}

// Erro de banco
{
  "success": false,
  "message": "Erro na verificação de saúde",
  "error": {
    "type": "DatabaseConnectionError",
    "details": "Falha ao conectar com MongoDB"
  },
  "timestamp": "2025-01-10T10:30:00Z"
}
```

### Monitoramento Automático

**Script de Monitoramento** (`scripts/health-monitor.sh`):
```bash
#!/bin/bash
while true; do
    response=$(curl -s http://localhost:8000/api/v1/health)
    status=$(echo $response | jq -r '.data.status')
    
    if [ "$status" != "healthy" ]; then
        echo "$(date): ALERTA - Sistema não saudável: $response"
        # Enviar notificação (email, Slack, etc.)
    else
        echo "$(date): OK - Sistema saudável"
    fi
    
    sleep 30
done
```

**Executar monitoramento**:
```bash
chmod +x scripts/health-monitor.sh
./scripts/health-monitor.sh &
```

## Logs e Debugging

### Estrutura dos Logs

**Formato JSON estruturado**:
```json
{
  "timestamp": "2025-01-10T10:30:00Z",
  "level": "INFO",
  "logger": "funcionario_service",
  "message": "Funcionário criado com sucesso",
  "extra": {
    "funcionario_id": "60d5ecb74b24c3b3d8f8e1a2",
    "operation": "create_funcionario",
    "user_context": "api_request"
  }
}
```

### Visualização de Logs

**Em desenvolvimento**:
```bash
# Logs em tempo real
docker-compose logs -f app

# Filtrar por nível
docker-compose logs app | grep "ERROR"

# Logs estruturados (com jq)
docker-compose logs app --since 1h | jq '.'
```

**Em produção (recomendado)**:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Fluentd + Elasticsearch
- CloudWatch (AWS)
- Azure Monitor
- Google Cloud Logging

### Níveis de Log

| Nível | Quando usar | Exemplo |
|-------|-------------|---------|
| `DEBUG` | Desenvolvimento detalhado | Query SQL, payload completo |
| `INFO` | Operações normais | Funcionário criado, busca realizada |
| `WARNING` | Situações atenção | Retry de operação, dados inconsistentes |
| `ERROR` | Erros recuperáveis | Validação falhou, ID não encontrado |
| `CRITICAL` | Erros graves | Banco indisponível, falha crítica |

### Configuração de Logs

**Desenvolvimento**:
```bash
export LOG_LEVEL=DEBUG
export DEBUG=true
docker-compose restart app
```

**Produção**:
```bash
export LOG_LEVEL=INFO
export DEBUG=false
```

## Backup e Recuperação

### Estratégia de Backup

**Backup Automático diário**:
```bash
#!/bin/bash
# scripts/backup-mongodb.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mongodb"
DB_NAME="funcionarios_db"

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Executar backup
docker-compose exec -T mongodb mongodump \
    --db $DB_NAME \
    --archive > $BACKUP_DIR/funcionarios_$DATE.archive

# Manter apenas últimos 7 backups
find $BACKUP_DIR -name "funcionarios_*.archive" -mtime +7 -delete

echo "Backup concluído: funcionarios_$DATE.archive"
```

**Agendar no cron**:
```bash
# Executar todo dia às 02:00
0 2 * * * /path/to/scripts/backup-mongodb.sh
```

### Recuperação de Backup

**Restaurar backup específico**:
```bash
# Parar aplicação
docker-compose stop app

# Restaurar banco
docker-compose exec -T mongodb mongorestore \
    --db funcionarios_db \
    --archive < /backups/mongodb/funcionarios_20250110_020000.archive

# Reiniciar aplicação
docker-compose start app
```

### Backup de Configurações

**Arquivos importantes para backup**:
- `docker-compose.yml`
- `docker-compose.override.yml`
- `.env` (sem secrets)
- `scripts/`
- `docs/`

## Deployment

### Ambiente de Desenvolvimento

```bash
# Iniciar ambiente completo
docker-compose up -d

# Verificar serviços
docker-compose ps

# Logs em tempo real
docker-compose logs -f app

# Parar ambiente
docker-compose down
```

### Ambiente de Produção

**1. Preparar servidor**:
```bash
# Instalar Docker e Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**2. Deploy da aplicação**:
```bash
# Clone do projeto
git clone <repository-url>
cd ms-cadastro-funcionario

# Configurar produção
cp .env.example .env
nano .env  # Ajustar para produção

# Executar em produção
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Verificar status
docker-compose ps
```

**3. Configuração de produção** (`docker-compose.prod.yml`):
```yaml
version: '3.8'
services:
  app:
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
      - DEBUG=false
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    restart: unless-stopped
    
  mongodb:
    volumes:
      - mongodb_data_prod:/data/db
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G

volumes:
  mongodb_data_prod:
    external: true
```

### Updates em Produção

**Deploy sem downtime**:
```bash
# 1. Fazer backup
./scripts/backup-mongodb.sh

# 2. Pull nova versão
git pull origin main

# 3. Rebuild e deploy
docker-compose build app
docker-compose up -d app

# 4. Verificar health
curl http://localhost:8000/api/v1/health

# 5. Rollback se necessário
# docker-compose up -d app --scale app=1
```

## Troubleshooting

### Problemas Comuns

**1. Aplicação não inicia**:
```bash
# Verificar logs
docker-compose logs app

# Verificar configuração
docker-compose config

# Verificar porta em uso
netstat -tulpn | grep 8000

# Reiniciar limpo
docker-compose down
docker-compose up -d
```

**2. Erro de conexão MongoDB**:
```bash
# Verificar status do MongoDB
docker-compose ps mongodb

# Logs do MongoDB
docker-compose logs mongodb

# Testar conectividade
docker-compose exec app python -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test():
    client = AsyncIOMotorClient('mongodb://mongodb:27017')
    await client.admin.command('ping')
    print('MongoDB OK!')

asyncio.run(test())
"
```

**3. Performance lenta**:
```bash
# Verificar índices
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.getIndexes()
"

# Estatísticas da collection
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.stats()
"

# Monitor de queries lentas
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.setProfilingLevel(1, { slowms: 100 })
"
```

**4. Erro 500 na API**:
```bash
# Logs de erro
docker-compose logs app | grep ERROR

# Debug mode (desenvolvimento)
export DEBUG=true
export LOG_LEVEL=DEBUG
docker-compose restart app

# Testar endpoint específico
curl -v http://localhost:8000/api/v1/funcionarios
```

### Comandos de Diagnóstico

**Status geral do sistema**:
```bash
#!/bin/bash
# scripts/system-status.sh

echo "=== Sistema ==="
docker-compose ps

echo -e "\n=== Saúde da aplicação ==="
curl -s http://localhost:8000/api/v1/health | jq '.'

echo -e "\n=== Uso de recursos ==="
docker stats --no-stream

echo -e "\n=== Logs recentes ==="
docker-compose logs --tail=10 app

echo -e "\n=== Estatísticas MongoDB ==="
docker-compose exec mongodb mongosh funcionarios_db --quiet --eval "
printjson(db.runCommand({dbStats: 1}))
"
```

**Executar diagnóstico**:
```bash
chmod +x scripts/system-status.sh
./scripts/system-status.sh
```

### Métricas de Performance

**Endpoints críticos para monitorar**:
- `POST /api/v1/funcionarios` (criação)
- `GET /api/v1/funcionarios` (listagem)
- `GET /api/v1/funcionarios/{id}` (consulta)
- `GET /api/v1/health` (health check)

**Métricas importantes**:
- Response time (< 200ms para consultas)
- Throughput (requests/segundo)
- Error rate (< 1%)
- Database connection pool usage
- Memory usage (< 80%)

### Alertas Recomendados

**Configurar alertas para**:
- Health check failures (> 2 consecutivos)
- Response time > 1s
- Error rate > 5%
- Memory usage > 90%
- Disk space < 20%
- MongoDB connection failures

### Manutenção Regular

**Tarefas semanais**:
- Verificar logs de erro
- Validar backups
- Monitorar uso de recursos
- Verificar atualizações de segurança

**Tarefas mensais**:
- Otimizar índices MongoDB
- Limpar logs antigos
- Revisar métricas de performance
- Atualizar dependências (se necessário)

**Tarefas trimestrais**:
- Teste de recuperação de backup
- Revisão de segurança
- Análise de capacidade
- Planejamento de escalabilidade

---

Este guia deve ser atualizado conforme o sistema evolui e novas necessidades operacionais são identificadas.
