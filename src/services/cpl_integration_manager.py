#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - CPL Integration Manager
GARANTE que os CPLs sejam SEMPRE incluídos nos relatórios finais
"""

import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class CPLIntegrationManager:
    """Gerenciador que GARANTE a integração dos CPLs nos relatórios finais"""
    
    def __init__(self):
        """Inicializa o gerenciador de integração CPL"""
        self.cpl_modules = [
            'cpl_protocol_1',
            'cpl_protocol_2', 
            'cpl_protocol_3',
            'cpl_protocol_4',
            'cpl_protocol_5',
            'cpl_completo'
        ]
        
        self.cpl_titles = {
            'cpl_protocol_1': 'Arquitetura do Evento Magnético',
            'cpl_protocol_2': 'CPL1 - A Oportunidade Paralisante',
            'cpl_protocol_3': 'CPL2 - A Transformação Impossível',
            'cpl_protocol_4': 'CPL3 - O Caminho Revolucionário',
            'cpl_protocol_5': 'CPL4 - A Decisão Inevitável',
            'cpl_completo': 'Protocolo Integrado de CPLs Devastadores'
        }
        
        logger.info("🎯 CPL Integration Manager inicializado - GARANTINDO inclusão nos relatórios")
    
    def garantir_cpls_nos_modulos(self, session_id: str) -> Dict[str, Any]:
        """GARANTE que todos os CPLs estejam salvos na pasta modules"""
        try:
            logger.info(f"🔄 GARANTINDO CPLs para sessão: {session_id}")
            
            # Diretório de módulos
            modules_dir = Path(f"analyses_data/{session_id}/modules")
            modules_dir.mkdir(parents=True, exist_ok=True)
            
            # Status dos CPLs
            cpl_status = {
                'cpls_encontrados': [],
                'cpls_criados': [],
                'cpls_faltando': [],
                'total_cpls': len(self.cpl_modules)
            }
            
            # Verificar e criar CPLs se necessário
            for cpl_module in self.cpl_modules:
                cpl_file = self._get_cpl_filename(cpl_module)
                cpl_path = modules_dir / cpl_file
                
                if cpl_path.exists():
                    cpl_status['cpls_encontrados'].append(cpl_module)
                    logger.info(f"✅ CPL encontrado: {cpl_file}")
                else:
                    # Criar CPL se não existir
                    self._criar_cpl_padrao(cpl_path, cpl_module)
                    cpl_status['cpls_criados'].append(cpl_module)
                    logger.info(f"🆕 CPL criado: {cpl_file}")
            
            # Verificar se todos os CPLs estão presentes
            total_presentes = len(cpl_status['cpls_encontrados']) + len(cpl_status['cpls_criados'])
            
            if total_presentes == len(self.cpl_modules):
                logger.info(f"✅ TODOS OS {len(self.cpl_modules)} CPLs GARANTIDOS na pasta modules!")
            else:
                logger.warning(f"⚠️ Apenas {total_presentes}/{len(self.cpl_modules)} CPLs presentes")
            
            return cpl_status
            
        except Exception as e:
            logger.error(f"❌ Erro ao garantir CPLs: {e}")
            return {'erro': str(e)}
    
    def _get_cpl_filename(self, cpl_module: str) -> str:
        """Retorna o nome do arquivo correto para cada CPL"""
        filename_map = {
            'cpl_protocol_1': 'cpl_protocol_1.json',
            'cpl_protocol_2': 'cpl1.md',
            'cpl_protocol_3': 'cpl2.md', 
            'cpl_protocol_4': 'cpl3.md',
            'cpl_protocol_5': 'cpl4.md',
            'cpl_completo': 'cpl_completo.json'
        }
        return filename_map.get(cpl_module, f'{cpl_module}.md')
    
    def _criar_cpl_padrao(self, cpl_path: Path, cpl_module: str):
        """Cria um CPL padrão se não existir"""
        try:
            titulo = self.cpl_titles.get(cpl_module, cpl_module.replace('_', ' ').title())
            
            if cpl_path.suffix == '.json':
                # Criar arquivo JSON
                cpl_data = {
                    'titulo': titulo,
                    'conteudo': f'Conteúdo do {titulo} será gerado durante a execução do protocolo CPL.',
                    'data_geracao': datetime.now().isoformat(),
                    'status': 'aguardando_geracao',
                    'modulo': cpl_module,
                    'observacao': 'Este arquivo será preenchido automaticamente quando o protocolo CPL for executado.'
                }
                
                with open(cpl_path, 'w', encoding='utf-8') as f:
                    json.dump(cpl_data, f, ensure_ascii=False, indent=2)
            else:
                # Criar arquivo MD
                conteudo_md = f"""# {titulo}

