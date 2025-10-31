#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Script de Build da Aplicação Nativa
Automatiza o processo de compilação com PyInstaller
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

def print_header():
    """Imprime cabeçalho do script"""
    print("🚀 ARQV30 Enhanced v3.0 - Build da Aplicação Nativa")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

def check_dependencies():
    """Verifica dependências necessárias"""
    print("🔍 Verificando dependências...")
    
    dependencies = {
        'pyinstaller': 'PyInstaller',
        'tkinter': 'Tkinter (interface nativa)',
        'PIL': 'Pillow (manipulação de imagens)',
    }
    
    missing = []
    
    for module, name in dependencies.items():
        try:
            if module == 'tkinter':
                import tkinter
            elif module == 'PIL':
                from PIL import Image
            elif module == 'pyinstaller':
                import PyInstaller
            else:
                __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NÃO ENCONTRADO")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Dependências faltando: {', '.join(missing)}")
        print("💡 Execute: pip install pyinstaller pillow")
        return False
    
    print("✅ Todas as dependências encontradas!")
    return True

def check_files():
    """Verifica arquivos necessários"""
    print("\n📁 Verificando arquivos...")
    
    required_files = [
        'native_windows_app.py',
        'ARQA20.spec',
        'src/run.py',
        '.env'
    ]
    
    missing = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NÃO ENCONTRADO")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Arquivos faltando: {', '.join(missing)}")
        return False
    
    print("✅ Todos os arquivos encontrados!")
    return True

def clean_build():
    """Limpa arquivos de build anteriores"""
    print("\n🧹 Limpando builds anteriores...")
    
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['*.pyc', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ Removido: {dir_name}/")
    
    # Remove __pycache__ recursivamente
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                shutil.rmtree(pycache_path)
                print(f"🗑️ Removido: {pycache_path}")
    
    print("✅ Limpeza concluída!")

def run_pyinstaller():
    """Executa PyInstaller"""
    print("\n🔨 Executando PyInstaller...")
    print("⏳ Isso pode levar alguns minutos...")
    
    try:
        # Executa PyInstaller
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            'ARQA20.spec',
            '--clean',
            '--noconfirm'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ PyInstaller executado com sucesso!")
            return True
        else:
            print("❌ Erro no PyInstaller:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar PyInstaller: {e}")
        return False

def verify_build():
    """Verifica se o build foi bem-sucedido"""
    print("\n🔍 Verificando build...")
    
    exe_path = Path('dist/ARQV30_Enhanced_v3_Native/ARQV30_Enhanced_v3_Native.exe')
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executável criado: {exe_path}")
        print(f"📦 Tamanho: {size_mb:.1f} MB")
        
        # Lista arquivos na pasta dist
        dist_path = Path('dist/ARQV30_Enhanced_v3_Native')
        if dist_path.exists():
            files = list(dist_path.iterdir())
            print(f"📁 Arquivos na pasta: {len(files)}")
            
        return True
    else:
        print("❌ Executável não encontrado!")
        return False

def create_installer_info():
    """Cria arquivo de informações do instalador"""
    print("\n📝 Criando informações do instalador...")
    
    info_content = f"""
ARQV30 Enhanced v3.0 - Aplicação Nativa para Windows
====================================================

📅 Data de Build: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
🎯 Versão: 3.0.0
💻 Plataforma: Windows (x64)
🔧 Interface: Nativa (tkinter)

📦 CONTEÚDO:
- ARQV30_Enhanced_v3_Native.exe (Aplicação principal)
- Todos os sistemas integrados:
  ✅ Sistema de Geração de Avatares
  ✅ Sistema de Análise de Concorrentes
  ✅ Sistema de Funil de Vendas
  ✅ External AI Verifier
  ✅ Interface Nativa Moderna

🚀 COMO USAR:
1. Execute ARQV30_Enhanced_v3_Native.exe
2. Configure suas APIs na aba Configurações
3. Use as abas para acessar diferentes funcionalidades

⚙️ REQUISITOS:
- Windows 10/11 (x64)
- Conexão com internet (para APIs)
- 4GB RAM mínimo
- 2GB espaço em disco

🔧 SUPORTE:
- Interface nativa moderna
- Design dark theme profissional
- Todas as funcionalidades do ARQV30 Enhanced v3.0

Build gerado automaticamente pelo script build_native_app.py
"""
    
    try:
        with open('dist/ARQV30_Enhanced_v3_Native/README.txt', 'w', encoding='utf-8') as f:
            f.write(info_content.strip())
        print("✅ README.txt criado!")
    except Exception as e:
        print(f"⚠️ Erro ao criar README: {e}")

def main():
    """Função principal"""
    print_header()
    
    # Verifica dependências
    if not check_dependencies():
        return False
    
    # Verifica arquivos
    if not check_files():
        return False
    
    # Limpa builds anteriores
    clean_build()
    
    # Executa PyInstaller
    if not run_pyinstaller():
        return False
    
    # Verifica build
    if not verify_build():
        return False
    
    # Cria informações
    create_installer_info()
    
    print("\n" + "=" * 60)
    print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("📁 Localização: dist/ARQV30_Enhanced_v3_Native/")
    print("🚀 Executável: ARQV30_Enhanced_v3_Native.exe")
    print("📋 Informações: README.txt")
    print("=" * 60)
    print("✅ Aplicação nativa pronta para distribuição!")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Build interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante build: {e}")
        sys.exit(1)