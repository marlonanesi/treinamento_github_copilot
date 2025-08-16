# Guia de Troubleshooting

## 🚨 Problemas Mais Comuns

### 1. Aplicação Não Inicia

**Sintomas**:
- Container não sobe
- Erro ao executar `docker-compose up`
- Aplicação não responde

**Diagnóstico**:
```bash
# Verificar status dos containers
docker-compose ps

# Ver logs de erro
docker-compose logs app

# Verificar configuração
docker-compose config
```

**Soluções**:

**A. Porta em uso**:
```bash
# Verificar quem está usando a porta 8000
netstat -tulpn | grep 8000

# No Windows
netstat -ano | findstr :8000

# Parar processo ou usar porta diferente
docker-compose down
# Editar docker-compose.yml para usar porta 8001
docker-compose up -d
```

**B. Problemas com Docker**:
```bash
# Rebuild completo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**C. Variáveis de ambiente**:
```bash
# Verificar arquivo .env
cat .env

# Verificar variáveis no container
docker-compose exec app env | grep MONGODB
```

### 2. Erro de Conexão MongoDB

**Sintomas**:
- Health check falhando
- Erro "could not connect to MongoDB"
- Timeout de conexão

**Diagnóstico**:
```bash
# Verificar status do MongoDB
docker-compose ps mongodb

# Logs do MongoDB
docker-compose logs mongodb

# Testar conectividade
docker-compose exec app python -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test():
    client = AsyncIOMotorClient('mongodb://mongodb:27017')
    try:
        await client.admin.command('ping')
        print('✅ MongoDB conectado!')
    except Exception as e:
        print(f'❌ Erro: {e}')

asyncio.run(test())
"
```

**Soluções**:

**A. MongoDB não iniciou**:
```bash
# Reiniciar serviços
docker-compose restart mongodb
docker-compose restart app

# Verificar logs de inicialização
docker-compose logs mongodb | head -20
```

**B. Problemas de permissão**:
```bash
# Verificar volumes e permissões
docker-compose exec mongodb ls -la /data/db

# Recriar volumes se necessário
docker-compose down -v
docker-compose up -d
```

**C. URL de conexão incorreta**:
```bash
# No .env, verificar:
MONGODB_URL=mongodb://mongodb:27017  # Use 'mongodb' não 'localhost'
```

### 3. Erro 500 na API

**Sintomas**:
- Internal Server Error
- Exceções não tratadas
- Stack traces nos logs

**Diagnóstico**:
```bash
# Logs detalhados
docker-compose logs --tail=50 app

# Habilitar debug
export DEBUG=true
export LOG_LEVEL=DEBUG
docker-compose restart app

# Testar endpoint específico
curl -v http://localhost:8000/api/v1/funcionarios
```

**Soluções**:

**A. Dados inválidos no banco**:
```bash
# Verificar dados no MongoDB
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.findOne()
"

# Limpar dados corrompidos
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.deleteMany({campo_problemático: {$exists: true}})
"
```

**B. Schema mismatch**:
```bash
# Verificar versão do Pydantic
docker-compose exec app pip list | grep pydantic

# Revalidar schemas
docker-compose exec app python -c "
from app.presentation.schemas.funcionario_schemas import *
print('Schemas OK')
"
```

### 4. Performance Lenta

**Sintomas**:
- Requests demoram mais que 1s
- Timeout em operações
- Alto uso de CPU/memória

**Diagnóstico**:
```bash
# Monitorar recursos
docker stats ms-cadastro-funcionario-app-1

# Verificar queries lentas no MongoDB
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().limit(5).sort({ ts: -1 }).pretty()
"

# Verificar índices
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.getIndexes()
"
```

**Soluções**:

**A. Falta de índices**:
```bash
# Criar índices necessários
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.createIndex({email: 1}, {unique: true})
db.funcionarios.createIndex({departamento: 1})
db.funcionarios.createIndex({cargo: 1})
"
```

**B. Queries ineficientes**:
```bash
# Analisar explain de queries
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.funcionarios.find({departamento: 'Tecnologia'}).explain('executionStats')
"
```

**C. Paginação excessiva**:
```bash
# Verificar se está usando paginação corretamente
curl "http://localhost:8000/api/v1/funcionarios?page=1&size=10"
# Evite: size > 100
```

### 5. Dados Não Persistem

**Sintomas**:
- Dados desaparecem após restart
- Criação parece funcionar mas não salva
- Inconsistências nos dados

**Diagnóstico**:
```bash
# Verificar volumes Docker
docker volume ls
docker volume inspect ms-cadastro-funcionario_mongodb_data

# Verificar mapeamento de volumes
docker-compose config | grep -A5 -B5 volumes

# Testar persistência
curl -X POST http://localhost:8000/api/v1/funcionarios -d '...' # Criar
docker-compose restart # Reiniciar
curl http://localhost:8000/api/v1/funcionarios # Verificar se existe
```

**Soluções**:

**A. Volume não mapeado**:
```yaml
# No docker-compose.yml
services:
  mongodb:
    volumes:
      - mongodb_data:/data/db  # Verificar se está presente

volumes:
  mongodb_data:  # Verificar se está declarado
```

**B. Transações não commitadas**:
```bash
# Verificar se o repositório está fazendo commit
docker-compose exec mongodb mongosh funcionarios_db --eval "
db.runCommand({currentOp: true})
"
```

### 6. Erro de Validação Pydantic

**Sintomas**:
- ValidationError 422
- Campos não aceitos
- Conversão de tipos falhando

**Diagnóstico**:
```bash
# Testar com dados mínimos
curl -X POST http://localhost:8000/api/v1/funcionarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome_completo": "Teste",
    "email": "teste@test.com",
    "cargo": "Dev",
    "data_admissao": "2024-01-15"
  }'

