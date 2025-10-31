import os
import logging
import requests
import asyncio
import aiohttp
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class RealCompetitorAnalyzer:
    """
    Sistema de análise de concorrentes reais do mercado brasileiro
    """
    def __init__(self):
        # Base de dados de concorrentes reais por segmento
        self.competitors_database = {
            'marketing_digital': [
                {
                    'name': 'RD Station',
                    'website': 'https://www.rdstation.com',
                    'description': 'Plataforma de automação de marketing e vendas',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/rd-station',
                        'instagram': '@rdstation',
                        'youtube': 'RD Station'
                    },
                    'key_products': ['RD Station Marketing', 'RD Station CRM', 'RD Station Conversas'],
                    'target_audience': 'PMEs e empresas de médio porte',
                    'pricing_model': 'SaaS mensal',
                    'market_position': 'Líder no Brasil'
                },
                {
                    'name': 'Hubspot Brasil',
                    'website': 'https://www.hubspot.com.br',
                    'description': 'Plataforma completa de CRM, marketing e vendas',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/hubspot',
                        'instagram': '@hubspot',
                        'youtube': 'HubSpot'
                    },
                    'key_products': ['HubSpot CRM', 'Marketing Hub', 'Sales Hub'],
                    'target_audience': 'Empresas de todos os portes',
                    'pricing_model': 'Freemium + SaaS',
                    'market_position': 'Líder global'
                },
                {
                    'name': 'Leadlovers',
                    'website': 'https://www.leadlovers.com',
                    'description': 'Plataforma de automação de marketing digital',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/leadlovers',
                        'instagram': '@leadlovers',
                        'youtube': 'Leadlovers'
                    },
                    'key_products': ['Automação de Email', 'Landing Pages', 'CRM'],
                    'target_audience': 'Empreendedores digitais e PMEs',
                    'pricing_model': 'SaaS mensal',
                    'market_position': 'Forte no mercado brasileiro'
                },
                {
                    'name': 'Klenty',
                    'website': 'https://www.klenty.com',
                    'description': 'Plataforma de automação de vendas e outreach',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/klenty',
                        'instagram': '@klenty',
                        'youtube': 'Klenty'
                    },
                    'key_products': ['Sales Automation', 'Email Sequences', 'CRM Integration'],
                    'target_audience': 'Equipes de vendas B2B',
                    'pricing_model': 'SaaS por usuário',
                    'market_position': 'Crescente no Brasil'
                },
                {
                    'name': 'ActiveCampaign Brasil',
                    'website': 'https://www.activecampaign.com/pt',
                    'description': 'Plataforma de automação de marketing e CRM',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/activecampaign',
                        'instagram': '@activecampaign',
                        'youtube': 'ActiveCampaign'
                    },
                    'key_products': ['Email Marketing', 'Marketing Automation', 'CRM'],
                    'target_audience': 'PMEs e empresas em crescimento',
                    'pricing_model': 'SaaS escalonável',
                    'market_position': 'Forte presença internacional'
                }
            ],
            'ecommerce': [
                {
                    'name': 'Shopify Brasil',
                    'website': 'https://www.shopify.com.br',
                    'description': 'Plataforma de e-commerce completa',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/shopify',
                        'instagram': '@shopify',
                        'youtube': 'Shopify'
                    },
                    'key_products': ['Loja Online', 'Shopify POS', 'Shopify Plus'],
                    'target_audience': 'Empreendedores e empresas de e-commerce',
                    'pricing_model': 'SaaS + taxa por transação',
                    'market_position': 'Líder global'
                },
                {
                    'name': 'Nuvemshop',
                    'website': 'https://www.nuvemshop.com.br',
                    'description': 'Plataforma brasileira de e-commerce',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/nuvemshop',
                        'instagram': '@nuvemshop',
                        'youtube': 'Nuvemshop'
                    },
                    'key_products': ['Loja Virtual', 'Nuvem Pago', 'Nuvem Frete'],
                    'target_audience': 'PMEs brasileiras',
                    'pricing_model': 'Freemium + SaaS',
                    'market_position': 'Líder na América Latina'
                },
                {
                    'name': 'VTEX',
                    'website': 'https://vtex.com',
                    'description': 'Plataforma de comércio digital enterprise',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/vtex',
                        'instagram': '@vtex',
                        'youtube': 'VTEX'
                    },
                    'key_products': ['VTEX Commerce', 'VTEX IO', 'VTEX Live Shopping'],
                    'target_audience': 'Grandes empresas e enterprises',
                    'pricing_model': 'SaaS enterprise',
                    'market_position': 'Líder no Brasil para grandes empresas'
                },
                {
                    'name': 'Magento Commerce Brasil',
                    'website': 'https://business.adobe.com/br/products/magento/magento-commerce.html',
                    'description': 'Plataforma de e-commerce da Adobe',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/magento',
                        'instagram': '@magento',
                        'youtube': 'Magento'
                    },
                    'key_products': ['Magento Commerce', 'Adobe Commerce Cloud'],
                    'target_audience': 'Empresas de médio e grande porte',
                    'pricing_model': 'Licença + SaaS',
                    'market_position': 'Forte presença global'
                },
                {
                    'name': 'Loja Integrada',
                    'website': 'https://lojaintegrada.com.br',
                    'description': 'Plataforma brasileira de e-commerce',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/loja-integrada',
                        'instagram': '@lojaintegrada',
                        'youtube': 'Loja Integrada'
                    },
                    'key_products': ['Loja Virtual', 'Sistema de Gestão', 'Marketplace'],
                    'target_audience': 'PMEs brasileiras',
                    'pricing_model': 'SaaS mensal',
                    'market_position': 'Tradicional no mercado brasileiro'
                }
            ],
            'influencers_marketing': [
                {
                    'name': 'Camila Farani',
                    'website': 'https://camilafarani.com.br',
                    'description': 'Investidora anjo e especialista em empreendedorismo',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/in/camilafarani',
                        'instagram': '@camilafarani',
                        'youtube': 'Camila Farani'
                    },
                    'key_products': ['Consultoria', 'Palestras', 'Investimentos'],
                    'target_audience': 'Empreendedores e startups',
                    'pricing_model': 'Consultoria personalizada',
                    'market_position': 'Influencer líder em empreendedorismo'
                },
                {
                    'name': 'Flávio Augusto',
                    'website': 'https://flavioaugusto.com.br',
                    'description': 'Empreendedor e investidor, fundador da Wise Up',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/in/flavioaugusto',
                        'instagram': '@flavioaugusto',
                        'youtube': 'Flávio Augusto'
                    },
                    'key_products': ['Mentoria', 'Livros', 'Palestras'],
                    'target_audience': 'Empreendedores e executivos',
                    'pricing_model': 'Produtos digitais + mentoria',
                    'market_position': 'Referência em empreendedorismo'
                },
                {
                    'name': 'Conrado Adolpho',
                    'website': 'https://conradoadolpho.com',
                    'description': 'Especialista em marketing digital e autor',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/in/conradoadolpho',
                        'instagram': '@conradoadolpho',
                        'youtube': 'Conrado Adolpho'
                    },
                    'key_products': ['Cursos', 'Livros', 'Consultoria'],
                    'target_audience': 'Profissionais de marketing',
                    'pricing_model': 'Cursos online + consultoria',
                    'market_position': 'Autoridade em marketing digital'
                },
                {
                    'name': 'Thiago Nigro (Primo Rico)',
                    'website': 'https://primorico.com.br',
                    'description': 'Educador financeiro e empreendedor',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/in/thiago-nigro',
                        'instagram': '@thiago.nigro',
                        'youtube': 'O Primo Rico'
                    },
                    'key_products': ['Cursos', 'Livros', 'Aplicativo'],
                    'target_audience': 'Pessoas interessadas em educação financeira',
                    'pricing_model': 'Freemium + cursos pagos',
                    'market_position': 'Maior influencer de finanças do Brasil'
                },
                {
                    'name': 'Nathalia Arcuri',
                    'website': 'https://nathaliaarcuri.com',
                    'description': 'Educadora financeira e empresária',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/in/nathaliaarcuri',
                        'instagram': '@nath.arcuri',
                        'youtube': 'Me Poupe!'
                    },
                    'key_products': ['Cursos', 'Livros', 'Aplicativo Me Poupe'],
                    'target_audience': 'Mulheres e jovens interessados em finanças',
                    'pricing_model': 'Cursos + produtos digitais',
                    'market_position': 'Líder em educação financeira feminina'
                }
            ],
            'tecnologia': [
                {
                    'name': 'Nubank',
                    'website': 'https://nubank.com.br',
                    'description': 'Fintech líder na América Latina',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/nubank',
                        'instagram': '@nubank',
                        'youtube': 'Nubank'
                    },
                    'key_products': ['Cartão de Crédito', 'Conta Digital', 'Investimentos'],
                    'target_audience': 'Consumidores digitais',
                    'pricing_model': 'Freemium + serviços financeiros',
                    'market_position': 'Unicórnio brasileiro'
                },
                {
                    'name': 'Stone',
                    'website': 'https://stone.com.br',
                    'description': 'Empresa de tecnologia financeira',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/stone-pagamentos',
                        'instagram': '@stone',
                        'youtube': 'Stone'
                    },
                    'key_products': ['Maquininhas', 'Banking', 'Software'],
                    'target_audience': 'PMEs e empreendedores',
                    'pricing_model': 'Taxa por transação + SaaS',
                    'market_position': 'Líder em meios de pagamento'
                },
                {
                    'name': 'PagSeguro',
                    'website': 'https://pagseguro.uol.com.br',
                    'description': 'Plataforma de pagamentos digitais',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/pagseguro',
                        'instagram': '@pagseguro',
                        'youtube': 'PagSeguro'
                    },
                    'key_products': ['Gateway de Pagamento', 'Maquininhas', 'Conta Digital'],
                    'target_audience': 'E-commerces e lojistas',
                    'pricing_model': 'Taxa por transação',
                    'market_position': 'Tradicional no mercado brasileiro'
                },
                {
                    'name': 'Mercado Pago',
                    'website': 'https://mercadopago.com.br',
                    'description': 'Solução de pagamentos do Mercado Livre',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/mercado-pago',
                        'instagram': '@mercadopago',
                        'youtube': 'Mercado Pago'
                    },
                    'key_products': ['Pagamentos Online', 'Point', 'Conta Mercado Pago'],
                    'target_audience': 'Vendedores online e físicos',
                    'pricing_model': 'Taxa por transação + serviços',
                    'market_position': 'Integrado ao maior marketplace da AL'
                },
                {
                    'name': 'iFood',
                    'website': 'https://ifood.com.br',
                    'description': 'Plataforma de delivery de comida',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/ifood',
                        'instagram': '@ifoodbrasil',
                        'youtube': 'iFood'
                    },
                    'key_products': ['Delivery', 'iFood Shop', 'iFood Card'],
                    'target_audience': 'Consumidores e restaurantes',
                    'pricing_model': 'Comissão por pedido',
                    'market_position': 'Líder absoluto em food delivery'
                }
            ],
            'consultoria': [
                {
                    'name': 'McKinsey & Company Brasil',
                    'website': 'https://www.mckinsey.com/br',
                    'description': 'Consultoria estratégica global',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/mckinsey',
                        'instagram': '@mckinsey_co',
                        'youtube': 'McKinsey & Company'
                    },
                    'key_products': ['Consultoria Estratégica', 'Transformação Digital', 'Analytics'],
                    'target_audience': 'Grandes corporações',
                    'pricing_model': 'Projeto customizado',
                    'market_position': 'Líder global em consultoria'
                },
                {
                    'name': 'Deloitte Brasil',
                    'website': 'https://www2.deloitte.com/br',
                    'description': 'Consultoria e auditoria global',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/deloitte',
                        'instagram': '@deloitte',
                        'youtube': 'Deloitte'
                    },
                    'key_products': ['Consultoria', 'Auditoria', 'Tax', 'Risk Advisory'],
                    'target_audience': 'Empresas de médio e grande porte',
                    'pricing_model': 'Projeto + hora técnica',
                    'market_position': 'Big Four global'
                },
                {
                    'name': 'Falconi',
                    'website': 'https://www.falconi.com',
                    'description': 'Consultoria brasileira de gestão',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/falconi',
                        'instagram': '@falconi_oficial',
                        'youtube': 'Falconi'
                    },
                    'key_products': ['Consultoria em Gestão', 'Lean Six Sigma', 'Transformação'],
                    'target_audience': 'Empresas de todos os portes',
                    'pricing_model': 'Projeto customizado',
                    'market_position': 'Líder brasileira'
                },
                {
                    'name': 'EY Brasil',
                    'website': 'https://www.ey.com/pt_br',
                    'description': 'Consultoria e auditoria global',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/ernstandyoung',
                        'instagram': '@ey_brasil',
                        'youtube': 'EY'
                    },
                    'key_products': ['Assurance', 'Tax', 'Strategy', 'Transactions'],
                    'target_audience': 'Empresas de médio e grande porte',
                    'pricing_model': 'Projeto + hora técnica',
                    'market_position': 'Big Four global'
                },
                {
                    'name': 'Bain & Company Brasil',
                    'website': 'https://www.bain.com/pt-br',
                    'description': 'Consultoria estratégica global',
                    'social_media': {
                        'linkedin': 'https://linkedin.com/company/bain-and-company',
                        'instagram': '@bainandcompany',
                        'youtube': 'Bain & Company'
                    },
                    'key_products': ['Estratégia', 'Private Equity', 'Transformação'],
                    'target_audience': 'Grandes corporações',
                    'pricing_model': 'Projeto customizado',
                    'market_position': 'Top 3 global em consultoria'
                }
            ]
        }
        
        self.competitor_content_db = []

    def get_competitors_by_segment(self, segment: str) -> List[Dict[str, Any]]:
        """
        Retorna concorrentes reais baseados no segmento de mercado
        """
        segment_lower = segment.lower()
        
        # Mapeia termos comuns para segmentos
        segment_mapping = {
            'marketing': 'marketing_digital',
            'digital': 'marketing_digital',
            'automacao': 'marketing_digital',
            'crm': 'marketing_digital',
            'vendas': 'marketing_digital',
            'ecommerce': 'ecommerce',
            'e-commerce': 'ecommerce',
            'loja': 'ecommerce',
            'virtual': 'ecommerce',
            'consultoria': 'consultoria',
            'consulting': 'consultoria',
            'estrategia': 'consultoria',
            'gestao': 'consultoria',
            'influencer': 'influencers_marketing',
            'influencers': 'influencers_marketing',
            'empreendedorismo': 'influencers_marketing',
            'coach': 'influencers_marketing',
            'mentor': 'influencers_marketing',
            'tecnologia': 'tecnologia',
            'tech': 'tecnologia',
            'fintech': 'tecnologia',
            'startup': 'tecnologia',
            'app': 'tecnologia',
            'software': 'tecnologia'
        }
        
        # Encontra o segmento correspondente
        matched_segment = None
        for key, value in segment_mapping.items():
            if key in segment_lower:
                matched_segment = value
                break
        
        if not matched_segment:
            # Se não encontrar, retorna uma mistura dos principais
            all_competitors = []
            for seg_competitors in self.competitors_database.values():
                all_competitors.extend(seg_competitors[:2])  # 2 de cada segmento
            return all_competitors[:5]
        
        return self.competitors_database.get(matched_segment, [])

    async def analyze_real_competitors(self, segment: str, target_count: int = 5) -> Dict[str, Any]:
        """
        Analisa concorrentes reais do mercado baseado no segmento
        """
        logger.info(f"🔍 Analisando concorrentes reais para segmento: {segment}")
        
        competitors = self.get_competitors_by_segment(segment)[:target_count]
        
        analysis_results = {
            'segment': segment,
            'total_competitors_found': len(competitors),
            'analysis_date': datetime.now().isoformat(),
            'competitors': [],
            'market_insights': {
                'dominant_pricing_models': {},
                'common_target_audiences': {},
                'key_market_positions': {},
                'social_media_presence': {
                    'linkedin': 0,
                    'instagram': 0,
                    'youtube': 0
                }
            }
        }
        
        for competitor in competitors:
            competitor_analysis = await self._analyze_single_competitor(competitor)
            analysis_results['competitors'].append(competitor_analysis)
            
            # Coleta insights do mercado
            pricing_model = competitor.get('pricing_model', 'Não informado')
            analysis_results['market_insights']['dominant_pricing_models'][pricing_model] = \
                analysis_results['market_insights']['dominant_pricing_models'].get(pricing_model, 0) + 1
            
            target_audience = competitor.get('target_audience', 'Não informado')
            analysis_results['market_insights']['common_target_audiences'][target_audience] = \
                analysis_results['market_insights']['common_target_audiences'].get(target_audience, 0) + 1
            
            market_position = competitor.get('market_position', 'Não informado')
            analysis_results['market_insights']['key_market_positions'][market_position] = \
                analysis_results['market_insights']['key_market_positions'].get(market_position, 0) + 1
            
            # Conta presença em redes sociais
            social_media = competitor.get('social_media', {})
            if social_media.get('linkedin'):
                analysis_results['market_insights']['social_media_presence']['linkedin'] += 1
            if social_media.get('instagram'):
                analysis_results['market_insights']['social_media_presence']['instagram'] += 1
            if social_media.get('youtube'):
                analysis_results['market_insights']['social_media_presence']['youtube'] += 1
        
        logger.info(f"✅ Análise concluída: {len(competitors)} concorrentes reais analisados")
        return analysis_results

    async def _analyze_single_competitor(self, competitor: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa um único concorrente em detalhes
        """
        logger.info(f"🎯 Analisando concorrente: {competitor['name']}")
        
        analysis = {
            'name': competitor['name'],
            'website': competitor['website'],
            'description': competitor['description'],
            'key_products': competitor['key_products'],
            'target_audience': competitor['target_audience'],
            'pricing_model': competitor['pricing_model'],
            'market_position': competitor['market_position'],
            'social_media': competitor['social_media'],
            'competitive_advantages': self._identify_competitive_advantages(competitor),
            'market_share_indicators': self._estimate_market_indicators(competitor),
            'digital_presence_score': self._calculate_digital_presence_score(competitor),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return analysis

    def _identify_competitive_advantages(self, competitor: Dict[str, Any]) -> List[str]:
        """
        Identifica vantagens competitivas baseadas nos dados do concorrente
        """
        advantages = []
        
        name = competitor['name'].lower()
        description = competitor['description'].lower()
        market_position = competitor['market_position'].lower()
        
        # Vantagens baseadas na posição de mercado
        if 'líder' in market_position:
            advantages.append('Liderança de mercado estabelecida')
        if 'global' in market_position:
            advantages.append('Presença global consolidada')
        if 'brasil' in market_position:
            advantages.append('Forte presença no mercado brasileiro')
        
        # Vantagens baseadas no modelo de negócio
        pricing_model = competitor['pricing_model'].lower()
        if 'freemium' in pricing_model:
            advantages.append('Modelo freemium para aquisição de clientes')
        if 'saas' in pricing_model:
            advantages.append('Modelo SaaS escalável')
        if 'enterprise' in pricing_model:
            advantages.append('Foco em clientes enterprise')
        
        # Vantagens baseadas nos produtos
        products = [p.lower() for p in competitor['key_products']]
        if any('automation' in p or 'automação' in p for p in products):
            advantages.append('Capacidades avançadas de automação')
        if any('crm' in p for p in products):
            advantages.append('Integração nativa com CRM')
        if any('analytics' in p or 'análise' in p for p in products):
            advantages.append('Recursos avançados de analytics')
        
        # Vantagens baseadas na empresa
        if any(brand in name for brand in ['rd station', 'hubspot', 'shopify', 'vtex']):
            advantages.append('Marca reconhecida no mercado')
        if any(term in description for term in ['completa', 'integrada', 'all-in-one']):
            advantages.append('Solução completa e integrada')
        
        return advantages if advantages else ['Posicionamento competitivo sólido']

    def _estimate_market_indicators(self, competitor: Dict[str, Any]) -> Dict[str, str]:
        """
        Estima indicadores de participação de mercado
        """
        indicators = {}
        
        market_position = competitor['market_position'].lower()
        name = competitor['name'].lower()
        
        # Estimativa de market share baseada na posição
        if 'líder global' in market_position:
            indicators['estimated_market_share'] = 'Alto (>20%)'
            indicators['growth_stage'] = 'Maturidade'
        elif 'líder' in market_position:
            indicators['estimated_market_share'] = 'Médio-Alto (10-20%)'
            indicators['growth_stage'] = 'Crescimento/Maturidade'
        elif 'forte' in market_position or 'tradicional' in market_position:
            indicators['estimated_market_share'] = 'Médio (5-10%)'
            indicators['growth_stage'] = 'Crescimento'
        else:
            indicators['estimated_market_share'] = 'Baixo-Médio (<5%)'
            indicators['growth_stage'] = 'Crescimento inicial'
        
        # Estimativa de receita baseada no tipo de empresa
        if any(brand in name for brand in ['hubspot', 'shopify', 'vtex', 'mckinsey', 'deloitte']):
            indicators['estimated_revenue_range'] = 'Alto (>R$ 100M/ano)'
        elif any(brand in name for brand in ['rd station', 'nuvemshop', 'leadlovers']):
            indicators['estimated_revenue_range'] = 'Médio (R$ 10-100M/ano)'
        else:
            indicators['estimated_revenue_range'] = 'Médio-Baixo (<R$ 10M/ano)'
        
        return indicators

    def _calculate_digital_presence_score(self, competitor: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula score de presença digital
        """
        score = 0
        max_score = 10
        details = {}
        
        social_media = competitor.get('social_media', {})
        
        # Pontuação por presença em redes sociais
        if social_media.get('linkedin'):
            score += 3
            details['linkedin'] = 'Presente'
        else:
            details['linkedin'] = 'Ausente'
            
        if social_media.get('instagram'):
            score += 2
            details['instagram'] = 'Presente'
        else:
            details['instagram'] = 'Ausente'
            
        if social_media.get('youtube'):
            score += 2
            details['youtube'] = 'Presente'
        else:
            details['youtube'] = 'Ausente'
        
        # Pontuação por website
        if competitor.get('website'):
            score += 3
            details['website'] = 'Presente'
        else:
            details['website'] = 'Ausente'
        
        # Classificação do score
        if score >= 8:
            classification = 'Excelente'
        elif score >= 6:
            classification = 'Boa'
        elif score >= 4:
            classification = 'Regular'
        else:
            classification = 'Fraca'
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round((score / max_score) * 100, 1),
            'classification': classification,
            'details': details
        }

    def generate_competitive_intelligence_report(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera relatório de inteligência competitiva
        """
        logger.info("📊 Gerando relatório de inteligência competitiva...")
        
        competitors = analysis_results.get('competitors', [])
        market_insights = analysis_results.get('market_insights', {})
        
        report = {
            'executive_summary': {
                'total_competitors_analyzed': len(competitors),
                'segment': analysis_results.get('segment'),
                'analysis_date': analysis_results.get('analysis_date'),
                'key_findings': []
            },
            'competitive_landscape': {
                'market_leaders': [],
                'emerging_players': [],
                'pricing_strategies': market_insights.get('dominant_pricing_models', {}),
                'target_audience_distribution': market_insights.get('common_target_audiences', {})
            },
            'digital_presence_analysis': {
                'average_digital_score': 0,
                'social_media_adoption': market_insights.get('social_media_presence', {}),
                'digital_leaders': [],
                'digital_laggards': []
            },
            'strategic_recommendations': [],
            'competitive_gaps': [],
            'market_opportunities': []
        }
        
        # Analisa líderes de mercado
        for competitor in competitors:
            market_position = competitor.get('market_position', '').lower()
            if 'líder' in market_position:
                report['competitive_landscape']['market_leaders'].append({
                    'name': competitor['name'],
                    'position': competitor['market_position'],
                    'key_advantages': competitor.get('competitive_advantages', [])
                })
            else:
                report['competitive_landscape']['emerging_players'].append({
                    'name': competitor['name'],
                    'position': competitor['market_position']
                })
        
        # Calcula score médio de presença digital
        digital_scores = [comp.get('digital_presence_score', {}).get('score', 0) for comp in competitors]
        if digital_scores:
            report['digital_presence_analysis']['average_digital_score'] = round(sum(digital_scores) / len(digital_scores), 1)
        
        # Identifica líderes e retardatários digitais
        for competitor in competitors:
            digital_score = competitor.get('digital_presence_score', {})
            if digital_score.get('score', 0) >= 8:
                report['digital_presence_analysis']['digital_leaders'].append(competitor['name'])
            elif digital_score.get('score', 0) <= 4:
                report['digital_presence_analysis']['digital_laggards'].append(competitor['name'])
        
        # Gera recomendações estratégicas
        report['strategic_recommendations'] = self._generate_strategic_recommendations(competitors, market_insights)
        
        # Identifica gaps competitivos
        report['competitive_gaps'] = self._identify_competitive_gaps(competitors)
        
        # Identifica oportunidades de mercado
        report['market_opportunities'] = self._identify_market_opportunities(competitors, market_insights)
        
        logger.info("✅ Relatório de inteligência competitiva gerado com sucesso")
        return report

    def _generate_strategic_recommendations(self, competitors: List[Dict], market_insights: Dict) -> List[str]:
        """
        Gera recomendações estratégicas baseadas na análise competitiva
        """
        recommendations = []
        
        # Análise de modelos de pricing
        pricing_models = market_insights.get('dominant_pricing_models', {})
        if pricing_models:
            most_common_pricing = max(pricing_models.keys(), key=lambda k: pricing_models[k])
            recommendations.append(f"Considerar modelo de pricing '{most_common_pricing}' que é dominante no mercado")
        
        # Análise de presença digital
        social_presence = market_insights.get('social_media_presence', {})
        total_competitors = len(competitors)
        
        if social_presence.get('linkedin', 0) / total_competitors > 0.8:
            recommendations.append("LinkedIn é essencial - 80%+ dos concorrentes têm presença ativa")
        
        if social_presence.get('youtube', 0) / total_competitors > 0.6:
            recommendations.append("Investir em conteúdo no YouTube - maioria dos concorrentes utiliza")
        
        # Análise de vantagens competitivas
        all_advantages = []
        for competitor in competitors:
            all_advantages.extend(competitor.get('competitive_advantages', []))
        
        common_advantages = {}
        for advantage in all_advantages:
            common_advantages[advantage] = common_advantages.get(advantage, 0) + 1
        
        if common_advantages:
            most_common_advantage = max(common_advantages.keys(), key=lambda k: common_advantages[k])
            recommendations.append(f"Foco em '{most_common_advantage}' - vantagem competitiva comum no mercado")
        
        return recommendations

    def _identify_competitive_gaps(self, competitors: List[Dict]) -> List[str]:
        """
        Identifica gaps competitivos no mercado
        """
        gaps = []
        
        # Analisa produtos oferecidos
        all_products = []
        for competitor in competitors:
            all_products.extend([p.lower() for p in competitor.get('key_products', [])])
        
        product_frequency = {}
        for product in all_products:
            product_frequency[product] = product_frequency.get(product, 0) + 1
        
        # Identifica produtos menos comuns (possíveis gaps)
        total_competitors = len(competitors)
        for product, frequency in product_frequency.items():
            if frequency / total_competitors < 0.3:  # Menos de 30% dos concorrentes
                gaps.append(f"Oportunidade em '{product}' - pouco explorado pelos concorrentes")
        
        # Analisa públicos-alvo
        target_audiences = [comp.get('target_audience', '').lower() for comp in competitors]
        if 'startups' not in ' '.join(target_audiences):
            gaps.append("Mercado de startups pode estar subatendido")
        
        if 'pequenas empresas' not in ' '.join(target_audiences):
            gaps.append("Pequenas empresas podem ter necessidades específicas não atendidas")
        
        return gaps if gaps else ["Mercado bem atendido pelos concorrentes atuais"]

    def _identify_market_opportunities(self, competitors: List[Dict], market_insights: Dict) -> List[str]:
        """
        Identifica oportunidades de mercado
        """
        opportunities = []
        
        # Oportunidades baseadas em pricing
        pricing_models = market_insights.get('dominant_pricing_models', {})
        if 'Freemium + SaaS' not in pricing_models and len(pricing_models) > 0:
            opportunities.append("Modelo freemium pode ser diferencial competitivo")
        
        # Oportunidades baseadas em presença digital
        social_presence = market_insights.get('social_media_presence', {})
        total_competitors = len(competitors)
        
        if social_presence.get('instagram', 0) / total_competitors < 0.5:
            opportunities.append("Instagram subutilizado - oportunidade de diferenciação")
        
        # Oportunidades baseadas em posicionamento
        market_positions = market_insights.get('key_market_positions', {})
        if not any('inovação' in pos.lower() for pos in market_positions.keys()):
            opportunities.append("Posicionamento focado em inovação pode ser diferencial")
        
        if not any('sustentabilidade' in pos.lower() for pos in market_positions.keys()):
            opportunities.append("Sustentabilidade e ESG podem ser diferenciais emergentes")
        
        return opportunities if opportunities else ["Mercado maduro com poucas oportunidades óbvias"]
        logger.info(f"Concorrente {name} adicionado/atualizado com URLs: {base_urls}")

    def _crawl_for_new_urls(self, base_url: str) -> List[str]:
        """Simula o rastreamento de uma URL base para encontrar novas URLs de conteúdo."""
        # Em um cenário real, isso seria um crawler mais sofisticado.
        # Por simplicidade, vamos mockar algumas URLs.
        logger.info(f"Simulando rastreamento para novas URLs em: {base_url}")
        if "example.com" in base_url:
            return [
                f"{base_url}/blog/novo-post-1",
                f"{base_url}/produtos/lancamento-x",
                f"{base_url}/noticias/ultimas-novidades"
            ]
        return []

    def collect_and_analyze_content(self, competitor_name: str) -> List[Dict[str, Any]]:
        """Coleta e analisa o conteúdo de um concorrente específico."""
        config = self.competitors_config.get(competitor_name)
        if not config:
            logger.warning(f"Concorrente {competitor_name} não configurado.")
            return []

        new_content_items = []
        for base_url in config["base_urls"]:
            new_urls = self._crawl_for_new_urls(base_url)
            for url in new_urls:
                logger.info(f"Extraindo conteúdo de concorrente: {url}")
                extracted_data = self.mcp_supadata_manager.extract_from_url(url)
                
                if "error" not in extracted_data:
                    content = extracted_data.get("extracted_text", "")
                    title = extracted_data.get("title", "Sem Título")
                    
                    # Simula análise de palavras-chave e tópicos
                    keywords = [word for word in content.lower().split() if len(word) > 5 and content.lower().count(word) > 2][:5]

                    content_item = {
                        "competitor": competitor_name,
                        "url": url,
                        "title": title,
                        "content_preview": content[:200] + "..." if len(content) > 200 else content,
                        "keywords": keywords,
                        "timestamp": datetime.now().isoformat()
                    }
                    self.competitor_content_db.append(content_item)
                    new_content_items.append(content_item)
                else:
                    logger.warning(f"Falha ao extrair conteúdo de {url} com Supadata: {extracted_data["error"]}")
        
        config["last_crawled"] = datetime.now().isoformat()
        logger.info(f"Coleta e análise para {competitor_name} concluída. Novos itens: {len(new_content_items)}")
        return new_content_items

    def get_competitor_content_summary(self, competitor_name: str = None) -> Dict[str, Any]:
        """Retorna um resumo do conteúdo coletado para um concorrente ou todos."""
        filtered_content = self.competitor_content_db
        if competitor_name:
            filtered_content = [c for c in self.competitor_content_db if c["competitor"] == competitor_name]

        total_items = len(filtered_content)
        unique_keywords = set()
        for item in filtered_content:
            unique_keywords.update(item["keywords"])

        return {
            "total_content_items": total_items,
            "unique_keywords": list(unique_keywords),
            "content_list": filtered_content
        }

# Exemplo de uso (apenas para demonstração)
if __name__ == "__main__":
    from dotenv import load_dotenv
    from datetime import datetime
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env.example'))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    collector = CompetitorContentCollector()

    print("Adicionando concorrente...")
    collector.add_competitor("Concorrente A", ["https://www.example.com/concorrenteA"])
    collector.add_competitor("Concorrente B", ["https://www.example.com/concorrenteB"])

    print("Coletando e analisando conteúdo para Concorrente A...")
    new_content_a = collector.collect_and_analyze_content("Concorrente A")
    print(f"Novos itens para Concorrente A: {len(new_content_a)}")

    print("Coletando e analisando conteúdo para Concorrente B...")
    new_content_b = collector.collect_and_analyze_content("Concorrente B")
    print(f"Novos itens para Concorrente B: {len(new_content_b)}")

    summary_all = collector.get_competitor_content_summary()
    print("\nResumo de todo o conteúdo de concorrentes:")
    print(summary_all)

    summary_a = collector.get_competitor_content_summary("Concorrente A")
    print("\nResumo do conteúdo para Concorrente A:")
    print(summary_a)


