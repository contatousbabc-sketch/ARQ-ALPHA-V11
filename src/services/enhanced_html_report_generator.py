#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced HTML Report Generator
Gerador de relatórios HTML com design moderno baseado no template modelo
"""

import os
import logging
import json
import base64
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import re
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedHTMLReportGenerator:
    """Gerador de relatórios HTML com design moderno e sidebar navegável"""

    def __init__(self):
        """Inicializa o gerador"""
        self.session_id = None
        self.report_data = {}
        self.images_base64 = {}
        
        # Ordem dos módulos
        self.modules_order = [
            'anti_objecao',
            'avatars',
            'concorrencia',
            'drivers_mentais',
            'funil_vendas',
            'insights_mercado',
            'palavras_chave',
            'plano_acao',
            'posicionamento',
            'pre_pitch',
            'predicoes_futuro',
            'provas_visuais',
            'metricas_conversao',
            'estrategia_preco',
            'canais_aquisicao',
            'cronograma_lancamento',
            'cpl_protocol_1',
            'cpl_protocol_2',
            'cpl_protocol_3',
            'cpl_protocol_4',
            'cpl_protocol_5',
            'cpl_completo',
            'analise_sentimento',
            'mapeamento_tendencias',
            'oportunidades_mercado',
            'riscos_ameacas',
            'conteudo_viral'
        ]

        # Títulos dos módulos
        self.module_titles = {
            'anti_objecao': 'Sistema Anti-Objeção',
            'avatars': 'Avatares do Público-Alvo',
            'concorrencia': 'Análise Competitiva',
            'drivers_mentais': 'Drivers Mentais',
            'funil_vendas': 'Funil de Vendas',
            'insights_mercado': 'Insights de Mercado',
            'palavras_chave': 'Estratégia de Palavras-Chave',
            'plano_acao': 'Plano de Ação',
            'posicionamento': 'Estratégia de Posicionamento',
            'pre_pitch': 'Estrutura de Pré-Pitch',
            'predicoes_futuro': 'Predições de Mercado',
            'provas_visuais': 'Sistema de Provas Visuais',
            'metricas_conversao': 'Métricas de Conversão',
            'estrategia_preco': 'Estratégia de Precificação',
            'canais_aquisicao': 'Canais de Aquisição',
            'cronograma_lancamento': 'Cronograma de Lançamento',
            'cpl_protocol_1': 'Arquitetura do Evento Magnético',
            'cpl_protocol_2': 'CPL1 - A Oportunidade Paralisante',
            'cpl_protocol_3': 'CPL2 - A Transformação Impossível',
            'cpl_protocol_4': 'CPL3 - O Caminho Revolucionário',
            'cpl_protocol_5': 'CPL4 - A Decisão Inevitável',
            'cpl_completo': 'Protocolo Integrado de CPLs Devastadores',
            'analise_sentimento': 'Análise de Sentimento Detalhada',
            'mapeamento_tendencias': 'Mapeamento de Tendências e Previsões',
            'oportunidades_mercado': 'Identificação de Oportunidades de Mercado',
            'riscos_ameacas': 'Avaliação de Riscos e Ameaças',
            'conteudo_viral': 'Análise de Conteúdo Viral e Fatores de Sucesso'
        }

    def generate_html_report(self, session_id: str, report_data: Dict[str, Any], output_path: str = None) -> str:
        """
        Gera relatório HTML completo com design moderno

        Args:
            session_id: ID da sessão
            report_data: Dados do relatório
            output_path: Caminho de saída (opcional)

        Returns:
            Caminho do arquivo HTML gerado
        """
        try:
            self.session_id = session_id
            self.report_data = report_data

            logger.info(f"🎨 Gerando relatório HTML moderno para sessão: {session_id}")

            # GARANTIR que os CPLs estejam presentes antes de gerar HTML
            from .cpl_integration_manager import cpl_integration_manager
            cpl_status = cpl_integration_manager.garantir_cpls_nos_modulos(session_id)
            logger.info(f"🎯 CPLs garantidos para HTML: {len(cpl_status.get('cpls_encontrados', []))} encontrados, {len(cpl_status.get('cpls_criados', []))} criados")

            # Carregar e converter imagens para base64
            self._load_images_as_base64()

            # Gerar HTML completo
            html_content = self._generate_complete_html()

            # Definir caminho de saída
            if not output_path:
                output_path = f"analyses_data/{session_id}/relatorio_final_moderno.html"

            # Salvar arquivo
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"✅ Relatório HTML moderno gerado: {output_file}")
            return str(output_file)

        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório HTML: {e}")
            raise

    def _load_images_as_base64(self):
        """Carrega todas as imagens encontradas e converte para base64"""
        try:
            # Diretórios onde procurar imagens
            image_dirs = [
                f"analyses_data/{self.session_id}",
                "downloaded_images",
                "screenshots",
                "viral_images_data"
            ]

            for dir_path in image_dirs:
                if os.path.exists(dir_path):
                    self._scan_directory_for_images(dir_path)

            logger.info(f"📸 {len(self.images_base64)} imagens carregadas como base64")

        except Exception as e:
            logger.error(f"❌ Erro ao carregar imagens: {e}")

    def _scan_directory_for_images(self, directory: str):
        """Escaneia diretório em busca de imagens"""
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'rb') as img_file:
                                img_data = img_file.read()
                                img_base64 = base64.b64encode(img_data).decode('utf-8')

                                # Determinar tipo MIME
                                ext = file.lower().split('.')[-1]
                                mime_type = f"image/{ext}" if ext != 'jpg' else "image/jpeg"

                                # Armazenar com chave única
                                key = f"{os.path.basename(root)}_{file}"
                                self.images_base64[key] = f"data:{mime_type};base64,{img_base64}"

                        except Exception as e:
                            logger.warning(f"⚠️ Erro ao processar imagem {file_path}: {e}")

        except Exception as e:
            logger.error(f"❌ Erro ao escanear diretório {directory}: {e}")

    def _generate_complete_html(self) -> str:
        """Gera o HTML completo com design moderno"""
        try:
            # Extrair dados principais
            titulo = self.report_data.get('titulo', f'Relatório de Análise - {self.session_id}')

            # Gerar seções do conteúdo
            content_sections = self._generate_content_sections()

            # Gerar sidebar com índice
            sidebar_html = self._generate_sidebar(content_sections)

            # Gerar conteúdo principal
            main_content = self._generate_main_content(content_sections)

            # Template HTML completo
            html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>{titulo}</title>
    <style>
        {self._get_modern_css()}
    </style>
</head>
<body>
    {sidebar_html}
    <div class="container">
        <h1>
            {self._get_header_image()}
            {titulo}
        </h1>

        {main_content}

        <footer>
            <div class="timestamp">
                <p>Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                <p>Sessão: {self.session_id}</p>
                <p>ARQV30 Enhanced v3.0 - Sistema de Análise Ultra-Detalhada</p>
            </div>
        </footer>
    </div>

    <script>
        {self._get_navigation_script()}
    </script>
</body>
</html>"""

            return html_template

        except Exception as e:
            logger.error(f"❌ Erro ao gerar HTML completo: {e}")
            raise

    def _generate_content_sections(self) -> List[Dict[str, Any]]:
        """Gera lista de seções do conteúdo"""
        sections = []

        try:
            # Seção de Sumário Executivo
            if 'sumario_executivo' in self.report_data:
                sections.append({
                    'id': 'sumario-executivo',
                    'title': 'SUMÁRIO EXECUTIVO',
                    'content': self.report_data['sumario_executivo'],
                    'type': 'summary'
                })

            # Seção de Evidências Visuais (imagens)
            if self.images_base64:
                sections.append({
                    'id': 'evidencias-visuais',
                    'title': 'EVIDÊNCIAS VISUAIS',
                    'content': self._generate_image_gallery(),
                    'type': 'images'
                })

            # Seções dos módulos
            if 'modules' in self.report_data:
                for module_name, module_data in self.report_data['modules'].items():
                    if isinstance(module_data, dict) and 'content' in module_data:
                        sections.append({
                            'id': self._generate_section_id(module_name),
                            'title': module_data.get('title', self.module_titles.get(module_name, module_name.replace('_', ' ').title())),
                            'content': module_data['content'],
                            'type': 'module'
                        })

            return sections

        except Exception as e:
            logger.error(f"❌ Erro ao gerar seções de conteúdo: {e}")
            return []

    def _generate_sidebar(self, sections: List[Dict[str, Any]]) -> str:
        """Gera HTML da sidebar com índice navegável"""
        try:
            sidebar_items = []

            for section in sections:
                # Gerar sub-itens se houver
                sub_items = self._extract_subsections(section['content'])
                sub_items_html = ""

                if sub_items:
                    sub_items_list = []
                    for sub_item in sub_items:
                        sub_items_list.append(f'<li class="toc-h3"><a href="#{sub_item["id"]}">{sub_item["title"]}</a></li>')
                    sub_items_html = f'<ul class="toc-h3-list">{"".join(sub_items_list)}</ul>'

                sidebar_items.append(f'''
                    <li class="toc-h2">
                        <a href="#{section['id']}">{section['title']}</a>
                        {sub_items_html}
                    </li>
                ''')

            sidebar_html = f'''
            <nav class="sidebar-toc" id="sidebar-toc">
                <h2>Índice</h2>
                <ul>
                    {"".join(sidebar_items)}
                </ul>
            </nav>
            '''

            return sidebar_html

        except Exception as e:
            logger.error(f"❌ Erro ao gerar sidebar: {e}")
            return '<nav class="sidebar-toc"><h2>Índice</h2><ul></ul></nav>'

    def _generate_main_content(self, sections: List[Dict[str, Any]]) -> str:
        """Gera conteúdo principal do relatório"""
        try:
            content_html = []

            for section in sections:
                section_html = f'''
                <section class="section-card" id="{section['id']}">
                    <h2>{section['title']}</h2>
                    {self._format_section_content(section['content'], section['type'])}
                </section>
                '''
                content_html.append(section_html)

            return "".join(content_html)

        except Exception as e:
            logger.error(f"❌ Erro ao gerar conteúdo principal: {e}")
            return "<p>Erro ao gerar conteúdo</p>"

    def _format_section_content(self, content: str, section_type: str) -> str:
        """Formata conteúdo da seção baseado no tipo"""
        try:
            if section_type == 'images':
                return content  # Já formatado como galeria

            # Converter markdown básico para HTML
            formatted_content = self._markdown_to_html(content)

            return formatted_content

        except Exception as e:
            logger.error(f"❌ Erro ao formatar conteúdo da seção: {e}")
            return str(content)

    def _markdown_to_html(self, text: str) -> str:
        """Converte markdown básico para HTML"""
        try:
            # Headers
            text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
            text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
            text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)

            # Bold e Italic
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)

            # Listas
            lines = text.split('\n')
            result_lines = []
            in_list = False
            
            for line in lines:
                if line.strip().startswith('- ') or line.strip().startswith('* '):
                    if not in_list:
                        result_lines.append('<ul>')
                        in_list = True
                    item_text = line.strip()[2:]
                    result_lines.append(f'<li>{item_text}</li>')
                else:
                    if in_list:
                        result_lines.append('</ul>')
                        in_list = False
                    result_lines.append(line)
            
            if in_list:
                result_lines.append('</ul>')
            
            text = '\n'.join(result_lines)

            # Parágrafos
            paragraphs = text.split('\n\n')
            formatted_paragraphs = []

            for para in paragraphs:
                para = para.strip()
                if para and not para.startswith('<'):
                    para = f'<p>{para}</p>'
                formatted_paragraphs.append(para)

            return '\n'.join(formatted_paragraphs)

        except Exception as e:
            logger.error(f"❌ Erro ao converter markdown: {e}")
            return text

    def _generate_image_gallery(self) -> str:
        """Gera galeria de imagens"""
        try:
            if not self.images_base64:
                return "<p>Nenhuma imagem encontrada.</p>"

            gallery_items = []

            for img_key, img_data in self.images_base64.items():
                gallery_items.append(f'''
                    <div class="screenshot-item">
                        <img src="{img_data}" alt="{img_key}" style="max-width: 100%; height: auto; border-radius: 8px;"/>
                        <p style="margin-top: 10px; font-size: 0.9em; color: #666;">{img_key}</p>
                    </div>
                ''')

            gallery_html = f'''
            <div class="image-grid">
                {"".join(gallery_items)}
            </div>
            '''

            return gallery_html

        except Exception as e:
            logger.error(f"❌ Erro ao gerar galeria de imagens: {e}")
            return "<p>Erro ao carregar imagens.</p>"

    def _extract_subsections(self, content: str) -> List[Dict[str, str]]:
        """Extrai subseções do conteúdo"""
        try:
            subsections = []

            # Procurar por headers H3
            h3_matches = re.findall(r'^### (.*$)', content, re.MULTILINE)

            for match in h3_matches:
                subsections.append({
                    'id': self._generate_section_id(match),
                    'title': match.strip()
                })

            return subsections

        except Exception as e:
            logger.error(f"❌ Erro ao extrair subseções: {e}")
            return []

    def _generate_section_id(self, title: str) -> str:
        """Gera ID único para seção"""
        try:
            # Remover caracteres especiais e converter para lowercase
            section_id = re.sub(r'[^a-zA-Z0-9\s]', '', title)
            section_id = re.sub(r'\s+', '-', section_id.strip())
            section_id = section_id.lower()

            return section_id

        except Exception as e:
            logger.error(f"❌ Erro ao gerar ID da seção: {e}")
            return "secao-sem-id"

    def _get_header_image(self) -> str:
        """Retorna imagem do cabeçalho"""
        # Usar primeira imagem disponível ou placeholder
        if self.images_base64:
            first_image = list(self.images_base64.values())[0]
            return f'<img src="{first_image}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; margin-right: 15px;"/>'

        # Placeholder SVG
        return '''<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; margin-right: 15px;">AR</div>'''

    def _get_modern_css(self) -> str:
        """Retorna CSS moderno baseado no template"""
        return '''
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            display: flex;
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }

        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            margin-left: 320px;
            max-width: 900px;
            flex-grow: 1;
            margin-top: 20px;
            margin-bottom: 20px;
            margin-right: 20px;
        }

        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
        }

        h2 {
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }

        h3 {
            color: #2c3e50;
            margin-top: 25px;
        }

        .section-card {
            background: white;
            padding: 2.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            position: relative;
            border-radius: 8px;
        }

        .section-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
            border-radius: 4px 0 0 4px;
        }

        .sidebar-toc {
            position: fixed;
            left: 0;
            top: 0;
            width: 300px;
            height: 100vh;
            overflow-y: auto;
            background-color: #f4f4f4;
            padding: 20px;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            z-index: 1000;
        }

        .sidebar-toc h2 {
            margin-top: 0;
            padding-left: 0;
            border-left: none;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }

        .sidebar-toc ul {
            list-style: none;
            padding-left: 0;
        }

        .sidebar-toc li {
            margin-bottom: 5px;
        }

        .sidebar-toc a {
            text-decoration: none;
            color: #333;
            display: block;
            padding: 5px 0;
            transition: color 0.2s;
        }

        .sidebar-toc a:hover {
            color: #3498db;
        }

        .sidebar-toc a.active {
            color: #3498db;
            font-weight: bold;
        }

        .toc-h2 > a {
            font-weight: bold;
            font-size: 1.1em;
            color: #2c3e50;
            margin-top: 10px;
        }

        .toc-h3-list {
            padding-left: 15px;
            margin-top: 5px;
        }

        .toc-h3 a {
            font-size: 0.9em;
            color: #666;
        }

        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }

        .image-grid img {
            width: 100%;
            height: auto;
            aspect-ratio: 1 / 1;
            object-fit: cover;
            border: 3px solid #e5e7eb;
            transition: all 0.3s ease;
            border-radius: 8px;
        }

        .image-grid img:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
            border-color: #3b82f6;
        }

        .screenshot-item {
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }

        footer {
            background: #f9fafb;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 3px solid #3b82f6;
            border-radius: 8px;
        }

        .timestamp {
            color: #7f8c8d;
            font-size: 0.9em;
            text-align: center;
        }

        .stats-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }

        pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }

        ul, ol {
            padding-left: 25px;
        }

        li {
            margin-bottom: 8px;
        }

        blockquote {
            border-left: 4px solid #f39c12;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            background: #fef9e7;
            padding: 15px 20px;
            border-radius: 0 8px 8px 0;
        }
        '''

    def _get_navigation_script(self) -> str:
        """Retorna JavaScript para navegação"""
        return '''
        // Smooth scrolling para links da sidebar
        document.querySelectorAll('.sidebar-toc a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Highlight da seção ativa na sidebar
        window.addEventListener('scroll', function() {
            const sections = document.querySelectorAll('.section-card[id]');
            const navLinks = document.querySelectorAll('.sidebar-toc a[href^="#"]');

            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (pageYOffset >= sectionTop - 200) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        });
        '''