# Verificar logs de validação
docker-compose logs app | grep -i validation
```

**Soluções**:

**A. Formato de data incorreto**:
```json
// ❌ Incorreto
"data_admissao": "15/01/2024"

// ✅ Correto
"data_admissao": "2024-01-15"
```

**B. Campos obrigatórios**:
```bash
# Verificar schema esperado na documentação
curl http://localhost:8000/docs

# Ou via OpenAPI JSON
curl http://localhost:8000/openapi.json | jq '.components.schemas.FuncionarioCreateSchema'
```

## 🛠️ Comandos de Diagnóstico

### Script de Diagnóstico Completo

```bash
#!/bin/bash
# diagnose.sh

echo "=== DIAGNÓSTICO DO SISTEMA ==="

echo -e "\n1. Status dos Containers:"
docker-compose ps

echo -e "\n2. Health Check:"
curl -s http://localhost:8000/api/v1/health | jq '.' || echo "❌ API indisponível"

echo -e "\n3. Uso de Recursos:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo -e "\n4. Logs Recentes (últimas 10 linhas):"
docker-compose logs --tail=10 app

echo -e "\n5. Status MongoDB:"
docker-compose exec mongodb mongosh --quiet funcionarios_db --eval "
try {
  print('✅ MongoDB conectado')
  print('Total funcionários:', db.funcionarios.countDocuments())
  print('Índices:', db.funcionarios.getIndexes().length)
} catch(e) {
  print('❌ Erro MongoDB:', e)
}" 2>/dev/null || echo "❌ MongoDB indisponível"

echo -e "\n6. Espaço em Disco:"
df -h | grep -E "(Size|docker|mongodb)"

echo -e "\n7. Conectividade de Rede:"
docker-compose exec app ping -c 2 mongodb 2>/dev/null || echo "❌ Conectividade falhando"

echo -e "\n=== DIAGNÓSTICO COMPLETO ==="
```

**Executar**:
```bash
chmod +x diagnose.sh
./diagnose.sh
```

### Script de Reset Completo

```bash
#!/bin/bash
# reset.sh

echo "🔄 RESET COMPLETO DO AMBIENTE"

echo "1. Parando containers..."
docker-compose down -v

echo "2. Removendo imagens..."
docker-compose down --rmi all

echo "3. Limpando volumes..."
docker volume prune -f

echo "4. Limpando cache Docker..."
docker system prune -f

echo "5. Rebuilding do zero..."
docker-compose build --no-cache

echo "6. Iniciando ambiente..."
docker-compose up -d

echo "7. Aguardando inicialização..."
sleep 10

echo "8. Testando health check..."
curl -s http://localhost:8000/api/v1/health | jq '.'

echo "✅ RESET COMPLETO CONCLUÍDO"
```

**Usar com cuidado** (remove todos os dados):
```bash
chmod +x reset.sh
./reset.sh
```

## 📊 Monitoramento e Alertas

### Healthcheck Automatizado

```bash
#!/bin/bash
# healthcheck-monitor.sh

while true; do
    response=$(curl -s http://localhost:8000/api/v1/health)
    status=$(echo $response | jq -r '.data.status' 2>/dev/null)
    
    if [ "$status" != "healthy" ]; then
        echo "$(date): 🚨 ALERTA - Sistema não saudável"
        echo "Response: $response"
        
        # Ações automáticas (opcional)
        # docker-compose restart app
        # Enviar notificação
        
    else
        echo "$(date): ✅ Sistema saudável"
    fi
    
    sleep 30
done
```

### Monitoramento de Logs

```bash
#!/bin/bash
# log-monitor.sh

# Monitorar erros críticos
docker-compose logs -f app | while read line; do
    if echo "$line" | grep -E "(ERROR|CRITICAL|Exception)"; then
        echo "🚨 ERRO DETECTADO: $line"
        # Enviar alerta
    fi
done
```

## 🔧 Problemas Específicos do Windows

### WSL2 e Docker

**Problema**: Docker lento no Windows
**Solução**:
```powershell
# Usar WSL2 backend
wsl --set-default-version 2

# Configurar limite de memória WSL
# No arquivo %USERPROFILE%\.wslconfig:
[wsl2]
memory=4GB
processors=2
```

### Permissões de Arquivo

**Problema**: Erro de permissão em volumes
**Solução**:
```bash
# No WSL, ajustar permissões
chmod 755 ./data
chown -R $USER:$USER ./data
```

## 🆘 Quando Pedir Ajuda

**Colete estas informações**:

1. **Versões**:
```bash
docker --version
docker-compose --version
python --version
```

2. **Status do sistema**:
```bash
./diagnose.sh > diagnostic-output.txt
```

3. **Logs completos**:
```bash
docker-compose logs > full-logs.txt
```

4. **Configuração**:
```bash
docker-compose config > current-config.yml
```

5. **O que estava fazendo**:
- Qual operação falhou?
- Existe um padrão de falha?
- Mudou alguma configuração recentemente?

## 📞 Escalação de Problemas

**Nível 1** - Problemas simples:
- Restart de containers
- Verificação de configuração
- Problemas de conectividade básica

**Nível 2** - Problemas técnicos:
- Performance issues
- Problemas de dados
- Configuração avançada

**Nível 3** - Problemas críticos:
- Sistema completamente indisponível
- Corrupção de dados
- Problemas de segurança

---

## 💡 Dicas de Prevenção

1. **Sempre fazer backup antes de mudanças**
2. **Monitorar logs regularmente**
3. **Manter documentação atualizada**
4. **Testar em ambiente similar à produção**
5. **Ter procedimentos de rollback prontos**

**Lembre-se**: A maioria dos problemas pode ser resolvida com restart e verificação de configuração! 🚀