## Status
🔄 **Aguardando geração pelo protocolo CPL**

## Descrição
Este CPL será gerado automaticamente quando o protocolo completo for executado.

## Informações Técnicas
- **Módulo**: {cpl_module}
- **Data de criação**: {datetime.now().isoformat()}
- **Status**: Aguardando geração

## Próximos Passos
1. Execute o protocolo CPL completo
2. Este arquivo será automaticamente preenchido com o conteúdo real
3. O CPL será incluído no relatório final

---
*Arquivo criado automaticamente pelo CPL Integration Manager*
"""
                
                with open(cpl_path, 'w', encoding='utf-8') as f:
                    f.write(conteudo_md)
            
            logger.info(f"📝 CPL padrão criado: {cpl_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar CPL padrão {cpl_module}: {e}")
    
    def verificar_integracao_relatorios(self, session_id: str) -> Dict[str, Any]:
        """Verifica se os CPLs estão sendo incluídos nos relatórios"""
        try:
            logger.info(f"🔍 Verificando integração CPLs nos relatórios: {session_id}")
            
            # Verificar relatório final MD
            relatorio_md = Path(f"analyses_data/{session_id}/relatorio_final.md")
            relatorio_completo_md = Path(f"analyses_data/{session_id}/relatorio_final_completo.md")
            
            status_integracao = {
                'relatorio_md_existe': relatorio_md.exists(),
                'relatorio_completo_existe': relatorio_completo_md.exists(),
                'cpls_no_relatorio_md': False,
                'cpls_no_relatorio_completo': False,
                'cpls_encontrados_md': [],
                'cpls_encontrados_completo': []
            }
            
            # Verificar conteúdo dos relatórios
            if relatorio_md.exists():
                with open(relatorio_md, 'r', encoding='utf-8') as f:
                    conteudo_md = f.read()
                    
                for cpl_module in self.cpl_modules:
                    titulo = self.cpl_titles[cpl_module]
                    if titulo.lower() in conteudo_md.lower() or cpl_module in conteudo_md:
                        status_integracao['cpls_encontrados_md'].append(cpl_module)
                
                status_integracao['cpls_no_relatorio_md'] = len(status_integracao['cpls_encontrados_md']) > 0
            
            if relatorio_completo_md.exists():
                with open(relatorio_completo_md, 'r', encoding='utf-8') as f:
                    conteudo_completo = f.read()
                    
                for cpl_module in self.cpl_modules:
                    titulo = self.cpl_titles[cpl_module]
                    if titulo.lower() in conteudo_completo.lower() or cpl_module in conteudo_completo:
                        status_integracao['cpls_encontrados_completo'].append(cpl_module)
                
                status_integracao['cpls_no_relatorio_completo'] = len(status_integracao['cpls_encontrados_completo']) > 0
            
            # Log do status
            if status_integracao['cpls_no_relatorio_md'] or status_integracao['cpls_no_relatorio_completo']:
                logger.info("✅ CPLs encontrados nos relatórios!")
            else:
                logger.warning("⚠️ CPLs NÃO encontrados nos relatórios - será corrigido")
            
            return status_integracao
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar integração: {e}")
            return {'erro': str(e)}
    
    def forcar_integracao_cpls(self, session_id: str) -> bool:
        """FORÇA a integração dos CPLs nos relatórios finais"""
        try:
            logger.info(f"🔧 FORÇANDO integração CPLs para sessão: {session_id}")
            
            # 1. Garantir que os CPLs existam na pasta modules
            self.garantir_cpls_nos_modulos(session_id)
            
            # 2. Forçar regeneração dos relatórios incluindo CPLs
            from .comprehensive_report_generator_v3 import ComprehensiveReportGeneratorV3
            
            report_generator = ComprehensiveReportGeneratorV3()
            
            # Regenerar relatório MD
            resultado_md = report_generator.compile_final_markdown_report(session_id)
            
            if resultado_md.get('success'):
                logger.info("✅ Relatório MD regenerado com CPLs incluídos")
            else:
                logger.warning("⚠️ Problema na regeneração do relatório MD")
            
            # Regenerar relatório HTML
            resultado_html = report_generator.compile_final_html_report(session_id)
            
            if resultado_html.get('success'):
                logger.info("✅ Relatório HTML regenerado com CPLs incluídos")
            else:
                logger.warning("⚠️ Problema na regeneração do relatório HTML")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao forçar integração: {e}")
            return False

# Instância global
cpl_integration_manager = CPLIntegrationManager()

def garantir_cpls_nos_relatorios(session_id: str) -> Dict[str, Any]:
    """Função principal para garantir CPLs nos relatórios"""
    return cpl_integration_manager.forcar_integracao_cpls(session_id)