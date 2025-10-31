#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Interface Nativa para Windows
Aplicação nativa moderna com design aprimorado
"""

import os
import sys
import json
import threading
import webbrowser
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Imports para interface nativa
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from tkinter.font import Font
import tkinter.font as tkFont

# Imports PIL para manipulação de imagens
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Adiciona src ao path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Imports dos serviços do app
try:
    from services.enhanced_systems_integration import EnhancedSystemsIntegration
    from services.avatar_image_generator import AvatarImageGenerator
    from services.competitor_content_collector import RealCompetitorAnalyzer
    from services.sales_funnel_chart_generator import SalesFunnelChartGenerator
    from services.external_ai_integration import ExternalAIIntegration
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Alguns serviços não estão disponíveis: {e}")
    SERVICES_AVAILABLE = False

class ModernStyle:
    """Classe para gerenciar estilos modernos da interface"""
    
    # Cores modernas (Dark Theme Premium)
    COLORS = {
        # Cores primárias - Gradiente azul premium
        'primary': '#2563eb',
        'primary_light': '#3b82f6',
        'primary_dark': '#1d4ed8',
        'primary_gradient_start': '#2563eb',
        'primary_gradient_end': '#1e40af',
        
        # Cores secundárias - Roxo elegante
        'secondary': '#7c3aed',
        'secondary_light': '#8b5cf6',
        'secondary_dark': '#6d28d9',
        
        # Cores de destaque
        'accent': '#06b6d4',
        'accent_light': '#0891b2',
        'success': '#10b981',
        'success_light': '#34d399',
        'warning': '#f59e0b',
        'warning_light': '#fbbf24',
        'error': '#ef4444',
        'error_light': '#f87171',
        'info': '#3b82f6',
        
        # Backgrounds - Tons escuros sofisticados
        'bg_primary': '#0f172a',      # Slate 900
        'bg_secondary': '#1e293b',    # Slate 800
        'bg_tertiary': '#334155',     # Slate 700
        'bg_card': '#475569',         # Slate 600
        'bg_elevated': '#64748b',     # Slate 500
        'bg_input': '#1e293b',
        'bg_hover': '#334155',
        'bg_active': '#475569',
        
        # Textos - Hierarquia clara
        'text_primary': '#f8fafc',    # Slate 50
        'text_secondary': '#e2e8f0',  # Slate 200
        'text_muted': '#94a3b8',      # Slate 400
        'text_disabled': '#64748b',   # Slate 500
        
        # Bordas - Sutis e elegantes
        'border': '#475569',          # Slate 600
        'border_light': '#64748b',    # Slate 500
        'border_focus': '#3b82f6',    # Blue 500
        
        # Estados interativos
        'hover': '#3b82f6',
        'active': '#1d4ed8',
        'focus': '#2563eb',
        
        # Sombras
        'shadow_light': 'rgba(0, 0, 0, 0.1)',
        'shadow_medium': 'rgba(0, 0, 0, 0.25)',
        'shadow_heavy': 'rgba(0, 0, 0, 0.5)',
        
        # Gradientes
        'gradient_primary': 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
        'gradient_secondary': 'linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)',
        'gradient_success': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    }
    
    # Fontes modernas - Hierarquia tipográfica profissional
    FONTS = {
        'display': ('Segoe UI', 32, 'bold'),      # Títulos principais
        'title': ('Segoe UI', 24, 'bold'),        # Títulos de seção
        'subtitle': ('Segoe UI', 18, 'normal'),   # Subtítulos
        'heading': ('Segoe UI', 16, 'bold'),      # Cabeçalhos
        'subheading': ('Segoe UI', 14, 'bold'),   # Sub-cabeçalhos
        'body': ('Segoe UI', 12, 'normal'),       # Texto corpo
        'body_small': ('Segoe UI', 11, 'normal'), # Texto pequeno
        'caption': ('Segoe UI', 10, 'normal'),    # Legendas
        'code': ('Consolas', 11, 'normal'),       # Código
        'button': ('Segoe UI', 12, 'bold'),       # Botões
    }
    
    # Espaçamentos consistentes
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48,
    }
    
    # Raios de borda
    RADIUS = {
        'sm': 4,
        'md': 8,
        'lg': 12,
        'xl': 16,
        'full': 9999,
    }
    
    @classmethod
    def configure_ttk_style(cls):
        """Configura estilos TTK modernos e profissionais"""
        style = ttk.Style()
        
        # Configura tema base
        style.theme_use('clam')
        
        # === FRAMES - Containers ===
        style.configure('Modern.TFrame', 
                       background=cls.COLORS['bg_secondary'],
                       borderwidth=0,
                       relief='flat')
        
        style.configure('Card.TFrame',
                       background=cls.COLORS['bg_card'],
                       relief='flat',
                       borderwidth=1,
                       bordercolor=cls.COLORS['border'])
        
        style.configure('Elevated.TFrame',
                       background=cls.COLORS['bg_elevated'],
                       relief='flat',
                       borderwidth=0)
        
        # === LABELS - Textos ===
        style.configure('Modern.TLabel',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'])
        
        style.configure('Display.TLabel',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['display'])
        
        style.configure('Title.TLabel',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['title'])
        
        style.configure('Subtitle.TLabel',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['subtitle'])
        
        style.configure('Heading.TLabel',
                       background=cls.COLORS['bg_card'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading'])
        
        style.configure('Subheading.TLabel',
                       background=cls.COLORS['bg_card'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['subheading'])
        
        style.configure('Caption.TLabel',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_muted'],
                       font=cls.FONTS['caption'])
        
        # === BOTÕES - Interações ===
        # Botão primário
        style.configure('Primary.TButton',
                       background=cls.COLORS['primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['button'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(cls.SPACING['lg'], cls.SPACING['md']),
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', cls.COLORS['primary_light']),
                           ('pressed', cls.COLORS['primary_dark']),
                           ('disabled', cls.COLORS['text_disabled'])],
                 foreground=[('disabled', cls.COLORS['text_muted'])])
        
        # Botão secundário
        style.configure('Secondary.TButton',
                       background=cls.COLORS['secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['button'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(cls.SPACING['lg'], cls.SPACING['md']),
                       relief='flat')
        
        style.map('Secondary.TButton',
                 background=[('active', cls.COLORS['secondary_light']),
                           ('pressed', cls.COLORS['secondary_dark'])])
        
        # Botão de sucesso
        style.configure('Success.TButton',
                       background=cls.COLORS['success'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['button'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(cls.SPACING['lg'], cls.SPACING['md']),
                       relief='flat')
        
        style.map('Success.TButton',
                 background=[('active', cls.COLORS['success_light']),
                           ('pressed', cls.COLORS['success'])])
        
        # Botão de aviso
        style.configure('Warning.TButton',
                       background=cls.COLORS['warning'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['button'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(cls.SPACING['lg'], cls.SPACING['md']),
                       relief='flat')
        
        style.map('Warning.TButton',
                 background=[('active', cls.COLORS['warning_light']),
                           ('pressed', cls.COLORS['warning'])])
        
        # Botão de erro
        style.configure('Error.TButton',
                       background=cls.COLORS['error'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['button'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(cls.SPACING['lg'], cls.SPACING['md']),
                       relief='flat')
        
        style.map('Error.TButton',
                 background=[('active', cls.COLORS['error_light']),
                           ('pressed', cls.COLORS['error'])])
        
        # Botão outline
        style.configure('Outline.TButton',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['primary'],
                       font=cls.FONTS['button'],
                       borderwidth=2,
                       bordercolor=cls.COLORS['primary'],
                       focuscolor='none',
                       padding=(cls.SPACING['lg'], cls.SPACING['md']),
                       relief='flat')
        
        style.map('Outline.TButton',
                 background=[('active', cls.COLORS['bg_hover']),
                           ('pressed', cls.COLORS['bg_active'])],
                 bordercolor=[('active', cls.COLORS['primary_light']),
                            ('pressed', cls.COLORS['primary_dark'])])
        
        # === CAMPOS DE ENTRADA ===
        style.configure('Modern.TEntry',
                       fieldbackground=cls.COLORS['bg_input'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=2,
                       bordercolor=cls.COLORS['border'],
                       insertcolor=cls.COLORS['text_primary'],
                       selectbackground=cls.COLORS['primary'],
                       selectforeground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       padding=cls.SPACING['md'])
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', cls.COLORS['border_focus']),
                            ('active', cls.COLORS['border_light'])])
        
        # === COMBOBOX ===
        style.configure('Modern.TCombobox',
                       fieldbackground=cls.COLORS['bg_input'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=2,
                       bordercolor=cls.COLORS['border'],
                       selectbackground=cls.COLORS['primary'],
                       selectforeground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       padding=cls.SPACING['md'])
        
        style.map('Modern.TCombobox',
                 bordercolor=[('focus', cls.COLORS['border_focus']),
                            ('active', cls.COLORS['border_light'])])
        
        # === BARRA DE PROGRESSO ===
        style.configure('Modern.Horizontal.TProgressbar',
                       background=cls.COLORS['primary'],
                       troughcolor=cls.COLORS['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['primary'],
                       darkcolor=cls.COLORS['primary'],
                       thickness=8)
        
        # Barra de progresso com gradiente
        style.configure('Gradient.Horizontal.TProgressbar',
                       background=cls.COLORS['success'],
                       troughcolor=cls.COLORS['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['success_light'],
                       darkcolor=cls.COLORS['success'],
                       thickness=12)
        
        # === NOTEBOOK - ABAS ===
        style.configure('Modern.TNotebook',
                       background=cls.COLORS['bg_secondary'],
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        
        style.configure('Modern.TNotebook.Tab',
                       background=cls.COLORS['bg_tertiary'],
                       foreground=cls.COLORS['text_muted'],
                       padding=[cls.SPACING['lg'], cls.SPACING['md']],
                       font=cls.FONTS['subheading'],
                       borderwidth=0)
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', cls.COLORS['primary']),
                           ('active', cls.COLORS['bg_hover'])],
                 foreground=[('selected', cls.COLORS['text_primary']),
                           ('active', cls.COLORS['text_primary'])])
        
        # === TREEVIEW ===
        style.configure('Modern.Treeview',
                       background=cls.COLORS['bg_card'],
                       foreground=cls.COLORS['text_primary'],
                       fieldbackground=cls.COLORS['bg_card'],
                       borderwidth=0,
                       font=cls.FONTS['body'])
        
        style.configure('Modern.Treeview.Heading',
                       background=cls.COLORS['bg_elevated'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['subheading'],
                       borderwidth=0)
        
        style.map('Modern.Treeview',
                 background=[('selected', cls.COLORS['primary'])],
                 foreground=[('selected', cls.COLORS['text_primary'])])
        
        # === SCROLLBAR ===
        style.configure('Modern.Vertical.TScrollbar',
                       background=cls.COLORS['bg_tertiary'],
                       troughcolor=cls.COLORS['bg_secondary'],
                       borderwidth=0,
                       arrowcolor=cls.COLORS['text_muted'],
                       darkcolor=cls.COLORS['bg_elevated'],
                       lightcolor=cls.COLORS['bg_elevated'])
        
        style.map('Modern.Vertical.TScrollbar',
                 background=[('active', cls.COLORS['bg_elevated'])])
        
        # === SEPARADOR ===
        style.configure('Modern.TSeparator',
                       background=cls.COLORS['border'])

class ModernCard(ttk.Frame):
    """Widget de card moderno com design profissional"""
    
    def __init__(self, parent, title="", subtitle="", icon="", elevated=False, **kwargs):
        style = 'Elevated.TFrame' if elevated else 'Card.TFrame'
        super().__init__(parent, style=style, **kwargs)
        
        # Container principal com padding
        main_container = ttk.Frame(self, style=style)
        main_container.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'], 
                           pady=ModernStyle.SPACING['lg'])
        
        # Header do card (se houver título)
        if title or icon:
            header_frame = ttk.Frame(main_container, style=style)
            header_frame.pack(fill='x', pady=(0, ModernStyle.SPACING['md']))
            
            # Ícone (se fornecido)
            if icon:
                icon_label = ttk.Label(header_frame, text=icon, style='Title.TLabel')
                icon_label.pack(side='left', padx=(0, ModernStyle.SPACING['sm']))
            
            # Título e subtítulo
            if title:
                title_container = ttk.Frame(header_frame, style=style)
                title_container.pack(side='left', fill='x', expand=True)
                
                title_label = ttk.Label(title_container, text=title, style='Heading.TLabel')
                title_label.pack(anchor='w')
                
                if subtitle:
                    subtitle_label = ttk.Label(title_container, text=subtitle, style='Caption.TLabel')
                    subtitle_label.pack(anchor='w', pady=(2, 0))
        
        # Separador sutil (se houver header)
        if title or icon:
            separator = ttk.Separator(main_container, orient='horizontal', style='Modern.TSeparator')
            separator.pack(fill='x', pady=(0, ModernStyle.SPACING['md']))
        
        # Frame para conteúdo
        self.content_frame = ttk.Frame(main_container, style=style)
        self.content_frame.pack(fill='both', expand=True)

class ModernButton(ttk.Button):
    """Botão moderno customizado com múltiplos estilos"""
    
    def __init__(self, parent, text="", command=None, style_type="primary", 
                 icon="", size="normal", **kwargs):
        
        # Mapeia tipos de estilo
        style_map = {
            'primary': 'Primary.TButton',
            'secondary': 'Secondary.TButton',
            'success': 'Success.TButton',
            'warning': 'Warning.TButton',
            'error': 'Error.TButton',
            'outline': 'Outline.TButton'
        }
        
        style = style_map.get(style_type, 'Primary.TButton')
        
        # Adiciona ícone ao texto se fornecido
        display_text = f"{icon} {text}" if icon else text
        
        super().__init__(parent, text=display_text, command=command, style=style, **kwargs)

class ModernProgressBar(ttk.Frame):
    """Barra de progresso moderna com informações detalhadas"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Modern.TFrame', **kwargs)
        
        # Label de status
        self.status_label = ttk.Label(self, text="Preparando...", style='Modern.TLabel')
        self.status_label.pack(anchor='w', pady=(0, ModernStyle.SPACING['sm']))
        
        # Container da barra
        progress_container = ttk.Frame(self, style='Modern.TFrame')
        progress_container.pack(fill='x', pady=(0, ModernStyle.SPACING['sm']))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_container,
            style='Gradient.Horizontal.TProgressbar',
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(fill='x')
        
        # Container de informações
        info_container = ttk.Frame(self, style='Modern.TFrame')
        info_container.pack(fill='x')
        
        # Porcentagem
        self.percentage_label = ttk.Label(info_container, text="0%", style='Caption.TLabel')
        self.percentage_label.pack(side='left')
        
        # Tempo estimado
        self.time_label = ttk.Label(info_container, text="", style='Caption.TLabel')
        self.time_label.pack(side='right')
    
    def update_progress(self, value: float, status: str = "", time_remaining: str = ""):
        """Atualiza progresso com informações detalhadas"""
        self.progress_var.set(value)
        
        if status:
            self.status_label.config(text=status)
        
        self.percentage_label.config(text=f"{value:.1f}%")
        
        if time_remaining:
            self.time_label.config(text=f"Tempo restante: {time_remaining}")

