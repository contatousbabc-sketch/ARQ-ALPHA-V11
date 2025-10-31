#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PREPARADOR DE DISTRIBUIÇÃO ARQ-ALPHA-V9
=======================================
Prepara todos os arquivos necessários para distribuição do ARQ-ALPHA-V9
incluindo verificações, otimizações e criação de pacotes.

Autor: ARQ-ALPHA-V9 Team
Data: 2025-10-31
"""

import os
import sys
import shutil
import zipfile
import json
from pathlib import Path
import subprocess
import hashlib

class DistributionPreparer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "distribuicao"
        self.version = "9.0.0"
        
    def print_step(self, message):
        print(f"🔧 {message}")
        
    def print_success(self, message):
        print(f"✅ {message}")
        
    def print_error(self, message):
        print(f"❌ {message}")

    def clean_project(self):
        """Remove arquivos desnecessários"""
        self.print_step("Limpando projeto...")
        
        # Diretórios para remover
        dirs_to_remove = [
            '__pycache__',
            '.pytest_cache',
            'build',
            'dist',
            '*.egg-info',
            '.coverage',
            'htmlcov',
            'node_modules'
        ]
        
        # Arquivos para remover
        files_to_remove = [
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.DS_Store',
            'Thumbs.db',
            '*.log',
            '*.tmp'
        ]
        
        removed_count = 0
        
        # Remover diretórios
        for pattern in dirs_to_remove:
            for path in self.project_root.rglob(pattern):
                if path.is_dir():
                    try:
                        shutil.rmtree(path)
                        removed_count += 1
                        print(f"  Removido: {path.relative_to(self.project_root)}")
                    except:
                        pass
        
        # Remover arquivos
        for pattern in files_to_remove:
            for path in self.project_root.rglob(pattern):
                if path.is_file():
                    try:
                        path.unlink()
                        removed_count += 1
                        print(f"  Removido: {path.relative_to(self.project_root)}")
                    except:
                        pass
        
        self.print_success(f"Limpeza concluída: {removed_count} itens removidos")

    def verify_dependencies(self):
        """Verifica se todas as dependências estão corretas"""
        self.print_step("Verificando dependências...")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            self.print_error("requirements.txt não encontrado!")
            return False
        
        # Ler requirements
        with open(requirements_file, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"  Encontradas {len(requirements)} dependências")
        
        # Verificar se as dependências críticas estão presentes
        critical_deps = [
            'flask', 'requests', 'beautifulsoup4', 'selenium', 
            'playwright', 'openai', 'anthropic', 'google-generativeai'
        ]
        
        missing_critical = []
        for dep in critical_deps:
            found = any(dep in req.lower() for req in requirements)
            if not found:
                missing_critical.append(dep)
        
        if missing_critical:
            self.print_error(f"Dependências críticas faltando: {', '.join(missing_critical)}")
            return False
        
        self.print_success("Todas as dependências críticas estão presentes")
        return True

    def create_distribution_structure(self):
        """Cria estrutura de distribuição"""
        self.print_step("Criando estrutura de distribuição...")
        
        # Limpar diretório de distribuição
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        
        self.dist_dir.mkdir(parents=True)
        
        # Estrutura de diretórios
        dirs_to_create = [
            "ARQ-ALPHA-V9",
            "ARQ-ALPHA-V9/src",
            "ARQ-ALPHA-V9/external_ai_verifier",
            "ARQ-ALPHA-V9/docs",
            "ARQ-ALPHA-V9/scripts",
            "Instaladores"
        ]
        
        for dir_name in dirs_to_create:
            (self.dist_dir / dir_name).mkdir(parents=True, exist_ok=True)
        
        self.print_success("Estrutura de distribuição criada")

    def copy_application_files(self):
        """Copia arquivos da aplicação"""
        self.print_step("Copiando arquivos da aplicação...")
        
        app_dir = self.dist_dir / "ARQ-ALPHA-V9"
        
        # Arquivos principais
        main_files = [
            "run.py",
            "requirements.txt",
            ".env.example",
            "README.md",
            "instalador_automatico.py",
            "criar_executavel.bat"
        ]
        
        for file_name in main_files:
            source = self.project_root / file_name
            if source.exists():
                shutil.copy2(source, app_dir / file_name)
                print(f"  Copiado: {file_name}")
        
        # Diretórios
        dirs_to_copy = [
            "src",
            "external_ai_verifier"
        ]
        
        for dir_name in dirs_to_copy:
            source = self.project_root / dir_name
            if source.exists():
                dest = app_dir / dir_name
                shutil.copytree(source, dest, dirs_exist_ok=True)
                print(f"  Copiado: {dir_name}/")
        
        self.print_success("Arquivos da aplicação copiados")

    def create_documentation(self):
        """Cria documentação de instalação"""
        self.print_step("Criando documentação...")
        
        docs_dir = self.dist_dir / "ARQ-ALPHA-V9" / "docs"
        
        # Manual de instalação
        install_manual = """# ARQ-ALPHA-V9 - Manual de Instalação

