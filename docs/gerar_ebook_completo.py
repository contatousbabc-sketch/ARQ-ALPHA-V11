#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERADOR DE EBOOK COMPLETO ARQ-ALPHA-V9
======================================
Gera um ebook HTML completo e detalhado com todos os capítulos,
códigos comentados, estruturas de arquivos e documentação técnica.

Autor: ARQ-ALPHA-V9 Team
Data: 2025-10-31
"""

import os
import json
from pathlib import Path
import ast
import re

class EbookGenerator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.src_dir = self.project_root / "src"
        self.external_ai_dir = self.project_root / "external_ai_verifier"
        
    def analyze_python_file(self, file_path):
        """Analisa um arquivo Python e extrai informações"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            info = {
                'imports': [],
                'classes': [],
                'functions': [],
                'variables': [],
                'docstring': ast.get_docstring(tree) or "Sem documentação disponível"
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        info['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        info['imports'].append(f"{module}.{alias.name}")
                elif isinstance(node, ast.ClassDef):
                    info['classes'].append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or "Sem documentação",
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
                elif isinstance(node, ast.FunctionDef) and not any(node in cls.body for cls in ast.walk(tree) if isinstance(cls, ast.ClassDef)):
                    info['functions'].append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or "Sem documentação",
                        'args': [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            info['variables'].append(target.id)
            
            return info, content
            
        except Exception as e:
            return {'error': str(e)}, ""

    def generate_file_structure(self):
        """Gera estrutura de arquivos do projeto"""
        structure = []
        
        def scan_directory(path, prefix="", max_depth=3, current_depth=0):
            if current_depth > max_depth:
                return
                
            try:
                items = sorted(path.iterdir())
                for item in items:
                    if item.name.startswith('.'):
                        continue
                        
                    if item.is_dir():
                        structure.append(f"{prefix}📁 {item.name}/")
                        if current_depth < max_depth:
                            scan_directory(item, prefix + "  ", max_depth, current_depth + 1)
                    else:
                        icon = "🐍" if item.suffix == ".py" else "📄" if item.suffix in [".html", ".css", ".js"] else "📋" if item.suffix in [".txt", ".md", ".json"] else "⚙️" if item.suffix in [".bat", ".sh"] else "📄"
                        structure.append(f"{prefix}{icon} {item.name}")
            except PermissionError:
                structure.append(f"{prefix}❌ Acesso negado")
        
        scan_directory(self.project_root)
        return "\n".join(structure)

    def generate_architecture_chapter(self):
        """Gera capítulo de arquitetura"""
        return '''
            <div class="chapter" id="architecture">
                <div class="chapter-header">
                    <h1 class="chapter-title">🏗️ Arquitetura</h1>
                    <p class="chapter-subtitle">Estrutura Técnica Detalhada do Sistema</p>
                </div>

                <div class="section">
                    <h2>Visão Geral da Arquitetura</h2>
                    <p>O ARQ-ALPHA-V9 segue uma arquitetura modular baseada em microserviços, com separação clara de responsabilidades e alta coesão entre componentes.</p>

                    <div class="code-block" data-lang="text">
┌─────────────────────────────────────────────────────────────┐
│                 CAMADA DE APRESENTAÇÃO                      │
├─────────────────────────────────────────────────────────────┤
│  Frontend Web (HTML5/CSS3/JavaScript ES6+)                 │
│  ├── Interface de Configuração                              │
│  ├── Dashboard de Monitoramento em Tempo Real               │
│  ├── Visualização de Resultados Interativa                 │
│  └── Sistema de Gerenciamento de Sessões                   │
├─────────────────────────────────────────────────────────────┤
│                 CAMADA DE APLICAÇÃO                         │
├─────────────────────────────────────────────────────────────┤
│  Flask Application Server                                   │
│  ├── Routes (API Endpoints)                                │
│  │   ├── /api/workflow/* (Workflow Management)             │
│  │   ├── /api/sessions/* (Session Management)              │
│  │   └── /api/results/* (Results Retrieval)               │
│  ├── Enhanced Workflow (Orquestrador Principal)            │
│  │   ├── Step 1: Massive Data Collection                   │
│  │   ├── Step 2: AI-Powered Synthesis                      │
│  │   └── Step 3: 16-Module Generation                      │
│  └── Middleware & Authentication                           │
├─────────────────────────────────────────────────────────────┤
│                 CAMADA DE SERVIÇOS                          │
├─────────────────────────────────────────────────────────────┤
│  Core Services                                              │
│  ├── Viral Integration Service                             │
│  │   ├── Instagram Content Scraper                         │
│  │   ├── TikTok Trend Analyzer                            │
│  │   └── Twitter/X Viral Content Detector                 │
│  ├── Enhanced Synthesis Engine                             │
│  │   ├── Multi-Model AI Orchestrator                      │
│  │   ├── Context-Aware Processing                         │
│  │   └── Quality Assurance Pipeline                       │
│  ├── Auto Save Manager                                     │
│  │   ├── Session State Persistence                        │
│  │   ├── Incremental Backup System                        │
│  │   └── Recovery Mechanisms                              │
│  └── Real-Time Logging System                             │
│      ├── Session-Specific Logging                         │
│      ├── Code Execution Tracking                          │
│      └── Performance Monitoring                           │
├─────────────────────────────────────────────────────────────┤
│                 CAMADA DE VERIFICAÇÃO                       │
├─────────────────────────────────────────────────────────────┤
│  External AI Verifier (Módulo Independente)                │
│  ├── Sentiment Analyzer                                    │
│  │   ├── VADER Sentiment Analysis                          │
│  │   └── TextBlob Polarity Detection                       │
│  ├── Bias & Disinformation Detector                        │
│  │   ├── Content Authenticity Verification                │
│  │   └── Source Credibility Assessment                     │
│  ├── LLM Reasoning Service                                 │
│  │   ├── Multi-Provider Support (Gemini, GPT, Claude)     │
│  │   ├── Rate Limiting & API Management                    │
│  │   └── Response Quality Validation                       │
│  ├── Rule Engine                                           │
│  │   ├── Configurable Quality Rules                       │
│  │   └── Dynamic Threshold Adjustment                      │
│  ├── Contextual Analyzer                                   │
│  │   ├── Domain-Specific Context Understanding            │
│  │   └── Cross-Reference Validation                        │
│  └── Confidence Thresholds                                │
│      ├── Multi-Level Confidence Scoring                   │
│      └── Adaptive Threshold Management                     │
├─────────────────────────────────────────────────────────────┤
│                 CAMADA DE INTEGRAÇÃO                        │
├─────────────────────────────────────────────────────────────┤
│  External APIs & Services                                   │
│  ├── AI/ML APIs                                            │
│  │   ├── OpenAI GPT-4 & GPT-3.5-Turbo                    │
│  │   ├── Anthropic Claude 3.5 Sonnet                      │
│  │   ├── Google Gemini Pro & Flash                        │
│  │   └── Fallback & Load Balancing                        │
│  ├── Search & Data APIs                                    │
│  │   ├── Serper (Google Search API)                       │
│  │   ├── Jina AI (Content Extraction)                     │
│  │   ├── Exa (Semantic Search)                            │
│  │   ├── Firecrawl (Web Scraping)                         │
│  │   └── RapidAPI (Multiple Providers)                    │
│  ├── Web Automation                                        │
│  │   ├── Playwright (Browser Automation)                  │
│  │   ├── Selenium (Legacy Support)                        │
│  │   └── Screenshot Capture System                        │
│  └── Social Media APIs                                     │
│      ├── Instagram Basic Display API                       │
│      ├── Twitter API v2                                    │
│      └── TikTok Research API                              │
├─────────────────────────────────────────────────────────────┤
│                 CAMADA DE DADOS                             │
├─────────────────────────────────────────────────────────────┤
│  Data Storage & Management                                  │
│  ├── Session Data Storage                                  │
│  │   ├── JSON-based Session Files                         │
│  │   ├── Hierarchical Directory Structure                 │
│  │   └── Automated Cleanup & Archiving                    │
│  ├── Intermediate Results Storage                          │
│  │   ├── Step-by-Step Result Caching                      │
│  │   ├── Screenshot & Media Storage                       │
│  │   └── Temporary File Management                        │
│  ├── Configuration Management                              │
│  │   ├── Environment Variables (.env)                     │
│  │   ├── YAML Configuration Files                         │
│  │   └── Runtime Configuration Updates                    │
│  └── Logging & Monitoring Data                            │
│      ├── Real-Time Log Files                              │
│      ├── Performance Metrics                              │
│      └── Error Tracking & Reporting                       │
└─────────────────────────────────────────────────────────────┘</div>

                    <h3>Princípios Arquiteturais</h3>
                    <div class="success-box">
                        <h4>Modularidade</h4>
                        <p>Cada componente tem responsabilidades bem definidas e interfaces claras, permitindo manutenção e evolução independentes.</p>
                        
                        <h4>Escalabilidade</h4>
                        <p>Arquitetura preparada para crescimento horizontal com suporte a múltiplas sessões simultâneas.</p>
                        
                        <h4>Resiliência</h4>
                        <p>Sistema de fallback para APIs, recuperação automática de falhas e persistência de estado.</p>
                        
                        <h4>Observabilidade</h4>
                        <p>Logging detalhado, monitoramento em tempo real e rastreamento completo de execução.</p>
                    </div>
                </div>

                <div class="section">
                    <h2>Componentes Principais</h2>
                    
                    <h3>1. Enhanced Workflow (Orquestrador)</h3>
                    <div class="info-box">
                        <h4>Localização</h4>
                        <p><code>src/routes/enhanced_workflow.py</code></p>
                        
                        <h4>Responsabilidades</h4>
                        <ul>
                            <li>Orquestração das 3 etapas do workflow</li>
                            <li>Gerenciamento de estado das sessões</li>
                            <li>Coordenação entre serviços</li>
                            <li>Tratamento de erros e recuperação</li>
                            <li>Logging e monitoramento</li>
                        </ul>
                        
                        <h4>Endpoints Principais</h4>
                        <ul>
                            <li><code>POST /api/workflow/start_step1</code> - Inicia coleta massiva</li>
                            <li><code>POST /api/workflow/start_step2</code> - Inicia síntese IA</li>
                            <li><code>POST /api/workflow/start_step3</code> - Inicia geração de módulos</li>
                            <li><code>POST /api/workflow/external_ai_verification</code> - Verificação AI</li>
                            <li><code>GET /api/workflow/status/{session_id}</code> - Status da sessão</li>
                        </ul>
                    </div>

                    <h3>2. Viral Integration Service</h3>
                    <div class="info-box">
                        <h4>Localização</h4>
                        <p><code>src/services/viral_integration.py</code></p>
                        
                        <h4>Responsabilidades</h4>
                        <ul>
                            <li>Busca de conteúdo viral em redes sociais</li>
                            <li>Análise de engagement e métricas</li>
                            <li>Extração de tendências</li>
                            <li>Captura de screenshots</li>
                        </ul>
                        
                        <h4>Plataformas Suportadas</h4>
                        <ul>
                            <li>Instagram (via Basic Display API)</li>
                            <li>TikTok (via Research API)</li>
                            <li>Twitter/X (via API v2)</li>
                            <li>YouTube (via Data API)</li>
                        </ul>
                    </div>

                    <h3>3. Enhanced Synthesis Engine</h3>
                    <div class="info-box">
                        <h4>Localização</h4>
                        <p><code>src/services/enhanced_synthesis_engine.py</code></p>
                        
                        <h4>Responsabilidades</h4>
                        <ul>
                            <li>Processamento de dados coletados</li>
                            <li>Orquestração de múltiplos modelos de IA</li>
                            <li>Síntese e estruturação de informações</li>
                            <li>Validação de qualidade</li>
                        </ul>
                        
                        <h4>Modelos de IA Integrados</h4>
                        <ul>
                            <li>OpenAI GPT-4 (Análise principal)</li>
                            <li>Anthropic Claude 3.5 (Verificação)</li>
                            <li>Google Gemini Pro (Síntese)</li>
                        </ul>
                    </div>

                    <h3>4. External AI Verifier</h3>
                    <div class="info-box">
                        <h4>Localização</h4>
                        <p><code>external_ai_verifier/src/</code></p>
                        
                        <h4>Responsabilidades</h4>
                        <ul>
                            <li>Verificação independente de qualidade</li>
                            <li>Análise de sentimento e viés</li>
                            <li>Validação por múltiplas camadas de IA</li>
                            <li>Aplicação de regras de qualidade</li>
                        </ul>
                        
                        <h4>Componentes</h4>
                        <ul>
                            <li>ExternalReviewAgent (Agente principal)</li>
                            <li>SentimentAnalyzer (Análise de sentimento)</li>
                            <li>BiasDisinformationDetector (Detecção de viés)</li>
                            <li>LLMReasoningService (Raciocínio LLM)</li>
                            <li>RuleEngine (Motor de regras)</li>
                            <li>ContextualAnalyzer (Análise contextual)</li>
                        </ul>
                    </div>
                </div>

                <div class="section">
                    <h2>Fluxo de Dados Detalhado</h2>
                    
                    <h3>Etapa 1: Coleta Massiva</h3>
                    <div class="flow-diagram">
                        <div class="flow-step">Configuração<br>do Usuário</div>
                        <div class="flow-step">Geração<br>de Query</div>
                        <div class="flow-step">Busca<br>Múltiplas APIs</div>
                        <div class="flow-step">Coleta<br>Viral</div>
                        <div class="flow-step">Screenshots</div>
                        <div class="flow-step">Consolidação</div>
                    </div>

                    <div class="code-block" data-lang="python">
# Fluxo simplificado da Etapa 1
def start_step1_collection(session_id, config):
    """Inicia coleta massiva de dados"""
    
    # 1. Preparar query de busca
    query = generate_search_query(config)
    
    # 2. Buscar em múltiplas APIs
    search_results = []
    for api in [serper_api, jina_api, exa_api]:
        try:
            results = api.search(query)
            search_results.extend(results)
        except Exception as e:
            log_error(f"API {api.name} falhou: {e}")
    
    # 3. Coletar conteúdo viral
    viral_results = viral_service.collect_viral_content(query)
    
    # 4. Capturar screenshots
    screenshots = capture_screenshots(search_results)
    
    # 5. Consolidar dados
    consolidated_data = {
        'search_results': search_results,
        'viral_content': viral_results,
        'screenshots': screenshots,
        'metadata': generate_metadata()
    }
    
    # 6. Salvar resultados
    save_step1_results(session_id, consolidated_data)
    
    return consolidated_data</div>

                    <h3>Etapa 2: Síntese com IA</h3>
                    <div class="flow-diagram">
                        <div class="flow-step">Carregar<br>Dados Etapa 1</div>
                        <div class="flow-step">Pré-processamento</div>
                        <div class="flow-step">Análise<br>Multi-IA</div>
                        <div class="flow-step">Buscas<br>Ativas</div>
                        <div class="flow-step">Síntese<br>Final</div>
                        <div class="flow-step">Estruturação<br>JSON</div>
                    </div>

                    <div class="code-block" data-lang="python">
# Fluxo simplificado da Etapa 2
def start_step2_synthesis(session_id):
    """Inicia síntese com IA ativa"""
    
    # 1. Carregar dados da Etapa 1
    step1_data = load_step1_results(session_id)
    
    # 2. Pré-processar dados
    processed_data = preprocess_data(step1_data)
    
    # 3. Análise por múltiplos modelos de IA
    ai_analyses = []
    for model in [gpt4_model, claude_model, gemini_model]:
        try:
            analysis = model.analyze(processed_data)
            ai_analyses.append(analysis)
        except Exception as e:
            log_error(f"Modelo {model.name} falhou: {e}")
    
    # 4. Realizar buscas ativas para validação
    validation_searches = perform_active_searches(ai_analyses)
    
    # 5. Síntese final
    final_synthesis = synthesize_results(
        ai_analyses, 
        validation_searches
    )
    
    # 6. Estruturar em JSON
    structured_output = structure_as_json(final_synthesis)
    
    # 7. Salvar resultados
    save_step2_results(session_id, structured_output)
    
    return structured_output</div>

                    <h3>Etapa 3: Geração de Módulos</h3>
                    <div class="flow-diagram">
                        <div class="flow-step">Carregar<br>Síntese</div>
                        <div class="flow-step">Gerar<br>16 Módulos</div>
                        <div class="flow-step">Compilar<br>Relatório</div>
                        <div class="flow-step">Formatação<br>Final</div>
                        <div class="flow-step">Exportação</div>
                    </div>
                </div>

                <div class="section">
                    <h2>Padrões de Design Utilizados</h2>
                    
                    <h3>1. Strategy Pattern</h3>
                    <div class="info-box">
                        <h4>Aplicação</h4>
                        <p>Utilizado para alternar entre diferentes APIs de busca e modelos de IA.</p>
                        
                        <h4>Benefícios</h4>
                        <ul>
                            <li>Flexibilidade para adicionar novos provedores</li>
                            <li>Fallback automático entre APIs</li>
                            <li>Configuração dinâmica de estratégias</li>
                        </ul>
                    </div>

                    <h3>2. Observer Pattern</h3>
                    <div class="info-box">
                        <h4>Aplicação</h4>
                        <p>Sistema de logging e monitoramento em tempo real.</p>
                        
                        <h4>Benefícios</h4>
                        <ul>
                            <li>Notificações automáticas de mudanças de estado</li>
                            <li>Logging desacoplado dos componentes principais</li>
                            <li>Monitoramento não-intrusivo</li>
                        </ul>
                    </div>

                    <h3>3. Factory Pattern</h3>
                    <div class="info-box">
                        <h4>Aplicação</h4>
                        <p>Criação de instâncias de APIs e serviços.</p>
                        
                        <h4>Benefícios</h4>
                        <ul>
                            <li>Centralização da lógica de criação</li>
                            <li>Configuração baseada em parâmetros</li>
                            <li>Facilita testes unitários</li>
                        </ul>
                    </div>

                    <h3>4. Chain of Responsibility</h3>
                    <div class="info-box">
                        <h4>Aplicação</h4>
                        <p>Pipeline de verificação do External AI Verifier.</p>
                        
                        <h4>Benefícios</h4>
                        <ul>
                            <li>Processamento sequencial de validações</li>
                            <li>Flexibilidade para adicionar/remover verificações</li>
                            <li>Isolamento de responsabilidades</li>
                        </ul>
                    </div>
                </div>
            </div>
        '''

    def generate_structure_chapter(self):
        """Gera capítulo de estrutura de arquivos"""
        structure = self.generate_file_structure()
        
        return f'''
            <div class="chapter" id="structure">
                <div class="chapter-header">
                    <h1 class="chapter-title">📁 Estrutura de Arquivos</h1>
                    <p class="chapter-subtitle">Organização Completa do Projeto</p>
                </div>

                <div class="section">
                    <h2>Visão Geral da Estrutura</h2>
                    <p>O ARQ-ALPHA-V9 segue uma estrutura organizacional clara e modular, facilitando manutenção e desenvolvimento.</p>

                    <div class="file-tree">
{structure}
                    </div>
                </div>

                <div class="section">
                    <h2>Diretórios Principais</h2>
                    
                    <h3>📁 src/ - Código Fonte Principal</h3>
                    <div class="info-box">
                        <h4>Propósito</h4>
                        <p>Contém todo o código fonte da aplicação principal, organizado em módulos especializados.</p>
                        
                        <h4>Subdiretórios</h4>
                        <ul>
                            <li><strong>routes/</strong> - Endpoints da API Flask</li>
                            <li><strong>services/</strong> - Serviços de negócio</li>
                            <li><strong>static/</strong> - Arquivos estáticos (CSS, JS, imagens)</li>
                            <li><strong>templates/</strong> - Templates HTML</li>
                        </ul>
                    </div>

                    <h3>📁 external_ai_verifier/ - Módulo de Verificação</h3>
                    <div class="info-box">
                        <h4>Propósito</h4>
                        <p>Módulo independente responsável pela verificação de qualidade dos dados usando múltiplas camadas de IA.</p>
                        
                        <h4>Estrutura Interna</h4>
                        <ul>
                            <li><strong>src/</strong> - Código fonte do verificador</li>
                            <li><strong>config/</strong> - Configurações específicas</li>
                            <li><strong>tests/</strong> - Testes unitários</li>
                        </ul>
                    </div>

                    <h3>📁 relatorios_intermediarios/ - Dados de Sessão</h3>
                    <div class="info-box">
                        <h4>Propósito</h4>
                        <p>Armazena todos os dados intermediários e finais das sessões de análise.</p>
                        
                        <h4>Organização</h4>
                        <ul>
                            <li><strong>workflow/</strong> - Dados do workflow por sessão</li>
                            <li><strong>screenshots/</strong> - Capturas de tela</li>
                            <li><strong>analyses_data/</strong> - Dados de análise</li>
                        </ul>
                    </div>
                </div>

                <div class="section">
                    <h2>Arquivos de Configuração</h2>
                    
                    <h3>🐍 run.py - Arquivo Principal</h3>
                    <div class="code-block" data-lang="python">
#!/usr/bin/env python3
"""
ARQ-ALPHA-V9 - Sistema de Análise Ultra-Detalhada
Arquivo principal de inicialização do sistema
"""

import os
import sys
from pathlib import Path
from flask import Flask
from src.routes.enhanced_workflow import enhanced_workflow_bp
from src.services.log_local_atual import setup_logging

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Registrar blueprints
    app.register_blueprint(enhanced_workflow_bp, url_prefix='/api')
    
    # Configurar logging
    setup_logging()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=12000, debug=True)
                    </div>

                    <h3>⚙️ .env - Variáveis de Ambiente</h3>
                    <div class="code-block" data-lang="bash">
# APIs de IA
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...

# APIs de Busca
SERPER_API_KEY=...
JINA_API_KEY=jina_...
EXA_API_KEY=...

# APIs Opcionais
FIRECRAWL_API_KEY=fc-...
SUPADATA_API_KEY=...
APIFY_API_KEY=apify_api_...
RAPIDAPI_KEY=...

# Configurações do Sistema
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
                    </div>

                    <h3>📋 requirements.txt - Dependências</h3>
                    <div class="code-block" data-lang="text">
# Framework Web
flask==2.3.3
werkzeug==2.3.7

# APIs e HTTP
requests==2.31.0
httpx==0.25.2
aiohttp==3.9.1

# IA e Machine Learning
openai==1.3.5
anthropic==0.7.7
google-generativeai==0.3.1

# Web Scraping e Automação
beautifulsoup4==4.12.2
selenium==4.15.2
playwright==1.40.0

# Processamento de Dados
pandas==2.0.3
numpy==1.24.3
python-dateutil==2.8.2

# Visualização
matplotlib==3.7.2
seaborn==0.12.2
plotly==5.17.0

# Utilitários
python-dotenv==1.0.0
pyyaml==6.0.1
colorama==0.4.6
tqdm==4.66.1
psutil==5.9.6
                    </div>
                </div>

                <div class="section">
                    <h2>Convenções de Nomenclatura</h2>
                    
                    <h3>Arquivos Python</h3>
                    <div class="variable-list">
                        <div class="variable-item">
                            <span class="variable-name">snake_case</span>
                            <span class="variable-type">Padrão</span>
                            <div class="variable-description">Todos os arquivos Python seguem snake_case</div>
                        </div>
                        <div class="variable-item">
                            <span class="variable-name">_service.py</span>
                            <span class="variable-type">Sufixo</span>
                            <div class="variable-description">Arquivos de serviço terminam com _service</div>
                        </div>
                        <div class="variable-item">
                            <span class="variable-name">_manager.py</span>
                            <span class="variable-type">Sufixo</span>
                            <div class="variable-description">Gerenciadores terminam com _manager</div>
                        </div>
                    </div>

                    <h3>Diretórios de Dados</h3>
                    <div class="variable-list">
                        <div class="variable-item">
                            <span class="variable-name">session_[timestamp]_[hash]</span>
                            <span class="variable-type">Padrão</span>
                            <div class="variable-description">Diretórios de sessão com timestamp e hash único</div>
                        </div>
                        <div class="variable-item">
                            <span class="variable-name">etapa[N]_[status]_[timestamp].json</span>
                            <span class="variable-type">Padrão</span>
                            <div class="variable-description">Arquivos de etapa com número, status e timestamp</div>
                        </div>
                    </div>

                    <h3>Logs</h3>
                    <div class="variable-list">
                        <div class="variable-item">
                            <span class="variable-name">log_session_[id]_[timestamp].txt</span>
                            <span class="variable-type">Padrão</span>
                            <div class="variable-description">Logs de sessão específica</div>
                        </div>
                        <div class="variable-item">
                            <span class="variable-name">app_runtime.log</span>
                            <span class="variable-type">Principal</span>
                            <div class="variable-description">Log principal da aplicação</div>
                        </div>
                    </div>
                </div>
            </div>
        '''

    def generate_complete_ebook(self):
        """Gera o ebook completo com todos os capítulos"""
        
        # Ler o template base
        with open(self.project_root / "ebook_arq_alpha_v9.html", 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # Gerar capítulos adicionais
        architecture_chapter = self.generate_architecture_chapter()
        structure_chapter = self.generate_structure_chapter()
        
        # Inserir capítulos no HTML base
        # Encontrar o ponto de inserção (após o capítulo de overview)
        insertion_point = base_content.find('<!-- Continua com outros capítulos... -->')
        
        if insertion_point != -1:
            additional_chapters = architecture_chapter + structure_chapter
            complete_content = (
                base_content[:insertion_point] + 
                additional_chapters + 
                base_content[insertion_point:]
            )
        else:
            complete_content = base_content
        
        # Salvar ebook completo
        output_file = self.project_root / "ebook_arq_alpha_v9_completo.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(complete_content)
        
        return output_file

    def run(self):
        """Executa o gerador de ebook"""
        print("=" * 60)
        print("    ARQ-ALPHA-V9 - GERADOR DE EBOOK COMPLETO")
        print("=" * 60)
        print()
        
        try:
            print("🔍 Analisando estrutura do projeto...")
            
            print("📖 Gerando capítulos detalhados...")
            
            print("🔧 Compilando ebook completo...")
            output_file = self.generate_complete_ebook()
            
            print()
            print("✅ Ebook gerado com sucesso!")
            print(f"📁 Localização: {output_file}")
            print(f"📊 Tamanho: {output_file.stat().st_size / 1024:.1f} KB")
            print()
            print("🌐 Para visualizar:")
            print(f"   Abra o arquivo em seu navegador:")
            print(f"   file:///{output_file.absolute()}")
            print()
            print("📋 Recursos incluídos:")
            print("   ✅ Índice navegável")
            print("   ✅ Menu lateral interativo")
            print("   ✅ Busca integrada")
            print("   ✅ Códigos comentados")
            print("   ✅ Estrutura de arquivos")
            print("   ✅ Diagramas de fluxo")
            print("   ✅ Documentação técnica")
            print("   ✅ Responsivo para mobile")
            print("   ✅ Função de impressão")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao gerar ebook: {e}")
            return False

def main():
    generator = EbookGenerator()
    success = generator.run()
    
    if success:
        print("\n🎉 Ebook completo gerado com sucesso!")
    else:
        print("\n❌ Falha na geração do ebook!")
    
    input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()