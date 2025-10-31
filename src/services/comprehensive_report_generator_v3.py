#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Comprehensive Report Generator V3
Compilador de relatório final a partir dos módulos gerados
"""

import os
import logging
import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
from .enhanced_html_report_generator import EnhancedHTMLReportGenerator

logger = logging.getLogger(__name__)

class ComprehensiveReportGeneratorV3:
    """Compilador de relatório final ultra robusto"""

    def __init__(self):
        """Inicializa o compilador"""
        # Inicializar gerador HTML moderno
        self.html_generator = EnhancedHTMLReportGenerator()
        
        # Ordem atualizada dos módulos, incluindo os novos módulos de CPL
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
            # Novos módulos de CPL adicionados conforme instruções do CPL.txt
            'cpl_protocol_1',
            'cpl_protocol_2',
            'cpl_protocol_3',
            'cpl_protocol_4',
            'cpl_protocol_5',
            # Módulos adicionais para completar os 26 módulos
            'cpl_completo',
            'analise_sentimento',
            'mapeamento_tendencias',
            'oportunidades_mercado',
            'riscos_ameacas',
            'conteudo_viral',
            # Módulo de verificação externa
            'external_ai_cpl_verification'
        ]

        # Títulos atualizados, incluindo os novos módulos de CPL
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
            # Novos títulos de módulos de CPL adicionados conforme instruções do CPL.txt
            'cpl_protocol_1': 'Arquitetura do Evento Magnético',
            'cpl_protocol_2': 'CPL1 - A Oportunidade Paralisante',
            'cpl_protocol_3': 'CPL2 - A Transformação Impossível',
            'cpl_protocol_4': 'CPL3 - O Caminho Revolucionário',
            'cpl_protocol_5': 'CPL4 - A Decisão Inevitável',
            # Títulos dos módulos adicionais para completar os 26 módulos
            'cpl_completo': 'Protocolo Integrado de CPLs Devastadores',
            'analise_sentimento': 'Análise de Sentimento Detalhada',
            'mapeamento_tendencias': 'Mapeamento de Tendências e Previsões',
            'oportunidades_mercado': 'Identificação de Oportunidades de Mercado',
            'riscos_ameacas': 'Avaliação de Riscos e Ameaças',
            'conteudo_viral': 'Análise de Conteúdo Viral e Fatores de Sucesso',
            'external_ai_cpl_verification': 'Verificação Externa dos CPLs com IA'
        }

        logger.info("📋 Comprehensive Report Generator ULTRA ROBUSTO inicializado")

    def compile_final_markdown_report(self, session_id: str) -> Dict[str, Any]:
        """
        Compila relatório final a partir dos módulos gerados

        Args:
            session_id: ID da sessão

        Returns:
            Dict com informações do relatório compilado
        """
        logger.info(f"📋 Compilando relatório final para sessão: {session_id}")

        try:
            # GARANTIR que os CPLs estejam presentes antes de compilar
            from .cpl_integration_manager import cpl_integration_manager
            cpl_status = cpl_integration_manager.garantir_cpls_nos_modulos(session_id)
            logger.info(f"🎯 Status CPLs: {len(cpl_status.get('cpls_encontrados', []))} encontrados, {len(cpl_status.get('cpls_criados', []))} criados")

            # 1. Verifica estrutura de diretórios
            session_dir = Path(f"analyses_data/{session_id}")
            modules_dir = session_dir / "modules"
            files_dir = Path(f"analyses_data/files/{session_id}")

            if not session_dir.exists():
                raise Exception(f"Diretório da sessão não encontrado: {session_dir}")

            # 2. Carrega módulos disponíveis
            available_modules = self._load_available_modules(modules_dir, session_id)

            # 3. Carrega screenshots disponíveis
            screenshot_paths = self._load_screenshot_paths(files_dir)

            # 4. Compila relatório
            final_report = self._compile_report_content(
                session_id, 
                available_modules, 
                screenshot_paths
            )

            # 5. Salva relatório final
            report_path = self._save_final_report(session_id, final_report)

            # 5.1. VERIFICAÇÃO EXTERNA COM AI VERIFIER
            try:
                from .external_ai_verifier_integration import verificar_relatorio_com_ai_externa, verificar_cpls_com_ai_externa
                
                logger.info("🔍 Iniciando verificação externa com AI Verifier")
                
                # Verificar relatório completo
                resultado_verificacao = verificar_relatorio_com_ai_externa(session_id, final_report)
                logger.info(f"✅ Verificação do relatório: {resultado_verificacao.get('status', 'N/A')}")
                
                # Verificar CPLs especificamente
                resultado_cpls = verificar_cpls_com_ai_externa(session_id)
                logger.info(f"✅ Verificação dos CPLs: {resultado_cpls.get('status', 'N/A')}")
                
            except Exception as e:
                logger.warning(f"⚠️ Erro na verificação externa: {e}")

            # 6. Gera estatísticas
            statistics = self._generate_report_statistics(
                available_modules, 
                screenshot_paths, 
                final_report
            )

            logger.info(f"✅ Relatório final compilado: {report_path}")

            return {
                "success": True,
                "session_id": session_id,
                "report_path": report_path,
                "modules_compiled": len(available_modules),
                "screenshots_included": len(screenshot_paths),
                "estatisticas_relatorio": statistics,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Erro na compilação: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }

    def get_final_report_content(self, session_id: str) -> str:
        """
        Retorna apenas o conteúdo do relatório final como string
        
        Args:
            session_id: ID da sessão
            
        Returns:
            String com o conteúdo do relatório final
        """
        try:
            # 1. Verifica estrutura de diretórios
            session_dir = Path(f"analyses_data/{session_id}")
            modules_dir = session_dir / "modules"
            files_dir = Path(f"analyses_data/files/{session_id}")

            if not session_dir.exists():
                return f"# ERRO\n\nDiretório da sessão não encontrado: {session_dir}"

            # 2. Carrega módulos disponíveis
            available_modules = self._load_available_modules(modules_dir, session_id)

            # 3. Carrega screenshots disponíveis
            screenshot_paths = self._load_screenshot_paths(files_dir)

            # 4. Compila e retorna apenas o conteúdo
            return self._compile_report_content(
                session_id, 
                available_modules, 
                screenshot_paths
            )

        except Exception as e:
            logger.error(f"❌ Erro ao obter conteúdo do relatório: {e}")
            return f"# ERRO\n\nErro ao gerar relatório: {str(e)}"

    def _load_available_modules(self, modules_dir: Path, session_id: str) -> Dict[str, str]:
        """Carrega módulos disponíveis"""
        available_modules = {}

        try:
            if not modules_dir.exists():
                logger.warning(f"⚠️ Diretório de módulos não existe: {modules_dir}")
                return available_modules

            for module_name in self.modules_order:
                # Primeiro tenta carregar arquivo .md
                module_file = modules_dir / f"{module_name}.md"
                if module_file.exists():
                    with open(module_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            available_modules[module_name] = content
                            logger.debug(f"✅ Módulo carregado: {module_name}")
                        else:
                            logger.warning(f"⚠️ Módulo vazio: {module_name}")
                else:
                    # Se não encontrar .md, tenta carregar arquivo .json (para módulos CPL)
                    module_file_json = modules_dir / f"{module_name}.json"
                    if module_file_json.exists():
                        try:
                            with open(module_file_json, 'r', encoding='utf-8') as f:
                                json_content = json.load(f)
                                # Converte o conteúdo JSON em uma representação em texto
                                content = json.dumps(json_content, indent=2, ensure_ascii=False)
                                available_modules[module_name] = content
                                logger.debug(f"✅ Módulo JSON carregado: {module_name}")
                        except Exception as e:
                            logger.warning(f"⚠️ Erro ao carregar módulo JSON {module_name}: {e}")
                    else:
                        # Para módulos CPL, tenta carregar do diretório de CPLs
                        if module_name.startswith('cpl_'):
                            cpl_content = self._load_cpl_module(session_id, module_name)
                            if cpl_content:
                                available_modules[module_name] = cpl_content
                                logger.debug(f"✅ Módulo CPL carregado: {module_name}")
                            else:
                                logger.warning(f"⚠️ Módulo CPL não encontrado: {module_name}")
                        else:
                            logger.warning(f"⚠️ Módulo não encontrado: {module_name}")

            logger.info(f"📊 {len(available_modules)}/{len(self.modules_order)} módulos carregados")
            return available_modules

        except Exception as e:
            logger.error(f"❌ Erro ao carregar módulos: {e}")
            return available_modules
    
    def _load_cpl_module(self, session_id: str, module_name: str) -> str:
        """Carrega módulo CPL do diretório específico de CPLs"""
        try:
            # Tentar carregar do diretório analyses_data/{session_id}/modules/
            cpl_dir = Path(f"analyses_data/{session_id}/modules")
            
            # Mapear nomes de módulos para arquivos reais gerados
            module_file_map = {
                'cpl_protocol_1': 'cpl_protocol_1.json',
                'cpl_protocol_2': 'cpl1.md',
                'cpl_protocol_3': 'cpl2.md',
                'cpl_protocol_4': 'cpl3.md',
                'cpl_protocol_5': 'cpl4.md',
                'cpl_completo': 'cpl_completo.json'
            }
            
            filename = module_file_map.get(module_name)
            if not filename:
                # Fallback: tentar carregar qualquer arquivo CPL disponível
                cpl_files = list(cpl_dir.glob("cpl_*.json")) + list(cpl_dir.glob("cpl_*.md"))
                if cpl_files:
                    file_path = cpl_files[0]  # Usar o primeiro arquivo encontrado
                    filename = file_path.name
                else:
                    return None
            else:
                file_path = cpl_dir / filename
            
            if file_path.exists():
                if filename.endswith('.json'):
                    # Carregar e formatar JSON
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_content = json.load(f)
                        return self._format_cpl_json_content(json_content)
                else:
                    # Carregar arquivo MD
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
            
            # Fallback: tentar carregar arquivo com nome do módulo
            fallback_md = cpl_dir / f"{module_name}.md"
            fallback_json = cpl_dir / f"{module_name}.json"
            
            if fallback_md.exists():
                with open(fallback_md, 'r', encoding='utf-8') as f:
                    return f.read()
            elif fallback_json.exists():
                with open(fallback_json, 'r', encoding='utf-8') as f:
                    json_content = json.load(f)
                    return self._format_cpl_json_content(json_content)
            
            # Último fallback: carregar qualquer arquivo CPL disponível
            cpl_files = list(cpl_dir.glob("cpl_*.json")) + list(cpl_dir.glob("cpl_*.md"))
            if cpl_files:
                file_path = cpl_files[0]
                if file_path.name.endswith('.json'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_content = json.load(f)
                        return self._format_cpl_json_content(json_content)
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar módulo CPL {module_name}: {e}")
            return None
    
    def _format_cpl_json_content(self, json_content: Dict[str, Any]) -> str:
        """Formata conteúdo JSON de CPL para exibição em markdown"""
        try:
            formatted = ""
            
            # Formato real dos CPLs gerados: {"titulo": "...", "conteudo": "...", "data_geracao": "...", "status": "..."}
            if 'titulo' in json_content and 'conteudo' in json_content:
                # Adicionar título
                formatted += f"## {json_content['titulo']}\n\n"
                
                # Adicionar conteúdo
                formatted += f"{json_content['conteudo']}\n\n"
                
                # Adicionar metadados se disponíveis
                if 'data_geracao' in json_content:
                    formatted += f"**Data de Geração:** {json_content['data_geracao']}\n\n"
                
                if 'status' in json_content:
                    formatted += f"**Status:** {json_content['status']}\n\n"
            
            # Fallback para estrutura de CPL completo (formato antigo)
            elif 'cpl_completo' in json_content:
                cpl_data = json_content['cpl_completo']
                
                if 'arquitetura_evento' in cpl_data:
                    formatted += "### Arquitetura do Evento\n\n"
                    arch = cpl_data['arquitetura_evento']
                    if 'conteudo' in arch:
                        formatted += f"{arch['conteudo']}\n\n"
                
                # Adicionar cada CPL
                for cpl_num in ['cpl1', 'cpl2', 'cpl3', 'cpl4']:
                    if cpl_num in cpl_data:
                        cpl_info = cpl_data[cpl_num]
                        if 'fase' in cpl_info:
                            formatted += f"### {cpl_info['fase']}\n\n"
                        if 'conteudo' in cpl_info:
                            formatted += f"{cpl_info['conteudo']}\n\n"
            
            # Se não conseguir extrair estrutura específica, usar formato genérico
            if not formatted:
                # Tentar extrair qualquer campo de título e conteúdo
                for key in ['titulo', 'title', 'nome', 'name']:
                    if key in json_content:
                        formatted += f"## {json_content[key]}\n\n"
                        break
                
                for key in ['conteudo', 'content', 'texto', 'text', 'descricao', 'description']:
                    if key in json_content:
                        formatted += f"{json_content[key]}\n\n"
                        break
                
                # Se ainda não tiver conteúdo, usar JSON formatado
                if not formatted:
                    formatted = f"```json\n{json.dumps(json_content, indent=2, ensure_ascii=False)}\n```\n\n"
            
            return formatted
            
        except Exception as e:
            logger.error(f"❌ Erro ao formatar conteúdo JSON: {e}")
            return f"```json\n{json.dumps(json_content, indent=2, ensure_ascii=False)}\n```\n\n"

    def _load_screenshot_paths(self, files_dir: Path) -> List[str]:
        """Carrega caminhos dos screenshots"""
        screenshot_paths = []

        try:
            if not files_dir.exists():
                logger.warning(f"⚠️ Diretório de arquivos não existe: {files_dir}")
                return screenshot_paths

            # Busca por arquivos PNG (screenshots)
            for screenshot_file in files_dir.glob("*.png"):
                relative_path = f"files/{files_dir.name}/{screenshot_file.name}"
                screenshot_paths.append(relative_path)
                logger.debug(f"📸 Screenshot encontrado: {screenshot_file.name}")

            logger.info(f"📸 {len(screenshot_paths)} screenshots encontrados")
            return screenshot_paths

        except Exception as e:
            logger.error(f"❌ Erro ao carregar screenshots: {e}")
            return screenshot_paths

    def _compile_report_content(
        self, 
        session_id: str, 
        modules: Dict[str, str], 
        screenshots: List[str]
    ) -> str:
        """Compila conteúdo do relatório final"""

        # Cabeçalho do relatório
        report = f"""# RELATÓRIO FINAL - ARQV30 Enhanced v3.0