## Instalação Automática (Recomendada)

### Para Usuários Finais (Windows)
1. Execute `ARQ-ALPHA-V9-Instalador.exe` como Administrador
2. Aguarde a instalação completa (pode demorar 15-30 minutos)
3. Siga as instruções na tela
4. Execute `iniciar_arq_alpha.bat` para iniciar o sistema

### Para Desenvolvedores
1. Execute `instalador_automatico.py` com Python
2. Ou use `criar_executavel.bat` para gerar o instalador

## Instalação Manual

### Pré-requisitos
- Windows 10/11
- Python 3.11+
- Node.js 18+
- Visual Studio Build Tools

### Passos
1. Instale Python: https://python.org/downloads/
2. Instale Node.js: https://nodejs.org/
3. Instale Visual Studio Build Tools
4. Execute: `pip install -r requirements.txt`
5. Execute: `python -m playwright install`
6. Configure arquivo `.env` com suas chaves de API
7. Execute: `python run.py`

## Configuração

### Chaves de API Necessárias
- OpenAI API Key
- Anthropic API Key
- Google Gemini API Key
- Serper API Key (busca)
- Jina API Key (extração)

### Arquivo .env
Copie `.env.example` para `.env` e configure suas chaves:

```
OPENAI_API_KEY=sua_chave_aqui
ANTHROPIC_API_KEY=sua_chave_aqui
GOOGLE_API_KEY=sua_chave_aqui
SERPER_API_KEY=sua_chave_aqui
JINA_API_KEY=sua_chave_aqui
```

## Uso

1. Acesse: http://localhost:12000
2. Configure sua análise
3. Execute as 3 etapas do workflow:
   - Etapa 1: Coleta Massiva Real
   - Etapa 2: Síntese com IA Ativa
   - Etapa 3: Geração de 16 Módulos

## Solução de Problemas

### Erro de Dependências
Execute: `python verificar_dependencias.py`

### Erro de Navegador
Execute: `python -m playwright install chromium`

### Erro de Compilação
Instale Visual Studio Build Tools

### Logs
- Log principal: `app_runtime.log`
- Logs de sessão: `log_session_*.txt`

## Suporte

Para suporte técnico, consulte:
- Documentação completa no código
- Logs de erro detalhados
- Sistema de logging em tempo real
"""
        
        with open(docs_dir / "INSTALACAO.md", 'w', encoding='utf-8') as f:
            f.write(install_manual)
        
        # Manual do usuário
        user_manual = """# ARQ-ALPHA-V9 - Manual do Usuário

## Visão Geral

O ARQ-ALPHA-V9 é um sistema avançado de análise de mercado que utiliza:
- Inteligência Artificial com múltiplos modelos
- Coleta massiva de dados reais
- Análise de conteúdo viral
- Geração de relatórios especializados

## Interface Principal

### Configuração da Análise
1. **Segmento de Mercado**: Defina o setor a ser analisado
2. **Produto/Serviço**: Especifique o que será analisado
3. **Preço**: Valor do produto/serviço
4. **Objetivo de Receita**: Meta financeira
5. **Público-Alvo**: Descrição detalhada do público
6. **Contexto Adicional**: Informações extras relevantes

### Workflow de 3 Etapas

#### Etapa 1: Coleta Massiva Real
- Busca em múltiplas APIs
- Extração de conteúdo viral
- Captura de screenshots
- Rotação automática de provedores