def load_modules_for_session(session_id: str) -> Dict[str, Dict[str, str]]:
    """
    Carrega módulos disponíveis de uma sessão específica, incluindo arquivos .md (CPLs)
    Procura na raiz da sessão E dentro da pasta modules/

    Args:
        session_id: ID da sessão

    Returns:
        Dicionário com módulos carregados
    """
    temp_generator = EnhancedHTMLReportGenerator()
    available_modules = {}
    
    # Diretório da sessão
    session_dir = Path(f"analyses_data/{session_id}")
    modules_dir = session_dir / "modules"
    
    # Lista de diretórios para procurar .md
    search_dirs = [session_dir]
    if modules_dir.exists():
        search_dirs.append(modules_dir)
    
    # Contador de arquivos carregados
    loaded_count = 0
    
    # Procurar arquivos .md em todos os diretórios
    for search_dir in search_dirs:
        if search_dir.exists():
            logger.info(f"📂 Procurando arquivos .md em: {search_dir}")
            
            # Procurar recursivamente por arquivos .md
            for md_file in search_dir.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Usar nome do arquivo como identificador
                    module_name = md_file.stem
                    
                    # Verificar se já existe um título personalizado
                    title = temp_generator.module_titles.get(
                        module_name, 
                        module_name.replace('_', ' ').replace('-', ' ').title()
                    )
                    
                    available_modules[module_name] = {
                        'title': title,
                        'content': content
                    }
                    loaded_count += 1
                    logger.info(f"✅ Módulo carregado: {md_file.name} (de {md_file.parent.name})")
                    
                except Exception as e:
                    logger.error(f"❌ Erro ao carregar {md_file.name}: {e}")
    
    logger.info(f"📊 Total de módulos .md carregados: {loaded_count}")
    
    # Se nenhum módulo foi carregado, adicionar mensagem informativa
    if loaded_count == 0:
        logger.warning("⚠️ Nenhum arquivo .md encontrado nas pastas da sessão")
        logger.warning(f"   Procurado em: {session_dir} e {modules_dir}")
        
        # Adicionar módulos placeholder com aviso
        for module_name in temp_generator.modules_order:
            available_modules[module_name] = {
                'title': temp_generator.module_titles.get(module_name, module_name.replace('_', ' ').title()),
                'content': f"⚠️ **Módulo não encontrado**\n\nO arquivo .md para este módulo não foi encontrado na pasta da sessão.\n\nProcurado em:\n- `{session_dir}`\n- `{modules_dir}`"
            }
    
    logger.info(f"📊 {len(available_modules)} módulos no total preparados para o relatório")
    return available_modules


