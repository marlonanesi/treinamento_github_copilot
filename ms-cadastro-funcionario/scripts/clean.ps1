# Script PowerShell para limpar ambiente
# Executar com: .\scripts\clean.ps1

Write-Host "🧹 Limpando ambiente do Microserviço de Funcionários..." -ForegroundColor Yellow

# Parar todos os containers relacionados
Write-Host "🛑 Parando containers..." -ForegroundColor Cyan
docker-compose down 2>$null

# Remover containers órfãos
Write-Host "🗑️  Removendo containers órfãos..." -ForegroundColor Cyan
docker-compose down --remove-orphans 2>$null

# Opção para remover volumes (dados persistentes)
$removeVolumes = Read-Host "Remover volumes de dados (ATENÇÃO: isso apagará todos os dados do banco)? (y/N)"
if ($removeVolumes -eq "y" -or $removeVolumes -eq "Y") {
    Write-Host "🗃️  Removendo volumes de dados..." -ForegroundColor Yellow
    docker-compose down -v 2>$null
    
    # Remover volumes nomeados específicos
    docker volume rm ms-cadastro-funcionario_mongodb_data 2>$null
    docker volume rm ms-cadastro-funcionario_mongodb_dev_data 2>$null
    docker volume rm ms-cadastro-funcionario_dev_cache 2>$null
    
    Write-Host "✅ Volumes removidos" -ForegroundColor Green
} else {
    Write-Host "✅ Volumes de dados preservados" -ForegroundColor Green
}

# Remover imagens não utilizadas do projeto
$removeImages = Read-Host "Remover imagens não utilizadas? (y/N)"
if ($removeImages -eq "y" -or $removeImages -eq "Y") {
    Write-Host "🖼️  Removendo imagens não utilizadas..." -ForegroundColor Yellow
    docker image prune -f
    
    # Tentar remover imagem específica do projeto
    docker image rm ms-cadastro-funcionario-app 2>$null
    docker image rm ms-cadastro-funcionario_app 2>$null
    
    Write-Host "✅ Imagens limpas" -ForegroundColor Green
}

# Remover rede se existir
Write-Host "🌐 Removendo rede personalizada..." -ForegroundColor Cyan
docker network rm funcionarios-network 2>$null

# Limpar logs locais
if (Test-Path logs) {
    $cleanLogs = Read-Host "Limpar logs locais? (y/N)"
    if ($cleanLogs -eq "y" -or $cleanLogs -eq "Y") {
        Write-Host "📝 Limpando logs..." -ForegroundColor Yellow
        Remove-Item logs\* -Force -Recurse 2>$null
        Write-Host "✅ Logs limpos" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "🎉 Limpeza concluída!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Para iniciar novamente:" -ForegroundColor Cyan
Write-Host "  .\scripts\start_dev.ps1    # Ambiente de desenvolvimento"
Write-Host "  .\scripts\start_prod.ps1   # Ambiente de produção"
Write-Host ""
