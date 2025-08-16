@echo off
echo ========================================
echo     GERENCIADOR DE TAREFAS - SETUP
echo ========================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado! Por favor, instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

echo ✅ Python detectado

:: Instalar dependências
echo.
echo 🔧 Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas com sucesso!

:: Executar aplicação
echo.
echo ========================================
echo         INICIANDO APLICACAO
echo ========================================
echo.
echo 🚀 A aplicacao sera aberta em: http://localhost:8501
echo 💡 Para parar a aplicacao, pressione Ctrl+C
echo.

streamlit run app.py

pause
