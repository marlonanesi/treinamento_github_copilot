# Script PowerShell para iniciar ambiente de desenvolvimento
# Executar com: .\scripts\start_dev.ps1

Write-Host "🚀 Iniciando ambiente de desenvolvimento do Microserviço de Funcionários..." -ForegroundColor Green

# Verificar se Docker está rodando
try {
    docker info | Out-Null
    Write-Host "✅ Docker verificado com sucesso" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não está rodando. Por favor, inicie o Docker primeiro." -ForegroundColor Red
    exit 1
}

# Verificar Docker Compose
if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose não está instalado." -ForegroundColor Red
    exit 1
}

# Copiar arquivo de ambiente se não existir
if (!(Test-Path .env)) {
    Write-Host "📝 Criando arquivo de configuração (.env)..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ Arquivo .env criado a partir do .env.example" -ForegroundColor Green
    Write-Host "💡 Edite o arquivo .env se necessário" -ForegroundColor Cyan
} else {
    Write-Host "✅ Arquivo .env já existe" -ForegroundColor Green
}

# Criar diretório de logs se não existir
if (!(Test-Path logs)) {
    New-Item -ItemType Directory -Path logs | Out-Null
}
Write-Host "✅ Diretório de logs verificado" -ForegroundColor Green

# Parar containers existentes
Write-Host "🛑 Parando containers existentes..." -ForegroundColor Yellow
docker-compose down 2>$null

# Construir e iniciar containers
Write-Host "🔨 Construindo e iniciando containers..." -ForegroundColor Yellow
docker-compose up -d --build

# Aguardar serviços estarem prontos
Write-Host "⏳ Aguardando serviços estarem prontos..." -ForegroundColor Yellow

# Aguardar MongoDB
Write-Host "  📊 Aguardando MongoDB..." -ForegroundColor Cyan
$timeout = 60
$counter = 0
do {
    Start-Sleep 2
    $counter += 2
    if ($counter -ge $timeout) {
        Write-Host "❌ Timeout aguardando MongoDB" -ForegroundColor Red
        docker-compose logs mongodb
        exit 1
    }
} while (!(docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" 2>$null))

Write-Host "  ✅ MongoDB pronto" -ForegroundColor Green

# Aguardar aplicação
Write-Host "  🐍 Aguardando aplicação Python..." -ForegroundColor Cyan
$timeout = 60
$counter = 0
do {
    Start-Sleep 2
    $counter += 2
    try {
        $response = Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) { break }
    } catch {
        # Continuar tentando
    }
    if ($counter -ge $timeout) {
        Write-Host "❌ Timeout aguardando aplicação" -ForegroundColor Red
        docker-compose logs app
        exit 1
    }
} while ($true)

Write-Host "  ✅ Aplicação pronta" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Ambiente de desenvolvimento iniciado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Informações importantes:" -ForegroundColor Cyan
Write-Host "  🌐 Aplicação:     http://localhost:8000"
Write-Host "  📚 Documentação:  http://localhost:8000/docs"
Write-Host "  🔧 Health Check:  http://localhost:8000/health"
Write-Host "  📊 MongoDB:       mongodb://localhost:27017"
Write-Host ""
Write-Host "📖 Comandos úteis:" -ForegroundColor Cyan
Write-Host "  docker-compose logs -f        # Ver logs em tempo real"
Write-Host "  docker-compose logs app       # Ver logs da aplicação"
Write-Host "  docker-compose logs mongodb   # Ver logs do MongoDB"
Write-Host "  .\scripts\clean.ps1          # Limpar ambiente"
Write-Host ""
