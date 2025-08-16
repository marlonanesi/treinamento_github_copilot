# Checklist de Produção

## 📋 Pré-Deploy

### Código e Build

- [ ] **Código na branch main/master atualizada**
- [ ] **Build da Docker image realizado com sucesso**
  ```bash
  docker build -t ms-funcionarios:latest .
  ```
- [ ] **Testes manuais executados e validados**
  - [ ] Health check funcionando
  - [ ] CRUD completo testado
  - [ ] Tratamento de erros validado
- [ ] **Documentação atualizada**
  - [ ] README.md completo
  - [ ] API documentation (Swagger) funcional
  - [ ] Changelog atualizado

### Configuração de Ambiente

- [ ] **Variáveis de ambiente configuradas**
  ```bash
  # Produção
  ENVIRONMENT=production
  LOG_LEVEL=INFO
  DEBUG=false
  MONGODB_URL=mongodb://prod-mongo:27017
  DATABASE_NAME=funcionarios_prod
  ```
- [ ] **Secrets e credenciais seguras**
  - [ ] MongoDB credentials em vault/secrets
  - [ ] SSL certificates disponíveis
  - [ ] API keys protegidas
- [ ] **Recursos de infraestrutura provisionados**
  - [ ] Servidor/VM com recursos adequados
  - [ ] Banco MongoDB configurado
  - [ ] Rede e firewall configurados

### Infraestrutura

- [ ] **Docker e Docker Compose instalados**
  ```bash
  docker --version
  docker-compose --version
  ```
- [ ] **Volumes persistentes configurados**
  - [ ] Volume MongoDB criado
  - [ ] Diretório de logs configurado
  - [ ] Diretório de backups disponível
- [ ] **Monitoramento preparado**
  - [ ] Health check endpoint testado
  - [ ] Logs estruturados configurados
  - [ ] Alertas configurados (se aplicável)

## 🚀 Deploy

### Processo de Deploy

- [ ] **Backup do ambiente atual realizado**
  ```bash
  ./scripts/backup-mongodb.sh
  ```
- [ ] **Deploy executado**
  ```bash
  docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
  ```
- [ ] **Verificação de containers rodando**
  ```bash
  docker-compose ps
  ```
- [ ] **Health check validado**
  ```bash
  curl http://localhost:8000/api/v1/health
  ```

### Validação Pós-Deploy

- [ ] **API endpoints funcionando**
  - [ ] `GET /api/v1/health` - Status 200
  - [ ] `POST /api/v1/funcionarios` - Criação testada
  - [ ] `GET /api/v1/funcionarios` - Listagem funcionando
  - [ ] `GET /docs` - Documentação acessível
- [ ] **Banco de dados conectado**
  ```bash
  docker-compose exec mongodb mongosh funcionarios_prod --eval "db.adminCommand('ping')"
  ```
- [ ] **Logs sendo gerados corretamente**
  ```bash
  docker-compose logs --tail=20 app
  ```

## 📊 Monitoramento

### Métricas Base

- [ ] **Response time < 200ms para consultas simples**
- [ ] **Error rate < 1%**
- [ ] **Memory usage < 70%**
- [ ] **CPU usage < 60%**
- [ ] **Disk space > 20% livre**

### Health Checks

- [ ] **Health endpoint sempre responsivo**
- [ ] **Conectividade MongoDB estável**
- [ ] **Logs sem erros críticos**

### Alertas Configurados

- [ ] **Aplicação indisponível (health check fail)**
- [ ] **Alta latência (> 1s response time)**
- [ ] **Error rate elevado (> 5%)**
- [ ] **Recursos esgotando (memory > 90%, disk < 10%)**

## 🔒 Segurança

### Configurações Básicas

- [ ] **Debug mode desabilitado**
  ```bash
  DEBUG=false
  ```
- [ ] **Logs não expõem dados sensíveis**
- [ ] **CORS configurado apropriadamente**
- [ ] **Headers de segurança configurados (futuramente)**

### Acesso e Permissões

- [ ] **MongoDB com autenticação habilitada**
- [ ] **Firewall configurado (portas necessárias apenas)**
- [ ] **SSL/TLS configurado (recomendado)**
- [ ] **Backup com permissões restritas**

### Auditoria

