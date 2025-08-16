"""
Script de Setup para o Gerenciador de Tarefas

Este script automatiza a instalação das dependências e execução da aplicação.
"""

import subprocess
import sys
import os
from pathlib import Path


def verificar_python():
    """Verifica se a versão do Python é adequada."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Erro: Python 3.8+ é necessário")
        print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True


def instalar_dependencias():
    """Instala as dependências do projeto."""
    print("🔧 Instalando dependências...")
    
    try:
        # Verificar se requirements.txt existe
        requirements_path = Path("requirements.txt")
        if requirements_path.exists():
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            # Instalar streamlit diretamente
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit>=1.28.0"])
        
        print("✅ Dependências instaladas com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False


def verificar_streamlit():
    """Verifica se o Streamlit está instalado corretamente."""
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} instalado")
        return True
    except ImportError:
        print("❌ Streamlit não encontrado")
        return False


def executar_aplicacao():
    """Executa a aplicação Streamlit."""
    app_path = Path("app.py")
    
    if not app_path.exists():
        print("❌ Arquivo app.py não encontrado!")
        return False
    
    print("🚀 Iniciando aplicação...")
    print("📌 A aplicação será aberta em: http://localhost:8501")
    print("💡 Para parar a aplicação, pressione Ctrl+C")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        return True
    except KeyboardInterrupt:
        print("\n👋 Aplicação finalizada pelo usuário")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")
        return False


def main():
    """Função principal do setup."""
    print("=" * 50)
    print("📋 GERENCIADOR DE TAREFAS - SETUP")
    print("=" * 50)
    
    # Verificar Python
    if not verificar_python():
        return
    
    # Instalar dependências
    if not instalar_dependencias():
        print("❌ Falha na instalação das dependências")
        return
    
    # Verificar instalação do Streamlit
    if not verificar_streamlit():
        print("❌ Falha na verificação do Streamlit")
        return
    
    print("\n" + "=" * 50)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    
    # Perguntar se deseja executar a aplicação
    resposta = input("\n🚀 Deseja executar a aplicação agora? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print()
        executar_aplicacao()
    else:
        print("\n💡 Para executar manualmente, use: streamlit run app.py")
        print("📌 URL da aplicação: http://localhost:8501")


if __name__ == "__main__":
    main()