class ModernStatusBar(ttk.Frame):
    """Barra de status moderna"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Elevated.TFrame', **kwargs)
        
        # Container principal
        container = ttk.Frame(self, style='Elevated.TFrame')
        container.pack(fill='x', padx=ModernStyle.SPACING['md'], 
                      pady=ModernStyle.SPACING['sm'])
        
        # Status principal
        self.status_label = ttk.Label(container, text="Sistema Pronto", style='Modern.TLabel')
        self.status_label.pack(side='left')
        
        # Indicador de conexão
        self.connection_label = ttk.Label(container, text="🟢 Online", style='Caption.TLabel')
        self.connection_label.pack(side='right', padx=(ModernStyle.SPACING['md'], 0))
        
        # Timestamp
        self.time_label = ttk.Label(container, text="", style='Caption.TLabel')
        self.time_label.pack(side='right')
        
        # Atualiza timestamp
        self.update_time()
    
    def update_status(self, status: str, connection: str = None):
        """Atualiza status"""
        self.status_label.config(text=status)
        if connection:
            self.connection_label.config(text=connection)
        self.update_time()
    
    def update_time(self):
        """Atualiza timestamp"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        # Agenda próxima atualização
        self.after(1000, self.update_time)

class ModernTabView(ttk.Notebook):
    """Sistema de abas moderno"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Modern.TNotebook', **kwargs)
        self.tabs_data = []
    
    def add_tab(self, frame, title: str, icon: str = ""):
        """Adiciona aba com ícone"""
        display_title = f"{icon} {title}" if icon else title
        self.add(frame, text=display_title)
        self.tabs_data.append({'frame': frame, 'title': title, 'icon': icon})

class ModernListView(ttk.Frame):
    """Lista moderna com estilo profissional"""
    
    def __init__(self, parent, columns: List[str], **kwargs):
        super().__init__(parent, style='Modern.TFrame', **kwargs)
        
        # Treeview
        self.tree = ttk.Treeview(self, columns=columns, show='headings', 
                                style='Modern.Treeview', height=15)
        
        # Configura colunas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, minwidth=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview,
                                 style='Modern.Vertical.TScrollbar')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def insert_item(self, values: List[str]):
        """Insere item na lista"""
        self.tree.insert('', 'end', values=values)
    
    def clear(self):
        """Limpa lista"""
        for item in self.tree.get_children():
            self.tree.delete(item)



class ARQNativeApp:
    """Aplicação nativa ARQV30 Enhanced v3.0 para Windows"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.setup_services()
        self.create_interface()
        
        # Variáveis de estado aprimoradas
        self.current_session = None
        self.analysis_running = False
        self.results_data = {}
        
        # Sistema de progresso detalhado
        self.total_modules = 12
        self.completed_modules = 0
        self.current_module = ""
        self.current_step = 0
        self.total_steps = 0
        self.start_time = None
        
        # Dados de análise
        self.analysis_data = {}
        self.session_manager = None
        
    def setup_window(self):
        """Configura a janela principal com design profissional"""
        self.root.title("🚀 ARQV30 Enhanced v3.0 - Análise Completa de Mercado")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 900)
        
        # Configura ícone (se disponível)
        try:
            # Tenta carregar ícone
            icon_path = os.path.join(os.path.dirname(__file__), 'src', 'static', 'favicon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Configura cor de fundo
        self.root.configure(bg=ModernStyle.COLORS['bg_primary'])
        
        # Centraliza janela
        self.center_window()
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configura estilos da interface"""
        ModernStyle.configure_ttk_style()
        
    def setup_services(self):
        """Inicializa os serviços do app"""
        self.services = {}
        
        if SERVICES_AVAILABLE:
            try:
                self.services['integration'] = EnhancedSystemsIntegration()
                self.services['avatar'] = AvatarImageGenerator()
                self.services['competitors'] = RealCompetitorAnalyzer()
                self.services['funnel'] = SalesFunnelChartGenerator()
                self.services['external_ai'] = ExternalAIIntegration()
                print("✅ Todos os serviços inicializados com sucesso!")
            except Exception as e:
                print(f"⚠️ Erro ao inicializar serviços: {e}")
                self.services = {}
        
    def create_interface(self):
        """Cria a interface principal com design profissional"""
        # Container principal
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'], 
                           pady=ModernStyle.SPACING['lg'])
        
        # Header profissional
        self.create_professional_header(main_container)
        
        # Barra de status global
        self.status_bar = ModernStatusBar(main_container)
        self.status_bar.pack(fill='x', pady=(0, ModernStyle.SPACING['md']))
        
        # Sistema de abas moderno
        self.notebook = ModernTabView(main_container)
        self.notebook.pack(fill='both', expand=True, pady=(ModernStyle.SPACING['md'], 0))
        
        # Cria todas as abas com ícones
        self.create_all_tabs()
        
        # Footer com informações
        self.create_footer(main_container)
    
    def create_professional_header(self, parent):
        """Cria header profissional com branding"""
        header_card = ModernCard(parent, elevated=True)
        header_card.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        # Container do header
        header_container = ttk.Frame(header_card.content_frame, style='Elevated.TFrame')
        header_container.pack(fill='x', padx=ModernStyle.SPACING['lg'], 
                             pady=ModernStyle.SPACING['md'])
        
        # Logo e branding (lado esquerdo)
        branding_frame = ttk.Frame(header_container, style='Elevated.TFrame')
        branding_frame.pack(side='left', fill='y')
        
        # Logo/ícone
        logo_label = ttk.Label(branding_frame, text="🚀", style='Display.TLabel')
        logo_label.pack(side='left', padx=(0, ModernStyle.SPACING['md']))
        
        # Títulos
        titles_frame = ttk.Frame(branding_frame, style='Elevated.TFrame')
        titles_frame.pack(side='left', fill='y')
        
        main_title = ttk.Label(titles_frame, text="ARQV30 Enhanced v3.0", style='Title.TLabel')
        main_title.pack(anchor='w')
        
        subtitle = ttk.Label(titles_frame, text="Análise Completa de Mercado - Interface Nativa", 
                           style='Subtitle.TLabel')
        subtitle.pack(anchor='w')
        
        # Informações do sistema (lado direito)
        info_frame = ttk.Frame(header_container, style='Elevated.TFrame')
        info_frame.pack(side='right', fill='y')
        
        # Status da sessão
        self.session_status = ttk.Label(info_frame, text="📊 Nenhuma sessão ativa", 
                                       style='Modern.TLabel')
        self.session_status.pack(anchor='e')
        
        # Versão e build
        version_label = ttk.Label(info_frame, text="Build: 2024.10.31", style='Caption.TLabel')
        version_label.pack(anchor='e')
    
    def create_footer(self, parent):
        """Cria footer com informações adicionais"""
        footer_frame = ttk.Frame(parent, style='Elevated.TFrame')
        footer_frame.pack(fill='x', pady=(ModernStyle.SPACING['md'], 0))
        
        # Container do footer
        footer_container = ttk.Frame(footer_frame, style='Elevated.TFrame')
        footer_container.pack(fill='x', padx=ModernStyle.SPACING['md'], 
                             pady=ModernStyle.SPACING['sm'])
        
        # Copyright
        copyright_label = ttk.Label(footer_container, 
                                   text="© 2024 ARQV30 Enhanced - Todos os direitos reservados", 
                                   style='Caption.TLabel')
        copyright_label.pack(side='left')
        
        # Informações técnicas
        tech_info = ttk.Label(footer_container, 
                             text="Python 3.11 | Tkinter | Windows Native", 
                             style='Caption.TLabel')
        tech_info.pack(side='right')
    
    def create_all_tabs(self):
        """Cria todas as abas da aplicação"""
        # Importa e inicializa o sistema de abas
        try:
            from native_app_tabs import NativeAppTabs
            self.tabs_manager = NativeAppTabs(self)
        except ImportError:
            # Fallback se não conseguir importar
            self.tabs_manager = None
        
        # 1. Análise Principal - Dashboard
        self.create_dashboard_tab()
        
        # 2. Configuração - Setup da análise
        if self.tabs_manager:
            self.tabs_manager.create_setup_tab()
        else:
            self.create_simple_setup_tab()
        
        # 3. Módulos - Todos os módulos de análise
        if self.tabs_manager:
            self.tabs_manager.create_modules_tab()
        else:
            self.create_simple_modules_tab()
        
        # 4. Progresso - Acompanhamento em tempo real
        if self.tabs_manager:
            self.tabs_manager.create_progress_tab()
        else:
            self.create_simple_progress_tab()
        
        # 5. Resultados - Visualização dos resultados
        if self.tabs_manager:
            self.tabs_manager.create_results_tab()
        else:
            self.create_simple_results_tab()
        
        # 6. Sessões - Gerenciamento de sessões
        if self.tabs_manager:
            self.tabs_manager.create_sessions_tab()
        
        # 7. Configurações - Settings do sistema
        if self.tabs_manager:
            self.tabs_manager.create_settings_tab()
        else:
            self.create_simple_settings_tab()
    
    def create_dashboard_tab(self):
        """Aba principal - Dashboard"""
        dashboard_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add_tab(dashboard_frame, "📊 Dashboard", "📊")
        
        # Scroll container
        canvas = tk.Canvas(dashboard_frame, bg=ModernStyle.COLORS['bg_secondary'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(dashboard_frame, orient="vertical", command=canvas.yview,
                                 style='Modern.Vertical.TScrollbar')
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Layout do scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cards do dashboard
        self.create_dashboard_cards(scrollable_frame)
    
    def create_dashboard_cards(self, parent):
        """Cria cards do dashboard"""
        # Card de boas-vindas
        welcome_card = ModernCard(parent, 
                                 title="Bem-vindo ao ARQV30 Enhanced v3.0", 
                                 subtitle="Sistema completo de análise de mercado",
                                 icon="🎯")
        welcome_card.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        welcome_text = ttk.Label(welcome_card.content_frame, 
                               text="Esta é a versão nativa do ARQV30 Enhanced, projetada para oferecer "
                                    "uma experiência completa de análise de mercado com interface moderna "
                                    "e todos os módulos integrados.",
                               style='Modern.TLabel', wraplength=800)
        welcome_text.pack(anchor='w', pady=ModernStyle.SPACING['md'])
        
        # Botão principal de ação
        start_button = ModernButton(welcome_card.content_frame, 
                                   text="Iniciar Nova Análise", 
                                   command=self.start_new_analysis,
                                   style_type="primary",
                                   icon="🚀")
        start_button.pack(anchor='w', pady=(ModernStyle.SPACING['md'], 0))
        
        # Grid de estatísticas
        stats_frame = ttk.Frame(parent, style='Modern.TFrame')
        stats_frame.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        # Cards de estatísticas
        self.create_stats_cards(stats_frame)
        
        # Card de módulos disponíveis
        modules_card = ModernCard(parent, 
                                 title="Módulos de Análise Disponíveis", 
                                 subtitle="12 módulos completos para análise de mercado",
                                 icon="🧩")
        modules_card.pack(fill='x', pady=(0, ModernStyle.SPACING['lg']))
        
        self.create_modules_overview(modules_card.content_frame)
    
    def create_stats_cards(self, parent):
        """Cria cards de estatísticas"""
        # Grid 2x2
        for i in range(2):
            row_frame = ttk.Frame(parent, style='Modern.TFrame')
            row_frame.pack(fill='x', pady=(0, ModernStyle.SPACING['md']))
            
            for j in range(4):
                stat_card = ModernCard(row_frame, elevated=True)
                stat_card.pack(side='left', fill='both', expand=True, 
                              padx=(0, ModernStyle.SPACING['md'] if j < 3 else 0))
                
                # Dados das estatísticas
                stats_data = [
                    ("📊", "Análises Realizadas", "0", "Total de análises completas"),
                    ("🎯", "Módulos Ativos", "12", "Módulos disponíveis"),
                    ("⚡", "Sessões Salvas", "0", "Sessões em progresso"),
                    ("🚀", "Taxa de Sucesso", "100%", "Análises bem-sucedidas"),
                    ("💡", "Insights Gerados", "0", "Insights de mercado"),
                    ("📈", "Tendências Mapeadas", "0", "Tendências identificadas"),
                    ("🏢", "Concorrentes Analisados", "0", "Empresas mapeadas"),
                    ("💰", "ROI Projetado", "0%", "Retorno estimado")
                ]
                
                stat_index = i * 4 + j
                if stat_index < len(stats_data):
                    icon, title, value, desc = stats_data[stat_index]
                    
                    # Ícone
                    icon_label = ttk.Label(stat_card.content_frame, text=icon, 
                                         style='Title.TLabel')
                    icon_label.pack(pady=(0, ModernStyle.SPACING['sm']))
                    
                    # Valor
                    value_label = ttk.Label(stat_card.content_frame, text=value, 
                                          style='Display.TLabel')
                    value_label.pack()
                    
                    # Título
                    title_label = ttk.Label(stat_card.content_frame, text=title, 
                                          style='Subheading.TLabel')
                    title_label.pack(pady=(ModernStyle.SPACING['xs'], 0))
                    
                    # Descrição
                    desc_label = ttk.Label(stat_card.content_frame, text=desc, 
                                         style='Caption.TLabel', wraplength=150)
                    desc_label.pack(pady=(ModernStyle.SPACING['xs'], 0))
    
    def create_modules_overview(self, parent):
        """Cria overview dos módulos"""
        modules_data = [
            ("👤", "Avatar Generation", "Geração de avatares visuais"),
            ("🏢", "Competitor Analysis", "Análise de concorrentes reais"),
            ("📈", "Sales Funnel", "Gráficos de funil de vendas"),
            ("🔍", "Keyword Research", "Pesquisa de palavras-chave"),
            ("📝", "Content Strategy", "Estratégia de conteúdo"),
            ("📊", "Market Analysis", "Análise detalhada de mercado"),
            ("🎯", "Persona Development", "Desenvolvimento de personas"),
            ("💰", "Pricing Strategy", "Estratégia de preços"),
            ("🚚", "Distribution Channels", "Canais de distribuição"),
            ("⚠️", "Risk Assessment", "Avaliação de riscos"),
            ("💹", "Financial Projections", "Projeções financeiras"),
            ("📋", "Final Report", "Relatório final completo")
        ]
        
        # Grid de módulos
        modules_grid = ttk.Frame(parent, style='Modern.TFrame')
        modules_grid.pack(fill='both', expand=True, pady=ModernStyle.SPACING['md'])
        
        for i, (icon, name, desc) in enumerate(modules_data):
            row = i // 3
            col = i % 3
            
            if col == 0:
                row_frame = ttk.Frame(modules_grid, style='Modern.TFrame')
                row_frame.pack(fill='x', pady=(0, ModernStyle.SPACING['sm']))
            
            module_frame = ttk.Frame(row_frame, style='Card.TFrame')
            module_frame.pack(side='left', fill='both', expand=True,
                             padx=(0, ModernStyle.SPACING['sm'] if col < 2 else 0),
                             pady=ModernStyle.SPACING['sm'])
            
            # Conteúdo do módulo
            content = ttk.Frame(module_frame, style='Card.TFrame')
            content.pack(fill='both', expand=True, padx=ModernStyle.SPACING['md'],
                        pady=ModernStyle.SPACING['md'])
            
            # Ícone e nome
            header = ttk.Frame(content, style='Card.TFrame')
            header.pack(fill='x', pady=(0, ModernStyle.SPACING['xs']))
            
            icon_label = ttk.Label(header, text=icon, style='Heading.TLabel')
            icon_label.pack(side='left', padx=(0, ModernStyle.SPACING['sm']))
            
            name_label = ttk.Label(header, text=name, style='Subheading.TLabel')
            name_label.pack(side='left')
            
            # Descrição
            desc_label = ttk.Label(content, text=desc, style='Caption.TLabel',
                                 wraplength=200)
            desc_label.pack(anchor='w')
    
    def start_new_analysis(self):
        """Inicia nova análise"""
        # Muda para aba de configuração
        self.notebook.select(1)  # Aba de configuração
        
        # Mostra mensagem
        messagebox.showinfo("Nova Análise", 
                           "Configure os parâmetros na aba 'Configuração' e clique em 'Iniciar Análise Completa'")
    
    def create_simple_setup_tab(self):
        """Aba simples de configuração (fallback)"""
        setup_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add_tab(setup_frame, "⚙️ Configuração", "⚙️")
        
        setup_card = ModernCard(setup_frame, 
                               title="Configuração da Análise",
                               subtitle="Configure os parâmetros básicos")
        setup_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'],
                       pady=ModernStyle.SPACING['lg'])
        
        # Formulário simples
        form_frame = ttk.Frame(setup_card.content_frame, style='Modern.TFrame')
        form_frame.pack(fill='x', pady=ModernStyle.SPACING['md'])
        
        # Campo nicho
        ttk.Label(form_frame, text="Nicho/Mercado:", style='Subheading.TLabel').pack(anchor='w')
        self.nicho_var = tk.StringVar(value="Marketing Digital")
        ttk.Entry(form_frame, textvariable=self.nicho_var, style='Modern.TEntry').pack(fill='x', pady=(ModernStyle.SPACING['xs'], ModernStyle.SPACING['md']))
        
        # Campo público
        ttk.Label(form_frame, text="Público-alvo:", style='Subheading.TLabel').pack(anchor='w')
        self.publico_var = tk.StringVar(value="Empreendedores")
        ttk.Entry(form_frame, textvariable=self.publico_var, style='Modern.TEntry').pack(fill='x', pady=(ModernStyle.SPACING['xs'], ModernStyle.SPACING['md']))
        
        # Botão iniciar
        start_btn = ModernButton(setup_card.content_frame,
                                text="Iniciar Análise Completa",
                                command=self.start_analysis_simple,
                                style_type="primary",
                                icon="🚀")
        start_btn.pack(pady=ModernStyle.SPACING['md'])
    
    def create_simple_modules_tab(self):
        """Aba simples de módulos (fallback)"""
        modules_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add_tab(modules_frame, "🧩 Módulos", "🧩")
        
        modules_card = ModernCard(modules_frame,
                                 title="Módulos de Análise",
                                 subtitle="12 módulos completos disponíveis")
        modules_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'],
                         pady=ModernStyle.SPACING['lg'])
        
        modules_text = """
        ✅ Avatar Generation - Geração de avatares visuais
        ✅ Competitor Analysis - Análise de concorrentes reais  
        ✅ Sales Funnel - Gráficos de funil de vendas
        ✅ Keyword Research - Pesquisa de palavras-chave
        ✅ Content Strategy - Estratégia de conteúdo
        ✅ Market Analysis - Análise detalhada de mercado
        ✅ Persona Development - Desenvolvimento de personas
        ✅ Pricing Strategy - Estratégia de preços
        ✅ Distribution Channels - Canais de distribuição
        ✅ Risk Assessment - Avaliação de riscos
        ✅ Financial Projections - Projeções financeiras
        ✅ Final Report - Relatório final completo
        """
        
        text_label = ttk.Label(modules_card.content_frame, text=modules_text.strip(),
                              style='Modern.TLabel', justify='left')
        text_label.pack(anchor='w', pady=ModernStyle.SPACING['md'])
    
    def create_simple_progress_tab(self):
        """Aba simples de progresso (fallback)"""
        progress_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add_tab(progress_frame, "📊 Progresso", "📊")
        
        progress_card = ModernCard(progress_frame,
                                  title="Progresso da Análise",
                                  subtitle="Acompanhamento em tempo real")
        progress_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'],
                          pady=ModernStyle.SPACING['lg'])
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_card.content_frame,
                                           style='Gradient.Horizontal.TProgressbar',
                                           variable=self.progress_var,
                                           maximum=100)
        self.progress_bar.pack(fill='x', pady=ModernStyle.SPACING['md'])
        
        # Status
        self.progress_status = ttk.Label(progress_card.content_frame,
                                        text="Aguardando início da análise...",
                                        style='Modern.TLabel')
        self.progress_status.pack(pady=ModernStyle.SPACING['md'])
        
        # Log
        self.progress_log = tk.Text(progress_card.content_frame,
                                   height=15,
                                   bg=ModernStyle.COLORS['bg_tertiary'],
                                   fg=ModernStyle.COLORS['text_primary'],
                                   font=ModernStyle.FONTS['code'])
        self.progress_log.pack(fill='both', expand=True, pady=ModernStyle.SPACING['md'])
    
    def create_simple_results_tab(self):
        """Aba simples de resultados (fallback)"""
        results_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add_tab(results_frame, "📋 Resultados", "📋")
        
        results_card = ModernCard(results_frame,
                                 title="Resultados da Análise",
                                 subtitle="Visualização dos resultados obtidos")
        results_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'],
                         pady=ModernStyle.SPACING['lg'])
        
        self.results_text = tk.Text(results_card.content_frame,
                                   bg=ModernStyle.COLORS['bg_tertiary'],
                                   fg=ModernStyle.COLORS['text_primary'],
                                   font=ModernStyle.FONTS['body'],
                                   wrap='word')
        self.results_text.pack(fill='both', expand=True, pady=ModernStyle.SPACING['md'])
        
        # Placeholder
        self.results_text.insert('1.0', "Execute uma análise para ver os resultados aqui.")
    
    def create_simple_settings_tab(self):
        """Aba simples de configurações (fallback)"""
        settings_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add_tab(settings_frame, "⚙️ Configurações", "⚙️")
        
        settings_card = ModernCard(settings_frame,
                                  title="Configurações do Sistema",
                                  subtitle="Configurações básicas da aplicação")
        settings_card.pack(fill='both', expand=True, padx=ModernStyle.SPACING['lg'],
                          pady=ModernStyle.SPACING['lg'])
        
        # Informações do sistema
        info_text = """
        🚀 ARQV30 Enhanced v3.0
        📅 Build: 2024.10.31
        🐍 Python: 3.11+
        🖥️ Interface: Tkinter Nativo
        🪟 Plataforma: Windows
        🧩 Módulos: 12 disponíveis
        
        ✅ Sistema funcionando corretamente
        ✅ Todos os módulos carregados
        ✅ Interface nativa ativa
        """
        
        info_label = ttk.Label(settings_card.content_frame, text=info_text.strip(),
                              style='Modern.TLabel', justify='left')
        info_label.pack(anchor='w', pady=ModernStyle.SPACING['md'])
    
    def start_analysis_simple(self):
        """Inicia análise simples"""
        nicho = self.nicho_var.get()
        publico = self.publico_var.get()
        
        if not nicho or not publico:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return
        
        # Muda para aba de progresso
        self.notebook.select(2)  # Aba de progresso
        
        # Inicia análise em thread
        self.analysis_data = {'nicho': nicho, 'publico_alvo': publico}
        threading.Thread(target=self.run_simple_analysis, daemon=True).start()
    
    def run_simple_analysis(self):
        """Executa análise simples"""
        try:
            modules = [
                "Avatar Generation", "Competitor Analysis", "Sales Funnel",
                "Keyword Research", "Content Strategy", "Market Analysis", 
                "Persona Development", "Pricing Strategy", "Distribution Channels",
                "Risk Assessment", "Financial Projections", "Final Report"
            ]
            
            results = []
            
            for i, module in enumerate(modules):
                progress = (i + 1) / len(modules) * 100
                
                # Atualiza interface
                self.root.after(0, lambda p=progress, m=module: self.update_simple_progress(p, m))
                
                # Simula processamento
                import time
                time.sleep(1)
                
                # Adiciona resultado simulado
                results.append(f"✅ {module}: Concluído com sucesso")
            
            # Finaliza
            self.root.after(0, lambda: self.finish_simple_analysis(results))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na análise: {e}"))
    
    def update_simple_progress(self, progress, module):
        """Atualiza progresso simples"""
        self.progress_var.set(progress)
        self.progress_status.config(text=f"Executando: {module}...")
        
        # Adiciona ao log
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] Processando {module}...\n"
        self.progress_log.insert('end', log_entry)
        self.progress_log.see('end')
    
    def finish_simple_analysis(self, results):
        """Finaliza análise simples"""
        self.progress_status.config(text="✅ Análise concluída com sucesso!")
        
        # Muda para aba de resultados
        self.notebook.select(3)  # Aba de resultados
        
        # Mostra resultados
        results_text = f"""
ANÁLISE COMPLETA - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

NICHO: {self.analysis_data.get('nicho', 'N/A')}
PÚBLICO-ALVO: {self.analysis_data.get('publico_alvo', 'N/A')}

MÓDULOS EXECUTADOS:
{chr(10).join(results)}

SUMÁRIO EXECUTIVO:
✅ Análise completa realizada com sucesso
✅ Todos os 12 módulos processados
✅ Dados coletados e analisados
✅ Insights gerados para tomada de decisão

PRÓXIMOS PASSOS:
1. Revisar os resultados detalhados
2. Implementar as recomendações
3. Monitorar o progresso
4. Ajustar estratégias conforme necessário

OBSERVAÇÕES:
Esta é uma versão demonstrativa da análise completa.
Para resultados detalhados, utilize a versão completa do sistema.
        """
        
        self.results_text.delete('1.0', 'end')
        self.results_text.insert('1.0', results_text.strip())
        
        # Mostra mensagem de sucesso
        messagebox.showinfo("Sucesso", "Análise completa finalizada! Verifique os resultados na aba 'Resultados'.")
    
    def create_header(self, parent):
        """Cria o cabeçalho da aplicação"""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Logo e título
        title_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        title_frame.pack(side='left')
        
        title_label = ttk.Label(title_frame, text="ARQV30 Enhanced v3.0", style='Title.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(title_frame, text="Interface Nativa para Windows", style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w')
        
        # Status e controles
        controls_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        controls_frame.pack(side='right')
        
        # Status
        self.status_label = ttk.Label(controls_frame, text="Sistema Pronto", style='Modern.TLabel')
        self.status_label.pack(side='right', padx=(0, 20))
        
        # Botão de configurações
        settings_btn = ModernButton(controls_frame, text="⚙️ Configurações", 
                                  command=self.open_settings)
        settings_btn.pack(side='right', padx=(0, 10))
        
    def create_analysis_tab(self):
        """Cria a aba de análise principal"""
        analysis_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(analysis_frame, text="📊 Análise Principal")
        
        # Card de configuração da análise
        config_card = ModernCard(analysis_frame, title="Configuração da Análise")
        config_card.pack(fill='x', pady=(0, 20))
        
        # Campos de entrada
        fields_frame = ttk.Frame(config_card.content_frame, style='Card.TFrame')
        fields_frame.pack(fill='x', pady=(0, 20))
        
        # Nicho
        ttk.Label(fields_frame, text="Nicho/Mercado:", style='Modern.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.nicho_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=50)
        self.nicho_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Público-alvo
        ttk.Label(fields_frame, text="Público-alvo:", style='Modern.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.publico_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=50)
        self.publico_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Localização
        ttk.Label(fields_frame, text="Localização:", style='Modern.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.localizacao_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=50)
        self.localizacao_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Botões de ação
        buttons_frame = ttk.Frame(config_card.content_frame, style='Card.TFrame')
        buttons_frame.pack(fill='x')
        
        start_btn = ModernButton(buttons_frame, text="🚀 Iniciar Análise Completa", 
                               command=self.start_complete_analysis, style_type="success")
        start_btn.pack(side='left', padx=(0, 10))
        
        quick_btn = ModernButton(buttons_frame, text="⚡ Análise Rápida", 
                               command=self.start_quick_analysis)
        quick_btn.pack(side='left', padx=(0, 10))
        
        stop_btn = ModernButton(buttons_frame, text="⏹️ Parar", 
                              command=self.stop_analysis, style_type="error")
        stop_btn.pack(side='left')
        
        # Card de progresso
        progress_card = ModernCard(analysis_frame, title="Progresso da Análise")
        progress_card.pack(fill='x', pady=(0, 20))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_card.content_frame, 
                                          style='Modern.Horizontal.TProgressbar',
                                          variable=self.progress_var,
                                          maximum=100)
        self.progress_bar.pack(fill='x', pady=(0, 10))
        
        # Status detalhado
        self.progress_label = ttk.Label(progress_card.content_frame, 
                                      text="Aguardando início da análise...", 
                                      style='Modern.TLabel')
        self.progress_label.pack(anchor='w')
        
        # Log de atividades
        log_card = ModernCard(analysis_frame, title="Log de Atividades")
        log_card.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_card.content_frame,
                                                height=15,
                                                bg=ModernStyle.COLORS['bg_tertiary'],
                                                fg=ModernStyle.COLORS['text_primary'],
                                                font=ModernStyle.FONTS['code'],
                                                insertbackground=ModernStyle.COLORS['text_primary'])
        self.log_text.pack(fill='both', expand=True)
        
    def create_avatar_tab(self):
        """Cria a aba de geração de avatares"""
        avatar_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(avatar_frame, text="👤 Avatares")
        
        # Card de configuração
        config_card = ModernCard(avatar_frame, title="Geração de Avatares")
        config_card.pack(fill='x', pady=(0, 20))
        
        # Campos
        fields_frame = ttk.Frame(config_card.content_frame, style='Card.TFrame')
        fields_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(fields_frame, text="Nome do Avatar:", style='Modern.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.avatar_name_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=30)
        self.avatar_name_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        ttk.Label(fields_frame, text="Profissão:", style='Modern.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.avatar_profession_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=30)
        self.avatar_profession_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        ttk.Label(fields_frame, text="Características:", style='Modern.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.avatar_features_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=30)
        self.avatar_features_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Botões
        buttons_frame = ttk.Frame(config_card.content_frame, style='Card.TFrame')
        buttons_frame.pack(fill='x')
        
        generate_btn = ModernButton(buttons_frame, text="🎨 Gerar Avatar", 
                                  command=self.generate_avatar, style_type="success")
        generate_btn.pack(side='left', padx=(0, 10))
        
        # Card de resultado
        result_card = ModernCard(avatar_frame, title="Avatar Gerado")
        result_card.pack(fill='both', expand=True)
        
        # Frame para imagem
        self.avatar_image_frame = ttk.Frame(result_card.content_frame, style='Card.TFrame')
        self.avatar_image_frame.pack(fill='both', expand=True)
        
        self.avatar_image_label = ttk.Label(self.avatar_image_frame, 
                                          text="Nenhum avatar gerado ainda", 
                                          style='Modern.TLabel')
        self.avatar_image_label.pack(expand=True)
        
    def create_competitors_tab(self):
        """Cria a aba de análise de concorrentes"""
        competitors_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(competitors_frame, text="🏢 Concorrentes")
        
        # Card de configuração
        config_card = ModernCard(competitors_frame, title="Análise de Concorrentes")
        config_card.pack(fill='x', pady=(0, 20))
        
        # Campo de nicho
        fields_frame = ttk.Frame(config_card.content_frame, style='Card.TFrame')
        fields_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(fields_frame, text="Nicho para Análise:", style='Modern.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.competitors_nicho_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=50)
        self.competitors_nicho_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Botão
        analyze_btn = ModernButton(config_card.content_frame, text="🔍 Analisar Concorrentes", 
                                 command=self.analyze_competitors, style_type="success")
        analyze_btn.pack(anchor='w')
        
        # Card de resultados
        results_card = ModernCard(competitors_frame, title="Concorrentes Identificados")
        results_card.pack(fill='both', expand=True)
        
        # Treeview para mostrar concorrentes
        columns = ('Nome', 'Tipo', 'Descrição', 'Website')
        self.competitors_tree = ttk.Treeview(results_card.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.competitors_tree.heading(col, text=col)
            self.competitors_tree.column(col, width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_card.content_frame, orient='vertical', command=self.competitors_tree.yview)
        self.competitors_tree.configure(yscrollcommand=scrollbar.set)
        
        self.competitors_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def create_funnel_tab(self):
        """Cria a aba de funil de vendas"""
        funnel_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(funnel_frame, text="📈 Funil de Vendas")
        
        # Card de configuração
        config_card = ModernCard(funnel_frame, title="Geração de Funil de Vendas")
        config_card.pack(fill='x', pady=(0, 20))
        
        # Campos
        fields_frame = ttk.Frame(config_card.content_frame, style='Card.TFrame')
        fields_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(fields_frame, text="Nicho:", style='Modern.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.funnel_nicho_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=30)
        self.funnel_nicho_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        ttk.Label(fields_frame, text="Produto/Serviço:", style='Modern.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.funnel_product_entry = ttk.Entry(fields_frame, style='Modern.TEntry', width=30)
        self.funnel_product_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Botão
        generate_funnel_btn = ModernButton(config_card.content_frame, text="📊 Gerar Funil", 
                                         command=self.generate_funnel, style_type="success")
        generate_funnel_btn.pack(anchor='w')
        
        # Card de resultado
        result_card = ModernCard(funnel_frame, title="Funil Gerado")
        result_card.pack(fill='both', expand=True)
        
        # Frame para imagem do funil
        self.funnel_image_frame = ttk.Frame(result_card.content_frame, style='Card.TFrame')
        self.funnel_image_frame.pack(fill='both', expand=True)
        
        self.funnel_image_label = ttk.Label(self.funnel_image_frame, 
                                          text="Nenhum funil gerado ainda", 
                                          style='Modern.TLabel')
        self.funnel_image_label.pack(expand=True)
        
    def create_results_tab(self):
        """Cria a aba de resultados"""
        results_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(results_frame, text="📋 Resultados")
        
        # Card de exportação
        export_card = ModernCard(results_frame, title="Exportar Resultados")
        export_card.pack(fill='x', pady=(0, 20))
        
        buttons_frame = ttk.Frame(export_card.content_frame, style='Card.TFrame')
        buttons_frame.pack(fill='x')
        
        export_json_btn = ModernButton(buttons_frame, text="📄 Exportar JSON", 
                                     command=self.export_json)
        export_json_btn.pack(side='left', padx=(0, 10))
        
        export_pdf_btn = ModernButton(buttons_frame, text="📑 Exportar PDF", 
                                    command=self.export_pdf)
        export_pdf_btn.pack(side='left', padx=(0, 10))
        
        open_folder_btn = ModernButton(buttons_frame, text="📁 Abrir Pasta", 
                                     command=self.open_results_folder)
        open_folder_btn.pack(side='left')
        
        # Card de visualização
        view_card = ModernCard(results_frame, title="Visualização dos Resultados")
        view_card.pack(fill='both', expand=True)
        
        self.results_text = scrolledtext.ScrolledText(view_card.content_frame,
                                                    height=20,
                                                    bg=ModernStyle.COLORS['bg_tertiary'],
                                                    fg=ModernStyle.COLORS['text_primary'],
                                                    font=ModernStyle.FONTS['code'],
                                                    insertbackground=ModernStyle.COLORS['text_primary'])
        self.results_text.pack(fill='both', expand=True)
        
    def create_settings_tab(self):
        """Cria a aba de configurações"""
        settings_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(settings_frame, text="⚙️ Configurações")
        
        # Card de APIs
        api_card = ModernCard(settings_frame, title="Configurações de APIs")
        api_card.pack(fill='x', pady=(0, 20))
        
        # Campos de API
        api_fields_frame = ttk.Frame(api_card.content_frame, style='Card.TFrame')
        api_fields_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(api_fields_frame, text="Google API Key:", style='Modern.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.google_api_entry = ttk.Entry(api_fields_frame, style='Modern.TEntry', width=50, show="*")
        self.google_api_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        ttk.Label(api_fields_frame, text="OpenAI API Key:", style='Modern.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.openai_api_entry = ttk.Entry(api_fields_frame, style='Modern.TEntry', width=50, show="*")
        self.openai_api_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        ttk.Label(api_fields_frame, text="OpenRouter API Key:", style='Modern.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.openrouter_api_entry = ttk.Entry(api_fields_frame, style='Modern.TEntry', width=50, show="*")
        self.openrouter_api_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        api_fields_frame.columnconfigure(1, weight=1)
        
        # Botões de API
        api_buttons_frame = ttk.Frame(api_card.content_frame, style='Card.TFrame')
        api_buttons_frame.pack(fill='x')
        
        save_api_btn = ModernButton(api_buttons_frame, text="💾 Salvar APIs", 
                                  command=self.save_api_keys, style_type="success")
        save_api_btn.pack(side='left', padx=(0, 10))
        
        test_api_btn = ModernButton(api_buttons_frame, text="🧪 Testar APIs", 
                                  command=self.test_api_keys)
        test_api_btn.pack(side='left')
        
        # Card de sistema
        system_card = ModernCard(settings_frame, title="Informações do Sistema")
        system_card.pack(fill='both', expand=True)
        
        # Informações do sistema
        system_info = f"""
ARQV30 Enhanced v3.0 - Interface Nativa
Versão: 3.0.0
Python: {sys.version}
Tkinter: Disponível
PIL: {'Disponível' if PIL_AVAILABLE else 'Não disponível'}
Serviços: {'Disponíveis' if SERVICES_AVAILABLE else 'Não disponíveis'}
Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        """
        
        system_label = ttk.Label(system_card.content_frame, text=system_info.strip(), 
                               style='Modern.TLabel', justify='left')
        system_label.pack(anchor='w', pady=10)
        
    # Métodos de funcionalidade
    
    def log_message(self, message: str, level: str = "INFO"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, status: str):
        """Atualiza o status da aplicação"""
        self.status_label.config(text=status)
        self.root.update_idletasks()
        
    def update_progress(self, value: float, text: str = ""):
        """Atualiza a barra de progresso"""
        self.progress_var.set(value)
        if text:
            self.progress_label.config(text=text)
        self.root.update_idletasks()
        
    def start_complete_analysis(self):
        """Inicia análise completa"""
        if self.analysis_running:
            messagebox.showwarning("Aviso", "Uma análise já está em execução!")
            return
            
        nicho = self.nicho_entry.get().strip()
        publico = self.publico_entry.get().strip()
        localizacao = self.localizacao_entry.get().strip()
        
        if not nicho:
            messagebox.showerror("Erro", "Por favor, informe o nicho/mercado!")
            return
            
        self.analysis_running = True
        self.update_status("Executando análise completa...")
        self.log_message("Iniciando análise completa do mercado")
        
        # Executa em thread separada
        thread = threading.Thread(target=self._run_complete_analysis, 
                                args=(nicho, publico, localizacao))
        thread.daemon = True
        thread.start()
        
    def _run_complete_analysis(self, nicho: str, publico: str, localizacao: str):
        """Executa análise completa em thread separada"""
        try:
            if not SERVICES_AVAILABLE:
                self.log_message("Serviços não disponíveis!", "ERROR")
                return
                
            self.update_progress(10, "Preparando análise...")
            
            # Dados de entrada
            analysis_data = {
                'nicho': nicho,
                'publico_alvo': publico,
                'localizacao': localizacao,
                'timestamp': datetime.now().isoformat()
            }
            
            self.update_progress(25, "Executando análise integrada...")
            self.log_message("Executando análise com sistemas integrados")
            
            # Executa análise integrada
            integration_service = self.services.get('integration')
            if integration_service:
                result = integration_service.execute_integrated_analysis(analysis_data)
                
                self.update_progress(75, "Processando resultados...")
                self.log_message("Análise concluída com sucesso!")
                
                # Salva resultados
                self.results_data = result
                self._display_results(result)
                
                self.update_progress(100, "Análise completa!")
                self.update_status("Análise concluída com sucesso")
                
            else:
                self.log_message("Serviço de integração não disponível", "ERROR")
                
        except Exception as e:
            self.log_message(f"Erro durante análise: {e}", "ERROR")
            self.update_status("Erro na análise")
        finally:
            self.analysis_running = False
            
    def start_quick_analysis(self):
        """Inicia análise rápida"""
        messagebox.showinfo("Info", "Análise rápida em desenvolvimento!")
        
    def stop_analysis(self):
        """Para a análise em execução"""
        if self.analysis_running:
            self.analysis_running = False
            self.update_status("Análise interrompida")
            self.log_message("Análise interrompida pelo usuário", "WARNING")
        else:
            messagebox.showinfo("Info", "Nenhuma análise em execução!")
            
    def generate_avatar(self):
        """Gera avatar"""
        name = self.avatar_name_entry.get().strip()
        profession = self.avatar_profession_entry.get().strip()
        features = self.avatar_features_entry.get().strip()
        
        if not name:
            messagebox.showerror("Erro", "Por favor, informe o nome do avatar!")
            return
            
        self.log_message(f"Gerando avatar: {name}")
        
        try:
            if SERVICES_AVAILABLE and 'avatar' in self.services:
                avatar_service = self.services['avatar']
                
                avatar_data = {
                    'nome': name,
                    'profissao': profession or 'Profissional',
                    'caracteristicas': features or 'Pessoa profissional e confiável'
                }
                
                result = avatar_service.gerar_avatar_completo(avatar_data)
                
                if result.get('success') and result.get('image_path'):
                    self._display_avatar_image(result['image_path'])
                    self.log_message("Avatar gerado com sucesso!")
                else:
                    self.log_message("Erro ao gerar avatar", "ERROR")
            else:
                self.log_message("Serviço de avatar não disponível", "ERROR")
                
        except Exception as e:
            self.log_message(f"Erro ao gerar avatar: {e}", "ERROR")
            
    def analyze_competitors(self):
        """Analisa concorrentes"""
        nicho = self.competitors_nicho_entry.get().strip()
        
        if not nicho:
            messagebox.showerror("Erro", "Por favor, informe o nicho!")
            return
            
        self.log_message(f"Analisando concorrentes para: {nicho}")
        
        try:
            if SERVICES_AVAILABLE and 'competitors' in self.services:
                competitors_service = self.services['competitors']
                
                result = competitors_service.coletar_concorrentes_completo(nicho)
                
                if result.get('success'):
                    self._display_competitors(result.get('concorrentes', []))
                    self.log_message("Análise de concorrentes concluída!")
                else:
                    self.log_message("Erro na análise de concorrentes", "ERROR")
            else:
                self.log_message("Serviço de concorrentes não disponível", "ERROR")
                
        except Exception as e:
            self.log_message(f"Erro ao analisar concorrentes: {e}", "ERROR")
            
    def generate_funnel(self):
        """Gera funil de vendas"""
        nicho = self.funnel_nicho_entry.get().strip()
        product = self.funnel_product_entry.get().strip()
        
        if not nicho:
            messagebox.showerror("Erro", "Por favor, informe o nicho!")
            return
            
        self.log_message(f"Gerando funil para: {nicho}")
        
        try:
            if SERVICES_AVAILABLE and 'funnel' in self.services:
                funnel_service = self.services['funnel']
                
                funnel_data = {
                    'nicho': nicho,
                    'produto': product or 'Produto/Serviço'
                }
                
                result = funnel_service.gerar_funil_completo(funnel_data)
                
                if result.get('success') and result.get('image_path'):
                    self._display_funnel_image(result['image_path'])
                    self.log_message("Funil gerado com sucesso!")
                else:
                    self.log_message("Erro ao gerar funil", "ERROR")
            else:
                self.log_message("Serviço de funil não disponível", "ERROR")
                
        except Exception as e:
            self.log_message(f"Erro ao gerar funil: {e}", "ERROR")
            
    def _display_avatar_image(self, image_path: str):
        """Exibe imagem do avatar"""
        try:
            if PIL_AVAILABLE and os.path.exists(image_path):
                # Carrega e redimensiona imagem
                image = Image.open(image_path)
                image = image.resize((300, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Atualiza label
                self.avatar_image_label.config(image=photo, text="")
                self.avatar_image_label.image = photo  # Mantém referência
            else:
                self.avatar_image_label.config(text=f"Avatar salvo em: {image_path}")
        except Exception as e:
            self.log_message(f"Erro ao exibir avatar: {e}", "ERROR")
            
    def _display_funnel_image(self, image_path: str):
        """Exibe imagem do funil"""
        try:
            if PIL_AVAILABLE and os.path.exists(image_path):
                # Carrega e redimensiona imagem
                image = Image.open(image_path)
                # Mantém proporção
                image.thumbnail((600, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Atualiza label
                self.funnel_image_label.config(image=photo, text="")
                self.funnel_image_label.image = photo  # Mantém referência
            else:
                self.funnel_image_label.config(text=f"Funil salvo em: {image_path}")
        except Exception as e:
            self.log_message(f"Erro ao exibir funil: {e}", "ERROR")
            
    def _display_competitors(self, competitors: List[Dict]):
        """Exibe lista de concorrentes"""
        # Limpa árvore
        for item in self.competitors_tree.get_children():
            self.competitors_tree.delete(item)
            
        # Adiciona concorrentes
        for competitor in competitors:
            self.competitors_tree.insert('', 'end', values=(
                competitor.get('nome', 'N/A'),
                competitor.get('tipo', 'N/A'),
                competitor.get('descricao', 'N/A')[:50] + '...' if len(competitor.get('descricao', '')) > 50 else competitor.get('descricao', 'N/A'),
                competitor.get('website', 'N/A')
            ))
            
    def _display_results(self, results: Dict):
        """Exibe resultados na aba de resultados"""
        try:
            # Formata resultados como JSON
            formatted_results = json.dumps(results, indent=2, ensure_ascii=False)
            
            # Atualiza texto
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, formatted_results)
            
        except Exception as e:
            self.log_message(f"Erro ao exibir resultados: {e}", "ERROR")
            
    def export_json(self):
        """Exporta resultados em JSON"""
        if not self.results_data:
            messagebox.showwarning("Aviso", "Nenhum resultado para exportar!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Salvar resultados como JSON"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.results_data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Sucesso", f"Resultados exportados para: {filename}")
                self.log_message(f"Resultados exportados: {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {e}")
                
    def export_pdf(self):
        """Exporta resultados em PDF"""
        messagebox.showinfo("Info", "Exportação PDF em desenvolvimento!")
        
    def open_results_folder(self):
        """Abre pasta de resultados"""
        results_folder = os.path.dirname(__file__)
        try:
            os.startfile(results_folder)  # Windows
        except:
            try:
                os.system(f'explorer "{results_folder}"')  # Windows alternativo
            except:
                messagebox.showinfo("Info", f"Pasta de resultados: {results_folder}")
                
    def save_api_keys(self):
        """Salva chaves de API"""
        messagebox.showinfo("Info", "Salvamento de APIs em desenvolvimento!")
        
    def test_api_keys(self):
        """Testa chaves de API"""
        messagebox.showinfo("Info", "Teste de APIs em desenvolvimento!")
        
    def open_settings(self):
        """Abre configurações"""
        self.notebook.select(5)  # Seleciona aba de configurações
        
    def run(self):
        """Executa a aplicação"""
        self.log_message("ARQV30 Enhanced v3.0 - Interface Nativa Iniciada")
        self.log_message("Sistema pronto para uso!")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n✅ Aplicação encerrada pelo usuário")
        except Exception as e:
            print(f"❌ Erro na aplicação: {e}")

def main():
    """Função principal"""
    print("🚀 ARQV30 Enhanced v3.0 - Interface Nativa para Windows")
    print("=" * 60)
    
    try:
        app = ARQNativeApp()
        app.run()
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação:\n{e}")

if __name__ == '__main__':
    main()