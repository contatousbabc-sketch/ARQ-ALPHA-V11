#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - External AI Verifier Integration
Integra o External AI Verifier no fluxo principal de relatórios
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

# Adicionar o caminho do External AI Verifier ao sys.path
external_verifier_path = Path(__file__).parent.parent.parent / "external_ai_verifier" / "src"
if str(external_verifier_path) not in sys.path:
    sys.path.insert(0, str(external_verifier_path))

logger = logging.getLogger(__name__)

class ExternalAIVerifierIntegration:
    """Integração do External AI Verifier com o sistema principal"""
    
    def __init__(self):
        """Inicializa a integração do External AI Verifier"""
        self.verifier_available = False
        self.external_agent = None
        
        try:
            # Tentar importar o External Review Agent
            from external_review_agent import ExternalReviewAgent
            
            # Inicializar o agente
            config_path = external_verifier_path / "config" / "external_config.yaml"
            self.external_agent = ExternalReviewAgent(str(config_path) if config_path.exists() else None)
            self.verifier_available = True
            
            logger.info("✅ External AI Verifier integrado com sucesso")
            
        except Exception as e:
            logger.warning(f"⚠️ External AI Verifier não disponível: {e}")
            self.verifier_available = False
    
    def verificar_relatorio_com_ai_externa(self, session_id: str, relatorio_content: str) -> Dict[str, Any]:
        """Verifica o relatório usando o External AI Verifier"""
        try:
            if not self.verifier_available:
                logger.warning("⚠️ External AI Verifier não disponível - pulando verificação")
                return {
                    'status': 'skipped',
                    'motivo': 'External AI Verifier não disponível',
                    'timestamp': datetime.now().isoformat()
                }
            
            logger.info(f"🔍 Iniciando verificação externa para sessão: {session_id}")
            
            # Preparar dados para revisão (método correto: process_item)
            review_data = {
                'session_id': session_id,
                'content': relatorio_content,
                'timestamp': datetime.now().isoformat(),
                'source': 'relatorio_final',
                'content_type': 'report'
            }
            
            # Executar revisão externa (método correto do ExternalReviewAgent)
            resultado_verificacao = self.external_agent.process_item(review_data)
            
            # Salvar resultado da verificação
            self._salvar_resultado_verificacao(session_id, resultado_verificacao)
            
            logger.info("✅ Verificação externa concluída")
            return resultado_verificacao
            
        except Exception as e:
            logger.error(f"❌ Erro na verificação externa: {e}")
            return {
                'status': 'error',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def verificar_cpls_com_ai_externa(self, session_id: str) -> Dict[str, Any]:
        """Verifica especificamente os CPLs usando o External AI Verifier"""
        try:
            if not self.verifier_available:
                return {
                    'status': 'skipped',
                    'motivo': 'External AI Verifier não disponível'
                }
            
            logger.info(f"🎯 Verificando CPLs com AI externa para sessão: {session_id}")
            
            # Carregar CPLs da pasta modules
            modules_dir = Path(f"analyses_data/{session_id}/modules")
            cpls_encontrados = {}
            
            # Buscar arquivos CPL
            cpl_files = list(modules_dir.glob("cpl*.json")) + list(modules_dir.glob("cpl*.md"))
            
            for cpl_file in cpl_files:
                try:
                    if cpl_file.suffix == '.json':
                        with open(cpl_file, 'r', encoding='utf-8') as f:
                            cpl_content = json.load(f)
                    else:
                        with open(cpl_file, 'r', encoding='utf-8') as f:
                            cpl_content = f.read()
                    
                    cpls_encontrados[cpl_file.stem] = cpl_content
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao carregar CPL {cpl_file}: {e}")
            
            if not cpls_encontrados:
                logger.warning("⚠️ Nenhum CPL encontrado para verificação")
                return {
                    'status': 'no_cpls',
                    'mensagem': 'Nenhum CPL encontrado para verificação'
                }
            
            # Analisar cada CPL
            resultados_cpls = {}
            
            for cpl_name, cpl_content in cpls_encontrados.items():
                try:
                    review_data = {
                        'session_id': session_id,
                        'content': str(cpl_content),
                        'timestamp': datetime.now().isoformat(),
                        'source': f'cpl_{cpl_name}',
                        'content_type': 'cpl',
                        'cpl_name': cpl_name
                    }
                    
                    # Usar método correto: process_item
                    resultado_cpl = self.external_agent.process_item(review_data)
                    resultados_cpls[cpl_name] = resultado_cpl
                    
                    logger.info(f"✅ CPL {cpl_name} verificado")
                    
                except Exception as e:
                    logger.error(f"❌ Erro ao verificar CPL {cpl_name}: {e}")
                    resultados_cpls[cpl_name] = {
                        'status': 'error',
                        'erro': str(e)
                    }
            
            # Compilar resultado final
            resultado_final = {
                'status': 'completed',
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'total_cpls_analisados': len(resultados_cpls),
                'cpls_com_sucesso': len([r for r in resultados_cpls.values() if r.get('status') != 'error']),
                'resultados_individuais': resultados_cpls,
                'resumo_geral': self._gerar_resumo_verificacao_cpls(resultados_cpls)
            }
            
            # Salvar resultado
            self._salvar_resultado_verificacao_cpls(session_id, resultado_final)
            
            logger.info(f"✅ Verificação de CPLs concluída: {len(resultados_cpls)} CPLs analisados")
            return resultado_final
            
        except Exception as e:
            logger.error(f"❌ Erro na verificação de CPLs: {e}")
            return {
                'status': 'error',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _gerar_resumo_verificacao_cpls(self, resultados_cpls: Dict[str, Any]) -> Dict[str, Any]:
        """Gera resumo da verificação dos CPLs"""
        try:
            total_cpls = len(resultados_cpls)
            cpls_aprovados = 0
            cpls_com_alertas = 0
            cpls_com_erros = 0
            
            principais_alertas = []
            principais_recomendacoes = []
            
            for cpl_name, resultado in resultados_cpls.items():
                if resultado.get('status') == 'error':
                    cpls_com_erros += 1
                elif resultado.get('confidence_score', 0) >= 0.8:
                    cpls_aprovados += 1
                else:
                    cpls_com_alertas += 1
                
                # Coletar alertas e recomendações
                if 'alerts' in resultado:
                    principais_alertas.extend(resultado['alerts'][:2])  # Top 2 alertas por CPL
                
                if 'recommendations' in resultado:
                    principais_recomendacoes.extend(resultado['recommendations'][:2])  # Top 2 recomendações por CPL
            
            return {
                'estatisticas': {
                    'total_cpls': total_cpls,
                    'cpls_aprovados': cpls_aprovados,
                    'cpls_com_alertas': cpls_com_alertas,
                    'cpls_com_erros': cpls_com_erros,
                    'taxa_aprovacao': round((cpls_aprovados / total_cpls) * 100, 2) if total_cpls > 0 else 0
                },
                'principais_alertas': principais_alertas[:5],  # Top 5 alertas gerais
                'principais_recomendacoes': principais_recomendacoes[:5],  # Top 5 recomendações gerais
                'status_geral': 'aprovado' if cpls_aprovados >= (total_cpls * 0.8) else 'requer_atencao'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar resumo: {e}")
            return {'erro': str(e)}
    
    def _salvar_resultado_verificacao(self, session_id: str, resultado: Dict[str, Any]):
        """Salva resultado da verificação externa"""
        try:
            session_dir = Path(f"analyses_data/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Salvar resultado completo
            resultado_path = session_dir / "external_ai_verification.json"
            with open(resultado_path, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=2)
            
            # Salvar resumo em MD
            resumo_path = session_dir / "external_ai_verification_summary.md"
            with open(resumo_path, 'w', encoding='utf-8') as f:
                f.write(self._gerar_resumo_md_verificacao(resultado))
            
            logger.info(f"✅ Resultado da verificação externa salvo: {resultado_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resultado da verificação: {e}")
    
    def _salvar_resultado_verificacao_cpls(self, session_id: str, resultado: Dict[str, Any]):
        """Salva resultado da verificação específica dos CPLs"""
        try:
            session_dir = Path(f"analyses_data/{session_id}")
            modules_dir = session_dir / "modules"
            modules_dir.mkdir(parents=True, exist_ok=True)
            
            # Salvar como módulo para inclusão no relatório final
            cpl_verification_path = modules_dir / "external_ai_cpl_verification.json"
            with open(cpl_verification_path, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=2)
            
            # Salvar também como MD
            cpl_verification_md_path = modules_dir / "external_ai_cpl_verification.md"
            with open(cpl_verification_md_path, 'w', encoding='utf-8') as f:
                f.write(self._gerar_resumo_md_verificacao_cpls(resultado))
            
            logger.info(f"✅ Verificação de CPLs salva como módulo: {cpl_verification_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar verificação de CPLs: {e}")
    
    def _gerar_resumo_md_verificacao(self, resultado: Dict[str, Any]) -> str:
        """Gera resumo em MD da verificação externa"""
        return f"""# Verificação Externa com AI

## Status da Verificação
- **Status**: {resultado.get('status', 'N/A')}
- **Data**: {resultado.get('timestamp', 'N/A')}
- **Confiança**: {resultado.get('confidence_score', 'N/A')}

## Resultados da Análise
{json.dumps(resultado, ensure_ascii=False, indent=2)}

---
*Verificação realizada pelo External AI Verifier*
"""
    
    def _gerar_resumo_md_verificacao_cpls(self, resultado: Dict[str, Any]) -> str:
        """Gera resumo em MD da verificação dos CPLs"""
        resumo = resultado.get('resumo_geral', {})
        stats = resumo.get('estatisticas', {})
        
        return f"""# Verificação Externa dos CPLs

## Estatísticas Gerais
- **Total de CPLs Analisados**: {stats.get('total_cpls', 0)}
- **CPLs Aprovados**: {stats.get('cpls_aprovados', 0)}
- **CPLs com Alertas**: {stats.get('cpls_com_alertas', 0)}
- **CPLs com Erros**: {stats.get('cpls_com_erros', 0)}
- **Taxa de Aprovação**: {stats.get('taxa_aprovacao', 0)}%

## Status Geral
**{resumo.get('status_geral', 'N/A').upper()}**

## Principais Alertas
{chr(10).join([f"- {alerta}" for alerta in resumo.get('principais_alertas', [])])}

## Principais Recomendações
{chr(10).join([f"- {rec}" for rec in resumo.get('principais_recomendacoes', [])])}

## Detalhes por CPL
{self._gerar_detalhes_cpls_md(resultado.get('resultados_individuais', {}))}

---
*Verificação realizada pelo External AI Verifier em {resultado.get('timestamp', 'N/A')}*
"""
    
    def _gerar_detalhes_cpls_md(self, resultados_individuais: Dict[str, Any]) -> str:
        """Gera detalhes dos CPLs em formato MD"""
        detalhes = []
        
        for cpl_name, resultado in resultados_individuais.items():
            status = resultado.get('status', 'N/A')
            confidence = resultado.get('confidence_score', 'N/A')
            
            detalhes.append(f"""
### {cpl_name.upper()}
- **Status**: {status}
- **Confiança**: {confidence}
- **Alertas**: {len(resultado.get('alerts', []))}
- **Recomendações**: {len(resultado.get('recommendations', []))}
""")
        
        return "\n".join(detalhes)

# Instância global
external_ai_verifier_integration = ExternalAIVerifierIntegration()

def verificar_relatorio_com_ai_externa(session_id: str, relatorio_content: str) -> Dict[str, Any]:
    """Função principal para verificação externa do relatório"""
    return external_ai_verifier_integration.verificar_relatorio_com_ai_externa(session_id, relatorio_content)

def verificar_cpls_com_ai_externa(session_id: str) -> Dict[str, Any]:
    """Função principal para verificação externa dos CPLs"""
    return external_ai_verifier_integration.verificar_cpls_com_ai_externa(session_id)