def solicitar_session_id() -> str:
    """
    Solicita o session_id ao usuário de forma interativa
    
    Returns:
        ID da sessão escolhida
    """
    print("\n" + "="*60)
    print("🎨 GERADOR DE RELATÓRIO HTML - ARQV30 Enhanced v3.0")
    print("="*60)
    
    # Verificar se o diretório analyses_data existe
    analyses_dir = Path("analyses_data")
    if not analyses_dir.exists():
        print("\n❌ Erro: Diretório 'analyses_data' não encontrado!")
        print("Por favor, certifique-se de que o diretório existe.")
        sys.exit(1)
    
    # Listar sessões disponíveis
    sessions = [d.name for d in analyses_dir.iterdir() if d.is_dir()]
    
    if not sessions:
        print("\n❌ Nenhuma sessão encontrada no diretório 'analyses_data'!")
        print("Por favor, execute uma análise primeiro.")
        sys.exit(1)
    
    print(f"\n📁 Sessões disponíveis ({len(sessions)}):")
    print("-" * 60)
    
    for idx, session in enumerate(sessions, 1):
        # Verificar se tem pasta modules
        modules_dir = analyses_dir / session / "modules"
        has_modules = "✓" if modules_dir.exists() else "✗"
        
        # Contar arquivos .md
        md_count = len(list((analyses_dir / session).rglob("*.md")))
        
        print(f"{idx}. {session} [{has_modules} modules | {md_count} arquivos .md]")
    
    print("-" * 60)
    
    # Solicitar escolha do usuário
    while True:
        try:
            escolha = input("\n👉 Digite o número da sessão ou o nome completo: ").strip()
            
            # Verificar se é um número
            if escolha.isdigit():
                idx = int(escolha)
                if 1 <= idx <= len(sessions):
                    session_id = sessions[idx - 1]
                    break
                else:
                    print(f"❌ Número inválido. Digite um número entre 1 e {len(sessions)}.")
            # Verificar se é um nome de sessão válido
            elif escolha in sessions:
                session_id = escolha
                break
            else:
                print("❌ Sessão não encontrada. Tente novamente.")
        
        except KeyboardInterrupt:
            print("\n\n❌ Operação cancelada pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print(f"\n✅ Sessão selecionada: {session_id}")
    return session_id


if __name__ == "__main__":
    try:
        # Solicitar session_id de forma interativa
        if len(sys.argv) > 1:
            # Se passou como argumento, usar
            session_id = sys.argv[1]
            print(f"\n📋 Usando sessão do argumento: {session_id}")
        else:
            # Solicitar interativamente
            session_id = solicitar_session_id()
        
        print(f"\n🚀 Iniciando geração de relatório HTML...")
        print(f"📂 Sessão: {session_id}")
        
        # Verificar se a pasta existe
        session_path = Path(f"analyses_data/{session_id}")
        if not session_path.exists():
            print(f"\n❌ Erro: Pasta da sessão não encontrada: {session_path}")
            sys.exit(1)
        
        # Verificar pasta modules
        modules_path = session_path / "modules"
        if modules_path.exists():
            print(f"✅ Pasta modules encontrada: {modules_path}")
            md_files_modules = list(modules_path.glob("*.md"))
            print(f"   📄 {len(md_files_modules)} arquivos .md na pasta modules")
        else:
            print(f"⚠️  Pasta modules não encontrada em: {modules_path}")
        
        # Verificar arquivos .md na raiz
        md_files_root = list(session_path.glob("*.md"))
        print(f"📄 {len(md_files_root)} arquivos .md na raiz da sessão")
        
        # Instanciar o gerador
        gerador_html = EnhancedHTMLReportGenerator()
        
        # Carregar os módulos da sessão (incluindo CPLs em .md)
        print("\n📚 Carregando módulos e CPLs...")
        loaded_modules = load_modules_for_session(session_id)
        
        # Preparar dados completos para o relatório
        report_data = {
            'titulo': f'Relatório de Análise Completa - {session_id}',
            'modules': loaded_modules,
            'sumario_executivo': f'''
# Sumário Executivo

Este relatório apresenta uma análise completa e detalhada para a sessão **{session_id}**.

## Visão Geral

O documento contém análises aprofundadas em múltiplas áreas estratégicas, incluindo:

- **Análise de Mercado**: Insights detalhados sobre o mercado-alvo
- **Estratégias de Marketing**: CPLs e abordagens persuasivas
- **Análise Competitiva**: Posicionamento frente aos concorrentes
- **Planejamento**: Cronogramas e planos de ação detalhados

## Metodologia

A análise foi conduzida utilizando o sistema ARQV30 Enhanced v3.0, que combina:
- Processamento avançado de dados
- Análise de tendências de mercado
- Criação de protocolos de CPL devastadores
- Geração de insights acionáveis

## Estrutura do Relatório

Este relatório está organizado em seções modulares, cada uma focando em um aspecto específico da análise. Use o índice lateral para navegar facilmente entre as seções.

## Próximos Passos

Revise cuidadosamente cada seção deste relatório e implemente as estratégias recomendadas de forma sistemática.
            '''
        }
        
        # Definir caminho de saída
        output_path = f"analyses_data/{session_id}/relatorio_final_completo.html"
        
        print(f"\n🎨 Gerando HTML moderno...")
        
        # Gerar o relatório
        caminho_gerado = gerador_html.generate_html_report(
            session_id=session_id,
            report_data=report_data,
            output_path=output_path
        )
        
        print("\n" + "="*60)
        print("✅ RELATÓRIO GERADO COM SUCESSO!")
        print("="*60)
        print(f"\n📄 Arquivo: {caminho_gerado}")
        print(f"📊 Módulos incluídos: {len(loaded_modules)}")
        print(f"📸 Imagens incluídas: {len(gerador_html.images_base64)}")
        
        # Estatísticas detalhadas
        modules_with_content = sum(1 for m in loaded_modules.values() if "não encontrado" not in m['content'].lower() and "não disponível" not in m['content'].lower())
        print(f"✓ Módulos com conteúdo: {modules_with_content}")
        print(f"⚠ Módulos sem conteúdo: {len(loaded_modules) - modules_with_content}")
        
        print("\n💡 Dica: Abra o arquivo HTML em seu navegador para visualizar!")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        sys.exit(0)
    except FileNotFoundError as fnf_error:
        print(f"\n❌ Erro: Diretório ou arquivo não encontrado: {fnf_error}")
        print(f"💡 Verifique se o diretório 'analyses_data/{session_id}' existe.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro ao gerar o relatório HTML: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
