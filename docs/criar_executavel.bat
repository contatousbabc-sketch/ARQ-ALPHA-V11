@echo off
echo ========================================
echo   ARQ-ALPHA-V9 - CRIADOR DE EXECUTAVEL
echo ========================================
echo.
echo Este script criara um executavel Windows (.exe) do instalador automatico
echo que pode ser executado em qualquer Windows sem Python instalado.
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python primeiro ou execute este script em um ambiente com Python.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
echo.

REM Verificar se PyInstaller esta instalado
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller nao encontrado. Instalando...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERRO: Falha ao instalar PyInstaller
        pause
        exit /b 1
    )
    echo ✅ PyInstaller instalado!
) else (
    echo ✅ PyInstaller ja instalado!
)

echo.
echo Criando executavel... (isso pode demorar alguns minutos)
echo.

REM Criar executavel com PyInstaller
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "ARQ-ALPHA-V9-Instalador" ^
    --icon=src/static/favicon.ico ^
    --add-data "src;src" ^
    --add-data "external_ai_verifier;external_ai_verifier" ^
    --add-data "requirements.txt;." ^
    --add-data ".env.example;." ^
    --hidden-import=winreg ^
    --hidden-import=ctypes ^
    --hidden-import=urllib.request ^
    --hidden-import=tempfile ^
    --hidden-import=zipfile ^
    --hidden-import=tarfile ^
    --hidden-import=pathlib ^
    --console ^
    instalador_automatico.py

if errorlevel 1 (
    echo.
    echo ❌ ERRO: Falha ao criar executavel
    echo Tentando versao simplificada...
    echo.
    
    REM Tentar versao mais simples
    python -m PyInstaller ^
        --onefile ^
        --name "ARQ-ALPHA-V9-Instalador-Simples" ^
        --console ^
        instalador_automatico.py
    
    if errorlevel 1 (
        echo ❌ ERRO: Falha mesmo na versao simplificada
        pause
        exit /b 1
    )
)

echo.
echo ✅ Executavel criado com sucesso!
echo.
echo 📁 Localizacao do executavel:
echo    %CD%\dist\ARQ-ALPHA-V9-Instalador.exe
echo.
echo 🚀 Para distribuir:
echo    1. Copie o arquivo .exe da pasta 'dist'
echo    2. O executavel pode ser executado em qualquer Windows
echo    3. Nao precisa de Python instalado no computador de destino
echo.
echo 📋 Instrucoes para o usuario final:
echo    1. Execute o .exe como Administrador
echo    2. Aguarde a instalacao completa
echo    3. Siga as instrucoes na tela
echo.

REM Verificar se o executavel foi criado
if exist "dist\ARQ-ALPHA-V9-Instalador.exe" (
    echo ✅ Arquivo executavel confirmado: dist\ARQ-ALPHA-V9-Instalador.exe
    echo    Tamanho: 
    dir "dist\ARQ-ALPHA-V9-Instalador.exe" | find "ARQ-ALPHA-V9-Instalador.exe"
) else if exist "dist\ARQ-ALPHA-V9-Instalador-Simples.exe" (
    echo ✅ Arquivo executavel confirmado: dist\ARQ-ALPHA-V9-Instalador-Simples.exe
    echo    Tamanho: 
    dir "dist\ARQ-ALPHA-V9-Instalador-Simples.exe" | find "ARQ-ALPHA-V9-Instalador-Simples.exe"
) else (
    echo ❌ ERRO: Executavel nao encontrado na pasta dist
)

echo.
echo ========================================
echo        PROCESSO CONCLUIDO
echo ========================================
pause