# Script PowerShell para configuração inicial do projeto
# Executar com: .\scripts\setup.ps1

Write-Host "🚀 Configurando Microserviço de Funcionários..." -ForegroundColor Cyan

# Verificar se Docker está instalado e rodando
Write-Host "🔍 Verificando Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker encontrado: $dockerVersion" -ForegroundColor Green
    } else {
        throw "Docker não encontrado"
    }
} catch {
    Write-Host "❌ Docker não está instalado ou não está rodando!" -ForegroundColor Red
    Write-Host "   Instale o Docker Desktop para Windows em: https://docs.docker.com/desktop/install/windows/" -ForegroundColor Yellow
    exit 1
}

# Verificar Docker Compose
Write-Host "🔍 Verificando Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker Compose encontrado: $composeVersion" -ForegroundColor Green
    } else {
        throw "Docker Compose não encontrado"
    }
} catch {
    Write-Host "❌ Docker Compose não está disponível!" -ForegroundColor Red
    Write-Host "   Instale o Docker Desktop que inclui o Docker Compose" -ForegroundColor Yellow
    exit 1
}

# Criar arquivo .env se não existir
Write-Host "📝 Configurando variáveis de ambiente..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✅ Arquivo .env criado a partir do .env.example" -ForegroundColor Green
    Write-Host "💡 Edite o arquivo .env conforme necessário" -ForegroundColor Cyan
} else {
    Write-Host "ℹ️  Arquivo .env já existe" -ForegroundColor Blue
}

# Criar diretórios necessários
Write-Host "📁 Criando diretórios..." -ForegroundColor Yellow
$directories = @("logs", "data", "data\mongodb")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Diretório $dir criado" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Diretório $dir já existe" -ForegroundColor Blue
    }
}

# Construir imagens Docker
Write-Host "🏗️  Construindo imagens Docker..." -ForegroundColor Yellow
try {
    docker-compose build --no-cache
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Imagens construídas com sucesso" -ForegroundColor Green
    } else {
        throw "Falha na construção das imagens"
    }
} catch {
    Write-Host "❌ Erro ao construir imagens Docker!" -ForegroundColor Red
    exit 1
}

# Criar rede personalizada se necessário
Write-Host "🌐 Configurando rede Docker..." -ForegroundColor Yellow
$networkExists = docker network ls --format "{{.Name}}" | Select-String "funcionarios-network" -Quiet
if (-not $networkExists) {
    docker network create funcionarios-network 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Rede funcionarios-network criada" -ForegroundColor Green
    }
} else {
    Write-Host "ℹ️  Rede funcionarios-network já existe" -ForegroundColor Blue
}

Write-Host ""
Write-Host "🎉 Configuração concluída com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Próximos passos:" -ForegroundColor Cyan
Write-Host "  1. Edite o arquivo .env se necessário"
Write-Host "  2. Execute: .\scripts\start_dev.ps1"
Write-Host ""
Write-Host "💡 Comandos úteis:" -ForegroundColor Yellow
Write-Host "  .\scripts\start_dev.ps1     # Inicia desenvolvimento"
Write-Host "  .\scripts\start_prod.ps1    # Inicia produção"
Write-Host "  .\scripts\clean.ps1         # Limpa ambiente"
Write-Host ""
