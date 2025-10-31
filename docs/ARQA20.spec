# -*- mode: python ; coding: utf-8 -*-
# ARQV30 Enhanced v3.0 - PyInstaller Spec File Aprimorado
# Interface Nativa para Windows com Todos os Sistemas Integrados

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all

block_cipher = None

print("🚀 ARQV30 Enhanced v3.0 - Configuração PyInstaller")
print("=" * 60)

# Detecção automática de dependências críticas
print("🔍 Detectando dependências...")

# Prophet (se disponível)
prophet_data = []
try:
    import prophet
    prophet_dir = os.path.dirname(prophet.__file__)
    prophet_data = [(prophet_dir, 'prophet')]
    print(f"✅ Prophet detectado: {prophet_dir}")
except ImportError:
    print("⚠️ Prophet não encontrado - continuando sem ele")

# Coleta dados de pacotes importantes
print("📦 Coletando dados de pacotes...")
spacy_data = collect_data_files('spacy') if 'spacy' in sys.modules else []
flask_data = collect_data_files('flask') if 'flask' in sys.modules else []

# Coleta dados de PIL/Pillow para interface nativa
pillow_data = []
try:
    pillow_data = collect_data_files('PIL')
    print("✅ PIL/Pillow detectado")
except:
    print("⚠️ PIL/Pillow não encontrado")

# Coleta dados de tkinter (já incluído no Python)
print("✅ Tkinter (interface nativa) disponível")

# Playwright browsers (se disponível)
playwright_browsers_data = []
try:
    browsers_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ms-playwright')
    if os.path.exists(browsers_path):
        playwright_browsers_data = [(browsers_path, 'playwright/driver/package/.local-browsers')]
        print(f"✅ Playwright browsers encontrados: {browsers_path}")
    else:
        print("⚠️ Playwright browsers não encontrados - continuando sem eles")
except:
    print("⚠️ Erro ao detectar Playwright - continuando sem ele")

# Hidden imports críticos - ARQV30 Enhanced v3.0
print("🔧 Configurando hidden imports...")
hidden_imports = [
    # Interface Nativa
    'tkinter', 'tkinter.ttk', 'tkinter.font', 'tkinter.messagebox', 
    'tkinter.filedialog', 'tkinter.scrolledtext',
    
    # Manipulação de Imagens (Interface Nativa)
    'PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL.ImageDraw', 'PIL.ImageFont',
    
    # Threading (Interface Nativa)
    'threading', 'queue',
    
    # Flask (Interface Web - Opcional)
    'flask', 'flask_cors', 'flask_socketio',
    'werkzeug', 'jinja2', 'markupsafe',
    
    # HTTP e Requests
    'requests', 'urllib3', 'certifi', 'httpx',
    
    # Análise de Dados
    'pandas', 'numpy', 'scipy',
    
    # Web Scraping
    'selenium', 'selenium.webdriver',
    'beautifulsoup4', 'bs4',
    'lxml', 'lxml.etree',
    'playwright', 'playwright.sync_api',
    
    # NLP e Análise de Texto
    'spacy', 'spacy.cli',
    'nltk', 'textblob', 'vaderSentiment',
    
    # APIs de IA
    'openai', 'anthropic',
    'google.generativeai', 'groq',
    
    # Configuração
    'yaml', 'pyyaml',
    'dotenv', 'python-dotenv',
    
    # Async
    'aiohttp', 'aiofiles', 'asyncio',
    
    # Banco de Dados
    'supabase', 'postgrest',
    
    # Documentos e Relatórios
    'PyPDF2', 'reportlab', 'openpyxl',
    
    # Gráficos e Visualização
    'matplotlib', 'matplotlib.pyplot', 'matplotlib.backends.backend_tkagg',
    'seaborn', 'plotly', 'plotly.graph_objects', 'plotly.express',
    
    # Machine Learning
    'sklearn', 'scikit-learn',
    
    # Visão Computacional
    'cv2', 'pytesseract',
    
    # WebDriver
    'webdriver_manager',
    
    # Prophet (se disponível)
    'prophet',
    
    # Módulos do ARQV30 Enhanced v3.0
    'services',
    'services.enhanced_systems_integration',
    'services.avatar_image_generator',
    'services.competitor_content_collector',
    'services.sales_funnel_chart_generator',
    'services.external_ai_integration',
    'services.realtime_logger',
    'services.environment_loader',
    'services.health_checker',
    
    'routes',
    'routes.analysis',
    'routes.enhanced_analysis',
    'routes.files',
    'routes.progress',
    'routes.user',
    'routes.enhanced_workflow',
    'routes.sessions',
    'routes.chat',
    
    'engine',
    'utils',
    'utils.logo_manager',
    
    'ubie',
    'ubie.agent',
    'ubie.services',
    'ubie.config',
    
    'database',
    
    # External AI Verifier
    'external_ai_verifier',
    'external_ai_verifier.src',
    'external_ai_verifier.src.external_review_agent',
    'external_ai_verifier.src.services',
    'external_ai_verifier.src.services.external_sentiment_analyzer',
    'external_ai_verifier.src.services.external_bias_disinformation_detector',
    'external_ai_verifier.src.services.external_llm_reasoning_service',
    'external_ai_verifier.src.services.external_rule_engine',
    'external_ai_verifier.src.services.external_contextual_analyzer',
    'external_ai_verifier.src.services.external_confidence_thresholds',
]