#### Etapa 2: Síntese com IA Ativa
- Análise por IA avançada
- Buscas online ativas
- Validação de informações
- Síntese em formato JSON

#### Etapa 3: Geração de 16 Módulos
- 16 módulos especializados
- Relatório final completo
- Mais de 25 páginas
- Análise ultra-detalhada

### Verificação AI
- Análise de sentimento
- Detecção de viés
- Validação por LLM
- Filtros avançados

## Recursos Avançados

### Sistema de Logging
- Logs em tempo real
- Rastreamento de sessões
- Códigos executados
- Dados extras capturados

### Gerenciamento de Sessões
- Múltiplas sessões simultâneas
- Pausar/retomar análises
- Renomear sessões
- Histórico completo

### Resultados
- Visão geral interativa
- 16 módulos detalhados
- Screenshots capturados
- Dados coletados brutos

## Dicas de Uso

1. **Configure bem o público-alvo** para melhores resultados
2. **Use contexto adicional** para análises mais precisas
3. **Aguarde cada etapa** completar antes de prosseguir
4. **Monitore os logs** para acompanhar o progresso
5. **Salve sessões importantes** para referência futura

## Limitações

- Requer conexão com internet
- Dependente de APIs externas
- Tempo de processamento varia
- Qualidade depende dos dados disponíveis

## Troubleshooting

### Análise não inicia
- Verifique conexão com internet
- Confirme chaves de API válidas
- Reinicie o sistema se necessário

### Resultados incompletos
- Aguarde mais tempo
- Verifique logs de erro
- Tente com parâmetros diferentes

### Performance lenta
- Feche outras aplicações
- Verifique recursos do sistema
- Use parâmetros mais específicos
"""
        
        with open(docs_dir / "MANUAL_USUARIO.md", 'w', encoding='utf-8') as f:
            f.write(user_manual)
        
        self.print_success("Documentação criada")

    def create_batch_scripts(self):
        """Cria scripts batch adicionais"""
        self.print_step("Criando scripts batch...")
        
        scripts_dir = self.dist_dir / "ARQ-ALPHA-V9" / "scripts"
        
        # Script de verificação rápida
        quick_check = """@echo off
echo ========================================
echo   ARQ-ALPHA-V9 - VERIFICACAO RAPIDA
echo ========================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python nao encontrado
    goto :error
) else (
    echo ✅ Python OK
)

echo.
echo Verificando Node.js...
node --version
if errorlevel 1 (
    echo ❌ Node.js nao encontrado
    goto :error
) else (
    echo ✅ Node.js OK
)

echo.
echo Verificando dependencias Python...
python -c "import flask, requests, playwright; print('✅ Dependencias principais OK')"
if errorlevel 1 (
    echo ❌ Dependencias Python com problema
    goto :error
)

echo.
echo ✅ SISTEMA PRONTO PARA USO!
echo.
echo Para iniciar: python run.py
echo Ou execute: iniciar_arq_alpha.bat
goto :end

:error
echo.
echo ❌ PROBLEMAS DETECTADOS
echo Execute o instalador automatico para corrigir
echo.

:end
pause
"""
        
        with open(scripts_dir / "verificacao_rapida.bat", 'w', encoding='utf-8') as f:
            f.write(quick_check)
        
        # Script de atualização
        update_script = """@echo off
echo ========================================
echo   ARQ-ALPHA-V9 - ATUALIZADOR
echo ========================================
echo.

echo Atualizando dependencias Python...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --upgrade

echo.
echo Atualizando navegadores Playwright...
python -m playwright install

