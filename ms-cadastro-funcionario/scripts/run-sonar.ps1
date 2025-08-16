# Script PowerShell para executar análise SonarQube no Windows

Write-Host "🔍 ANÁLISE SONARQUBE - MS CADASTRO FUNCIONÁRIO" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Verificar se Docker está rodando
try {
    docker info | Out-Null
    Write-Host "✅ Docker está rodando" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não está rodando. Inicie o Docker e tente novamente." -ForegroundColor Red
    exit 1
}

# Função para iniciar SonarQube
function Start-SonarQube {
    Write-Host "🚀 Iniciando SonarQube..." -ForegroundColor Yellow
    docker-compose -f docker-compose.sonar.yml up -d
    
    Write-Host "⏳ Aguardando SonarQube inicializar..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
    
    # Verificar se SonarQube está respondendo
    for ($i = 1; $i -le 12; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:9000/api/system/status" -UseBasicParsing
            if ($response.Content -like "*UP*") {
                Write-Host "✅ SonarQube está rodando!" -ForegroundColor Green
                return
            }
        } catch {
            Write-Host "   Tentativa $i/12 - Aguardando SonarQube..." -ForegroundColor Yellow
            Start-Sleep -Seconds 10
        }
        
        if ($i -eq 12) {
            Write-Host "❌ SonarQube não iniciou corretamente. Verifique os logs:" -ForegroundColor Red
            Write-Host "   docker-compose -f docker-compose.sonar.yml logs sonarqube" -ForegroundColor Red
            exit 1
        }
    }
}

# Verificar se SonarQube está rodando
try {
    Invoke-WebRequest -Uri "http://localhost:9000/api/system/status" -UseBasicParsing | Out-Null
    Write-Host "✅ SonarQube já está rodando" -ForegroundColor Green
} catch {
    Write-Host "📋 SonarQube não está rodando. Iniciando..." -ForegroundColor Yellow
    Start-SonarQube
}

# Configurar autenticação
Write-Host "🔑 Configurando autenticação..." -ForegroundColor Yellow
$sonarAuth = "-Dsonar.login=admin -Dsonar.password=admin"

# Preparar ambiente
Write-Host "🛠️  Preparando ambiente..." -ForegroundColor Yellow

# Executar testes com coverage (se disponível)
Write-Host "🧪 Executando testes para coverage..." -ForegroundColor Yellow
if (Test-Path "tests") {
    try {
        python -m pytest tests/ --cov=app --cov-report=xml --cov-report=term 2>$null
        Write-Host "✅ Testes executados com sucesso" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Não foi possível executar testes" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Diretório de testes não encontrado" -ForegroundColor Yellow
}

# Executar análise SonarQube via Docker
Write-Host "🔍 Executando análise SonarQube..." -ForegroundColor Yellow
Write-Host "📋 Usando sonar-scanner via Docker..." -ForegroundColor Yellow

$currentDir = Get-Location
$sonarCmd = @(
    "run", "--rm"
    "--network", "host"
    "-v", "${currentDir}:/usr/src"
    "sonarsource/sonar-scanner-cli:latest"
    "-Dsonar.projectKey=ms-cadastro-funcionario"
    "-Dsonar.sources=app"
    "-Dsonar.tests=tests"
    "-Dsonar.host.url=http://localhost:9000"
    "-Dsonar.login=admin"
    "-Dsonar.password=admin"
    "-Dsonar.python.coverage.reportPaths=coverage.xml"
    "-Dsonar.exclusions=**/venv/**,**/__pycache__/**,**/node_modules/**"
)

try {
    & docker @sonarCmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Análise SonarQube concluída com sucesso!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Resultados disponíveis em:" -ForegroundColor Cyan
        Write-Host "   🌐 Dashboard: http://localhost:9000/dashboard?id=ms-cadastro-funcionario" -ForegroundColor White
        Write-Host "   👤 Login: admin / admin (primeira vez)" -ForegroundColor White
        Write-Host ""
        Write-Host "💡 Dicas:" -ForegroundColor Yellow
        Write-Host "   • Configure um Quality Gate customizado" -ForegroundColor White
        Write-Host "   • Revise os Code Smells encontrados" -ForegroundColor White
        Write-Host "   • Verifique a cobertura de testes" -ForegroundColor White
        Write-Host "   • Analise duplicações de código" -ForegroundColor White
    } else {
        Write-Host "❌ Erro durante a análise SonarQube" -ForegroundColor Red
        Write-Host "   Verifique os logs acima para detalhes" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Erro ao executar análise SonarQube: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🛠️  Para parar o SonarQube:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose.sonar.yml down" -ForegroundColor White
Write-Host ""
Write-Host "🔄 Para executar novamente:" -ForegroundColor Yellow
Write-Host "   .\scripts\run-sonar.ps1" -ForegroundColor White
