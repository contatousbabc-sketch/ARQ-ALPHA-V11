#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Abas da Interface Nativa - ARQV30 Enhanced v3.0
Implementação das abas restantes da aplicação nativa
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import threading
import asyncio
from typing import Dict, Any, List, Optional

# Importa componentes locais
from native_windows_app import ModernStyle, ModernCard, ModernButton, ModernProgressBar, ModernListView

class NativeAppTabs:
    """Classe com implementação das abas da aplicação nativa"""
    
    def __init__(self, app_instance):
        self.app = app_instance
    
    def create_setup_tab(self):
        """Aba de configuração da análise"""
        setup_frame = ttk.Frame(self.app.notebook, style='Modern.TFrame')
        self.app.notebook.add_tab(setup_frame, "⚙️ Configuração", "⚙️")
        
        # Scroll container
        canvas = tk.Canvas(setup_frame, bg=ModernStyle.COLORS['bg_secondary'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(setup_frame, orient="vertical", command=canvas.yview,
                                 style='Modern.Vertical.TScrollbar')
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Card de configuração principal
        config_card = ModernCard(scrollable_frame, 
                                title="Configuração da Análise", 
                                subtitle="Configure os parâmetros para análise completa",
                                icon="⚙️")
        config_card.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        # Formulário de configuração
        self.create_config_form(config_card.content_frame)
        
        # Card de sessões existentes
        sessions_card = ModernCard(scrollable_frame,
                                  title="Sessões Existentes",
                                  subtitle="Continue uma análise em progresso",
                                  icon="📂")
        sessions_card.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        self.create_sessions_list(sessions_card.content_frame)
    
    def create_config_form(self, parent):
        """Cria formulário de configuração"""
        form_frame = ttk.Frame(parent, style='Modern.TFrame')
        form_frame.pack(fill='both', expand=True, pady=ModernStyle.SPACING['md'])
        
        # Grid de campos
        fields = [
            ("Nicho/Mercado:", "nicho", "Ex: Marketing Digital, E-commerce, Consultoria"),
            ("Público-alvo:", "publico_alvo", "Ex: Empreendedores, PMEs, Freelancers"),
            ("Localização:", "localizacao", "Ex: Brasil, São Paulo, Nacional"),
            ("Produto/Serviço:", "produto", "Ex: Curso Online, Software, Consultoria"),
            ("Orçamento (R$):", "orcamento", "Ex: 10000, 50000, 100000"),
        ]
        
        self.form_vars = {}
        
        for i, (label, key, placeholder) in enumerate(fields):
            # Label
            label_widget = ttk.Label(form_frame, text=label, style='Subheading.TLabel')
            label_widget.grid(row=i, column=0, sticky='w', padx=(0, ModernStyle.SPACING['md']),
                             pady=(ModernStyle.SPACING['sm'], 0))
            
            # Entry
            var = tk.StringVar()
            entry = ttk.Entry(form_frame, textvariable=var, style='Modern.TEntry',
                             width=40, font=ModernStyle.FONTS['body'])
            entry.grid(row=i, column=1, sticky='ew', pady=(ModernStyle.SPACING['sm'], 0))
            
            # Placeholder como tooltip
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e, entry=entry, ph=placeholder: 
                      entry.delete(0, 'end') if entry.get() == ph else None)
            entry.bind('<FocusOut>', lambda e, entry=entry, ph=placeholder: 
                      entry.insert(0, ph) if entry.get() == '' else None)
            
            self.form_vars[key] = var
        
        # Configura grid
        form_frame.columnconfigure(1, weight=1)
        
        # Botões de ação
        buttons_frame = ttk.Frame(parent, style='Modern.TFrame')
        buttons_frame.pack(fill='x', pady=(ModernStyle.SPACING['lg'], 0))
        
        # Botão iniciar análise
        start_btn = ModernButton(buttons_frame, 
                                text="Iniciar Análise Completa",
                                command=self.start_complete_analysis,
                                style_type="primary",
                                icon="🚀")
        start_btn.pack(side='left', padx=(0, ModernStyle.SPACING['md']))
        
        # Botão salvar configuração
        save_btn = ModernButton(buttons_frame,
                               text="Salvar Configuração",
                               command=self.save_configuration,
                               style_type="secondary",
                               icon="💾")
        save_btn.pack(side='left', padx=(0, ModernStyle.SPACING['md']))
        
        # Botão carregar configuração
        load_btn = ModernButton(buttons_frame,
                               text="Carregar Configuração",
                               command=self.load_configuration,
                               style_type="outline",
                               icon="📂")
        load_btn.pack(side='left')
    
    def create_sessions_list(self, parent):
        """Cria lista de sessões existentes"""
        # Lista de sessões
        self.sessions_list = ModernListView(parent, 
                                           columns=['ID', 'Criada em', 'Status', 'Progresso', 'Módulos'])
        self.sessions_list.pack(fill='both', expand=True, pady=ModernStyle.SPACING['md'])
        
        # Botões de sessão
        session_buttons = ttk.Frame(parent, style='Modern.TFrame')
        session_buttons.pack(fill='x', pady=(ModernStyle.SPACING['md'], 0))
        
        continue_btn = ModernButton(session_buttons,
                                   text="Continuar Sessão",
                                   command=self.continue_session,
                                   style_type="success",
                                   icon="▶️")
        continue_btn.pack(side='left', padx=(0, ModernStyle.SPACING['md']))
        
        delete_btn = ModernButton(session_buttons,
                                 text="Excluir Sessão",
                                 command=self.delete_session,
                                 style_type="error",
                                 icon="🗑️")
        delete_btn.pack(side='left')
        
        # Carrega sessões existentes
        self.refresh_sessions_list()
    
    def create_modules_tab(self):
        """Aba de módulos de análise"""
        modules_frame = ttk.Frame(self.app.notebook, style='Modern.TFrame')
        self.app.notebook.add_tab(modules_frame, "🧩 Módulos", "🧩")
        
        # Scroll container
        canvas = tk.Canvas(modules_frame, bg=ModernStyle.COLORS['bg_secondary'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(modules_frame, orient="vertical", command=canvas.yview,
                                 style='Modern.Vertical.TScrollbar')
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cards dos módulos
        self.create_detailed_modules(scrollable_frame)
    
    def create_detailed_modules(self, parent):
        """Cria cards detalhados dos módulos"""
        modules_data = [
            {
                'icon': '👤', 'name': 'Avatar Generation', 
                'description': 'Geração de avatares visuais do público-alvo usando IA',
                'features': ['Imagens 1080x1080', 'Gemini + OpenRouter', 'Base64 encoding'],
                'status': 'Disponível'
            },
            {
                'icon': '🏢', 'name': 'Competitor Analysis', 
                'description': 'Análise detalhada de concorrentes reais do mercado',
                'features': ['15+ concorrentes', 'Dados reais', 'Análise SWOT'],
                'status': 'Disponível'
            },
            {
                'icon': '📈', 'name': 'Sales Funnel', 
                'description': 'Geração de gráficos de funil de vendas personalizados',
                'features': ['Gráficos IA', 'Múltiplos formatos', 'Base64 export'],
                'status': 'Disponível'
            },
            {
                'icon': '🔍', 'name': 'Keyword Research', 
                'description': 'Pesquisa abrangente de palavras-chave do nicho',
                'features': ['Palavras primárias', 'Long-tail', 'Volume de busca'],
                'status': 'Disponível'
            },
            {
                'icon': '📝', 'name': 'Content Strategy', 
                'description': 'Estratégia completa de marketing de conteúdo',
                'features': ['Pilares de conteúdo', 'Calendário editorial', 'Multi-plataforma'],
                'status': 'Disponível'
            },
            {
                'icon': '📊', 'name': 'Market Analysis', 
                'description': 'Análise detalhada do mercado e oportunidades',
                'features': ['Segmentação', 'Tendências', 'TAM/SAM/SOM'],
                'status': 'Disponível'
            },
            {
                'icon': '🎯', 'name': 'Persona Development', 
                'description': 'Desenvolvimento de personas detalhadas',
                'features': ['Personas primárias', 'Comportamento', 'Jornada do cliente'],
                'status': 'Disponível'
            },
            {
                'icon': '💰', 'name': 'Pricing Strategy', 
                'description': 'Estratégia de precificação baseada em valor',
                'features': ['Modelos de preço', 'Tiers', 'Análise competitiva'],
                'status': 'Disponível'
            },
            {
                'icon': '🚚', 'name': 'Distribution Channels', 
                'description': 'Mapeamento de canais de distribuição',
                'features': ['Canais digitais', 'Parcerias', 'ROI por canal'],
                'status': 'Disponível'
            },
            {
                'icon': '⚠️', 'name': 'Risk Assessment', 
                'description': 'Avaliação completa de riscos do negócio',
                'features': ['Riscos de mercado', 'Mitigação', 'Planos B'],
                'status': 'Disponível'
            },
            {
                'icon': '💹', 'name': 'Financial Projections', 
                'description': 'Projeções financeiras e análise de viabilidade',
                'features': ['Receitas', 'Custos', 'ROI projetado'],
                'status': 'Disponível'
            },
            {
                'icon': '📋', 'name': 'Final Report', 
                'description': 'Relatório final consolidado com todos os insights',
                'features': ['Sumário executivo', 'Recomendações', 'Próximos passos'],
                'status': 'Disponível'
            }
        ]
        
        # Grid de módulos (3 por linha)
        for i, module in enumerate(modules_data):
            if i % 3 == 0:
                row_frame = ttk.Frame(parent, style='Modern.TFrame')
                row_frame.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
            
            module_card = ModernCard(row_frame, 
                                    title=f"{module['icon']} {module['name']}", 
                                    subtitle=module['status'])
            module_card.pack(side='left', fill='both', expand=True,
                            padx=(0, ModernStyle.SPACING['md'] if i % 3 < 2 else 0))
            
            # Descrição
            desc_label = ttk.Label(module_card.content_frame, 
                                  text=module['description'],
                                  style='Modern.TLabel', 
                                  wraplength=250)
            desc_label.pack(anchor='w', pady=(0, ModernStyle.SPACING['md']))
            
            # Features
            features_label = ttk.Label(module_card.content_frame, 
                                      text="Recursos:",
                                      style='Subheading.TLabel')
            features_label.pack(anchor='w', pady=(0, ModernStyle.SPACING['xs']))
            
            for feature in module['features']:
                feature_label = ttk.Label(module_card.content_frame, 
                                         text=f"• {feature}",
                                         style='Caption.TLabel')
                feature_label.pack(anchor='w', padx=(ModernStyle.SPACING['md'], 0))
            
            # Botão de teste individual
            test_btn = ModernButton(module_card.content_frame,
                                   text="Testar Módulo",
                                   command=lambda m=module: self.test_individual_module(m),
                                   style_type="outline")
            test_btn.pack(anchor='w', pady=(ModernStyle.SPACING['md'], 0))
    
    def create_progress_tab(self):
        """Aba de progresso em tempo real"""
        progress_frame = ttk.Frame(self.app.notebook, style='Modern.TFrame')
        self.app.notebook.add_tab(progress_frame, "📊 Progresso", "📊")
        
        # Card principal de progresso
        progress_card = ModernCard(progress_frame, 
                                  title="Progresso da Análise", 
                                  subtitle="Acompanhamento em tempo real",
                                  icon="📊")
        progress_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'],
                          pady=ModernStyle.SPACING['lg'])
        
        # Barra de progresso principal
        self.main_progress = ModernProgressBar(progress_card.content_frame)
        self.main_progress.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        # Grid de progresso por módulo
        modules_progress_frame = ttk.Frame(progress_card.content_frame, style='Modern.TFrame')
        modules_progress_frame.pack(fill='both', expand=True, pady=(0, ModernStyle.SPACING['lg']))
        
        # Título da seção
        modules_title = ttk.Label(modules_progress_frame, 
                                 text="Progresso por Módulo",
                                 style='Heading.TLabel')
        modules_title.pack(anchor='w', pady=(0, ModernStyle.SPACING['md']))
        
        # Lista de módulos com progresso
        self.modules_progress_list = ModernListView(modules_progress_frame,
                                                   columns=['Módulo', 'Status', 'Progresso', 'Tempo'])
        self.modules_progress_list.pack(fill='both', expand=True)
        
        # Log de atividades
        log_frame = ttk.Frame(progress_card.content_frame, style='Modern.TFrame')
        log_frame.pack(fill='both', expand=True, pady=(ModernStyle.SPACING['lg'], 0))
        
        log_title = ttk.Label(log_frame, text="Log de Atividades", style='Heading.TLabel')
        log_title.pack(anchor='w', pady=(0, ModernStyle.SPACING['md']))
        
        # Text widget para log
        self.log_text = tk.Text(log_frame, 
                               bg=ModernStyle.COLORS['bg_tertiary'],
                               fg=ModernStyle.COLORS['text_primary'],
                               font=ModernStyle.FONTS['code'],
                               height=10,
                               wrap='word')
        self.log_text.pack(fill='both', expand=True)
        
        # Scrollbar para log
        log_scrollbar = ttk.Scrollbar(log_frame, orient='vertical', 
                                     command=self.log_text.yview,
                                     style='Modern.Vertical.TScrollbar')
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        log_scrollbar.pack(side='right', fill='y')
    
    def create_results_tab(self):
        """Aba de resultados"""
        results_frame = ttk.Frame(self.app.notebook, style='Modern.TFrame')
        self.app.notebook.add_tab(results_frame, "📋 Resultados", "📋")
        
        # Notebook interno para diferentes tipos de resultado
        results_notebook = ttk.Notebook(results_frame, style='Modern.TNotebook')
        results_notebook.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'],
                             pady=ModernStyle.SPACING['lg'])
        
        # Aba de sumário
        self.create_summary_results(results_notebook)
        
        # Aba de módulos individuais
        self.create_individual_results(results_notebook)
        
        # Aba de exportação
        self.create_export_results(results_notebook)
    
    def create_summary_results(self, parent):
        """Cria aba de sumário dos resultados"""
        summary_frame = ttk.Frame(parent, style='Modern.TFrame')
        parent.add(summary_frame, text="📊 Sumário")
        
        # Card de sumário executivo
        summary_card = ModernCard(summary_frame,
                                 title="Sumário Executivo",
                                 subtitle="Principais insights da análise",
                                 icon="📊")
        summary_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['md'],
                         pady=ModernStyle.SPACING['md'])
        
        # Placeholder para resultados
        placeholder_label = ttk.Label(summary_card.content_frame,
                                     text="Execute uma análise para ver os resultados aqui.",
                                     style='Modern.TLabel')
        placeholder_label.pack(expand=True)
    
    def create_individual_results(self, parent):
        """Cria aba de resultados individuais"""
        individual_frame = ttk.Frame(parent, style='Modern.TFrame')
        parent.add(individual_frame, text="🧩 Por Módulo")
        
        # Lista de resultados por módulo
        self.results_list = ModernListView(individual_frame,
                                          columns=['Módulo', 'Status', 'Resultado', 'Ações'])
        self.results_list.pack(fill='both', expand=True, padx=ModernStyle.SPACING['md'],
                              pady=ModernStyle.SPACING['md'])
    
    def create_export_results(self, parent):
        """Cria aba de exportação"""
        export_frame = ttk.Frame(parent, style='Modern.TFrame')
        parent.add(export_frame, text="📤 Exportar")
        
        # Card de exportação
        export_card = ModernCard(export_frame,
                                title="Exportar Resultados",
                                subtitle="Exporte os resultados em diferentes formatos",
                                icon="📤")
        export_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['md'],
                        pady=ModernStyle.SPACING['md'])
        
        # Opções de exportação
        export_options = ttk.Frame(export_card.content_frame, style='Modern.TFrame')
        export_options.pack(fill='x', pady=ModernStyle.SPACING['md'])
        
        # Botões de exportação
        pdf_btn = ModernButton(export_options,
                              text="Exportar PDF",
                              command=self.export_pdf,
                              style_type="primary",
                              icon="📄")
        pdf_btn.pack(side='left', padx=(0, ModernStyle.SPACING['md']))
        
        excel_btn = ModernButton(export_options,
                                text="Exportar Excel",
                                command=self.export_excel,
                                style_type="success",
                                icon="📊")
        excel_btn.pack(side='left', padx=(0, ModernStyle.SPACING['md']))
        
        json_btn = ModernButton(export_options,
                               text="Exportar JSON",
                               command=self.export_json,
                               style_type="secondary",
                               icon="📋")
        json_btn.pack(side='left')
    
    def create_sessions_tab(self):
        """Aba de gerenciamento de sessões"""
        sessions_frame = ttk.Frame(self.app.notebook, style='Modern.TFrame')
        self.app.notebook.add_tab(sessions_frame, "💾 Sessões", "💾")
        
        # Card de gerenciamento
        sessions_card = ModernCard(sessions_frame,
                                  title="Gerenciamento de Sessões",
                                  subtitle="Gerencie suas análises salvas",
                                  icon="💾")
        sessions_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'],
                          pady=ModernStyle.SPACING['lg'])
        
        # Lista detalhada de sessões
        self.detailed_sessions_list = ModernListView(sessions_card.content_frame,
                                                    columns=['ID', 'Criada', 'Atualizada', 
                                                           'Status', 'Progresso', 'Módulos', 'Tamanho'])
        self.detailed_sessions_list.pack(fill='both', expand=True, 
                                        pady=(0, ModernStyle.SPACING['lg']))
        
        # Botões de ação
        actions_frame = ttk.Frame(sessions_card.content_frame, style='Modern.TFrame')
        actions_frame.pack(fill='x')
        
        refresh_btn = ModernButton(actions_frame,
                                  text="Atualizar Lista",
                                  command=self.refresh_sessions_list,
                                  style_type="outline",
                                  icon="🔄")
        refresh_btn.pack(side='left', padx=(0, ModernStyle.SPACING['md']))
        
        backup_btn = ModernButton(actions_frame,
                                 text="Backup Sessões",
                                 command=self.backup_sessions,
                                 style_type="secondary",
                                 icon="💾")
        backup_btn.pack(side='left', padx=(0, ModernStyle.SPACING['md']))
        
        cleanup_btn = ModernButton(actions_frame,
                                  text="Limpar Antigas",
                                  command=self.cleanup_old_sessions,
                                  style_type="warning",
                                  icon="🧹")
        cleanup_btn.pack(side='left')
    
    def create_settings_tab(self):
        """Aba de configurações do sistema"""
        settings_frame = ttk.Frame(self.app.notebook, style='Modern.TFrame')
        self.app.notebook.add_tab(settings_frame, "⚙️ Configurações", "⚙️")
        
        # Scroll container
        canvas = tk.Canvas(settings_frame, bg=ModernStyle.COLORS['bg_secondary'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(settings_frame, orient="vertical", command=canvas.yview,
                                 style='Modern.Vertical.TScrollbar')
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cards de configurações
        self.create_settings_cards(scrollable_frame)
    
    def create_settings_cards(self, parent):
        """Cria cards de configurações"""
        # Card de APIs
        api_card = ModernCard(parent,
                             title="Configurações de API",
                             subtitle="Configure suas chaves de API",
                             icon="🔑")
        api_card.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        # Campos de API
        api_fields = [
            ("OpenAI API Key:", "openai_key"),
            ("Gemini API Key:", "gemini_key"),
            ("OpenRouter API Key:", "openrouter_key"),
        ]
        
        for label, key in api_fields:
            field_frame = ttk.Frame(api_card.content_frame, style='Modern.TFrame')
            field_frame.pack(fill='x', pady=(0, ModernStyle.SPACING['md']))
            
            label_widget = ttk.Label(field_frame, text=label, style='Subheading.TLabel')
            label_widget.pack(anchor='w', pady=(0, ModernStyle.SPACING['xs']))
            
            entry = ttk.Entry(field_frame, style='Modern.TEntry', show='*', width=50)
            entry.pack(fill='x')
        
        # Card de preferências
        prefs_card = ModernCard(parent,
                               title="Preferências do Sistema",
                               subtitle="Personalize o comportamento da aplicação",
                               icon="🎛️")
        prefs_card.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        # Checkboxes de preferências
        self.auto_save_var = tk.BooleanVar(value=True)
        auto_save_check = ttk.Checkbutton(prefs_card.content_frame,
                                         text="Salvamento automático de sessões",
                                         variable=self.auto_save_var,
                                         style='Modern.TCheckbutton')
        auto_save_check.pack(anchor='w', pady=(0, ModernStyle.SPACING['sm']))
        
        self.notifications_var = tk.BooleanVar(value=True)
        notifications_check = ttk.Checkbutton(prefs_card.content_frame,
                                             text="Notificações de progresso",
                                             variable=self.notifications_var,
                                             style='Modern.TCheckbutton')
        notifications_check.pack(anchor='w', pady=(0, ModernStyle.SPACING['sm']))
        
        self.detailed_logs_var = tk.BooleanVar(value=False)
        logs_check = ttk.Checkbutton(prefs_card.content_frame,
                                    text="Logs detalhados (debug)",
                                    variable=self.detailed_logs_var,
                                    style='Modern.TCheckbutton')
        logs_check.pack(anchor='w')
        
        # Card de informações do sistema
        info_card = ModernCard(parent,
                              title="Informações do Sistema",
                              subtitle="Detalhes técnicos da aplicação",
                              icon="ℹ️")
        info_card.pack(fill='x')
        
        # Informações
        info_data = [
            ("Versão:", "ARQV30 Enhanced v3.0"),
            ("Build:", "2024.10.31"),
            ("Python:", "3.11+"),
            ("Interface:", "Tkinter Nativo"),
            ("Plataforma:", "Windows"),
            ("Módulos:", "12 disponíveis"),
        ]
        
        for label, value in info_data:
            info_frame = ttk.Frame(info_card.content_frame, style='Modern.TFrame')
            info_frame.pack(fill='x', pady=(0, ModernStyle.SPACING['xs']))
            
            label_widget = ttk.Label(info_frame, text=label, style='Subheading.TLabel')
            label_widget.pack(side='left')
            
            value_widget = ttk.Label(info_frame, text=value, style='Modern.TLabel')
            value_widget.pack(side='right')
    
    # Métodos de ação
    def start_complete_analysis(self):
        """Inicia análise completa"""
        # Coleta dados do formulário
        analysis_data = {}
        for key, var in self.form_vars.items():
            value = var.get()
            if value and not any(placeholder in value for placeholder in ["Ex:", "exemplo"]):
                analysis_data[key] = value
        
        if not analysis_data:
            messagebox.showwarning("Aviso", "Preencha pelo menos um campo para iniciar a análise.")
            return
        
        # Inicia análise em thread separada
        self.app.analysis_data = analysis_data
        threading.Thread(target=self.run_analysis_thread, daemon=True).start()
    
    def run_analysis_thread(self):
        """Executa análise em thread separada"""
        try:
            # Simula análise completa
            self.app.root.after(0, lambda: self.update_progress("Iniciando análise...", 0))
            
            modules = [
                "Avatar Generation", "Competitor Analysis", "Sales Funnel",
                "Keyword Research", "Content Strategy", "Market Analysis",
                "Persona Development", "Pricing Strategy", "Distribution Channels",
                "Risk Assessment", "Financial Projections", "Final Report"
            ]
            
            for i, module in enumerate(modules):
                progress = (i + 1) / len(modules) * 100
                self.app.root.after(0, lambda m=module, p=progress: 
                                   self.update_progress(f"Executando {m}...", p))
                
                # Simula tempo de processamento
                import time
                time.sleep(2)
            
            self.app.root.after(0, lambda: self.update_progress("Análise concluída!", 100))
            self.app.root.after(0, lambda: messagebox.showinfo("Sucesso", 
                                                              "Análise completa finalizada!"))
            
        except Exception as e:
            self.app.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na análise: {e}"))
    
    def update_progress(self, message, percentage):
        """Atualiza progresso na interface"""
        if hasattr(self, 'main_progress'):
            self.main_progress.update_progress(percentage, message)
        
        if hasattr(self, 'log_text'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert('end', f"[{timestamp}] {message}\n")
            self.log_text.see('end')
    
    def save_configuration(self):
        """Salva configuração atual"""
        config_data = {key: var.get() for key, var in self.form_vars.items()}
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
    
    def load_configuration(self):
        """Carrega configuração salva"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                import json
                with open(filename, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                for key, value in config_data.items():
                    if key in self.form_vars:
                        self.form_vars[key].set(value)
                
                messagebox.showinfo("Sucesso", "Configuração carregada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar configuração: {e}")
    
    def refresh_sessions_list(self):
        """Atualiza lista de sessões"""
        # Placeholder - implementar com session_manager real
        pass
    
    def continue_session(self):
        """Continua sessão selecionada"""
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def delete_session(self):
        """Exclui sessão selecionada"""
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def test_individual_module(self, module):
        """Testa módulo individual"""
        messagebox.showinfo("Teste", f"Testando módulo: {module['name']}")
    
    def export_pdf(self):
        """Exporta resultados em PDF"""
        messagebox.showinfo("Export", "Exportação PDF em desenvolvimento")
    
    def export_excel(self):
        """Exporta resultados em Excel"""
        messagebox.showinfo("Export", "Exportação Excel em desenvolvimento")
    
    def export_json(self):
        """Exporta resultados em JSON"""
        messagebox.showinfo("Export", "Exportação JSON em desenvolvimento")
    
    def backup_sessions(self):
        """Faz backup das sessões"""
        messagebox.showinfo("Backup", "Backup em desenvolvimento")
    
    def cleanup_old_sessions(self):
        """Limpa sessões antigas"""
        messagebox.showinfo("Cleanup", "Limpeza em desenvolvimento")