echo.
echo ✅ Atualizacao concluida!
pause
"""
        
        with open(scripts_dir / "atualizar_sistema.bat", 'w', encoding='utf-8') as f:
            f.write(update_script)
        
        self.print_success("Scripts batch criados")

    def create_version_info(self):
        """Cria arquivo de informações da versão"""
        self.print_step("Criando informações da versão...")
        
        version_info = {
            "name": "ARQ-ALPHA-V9",
            "version": self.version,
            "description": "Sistema de Análise Ultra-Detalhada com IA e Ferramentas",
            "author": "ARQ-ALPHA-V9 Team",
            "build_date": "2025-10-31",
            "python_version": "3.11+",
            "node_version": "18+",
            "features": [
                "Coleta Massiva Real",
                "Síntese com IA Ativa",
                "Verificação AI",
                "16 Módulos Especializados",
                "Sistema de Logging em Tempo Real",
                "Interface Web Responsiva",
                "Múltiplas APIs de IA",
                "Captura de Screenshots",
                "Análise de Conteúdo Viral"
            ],
            "requirements": {
                "os": "Windows 10/11",
                "python": "3.11+",
                "nodejs": "18+",
                "memory": "4GB RAM mínimo",
                "storage": "2GB espaço livre",
                "internet": "Conexão estável necessária"
            },
            "apis_supported": [
                "OpenAI GPT-4",
                "Anthropic Claude",
                "Google Gemini",
                "Serper Search",
                "Jina AI",
                "Exa Search",
                "Firecrawl",
                "Playwright"
            ]
        }
        
        version_file = self.dist_dir / "ARQ-ALPHA-V9" / "version_info.json"
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, indent=2, ensure_ascii=False)
        
        self.print_success("Informações da versão criadas")

    def create_zip_package(self):
        """Cria pacote ZIP para distribuição"""
        self.print_step("Criando pacote ZIP...")
        
        zip_path = self.dist_dir / f"ARQ-ALPHA-V9-v{self.version}-Completo.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            app_dir = self.dist_dir / "ARQ-ALPHA-V9"
            
            for file_path in app_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.dist_dir)
                    zipf.write(file_path, arcname)
                    print(f"  Adicionado: {arcname}")
        
        # Calcular hash do arquivo
        with open(zip_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Criar arquivo de hash
        hash_file = zip_path.with_suffix('.zip.sha256')
        with open(hash_file, 'w') as f:
            f.write(f"{file_hash}  {zip_path.name}\n")
        
        file_size = zip_path.stat().st_size / (1024 * 1024)  # MB
        
        self.print_success(f"Pacote ZIP criado: {zip_path.name} ({file_size:.1f} MB)")
        print(f"  Hash SHA256: {file_hash}")

    def generate_checksums(self):
        """Gera checksums para todos os arquivos"""
        self.print_step("Gerando checksums...")
        
        checksums = {}
        app_dir = self.dist_dir / "ARQ-ALPHA-V9"
        
        for file_path in app_dir.rglob('*'):
            if file_path.is_file():
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                
                rel_path = file_path.relative_to(app_dir)
                checksums[str(rel_path)] = file_hash
        
        # Salvar checksums
        checksums_file = self.dist_dir / "checksums.json"
        with open(checksums_file, 'w', encoding='utf-8') as f:
            json.dump(checksums, f, indent=2, ensure_ascii=False)
        
        self.print_success(f"Checksums gerados para {len(checksums)} arquivos")

    def run(self):
        """Executa o preparador de distribuição"""
        print("=" * 60)
        print("    ARQ-ALPHA-V9 - PREPARADOR DE DISTRIBUIÇÃO")
        print("=" * 60)
        print()
        
        try:
            # Executar todas as etapas
            self.clean_project()
            
            if not self.verify_dependencies():
                return False
            
            self.create_distribution_structure()
            self.copy_application_files()
            self.create_documentation()
            self.create_batch_scripts()
            self.create_version_info()
            self.generate_checksums()
            self.create_zip_package()
            
            print()
            print("=" * 60)
            print("    DISTRIBUIÇÃO PREPARADA COM SUCESSO!")
            print("=" * 60)
            print()
            print(f"📁 Localização: {self.dist_dir}")
            print(f"📦 Pacote ZIP: ARQ-ALPHA-V9-v{self.version}-Completo.zip")
            print()
            print("🚀 Próximos passos:")
            print("   1. Execute 'criar_executavel.bat' para gerar o instalador")
            print("   2. Teste o instalador em um Windows limpo")
            print("   3. Distribua o pacote ZIP + executável")
            print()
            
            return True
            
        except Exception as e:
            self.print_error(f"Erro durante preparação: {e}")
            return False

def main():
    preparer = DistributionPreparer()
    success = preparer.run()
    
    if success:
        print("✅ Preparação concluída com sucesso!")
    else:
        print("❌ Preparação falhou!")
    
    input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()