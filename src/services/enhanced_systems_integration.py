#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integração dos Sistemas Aprimorados - ARQV30 Enhanced v3.0
Sistema de integração dos novos módulos implementados
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from services.avatar_image_generator import AvatarImageGenerator
from services.competitor_content_collector import RealCompetitorAnalyzer
from services.sales_funnel_chart_generator import SalesFunnelChartGenerator

logger = logging.getLogger(__name__)

class EnhancedSystemsIntegration:
    """
    Classe principal para integração dos sistemas aprimorados
    """
    
    def __init__(self):
        self.avatar_generator = None
        self.competitor_analyzer = RealCompetitorAnalyzer()
        self.funnel_generator = None
        
    async def __aenter__(self):
        """Context manager entry"""
        self.avatar_generator = AvatarImageGenerator()
        await self.avatar_generator.__aenter__()
        
        self.funnel_generator = SalesFunnelChartGenerator()
        await self.funnel_generator.__aenter__()
        
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.avatar_generator:
            await self.avatar_generator.__aexit__(exc_type, exc_val, exc_tb)
        if self.funnel_generator:
            await self.funnel_generator.__aexit__(exc_type, exc_val, exc_tb)
    
    async def generate_complete_analysis_package(self, 
                                               persona_data: Dict[str, Any],
                                               segment: str,
                                               target_audience: str,
                                               product: str = None) -> Dict[str, Any]:
        """
        Gera pacote completo de análise com todos os sistemas integrados
        """
        logger.info("🚀 Gerando pacote completo de análise...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'persona_data': persona_data,
            'segment': segment,
            'target_audience': target_audience,
            'product': product,
            'avatar_image': None,
            'competitor_analysis': None,
            'funnel_chart': None,
            'success': True,
            'errors': []
        }
        
        # 1. Gerar imagem de avatar
        try:
            logger.info("🎨 Gerando imagem de avatar...")
            avatar_result = await self.avatar_generator.gerar_imagem_avatar(persona_data)
            
            if avatar_result.get('success'):
                results['avatar_image'] = {
                    'base64': avatar_result['image_base64'],
                    'data_url': avatar_result['image_data_url'],
                    'method': avatar_result['method'],
                    'size': '1080x1080'
                }
                logger.info("✅ Avatar gerado com sucesso")
            else:
                results['errors'].append(f"Falha na geração do avatar: {avatar_result.get('error')}")
                
        except Exception as e:
            logger.error(f"❌ Erro na geração do avatar: {e}")
            results['errors'].append(f"Erro no sistema de avatar: {str(e)}")
        
        # 2. Análise de concorrentes
        try:
            logger.info("🔍 Analisando concorrentes...")
            competitor_analysis = await self.competitor_analyzer.analyze_real_competitors(segment, 5)
            competitor_report = self.competitor_analyzer.generate_competitive_intelligence_report(competitor_analysis)
            
            results['competitor_analysis'] = {
                'raw_analysis': competitor_analysis,
                'intelligence_report': competitor_report,
                'total_competitors': competitor_analysis['total_competitors_found'],
                'recommendations_count': len(competitor_report['strategic_recommendations'])
            }
            logger.info(f"✅ Análise de {competitor_analysis['total_competitors_found']} concorrentes concluída")
            
        except Exception as e:
            logger.error(f"❌ Erro na análise de concorrentes: {e}")
            results['errors'].append(f"Erro no sistema de concorrentes: {str(e)}")
        
        # 3. Gerar gráfico de funil
        try:
            logger.info("📊 Gerando gráfico de funil...")
            funnel_data = self.funnel_generator.create_custom_funnel_data(segment, target_audience, product)
            funnel_result = await self.funnel_generator.generate_sales_funnel_chart(funnel_data)
            
            if funnel_result.get('success'):
                results['funnel_chart'] = {
                    'base64': funnel_result['chart_base64'],
                    'data_url': funnel_result['chart_data_url'],
                    'stages': funnel_result['funnel_stages'],
                    'method': funnel_result['method'],
                    'size': '1080x1080'
                }
                logger.info("✅ Gráfico de funil gerado com sucesso")
            else:
                results['errors'].append(f"Falha na geração do funil: {funnel_result.get('error')}")
                
        except Exception as e:
            logger.error(f"❌ Erro na geração do funil: {e}")
            results['errors'].append(f"Erro no sistema de funil: {str(e)}")
        
        # Verificar se houve erros críticos
        if len(results['errors']) >= 3:
            results['success'] = False
            logger.error("❌ Muitos erros críticos no pacote de análise")
        
        logger.info(f"🎯 Pacote de análise concluído - Sucesso: {results['success']}")
        return results
    
    def format_for_report_integration(self, analysis_package: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formata os resultados para integração no relatório final
        """
        logger.info("📋 Formatando resultados para integração no relatório...")
        
        formatted = {
            'avatar_section': {
                'title': 'Avatar do Cliente Ideal',
                'image_base64': analysis_package.get('avatar_image', {}).get('base64'),
                'description': self._generate_avatar_description(analysis_package['persona_data'])
            },
            'competitor_section': {
                'title': 'Análise Competitiva',
                'competitors': analysis_package.get('competitor_analysis', {}).get('raw_analysis', {}).get('competitors', []),
                'recommendations': analysis_package.get('competitor_analysis', {}).get('intelligence_report', {}).get('strategic_recommendations', []),
                'market_opportunities': analysis_package.get('competitor_analysis', {}).get('intelligence_report', {}).get('market_opportunities', [])
            },
            'funnel_section': {
                'title': 'Funil de Vendas',
                'chart_base64': analysis_package.get('funnel_chart', {}).get('base64'),
                'stages_count': analysis_package.get('funnel_chart', {}).get('stages', 0),
                'description': f"Funil de vendas customizado para {analysis_package['segment']}"
            },
            'metadata': {
                'generated_at': analysis_package['timestamp'],
                'segment': analysis_package['segment'],
                'target_audience': analysis_package['target_audience'],
                'success': analysis_package['success'],
                'errors_count': len(analysis_package['errors'])
            }
        }
        
        logger.info("✅ Formatação concluída")
        return formatted
    
    def _generate_avatar_description(self, persona_data: Dict[str, Any]) -> str:
        """
        Gera descrição textual do avatar baseada nos dados da persona
        """
        dados_demo = persona_data.get('dados_demograficos', {})
        perfil_psico = persona_data.get('perfil_psicologico', {})
        
        nome = dados_demo.get('nome_completo', 'Cliente Ideal')
        idade = dados_demo.get('idade', 'N/A')
        profissao = dados_demo.get('profissao', 'Profissional')
        mbti = perfil_psico.get('personalidade_mbti', 'N/A')
        
        return f"""
        {nome} representa o perfil ideal do cliente-alvo. 
        Com {idade} anos, atua como {profissao} e possui personalidade {mbti}.
        Esta representação visual facilita a identificação e conexão emocional 
        com o público-alvo durante apresentações e materiais de marketing.
        """
    
    async def test_all_systems(self) -> Dict[str, bool]:
        """
        Testa todos os sistemas integrados
        """
        logger.info("🧪 Testando todos os sistemas integrados...")
        
        # Dados de teste
        test_persona = {
            'dados_demograficos': {
                'nome_completo': 'Maria Silva',
                'idade': 35,
                'genero': 'Feminino',
                'profissao': 'Gerente de Marketing'
            },
            'perfil_psicologico': {
                'personalidade_mbti': 'ENFJ'
            }
        }
        
        results = {
            'avatar_system': False,
            'competitor_system': False,
            'funnel_system': False,
            'integration': False
        }
        
        try:
            # Teste do sistema de avatar
            avatar_result = await self.avatar_generator.gerar_imagem_avatar(test_persona)
            results['avatar_system'] = avatar_result.get('success', False)
            
            # Teste do sistema de concorrentes
            competitor_analysis = await self.competitor_analyzer.analyze_real_competitors('marketing digital', 3)
            results['competitor_system'] = competitor_analysis.get('total_competitors_found', 0) > 0
            
            # Teste do sistema de funil
            funnel_data = self.funnel_generator.create_custom_funnel_data('marketing digital', 'PMEs', 'Software')
            funnel_result = await self.funnel_generator.generate_sales_funnel_chart(funnel_data)
            results['funnel_system'] = funnel_result.get('success', False)
            
            # Teste de integração completa
            if all([results['avatar_system'], results['competitor_system'], results['funnel_system']]):
                package = await self.generate_complete_analysis_package(
                    test_persona, 'marketing digital', 'PMEs brasileiras', 'Plataforma SaaS'
                )
                results['integration'] = package.get('success', False)
            
        except Exception as e:
            logger.error(f"❌ Erro nos testes: {e}")
        
        # Log dos resultados
        for system, success in results.items():
            status = "✅ PASSOU" if success else "❌ FALHOU"
            logger.info(f"{system.upper()}: {status}")
        
        total_passed = sum(results.values())
        logger.info(f"🎯 RESULTADO: {total_passed}/4 sistemas funcionando")
        
        return results

# Instância global para uso direto
enhanced_systems = EnhancedSystemsIntegration()

# Função de conveniência para uso externo
async def generate_enhanced_analysis(persona_data: Dict[str, Any], 
                                   segment: str, 
                                   target_audience: str,
                                   product: str = None) -> Dict[str, Any]:
    """
    Função de conveniência para gerar análise completa
    """
    async with EnhancedSystemsIntegration() as systems:
        return await systems.generate_complete_analysis_package(
            persona_data, segment, target_audience, product
        )