**Sessão:** {session_id}  
**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Módulos Compilados:** {len(modules)}/{len(self.modules_order)}  
**Screenshots Incluídos:** {len(screenshots)}

---

## SUMÁRIO EXECUTIVO

Este relatório consolida a análise ultra-detalhada realizada pelo sistema ARQV30 Enhanced v3.0, contemplando {len(modules)} módulos especializados de análise estratégica.

### Módulos Incluídos:
"""

        # Lista de módulos
        for i, module_name in enumerate(self.modules_order, 1):
            title = self.module_titles.get(module_name, module_name.replace('_', ' ').title())
            status = "✅" if module_name in modules else "❌"
            report += f"{i}. {status} {title}\n"

        report += "\n---\n\n"

        # Adiciona screenshots se disponíveis
        if screenshots:
            report += "## EVIDÊNCIAS VISUAIS\n\n"
            for i, screenshot in enumerate(screenshots, 1):
                report += f"### Screenshot {i}\n"
                report += f"![Screenshot {i}]({screenshot})\n\n"
            report += "---\n\n"

        # Compila módulos na ordem definida
        for module_name in self.modules_order:
            if module_name in modules:
                title = self.module_titles.get(module_name, module_name.replace('_', ' ').title())
                report += f"## {title}\n\n"
                
                # Trata módulos CPL de forma especial (JSON)
                if module_name.startswith('cpl_protocol_'):
                    try:
                        # Tenta parsear o conteúdo como JSON
                        module_content = json.loads(modules[module_name])
                        report += self._format_cpl_module_content(module_content)
                    except json.JSONDecodeError:
                        # Se não for JSON válido, adiciona o conteúdo como está
                        report += modules[module_name]
                else:
                    # Módulos normais em Markdown
                    report += modules[module_name]
                
                report += "\n\n---\n\n"

        # Rodapé
        report += f"""