print(f"✅ {len(hidden_imports)} hidden imports configurados")

# Configuração de arquivos de dados
print("📁 Configurando arquivos de dados...")

# Arquivos de dados essenciais
essential_data = [
    # Interface Web (Flask) - Opcional
    ('src/templates', 'templates'),
    ('src/static', 'static'),
    
    # Configurações
    ('.env', '.'),
    
    # External AI Verifier
    ('external_ai_verifier', 'external_ai_verifier'),
    
    # Interface Nativa (arquivo principal)
    ('native_windows_app.py', '.'),
    
    # Arquivos de sistema gerados
    ('avatar_enhanced_dr_ricardo.png', '.'),
    ('funnel_1_marketing_digital.png', '.'),
    ('funnel_2_ecommerce.png', '.'),
    ('funnel_3_consultoria.png', '.'),
]

# Arquivos opcionais (se existirem)
optional_data = []
optional_files = [
    ('src/engine/pt_core_news_sm-3.8.0-py3-none-any.whl', 'engine'),
    ('requirements.txt', '.'),
    ('install.bat', '.'),
    ('run.bat', '.'),
]

for src, dst in optional_files:
    if os.path.exists(src):
        optional_data.append((src, dst))
        print(f"✅ Arquivo opcional encontrado: {src}")

# Combina todos os dados
all_data = essential_data + optional_data + spacy_data + flask_data + prophet_data + pillow_data + playwright_browsers_data

print(f"✅ {len(all_data)} arquivos de dados configurados")

# Configuração principal do Analysis
print("⚙️ Configurando Analysis...")

a = Analysis(
    # Arquivo principal - Interface Nativa
    ['native_windows_app.py'],
    
    # Caminhos adicionais
    pathex=['src', 'external_ai_verifier/src'],
    
    # Binários (vazios por padrão)
    binaries=[],
    
    # Dados
    datas=all_data,
    
    # Hidden imports
    hiddenimports=hidden_imports,
    
    # Hooks
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    
    # Exclusões (removemos tkinter da exclusão pois precisamos dele)
    excludes=['matplotlib.tests', 'numpy.tests', 'pytest', 'unittest'],
    
    # Configurações Windows
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

print("🔧 Configurando PYZ...")
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

print("🔧 Configurando EXE...")
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ARQV30_Enhanced_v3_Native',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Interface nativa - sem console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/static/favicon.ico' if os.path.exists('src/static/favicon.ico') else None,
    version_file=None,  # Pode adicionar arquivo de versão aqui
)

print("🔧 Configurando COLLECT...")
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ARQV30_Enhanced_v3_Native',
)

print("=" * 60)
print("✅ CONFIGURAÇÃO PYINSTALLER CONCLUÍDA!")
print("=" * 60)
print("📦 Nome do executável: ARQV30_Enhanced_v3_Native.exe")
print("🎯 Interface: Nativa para Windows (tkinter)")
print("🔧 Modo: Windowed (sem console)")
print("📁 Pasta de saída: dist/ARQV30_Enhanced_v3_Native/")
print("=" * 60)
print("🚀 Para compilar execute: pyinstaller ARQA20.spec")
print("=" * 60)