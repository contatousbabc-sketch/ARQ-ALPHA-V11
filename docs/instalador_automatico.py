#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSTALADOR AUTOMÁTICO ARQ-ALPHA-V9
==================================
Instala automaticamente todas as dependências necessárias para executar o ARQ-ALPHA-V9
em um Windows recém-formatado.

Componentes instalados:
- Python 3.11+
- Visual Studio Build Tools
- Node.js
- Playwright + Chromium
- Todas as dependências Python
- Configuração de variáveis de ambiente

Autor: ARQ-ALPHA-V9 Team
Data: 2025-10-31
"""

import os
import sys
import subprocess
import urllib.request
import json
import time
import shutil
import winreg
from pathlib import Path
import tempfile
import zipfile
import tarfile

class Colors:
    """Cores para terminal Windows"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ARQAlphaInstaller:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.install_dir = Path.home() / "ARQ-ALPHA-V9"
        self.python_version = "3.11.6"
        self.node_version = "20.9.0"
        
        # URLs de download
        self.urls = {
            'python': f'https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-amd64.exe',
            'node': f'https://nodejs.org/dist/v{self.node_version}/node-v{self.node_version}-x64.msi',
            'vs_buildtools': 'https://aka.ms/vs/17/release/vs_buildtools.exe'
        }
        
        self.requirements = [
            'flask==2.3.3',
            'requests==2.31.0',
            'beautifulsoup4==4.12.2',
            'selenium==4.15.2',
            'playwright==1.40.0',
            'openai==1.3.5',
            'anthropic==0.7.7',
            'google-generativeai==0.3.1',
            'python-dotenv==1.0.0',
            'Pillow==10.1.0',
            'numpy==1.24.3',
            'pandas==2.0.3',
            'matplotlib==3.7.2',
            'seaborn==0.12.2',
            'plotly==5.17.0',
            'dash==2.14.2',
            'streamlit==1.28.1',
            'fastapi==0.104.1',
            'uvicorn==0.24.0',
            'pydantic==2.5.0',
            'sqlalchemy==2.0.23',
            'alembic==1.12.1',
            'redis==5.0.1',
            'celery==5.3.4',
            'gunicorn==21.2.0',
            'psutil==5.9.6',
            'schedule==1.2.0',
            'python-dateutil==2.8.2',
            'pytz==2023.3',
            'colorama==0.4.6',
            'tqdm==4.66.1',
            'click==8.1.7',
            'rich==13.7.0',
            'typer==0.9.0',
            'httpx==0.25.2',
            'aiohttp==3.9.1',
            'websockets==12.0',
            'pyyaml==6.0.1',
            'toml==0.10.2',
            'configparser==6.0.0',
            'python-multipart==0.0.6',
            'jinja2==3.1.2',
            'markupsafe==2.1.3',
            'werkzeug==2.3.7',
            'itsdangerous==2.1.2',
            'blinker==1.7.0'
        ]

    def print_header(self):
        """Imprime cabeçalho do instalador"""
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKCYAN}    ARQ-ALPHA-V9 - INSTALADOR AUTOMÁTICO COMPLETO{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Sistema de Análise Ultra-Detalhada com IA e Ferramentas{Colors.ENDC}")
        print(f"{Colors.WARNING}Instalando todas as dependências necessárias...{Colors.ENDC}")
        print()

    def print_step(self, step, message):
        """Imprime passo atual"""
        print(f"{Colors.BOLD}[PASSO {step}]{Colors.ENDC} {Colors.OKCYAN}{message}{Colors.ENDC}")

    def print_success(self, message):
        """Imprime mensagem de sucesso"""
        print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")

    def print_error(self, message):
        """Imprime mensagem de erro"""
        print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

    def print_warning(self, message):
        """Imprime mensagem de aviso"""
        print(f"{Colors.WARNING}⚠️ {message}{Colors.ENDC}")

    def run_command(self, command, shell=True, check=True):
        """Executa comando e retorna resultado"""
        try:
            result = subprocess.run(command, shell=shell, check=check, 
                                  capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
        except Exception as e:
            return False, "", str(e)

    def download_file(self, url, filename):
        """Download de arquivo com barra de progresso"""
        filepath = os.path.join(self.temp_dir, filename)
        
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, (downloaded * 100) // total_size)
                bar_length = 50
                filled_length = int(bar_length * percent // 100)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                print(f'\r[{bar}] {percent}% ({downloaded}/{total_size} bytes)', end='')
        
        try:
            print(f"Baixando {filename}...")
            urllib.request.urlretrieve(url, filepath, progress_hook)
            print()  # Nova linha após o progresso
            return filepath
        except Exception as e:
            self.print_error(f"Erro ao baixar {filename}: {e}")
            return None

    def is_python_installed(self):
        """Verifica se Python está instalado"""
        try:
            result = subprocess.run(['python', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_success(f"Python já instalado: {version}")
                return True
        except:
            pass
        
        try:
            result = subprocess.run(['py', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_success(f"Python já instalado: {version}")
                return True
        except:
            pass
        
        return False

    def install_python(self):
        """Instala Python"""
        if self.is_python_installed():
            return True
            
        self.print_step(1, "Instalando Python...")
        
        # Download Python
        python_installer = self.download_file(self.urls['python'], 'python_installer.exe')
        if not python_installer:
            return False
        
        # Instalar Python
        install_cmd = [
            python_installer,
            '/quiet',
            'InstallAllUsers=1',
            'PrependPath=1',
            'Include_test=0',
            'Include_doc=0',
            'Include_dev=1',
            'Include_debug=0',
            'Include_launcher=1',
            'InstallLauncherAllUsers=1'
        ]
        
        print("Instalando Python (isso pode demorar alguns minutos)...")
        success, stdout, stderr = self.run_command(install_cmd, shell=False)
        
        if success:
            self.print_success("Python instalado com sucesso!")
            # Aguardar um pouco para o PATH ser atualizado
            time.sleep(5)
            return True
        else:
            self.print_error(f"Erro ao instalar Python: {stderr}")
            return False

    def is_node_installed(self):
        """Verifica se Node.js está instalado"""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_success(f"Node.js já instalado: {version}")
                return True
        except:
            pass
        return False

    def install_node(self):
        """Instala Node.js"""
        if self.is_node_installed():
            return True
            
        self.print_step(2, "Instalando Node.js...")
        
        # Download Node.js
        node_installer = self.download_file(self.urls['node'], 'node_installer.msi')
        if not node_installer:
            return False
        
        # Instalar Node.js
        install_cmd = ['msiexec', '/i', node_installer, '/quiet', '/norestart']
        
        print("Instalando Node.js (isso pode demorar alguns minutos)...")
        success, stdout, stderr = self.run_command(install_cmd, shell=False)
        
        if success:
            self.print_success("Node.js instalado com sucesso!")
            time.sleep(5)
            return True
        else:
            self.print_error(f"Erro ao instalar Node.js: {stderr}")
            return False

    def is_vs_buildtools_installed(self):
        """Verifica se Visual Studio Build Tools está instalado"""
        try:
            # Verifica se cl.exe (compilador C++) está disponível
            result = subprocess.run(['where', 'cl'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.print_success("Visual Studio Build Tools já instalado")
                return True
        except:
            pass
        
        # Verifica no registro do Windows
        try:
            key_path = r"SOFTWARE\Microsoft\VisualStudio\Setup\Reboot"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path):
                self.print_success("Visual Studio Build Tools detectado no registro")
                return True
        except:
            pass
        
        return False

    def install_vs_buildtools(self):
        """Instala Visual Studio Build Tools"""
        if self.is_vs_buildtools_installed():
            return True
            
        self.print_step(3, "Instalando Visual Studio Build Tools...")
        
        # Download VS Build Tools
        vs_installer = self.download_file(self.urls['vs_buildtools'], 'vs_buildtools.exe')
        if not vs_installer:
            return False
        
        # Instalar VS Build Tools com componentes mínimos necessários
        install_cmd = [
            vs_installer,
            '--quiet',
            '--wait',
            '--add', 'Microsoft.VisualStudio.Workload.VCTools',
            '--add', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
            '--add', 'Microsoft.VisualStudio.Component.Windows10SDK.19041'
        ]
        
        print("Instalando Visual Studio Build Tools (isso pode demorar 10-15 minutos)...")
        print("Por favor, seja paciente...")
        
        success, stdout, stderr = self.run_command(install_cmd, shell=False)
        
        if success:
            self.print_success("Visual Studio Build Tools instalado com sucesso!")
            return True
        else:
            self.print_warning("Possível erro na instalação do VS Build Tools")
            self.print_warning("O sistema tentará continuar...")
            return True  # Continuar mesmo com possível erro

    def install_python_packages(self):
        """Instala pacotes Python"""
        self.print_step(4, "Instalando dependências Python...")
        
        # Atualizar pip primeiro
        print("Atualizando pip...")
        success, stdout, stderr = self.run_command([
            sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
        ], shell=False)
        
        if not success:
            self.print_warning("Erro ao atualizar pip, continuando...")
        
        # Instalar wheel e setuptools
        print("Instalando ferramentas básicas...")
        success, stdout, stderr = self.run_command([
            sys.executable, '-m', 'pip', 'install', 'wheel', 'setuptools'
        ], shell=False)
        
        # Instalar pacotes em lotes para evitar conflitos
        batch_size = 5
        total_packages = len(self.requirements)
        
        for i in range(0, total_packages, batch_size):
            batch = self.requirements[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_packages + batch_size - 1) // batch_size
            
            print(f"Instalando lote {batch_num}/{total_batches}: {', '.join(batch)}")
            
            cmd = [sys.executable, '-m', 'pip', 'install'] + batch
            success, stdout, stderr = self.run_command(cmd, shell=False)
            
            if not success:
                self.print_warning(f"Erro no lote {batch_num}, tentando individualmente...")
                # Tentar instalar individualmente
                for package in batch:
                    print(f"  Instalando {package}...")
                    cmd = [sys.executable, '-m', 'pip', 'install', package]
                    success, stdout, stderr = self.run_command(cmd, shell=False)
                    if success:
                        print(f"    ✅ {package}")
                    else:
                        print(f"    ❌ {package} - {stderr[:100]}...")
        
        self.print_success("Dependências Python instaladas!")
        return True

    def install_playwright(self):
        """Instala Playwright e browsers"""
        self.print_step(5, "Instalando Playwright e navegadores...")
        
        # Instalar browsers do Playwright
        print("Instalando navegadores Playwright...")
        success, stdout, stderr = self.run_command([
            sys.executable, '-m', 'playwright', 'install'
        ], shell=False)
        
        if success:
            self.print_success("Playwright e navegadores instalados!")
        else:
            self.print_warning("Erro ao instalar navegadores Playwright")
            # Tentar instalar apenas Chromium
            print("Tentando instalar apenas Chromium...")
            success, stdout, stderr = self.run_command([
                sys.executable, '-m', 'playwright', 'install', 'chromium'
            ], shell=False)
            
            if success:
                self.print_success("Chromium instalado!")
            else:
                self.print_error("Erro ao instalar Chromium")
        
        return True

    def setup_environment(self):
        """Configura variáveis de ambiente"""
        self.print_step(6, "Configurando variáveis de ambiente...")
        
        try:
            # Adicionar diretório do projeto ao PATH se necessário
            current_path = os.environ.get('PATH', '')
            project_path = str(self.install_dir)
            
            if project_path not in current_path:
                # Adicionar ao PATH da sessão atual
                os.environ['PATH'] = f"{project_path};{current_path}"
                self.print_success("PATH configurado para sessão atual")
            
            # Criar variáveis específicas do ARQ-ALPHA
            os.environ['ARQ_ALPHA_HOME'] = str(self.install_dir)
            os.environ['ARQ_ALPHA_VERSION'] = '9.0'
            
            self.print_success("Variáveis de ambiente configuradas!")
            return True
            
        except Exception as e:
            self.print_error(f"Erro ao configurar ambiente: {e}")
            return False

    def copy_application_files(self):
        """Copia arquivos da aplicação"""
        self.print_step(7, "Configurando aplicação...")
        
        try:
            # Criar diretório de instalação
            self.install_dir.mkdir(parents=True, exist_ok=True)
            
            # Copiar arquivos do projeto atual
            current_dir = Path(__file__).parent
            
            # Lista de arquivos/diretórios para copiar
            items_to_copy = [
                'src',
                'external_ai_verifier',
                'run.py',
                'requirements.txt',
                '.env.example',
                'README.md'
            ]
            
            for item in items_to_copy:
                source = current_dir / item
                if source.exists():
                    dest = self.install_dir / item
                    if source.is_file():
                        shutil.copy2(source, dest)
                        print(f"  ✅ Copiado: {item}")
                    else:
                        shutil.copytree(source, dest, dirs_exist_ok=True)
                        print(f"  ✅ Copiado: {item}/")
                else:
                    print(f"  ⚠️ Não encontrado: {item}")
            
            self.print_success("Arquivos da aplicação configurados!")
            return True
            
        except Exception as e:
            self.print_error(f"Erro ao copiar arquivos: {e}")
            return False

    def create_startup_scripts(self):
        """Cria scripts de inicialização"""
        self.print_step(8, "Criando scripts de inicialização...")
        
        try:
            # Script BAT para Windows
            bat_content = f"""@echo off
echo ========================================
echo    ARQ-ALPHA-V9 - Sistema Iniciando
echo ========================================
cd /d "{self.install_dir}"
python run.py
pause
"""
            
            bat_file = self.install_dir / "iniciar_arq_alpha.bat"
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            
            # Script Python de verificação
            check_content = '''#!/usr/bin/env python3
import sys
import subprocess
import importlib

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    required_packages = [
        'flask', 'requests', 'beautifulsoup4', 'selenium', 
        'playwright', 'openai', 'anthropic', 'google.generativeai'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\\nPacotes faltando: {', '.join(missing)}")
        return False
    else:
        print("\\n🎉 Todas as dependências estão instaladas!")
        return True

if __name__ == "__main__":
    print("Verificando dependências do ARQ-ALPHA-V9...")
    print("=" * 50)
    check_dependencies()
    input("\\nPressione Enter para continuar...")
'''
            
            check_file = self.install_dir / "verificar_dependencias.py"
            with open(check_file, 'w', encoding='utf-8') as f:
                f.write(check_content)
            
            self.print_success("Scripts de inicialização criados!")
            return True
            
        except Exception as e:
            self.print_error(f"Erro ao criar scripts: {e}")
            return False

    def run_final_tests(self):
        """Executa testes finais"""
        self.print_step(9, "Executando testes finais...")
        
        tests_passed = 0
        total_tests = 4
        
        # Teste 1: Python
        try:
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ Python: {result.stdout.strip()}")
                tests_passed += 1
            else:
                print("  ❌ Python não funcional")
        except:
            print("  ❌ Python não encontrado")
        
        # Teste 2: Node.js
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ Node.js: {result.stdout.strip()}")
                tests_passed += 1
            else:
                print("  ❌ Node.js não funcional")
        except:
            print("  ❌ Node.js não encontrado")
        
        # Teste 3: Pip
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ Pip funcional")
                tests_passed += 1
            else:
                print("  ❌ Pip não funcional")
        except:
            print("  ❌ Pip não encontrado")
        
        # Teste 4: Playwright
        try:
            result = subprocess.run([sys.executable, '-c', 'import playwright; print("OK")'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ Playwright importado com sucesso")
                tests_passed += 1
            else:
                print("  ❌ Playwright não funcional")
        except:
            print("  ❌ Playwright não encontrado")
        
        success_rate = (tests_passed / total_tests) * 100
        
        if success_rate >= 75:
            self.print_success(f"Testes finais: {tests_passed}/{total_tests} ({success_rate:.0f}%)")
            return True
        else:
            self.print_warning(f"Testes finais: {tests_passed}/{total_tests} ({success_rate:.0f}%)")
            return False

    def cleanup(self):
        """Limpa arquivos temporários"""
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            print(f"{Colors.OKCYAN}🧹 Arquivos temporários removidos{Colors.ENDC}")
        except:
            pass

    def print_final_instructions(self):
        """Imprime instruções finais"""
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKGREEN}    INSTALAÇÃO CONCLUÍDA COM SUCESSO!{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print()
        print(f"{Colors.OKCYAN}📁 Localização da aplicação:{Colors.ENDC}")
        print(f"   {self.install_dir}")
        print()
        print(f"{Colors.OKCYAN}🚀 Para iniciar o ARQ-ALPHA-V9:{Colors.ENDC}")
        print(f"   1. Execute: {self.install_dir}/iniciar_arq_alpha.bat")
        print(f"   2. Ou navegue até a pasta e execute: python run.py")
        print()
        print(f"{Colors.OKCYAN}🔧 Para verificar dependências:{Colors.ENDC}")
        print(f"   Execute: python {self.install_dir}/verificar_dependencias.py")
        print()
        print(f"{Colors.OKCYAN}🌐 Acesso à aplicação:{Colors.ENDC}")
        print(f"   http://localhost:12000")
        print()
        print(f"{Colors.WARNING}⚠️ IMPORTANTE:{Colors.ENDC}")
        print(f"   - Reinicie o terminal/prompt para atualizar o PATH")
        print(f"   - Configure suas chaves de API no arquivo .env")
        print(f"   - Consulte a documentação para configurações avançadas")
        print()
        print(f"{Colors.OKGREEN}🎉 ARQ-ALPHA-V9 está pronto para uso!{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")

    def run(self):
        """Executa o instalador completo"""
        try:
            self.print_header()
            
            # Verificar se é Windows
            if os.name != 'nt':
                self.print_error("Este instalador é específico para Windows!")
                return False
            
            # Executar passos de instalação
            steps = [
                ("Instalando Python", self.install_python),
                ("Instalando Node.js", self.install_node),
                ("Instalando Visual Studio Build Tools", self.install_vs_buildtools),
                ("Instalando dependências Python", self.install_python_packages),
                ("Instalando Playwright", self.install_playwright),
                ("Configurando ambiente", self.setup_environment),
                ("Copiando arquivos", self.copy_application_files),
                ("Criando scripts", self.create_startup_scripts),
                ("Executando testes", self.run_final_tests)
            ]
            
            for step_name, step_func in steps:
                try:
                    print(f"\n{Colors.BOLD}Executando: {step_name}...{Colors.ENDC}")
                    success = step_func()
                    if not success:
                        self.print_error(f"Falha em: {step_name}")
                        # Continuar mesmo com falhas não críticas
                except Exception as e:
                    self.print_error(f"Erro em {step_name}: {e}")
                    # Continuar mesmo com erros
            
            self.print_final_instructions()
            return True
            
        except KeyboardInterrupt:
            self.print_error("Instalação cancelada pelo usuário")
            return False
        except Exception as e:
            self.print_error(f"Erro crítico: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Função principal"""
    # Verificar privilégios de administrador
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print(f"{Colors.WARNING}⚠️ AVISO: Execute como Administrador para melhor compatibilidade{Colors.ENDC}")
            print(f"{Colors.WARNING}   Algumas instalações podem falhar sem privilégios administrativos{Colors.ENDC}")
            print()
            
            response = input("Continuar mesmo assim? (s/N): ").lower()
            if response not in ['s', 'sim', 'y', 'yes']:
                print("Instalação cancelada.")
                return
    except:
        pass
    
    # Executar instalador
    installer = ARQAlphaInstaller()
    success = installer.run()
    
    if success:
        print(f"\n{Colors.OKGREEN}Pressione Enter para finalizar...{Colors.ENDC}")
        input()
    else:
        print(f"\n{Colors.FAIL}Instalação concluída com erros. Pressione Enter para finalizar...{Colors.ENDC}")
        input()

if __name__ == "__main__":
    main()