## INFORMAÇÕES TÉCNICAS

**Sistema:** ARQV30 Enhanced v3.0  
**Sessão:** {session_id}  
**Data de Compilação:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Módulos Processados:** {len(modules)}/{len(self.modules_order)}  
**Status:** {'Completo' if len(modules) == len(self.modules_order) else 'Parcial'}

### Estatísticas de Compilação:
- ✅ Sucessos: {len(modules)}
- ❌ Falhas: {len(self.modules_order) - len(modules)}
- 📊 Taxa de Sucesso: {(len(modules)/len(self.modules_order)*100):.1f}%

---

*Relatório compilado automaticamente pelo ARQV30 Enhanced v3.0*
"""

        return report

    def _format_cpl_module_content(self, cpl_content: Dict[str, Any]) -> str:
        """Formata o conteúdo de um módulo CPL para exibição no relatório"""
        try:
            formatted_content = ""
            
            # Adiciona título e descrição se disponíveis
            if 'titulo' in cpl_content:
                formatted_content += f"**{cpl_content['titulo']}**\n\n"
            
            if 'descricao' in cpl_content:
                formatted_content += f"{cpl_content['descricao']}\n\n"
            
            # Adiciona fases se disponíveis
            if 'fases' in cpl_content:
                for fase_key, fase_data in cpl_content['fases'].items():
                    if isinstance(fase_data, dict):
                        # Título da fase
                        if 'titulo' in fase_data:
                            formatted_content += f"### {fase_data['titulo']}\n\n"
                        
                        # Descrição da fase
                        if 'descricao' in fase_data:
                            formatted_content += f"{fase_data['descricao']}\n\n"
                        
                        # Outros campos da fase
                        for key, value in fase_data.items():
                            if key not in ['titulo', 'descricao']:
                                if isinstance(value, str):
                                    formatted_content += f"**{key.replace('_', ' ').title()}:** {value}\n\n"
                                elif isinstance(value, list):
                                    formatted_content += f"**{key.replace('_', ' ').title()}:**\n"
                                    for item in value:
                                        if isinstance(item, str):
                                            formatted_content += f"- {item}\n"
                                        elif isinstance(item, dict):
                                            formatted_content += f"- {json.dumps(item, ensure_ascii=False)}\n"
                                    formatted_content += "\n"
                                elif isinstance(value, dict):
                                    formatted_content += f"**{key.replace('_', ' ').title()}:**\n"
                                    for sub_key, sub_value in value.items():
                                        formatted_content += f"  - {sub_key}: {sub_value}\n"
                                    formatted_content += "\n"
                    
            # Adiciona considerações finais se disponíveis
            if 'consideracoes_finais' in cpl_content:
                formatted_content += "### Considerações Finais\n\n"
                for key, value in cpl_content['consideracoes_finais'].items():
                    if isinstance(value, str):
                        formatted_content += f"**{key.replace('_', ' ').title()}:** {value}\n\n"
                    elif isinstance(value, list):
                        formatted_content += f"**{key.replace('_', ' ').title()}:**\n"
                        for item in value:
                            formatted_content += f"- {item}\n"
                        formatted_content += "\n"
            
            return formatted_content
            
        except Exception as e:
            logger.error(f"❌ Erro ao formatar conteúdo CPL: {e}")
            return f"*Erro ao formatar conteúdo do módulo CPL: {str(e)}*\n\n{json.dumps(cpl_content, indent=2, ensure_ascii=False)}"

    def _save_final_report(self, session_id: str, report_content: str) -> str:
        """Salva relatório final em Markdown e HTML"""
        try:
            # Salva relatório compilado
            os.makedirs(f"analyses_data/{session_id}", exist_ok=True)
            final_report_path = f"analyses_data/{session_id}/relatorio_final.md"

            with open(final_report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)

            # 🆕 GERA AUTOMATICAMENTE O HTML MODERNO
            try:
                # Preparar dados para o gerador HTML moderno
                report_data = {
                    'titulo': f'Relatório de Análise - {session_id}',
                    'sumario_executivo': self._extract_summary_from_markdown(report_content),
                    'modules': self._extract_modules_from_markdown(report_content, session_id)
                }
                
                # Gerar HTML moderno
                html_report_path = self.html_generator.generate_html_report(
                    session_id, 
                    report_data, 
                    f"analyses_data/{session_id}/relatorio_final_moderno.html"
                )
                
                logger.info(f"✅ Relatório HTML moderno gerado: {html_report_path}")
                
                # Manter compatibilidade com HTML simples
                html_content = self._convert_markdown_to_html(report_content, session_id)
                html_simple_path = f"analyses_data/{session_id}/relatorio_final.html"
                
                with open(html_simple_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                logger.info(f"✅ Relatório HTML simples gerado: {html_simple_path}")
                
            except Exception as html_error:
                logger.error(f"⚠️ Erro ao gerar HTML moderno: {html_error}")
                # Fallback para HTML simples
                html_content = self._convert_markdown_to_html(report_content, session_id)
                html_report_path = f"analyses_data/{session_id}/relatorio_final.html"
                
                with open(html_report_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                logger.info(f"✅ Relatório HTML simples gerado (fallback): {html_report_path}")

            return str(final_report_path)

        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")
            raise

    def _convert_markdown_to_html(self, markdown_content: str, session_id: str) -> str:
        """Converte conteúdo Markdown para HTML profissional"""
        try:
            # Template HTML profissional
            html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Análise de Mercado - {session_id}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }}
        h3 {{
            color: #2c3e50;
            margin-top: 25px;
        }}
        .module-section {{
            background: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
        }}
        .stats-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .screenshot-gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .screenshot-item {{
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            text-align: right;
            margin-top: 30px;
            border-top: 1px solid #ecf0f1;
            padding-top: 15px;
        }}
        ul, ol {{
            padding-left: 25px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        blockquote {{
            border-left: 4px solid #f39c12;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            background: #fef9e7;
            padding: 15px 20px;
            border-radius: 0 8px 8px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        {self._process_markdown_to_html(markdown_content)}
        {self._generate_images_section(session_id)}
        <div class="timestamp">
            Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
            return html_template
            
        except Exception as e:
            logger.error(f"❌ Erro ao converter Markdown para HTML: {e}")
            return f"<html><body><h1>Erro na conversão</h1><p>{str(e)}</p></body></html>"

    def _process_markdown_to_html(self, markdown_content: str) -> str:
        """Processa conteúdo Markdown para HTML"""
        try:
            html_content = markdown_content
            
            # Conversões básicas de Markdown para HTML
            import re
            
            # Headers
            html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
            
            # Bold e Italic
            html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
            html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
            
            # Code blocks
            html_content = re.sub(r'```([\\s\\S]*?)```', r'<pre><code>\1</code></pre>', html_content)
            html_content = re.sub(r'`(.+?)`', r'<code>\1</code>', html_content)
            
            # Links
            html_content = re.sub(r'\\[(.+?)\\]\\((.+?)\\)', r'<a href="\2">\1</a>', html_content)
            
            # Listas
            lines = html_content.split('\\n')
            processed_lines = []
            in_list = False
            
            for line in lines:
                if re.match(r'^\\s*[-*+]\\s+', line):
                    if not in_list:
                        processed_lines.append('<ul>')
                        in_list = True
                    item_text = re.sub(r'^\\s*[-*+]\\s+', '', line)
                    processed_lines.append(f'<li>{item_text}</li>')
                else:
                    if in_list:
                        processed_lines.append('</ul>')
                        in_list = False
                    processed_lines.append(line)
            
            if in_list:
                processed_lines.append('</ul>')
            
            # Parágrafos
            html_content = '\\n'.join(processed_lines)
            paragraphs = html_content.split('\\n\\n')
            processed_paragraphs = []
            
            for para in paragraphs:
                para = para.strip()
                if para and not para.startswith('<'):
                    processed_paragraphs.append(f'<p>{para}</p>')
                else:
                    processed_paragraphs.append(para)
            
            return '\\n'.join(processed_paragraphs)
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar Markdown: {e}")
            return markdown_content

    def _generate_images_section(self, session_id: str) -> str:
        """Gera seção HTML com imagens 1080x1080 extraídas na primeira etapa"""
        try:
            # Busca por imagens na pasta da sessão
            session_path = Path(f"sessions/{session_id}")
            images_path = session_path / "images"
            
            # Procura por imagens 1080x1080
            image_files = []
            if images_path.exists():
                # Busca por arquivos de imagem comuns
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.gif']:
                    image_files.extend(images_path.glob(ext))
            
            # Se não encontrar na pasta images, busca na pasta da sessão
            if not image_files and session_path.exists():
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.gif']:
                    image_files.extend(session_path.glob(ext))
            
            # Filtra apenas imagens que podem ser 1080x1080 (baseado no nome ou tamanho)
            filtered_images = []
            for img_file in image_files:
                # Verifica se o nome sugere que é 1080x1080 ou se é uma imagem grande
                if ('1080' in img_file.name.lower() or 
                    'square' in img_file.name.lower() or 
                    'post' in img_file.name.lower() or
                    img_file.stat().st_size > 100000):  # Maior que 100KB
                    filtered_images.append(img_file)
            
            if not filtered_images:
                return ""  # Não adiciona seção se não há imagens
            
            # Gera HTML da seção de imagens
            images_html = """
        <div class="module-section">
            <h2>📸 Imagens Extraídas (1080x1080)</h2>
            <p>Imagens coletadas durante a primeira etapa de análise, otimizadas para redes sociais:</p>
            <div class="screenshot-gallery">