- [ ] **Logs de acesso configurados**
- [ ] **Operações críticas logadas**
- [ ] **Rotação de logs configurada**

## 💾 Backup e Recuperação

### Estratégia de Backup

- [ ] **Backup automático configurado**
  ```bash
  # Cron job para backup diário
  0 2 * * * /path/to/scripts/backup-mongodb.sh
  ```
- [ ] **Retenção de backups definida**
  - [ ] Diários: 7 dias
  - [ ] Semanais: 4 semanas
  - [ ] Mensais: 6 meses
- [ ] **Local de armazenamento de backup seguro**

### Teste de Recuperação

- [ ] **Procedimento de restore documentado**
- [ ] **Teste de restore realizado pelo menos 1x**
- [ ] **RTO (Recovery Time Objective) < 1 hora**
- [ ] **RPO (Recovery Point Objective) < 24 horas**

## 📈 Performance

### Otimizações MongoDB

- [ ] **Índices criados e validados**
  ```bash
  # Verificar índices
  db.funcionarios.getIndexes()
  ```
- [ ] **Queries otimizadas**
- [ ] **Connection pool configurado adequadamente**

### Otimizações Aplicação

- [ ] **Paginação implementada em endpoints de listagem**
- [ ] **Validação de entrada eficiente**
- [ ] **Serialização otimizada**

### Capacidade

- [ ] **Testes de carga executados (recomendado)**
- [ ] **Limites de capacidade documentados**
- [ ] **Plano de escalabilidade definido**

## 🐛 Troubleshooting

### Procedimentos de Diagnóstico

- [ ] **Script de diagnóstico disponível**
  ```bash
  ./scripts/system-status.sh
  ```
- [ ] **Logs centralizados e pesquisáveis**
- [ ] **Métricas históricas disponíveis**

### Procedimentos de Recuperação

- [ ] **Restart automático configurado**
  ```yaml
  restart: unless-stopped
  ```
- [ ] **Rollback procedure documentado**
- [ ] **Contacts de emergência definidos**

## 📋 Documentação Operacional

### Runbooks

- [ ] **Procedimento de deploy documentado**
- [ ] **Procedimento de rollback documentado**
- [ ] **Troubleshooting guide atualizado**
- [ ] **Contatos e escalação definidos**

### Conhecimento da Equipe

- [ ] **Pelo menos 2 pessoas sabem fazer deploy**
- [ ] **Acesso aos ambientes documentado**
- [ ] **Credenciais compartilhadas de forma segura**

## 🔄 Pós-Deploy

### Validação Contínua (Primeiras 24h)

- [ ] **Monitoramento intensivo**
  - [ ] Health checks a cada 5min
  - [ ] Response time monitoring
  - [ ] Error rate tracking
- [ ] **Validação de funcionalidades críticas**
  - [ ] Criação de funcionário
  - [ ] Consulta de funcionários
  - [ ] Operações CRUD completas

### Métricas de Sucesso

- [ ] **Zero downtime durante deploy**
- [ ] **Todos os endpoints funcionais**
- [ ] **Performance dentro dos SLAs**
- [ ] **Nenhum erro crítico nos logs**

## 📞 Contatos e Escalação

### Equipe Técnica
- **Developer Lead**: [nome] - [email] - [telefone]
- **DevOps Engineer**: [nome] - [email] - [telefone]
- **Database Admin**: [nome] - [email] - [telefone]

### Escalação
1. **Nível 1**: Developer on-duty
2. **Nível 2**: Tech Lead
3. **Nível 3**: Engineering Manager

---

## ⚡ Quick Commands

```bash
# Status rápido do sistema
docker-compose ps

# Health check
curl http://localhost:8000/api/v1/health

# Logs da aplicação (últimas 50 linhas)
docker-compose logs --tail=50 app

# Restart da aplicação
docker-compose restart app

# Backup manual
./scripts/backup-mongodb.sh

# Status completo do sistema
./scripts/system-status.sh

# Parar ambiente
docker-compose down

# Iniciar ambiente
docker-compose up -d
```

---

**✅ CRITÉRIO DE PRONTO**: Todos os itens deste checklist devem estar marcados antes de considerar o deploy para produção concluído.

**🔄 REVISÃO**: Este checklist deve ser revisado e atualizado após cada deploy para incorporar lições aprendidas.
