# Script PowerShell para iniciar ambiente de produção
# Executar com: .\scripts\start_prod.ps1

Write-Host "🚀 Iniciando Microserviço de Funcionários - PRODUÇÃO" -ForegroundColor Green

# Verificar se o arquivo .env existe
if (-not (Test-Path .env)) {
    Write-Host "❌ Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "   Execute primeiro: .\scripts\setup.ps1" -ForegroundColor Yellow
    exit 1
}

# Definir ambiente de produção
$env:ENVIRONMENT = "production"

Write-Host "🔧 Configuração:" -ForegroundColor Cyan
Write-Host "  - Ambiente: PRODUÇÃO" -ForegroundColor Yellow
Write-Host "  - Hot-reload: Desabilitado" -ForegroundColor Red
Write-Host "  - Debug: Desabilitado" -ForegroundColor Red
Write-Host "  - Logs: Nível INFO" -ForegroundColor Blue
Write-Host ""

# Parar containers existentes
Write-Host "🛑 Parando containers existentes..." -ForegroundColor Yellow
docker-compose down 2>$null

# Construir e iniciar em modo produção
Write-Host "🏗️  Construindo e iniciando serviços..." -ForegroundColor Yellow
try {
    # Construir imagens se necessário
    docker-compose build

    # Iniciar em modo detached (background)
    docker-compose up -d

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 Microserviço iniciado em modo PRODUÇÃO!" -ForegroundColor Green
        Write-Host ""
        
        # Aguardar um momento para os serviços subirem
        Write-Host "⏳ Aguardando inicialização dos serviços..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        # Verificar status dos serviços
        Write-Host "📊 Status dos serviços:" -ForegroundColor Cyan
        docker-compose ps
        
        Write-Host ""
        Write-Host "🌐 Serviços disponíveis:" -ForegroundColor Cyan
        Write-Host "  📱 API:           http://localhost:8000" -ForegroundColor Green
        Write-Host "  📚 Documentação:  http://localhost:8000/docs" -ForegroundColor Green
        Write-Host "  ❤️  Health Check:  http://localhost:8000/health" -ForegroundColor Green
        Write-Host "  🗄️  MongoDB:       mongodb://localhost:27017" -ForegroundColor Blue
        Write-Host ""
        
        Write-Host "💡 Comandos úteis:" -ForegroundColor Yellow
        Write-Host "  docker-compose logs -f           # Ver logs"
        Write-Host "  docker-compose logs -f app       # Ver logs da API"
        Write-Host "  docker-compose logs -f mongodb   # Ver logs do MongoDB"
        Write-Host "  docker-compose down              # Parar serviços"
        Write-Host "  .\scripts\clean.ps1              # Limpar ambiente"
        Write-Host ""
        
        Write-Host "⚠️  ATENÇÃO: Este é o ambiente de PRODUÇÃO!" -ForegroundColor Red
        Write-Host "   Use .\scripts\start_dev.ps1 para desenvolvimento" -ForegroundColor Yellow
        
    } else {
        throw "Falha ao iniciar os serviços"
    }
} catch {
    Write-Host ""
    Write-Host "❌ Erro ao iniciar os serviços!" -ForegroundColor Red
    Write-Host "   Verifique os logs com: docker-compose logs" -ForegroundColor Yellow
    Write-Host ""
    
    # Mostrar status dos containers para debug
    Write-Host "🔍 Status atual dos containers:" -ForegroundColor Cyan
    docker-compose ps
    exit 1
}

# Teste rápido de conectividade
Write-Host "🔍 Testando conectividade..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 10 -ErrorAction Stop
    Write-Host "✅ API respondendo: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  API ainda não está respondendo (pode levar alguns segundos)" -ForegroundColor Yellow
    Write-Host "   Verifique com: curl http://localhost:8000/health" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎯 Microserviço em execução!" -ForegroundColor Green
Write-Host ""