"""
            
            for i, img_file in enumerate(filtered_images[:12]):  # Máximo 12 imagens
                # Caminho relativo para a imagem
                img_relative_path = str(img_file.relative_to(Path.cwd()))
                
                images_html += f"""
                <div class="screenshot-item">
                    <img src="{img_relative_path}" alt="Imagem {i+1}" 
                         style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <p style="margin-top: 10px; font-size: 0.9em; color: #666;">
                        <strong>Imagem {i+1}</strong><br>
                        {img_file.name}<br>
                        <small>Tamanho: {self._format_file_size(img_file.stat().st_size)}</small>
                    </p>
                </div>
"""
            
            images_html += """
            </div>
            <p style="margin-top: 20px; font-size: 0.9em; color: #666; font-style: italic;">
                💡 <strong>Dica:</strong> Estas imagens foram automaticamente extraídas e podem ser utilizadas 
                para campanhas de marketing, posts em redes sociais ou materiais promocionais.
            </p>
        </div>
"""
            
            return images_html
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar seção de imagens: {e}")
            return ""
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Formata tamanho do arquivo em formato legível"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB".replace('\\n', '<br>')

    def _generate_report_statistics(
        self, 
        modules: Dict[str, str], 
        screenshots: List[str], 
        report_content: str
    ) -> Dict[str, Any]:
        """Gera estatísticas do relatório"""

        return {
            "total_modules": len(self.modules_order),
            "modules_compiled": len(modules),
            "modules_missing": len(self.modules_order) - len(modules),
            "success_rate": (len(modules) / len(self.modules_order)) * 100,
            "screenshots_included": len(screenshots),
            "total_characters": len(report_content),
            "estimated_pages": len(report_content) // 2000,  # ~2000 chars por página
            "compilation_timestamp": datetime.now().isoformat(),
            "paginas_estimadas": max(20, len(report_content) // 2000),  # Mínimo 20 páginas
            "secoes_geradas": len(modules),
            "taxa_completude": (len(modules) / len(self.modules_order)) * 100
        }

    def generate_final_report(self, session_id: str) -> Dict[str, Any]:
        """Método de compatibilidade"""
        return self.compile_final_markdown_report(session_id)

    def generate_detailed_report(
        self, 
        massive_data: Dict[str, Any], 
        modules_data: Dict[str, Any], 
        context: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """Gera relatório detalhado (método de compatibilidade)"""
        return self.compile_final_markdown_report(session_id)
    
    def _extract_summary_from_markdown(self, markdown_content: str) -> str:
        """Extrai sumário executivo do conteúdo markdown"""
        try:
            # Procurar por seção de sumário executivo
            lines = markdown_content.split('\n')
            summary_lines = []
            in_summary = False
            
            for line in lines:
                if 'sumário executivo' in line.lower() or 'resumo executivo' in line.lower():
                    in_summary = True
                    continue
                elif in_summary and line.startswith('#') and not line.startswith('###'):
                    break
                elif in_summary:
                    summary_lines.append(line)
            
            if summary_lines:
                return '\n'.join(summary_lines).strip()
            
            # Fallback: usar primeiros parágrafos
            paragraphs = markdown_content.split('\n\n')
            return '\n\n'.join(paragraphs[:3]) if paragraphs else "Sumário não disponível"
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair sumário: {e}")
            return "Sumário não disponível"
    
    def _extract_modules_from_markdown(self, markdown_content: str, session_id: str) -> Dict[str, Dict[str, str]]:
        """Extrai módulos do conteúdo markdown"""
        try:
            modules = {}
            
            # Carregar módulos disponíveis diretamente
            modules_dir = Path(f"analyses_data/{session_id}/modules")
            available_modules = self._load_available_modules(modules_dir, session_id)
            
            for module_name, module_content in available_modules.items():
                modules[module_name] = {
                    'title': self.module_titles.get(module_name, module_name.replace('_', ' ').title()),
                    'content': module_content
                }
            
            return modules
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair módulos: {e}")
            return {}

# Instância global
comprehensive_report_generator_v3 = ComprehensiveReportGeneratorV3()
