#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Geração de Gráfico de Funil de Vendas - V1.0
Gera gráficos de funil usando Gemini/OpenRouter, convertido em base64
"""

import os
import json
import base64
import logging
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import io
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

logger = logging.getLogger(__name__)

class SalesFunnelChartGenerator:
    """
    Sistema para gerar gráficos de funil de vendas usando IA
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GOOGLE_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.session = None
        
        # Configurações padrão do funil
        self.default_funnel_stages = [
            {
                'name': 'TOPO DO FUNIL (ATRAÇÃO - AWARENESS)',
                'description': 'Atrair a atenção do público-alvo e despertar o interesse pelo tema',
                'content': 'Artigos de blog sobre temas relevantes em neuropsiquiatria, posts informativos nas redes sociais, webinars gratuitos com especialistas, infográficos com dados estatísticos, vídeos curtos com dicas práticas',
                'channels': '900k pessoas/mês YouTube, e-mail marketing (para lista de contatos existente)',
                'color': '#4A90E2'
            },
            {
                'name': 'MEIO DO FUNIL (CONSIDERAÇÃO - INTEREST/DESIRE)',
                'description': 'Educar o público sobre o valor do e-book e construir relacionamento',
                'content': 'E-books gratuitos com amostras do conteúdo do guia, estudos de caso, depoimentos de profissionais que já utilizaram o guia, checklists de protocolos de tratamento, e-mail marketing com conteúdos exclusivos',
                'channels': '',
                'color': '#7ED321'
            },
            {
                'name': 'FUNDO DO FUNIL (DECISÃO - ACTION)',
                'description': 'Converter leads em clientes e gerar vendas',
                'content': 'Página de vendas de e-book com informações detalhadas, demonstração do conteúdo completo, bônus exclusivos, garantia de satisfação, depoimentos de clientes satisfeitos, ofertas especiais por tempo limitado',
                'channels': '',
                'color': '#F5A623'
            }
        ]
        
    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()
    
    def _create_funnel_prompt(self, funnel_data: Dict[str, Any]) -> str:
        """
        Cria prompt detalhado para geração de gráfico de funil
        """
        stages = funnel_data.get('stages', self.default_funnel_stages)
        
        prompt = f"""
        Create a professional sales funnel infographic with the following specifications:
        
        FUNNEL STAGES ({len(stages)} levels):
        """
        
        for i, stage in enumerate(stages):
            prompt += f"""
        
        Stage {i+1}: {stage['name']}
        - Description: {stage['description']}
        - Content: {stage['content'][:200]}...
        - Color: {stage.get('color', '#4A90E2')}
        """
        
        prompt += f"""
        
        DESIGN SPECIFICATIONS:
        - Create a 3D funnel diagram with {len(stages)} distinct levels
        - Each level should be clearly labeled with stage names
        - Use the specified colors for each stage
        - Include percentage or volume indicators if available
        - Professional business style with clean typography
        - Size: 1080x1080 pixels, square format
        - Background: Clean white or light gradient
        - Include icons or symbols relevant to each stage
        - Add subtle shadows and depth for 3D effect
        - Modern, minimalist design aesthetic
        
        CONTENT ELEMENTS:
        - Title: "FUNIL DE VENDAS" at the top
        - Each stage clearly labeled in Portuguese
        - Visual flow indicators (arrows or connectors)
        - Professional color scheme
        - Clean, readable fonts
        - Balanced composition
        
        Style: Professional infographic, business presentation quality, not cartoon or illustration
        """
        
        return prompt
    
    async def _generate_with_gemini_direct(self, prompt: str) -> Optional[str]:
        """
        Gera gráfico usando Gemini Direct API
        """
        if not self.gemini_api_key:
            logger.warning("Google API Key não encontrada")
            return None
            
        try:
            logger.info("🎨 Gerando gráfico de funil com Gemini Direct")
            
            # Usando Google AI Generative API
            import google.generativeai as genai
            
            genai.configure(api_key=self.gemini_api_key)
            
            # Como o Gemini não gera imagens diretamente, vamos criar um prompt aprimorado
            enhanced_prompt = f"""
            Professional sales funnel infographic for business presentation:
            
            {prompt}
            
            Additional requirements:
            - Ultra-high quality business infographic
            - Perfect for PowerPoint or business presentations
            - Clean, professional design
            - Optimized for digital display
            - Corporate visual identity
            - Data visualization best practices
            - Accessible color contrast
            - Scalable vector-style appearance
            """
            
            logger.info("✅ Prompt aprimorado com Gemini Direct")
            return None  # Retorna None para usar OpenRouter com prompt melhorado
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar gráfico com Gemini Direct: {e}")
            return None
    
    async def _generate_with_openrouter(self, prompt: str) -> Optional[str]:
        """
        Gera gráfico usando OpenRouter com múltiplos modelos
        """
        if not self.openrouter_api_key:
            logger.warning("OpenRouter API Key não encontrada")
            return None
            
        # Lista de modelos para tentar
        models = [
            "openai/dall-e-3",
            "openai/dall-e-2",
            "stability-ai/stable-diffusion-xl"
        ]
        
        for model in models:
            try:
                logger.info(f"🎨 Tentando gerar gráfico com OpenRouter usando {model}...")
                
                headers = {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://arqv30.com",
                    "X-Title": "ARQV30 Sales Funnel Generator"
                }
                
                if "dall-e" in model:
                    payload = {
                        "model": model,
                        "prompt": prompt,
                        "n": 1,
                        "size": "1024x1024",
                        "quality": "hd",
                        "style": "natural"
                    }
                    endpoint = "https://openrouter.ai/api/v1/images/generations"
                else:
                    payload = {
                        "model": model,
                        "prompt": prompt,
                        "max_tokens": 1000,
                        "temperature": 0.7
                    }
                    endpoint = "https://openrouter.ai/api/v1/chat/completions"
                
                async with self.session.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=90
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        if "dall-e" in model and result.get('data'):
                            image_url = result['data'][0].get('url')
                            if image_url:
                                logger.info(f"✅ Gráfico gerado com sucesso usando {model}")
                                return await self._download_and_convert_base64(image_url)
                    
                    else:
                        error_text = await response.text()
                        logger.warning(f"⚠️ Modelo {model} falhou: {response.status} - {error_text}")
                        continue
                        
            except Exception as e:
                logger.warning(f"⚠️ Erro com modelo {model}: {e}")
                continue
        
        logger.error("❌ Todos os modelos OpenRouter falharam")
        return None
    
    async def _download_and_convert_base64(self, image_url: str) -> Optional[str]:
        """
        Baixa imagem da URL e converte para base64
        """
        try:
            async with self.session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    
                    # Redimensiona para 1080x1080 se necessário
                    image = Image.open(io.BytesIO(image_data))
                    if image.size != (1080, 1080):
                        image = image.resize((1080, 1080), Image.Resampling.LANCZOS)
                    
                    # Converte para base64
                    buffer = io.BytesIO()
                    image.save(buffer, format='PNG')
                    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    logger.info(f"✅ Gráfico convertido para base64: {len(image_base64)} caracteres")
                    return image_base64
                    
        except Exception as e:
            logger.error(f"❌ Erro ao baixar e converter gráfico: {e}")
            return None
    
    def _generate_fallback_funnel(self, funnel_data: Dict[str, Any]) -> str:
        """
        Gera gráfico de funil de fallback usando matplotlib
        """
        try:
            logger.info("🎨 Gerando gráfico de funil de fallback com matplotlib...")
            
            stages = funnel_data.get('stages', self.default_funnel_stages)
            
            # Configuração da figura
            fig, ax = plt.subplots(figsize=(12, 12))
            fig.patch.set_facecolor('white')
            
            # Configurações do funil
            funnel_width = 8
            funnel_height = 10
            stage_height = funnel_height / len(stages)
            
            # Cores padrão se não especificadas
            default_colors = ['#4A90E2', '#7ED321', '#F5A623', '#D0021B', '#9013FE']
            
            # Desenha cada estágio do funil
            for i, stage in enumerate(stages):
                # Calcula largura do estágio (diminui conforme desce)
                width_ratio = 1 - (i * 0.3 / len(stages))
                stage_width = funnel_width * width_ratio
                
                # Posição do estágio
                x = (funnel_width - stage_width) / 2
                y = funnel_height - (i + 1) * stage_height
                
                # Cor do estágio
                color = stage.get('color', default_colors[i % len(default_colors)])
                
                # Desenha retângulo do estágio
                rect = patches.Rectangle(
                    (x, y), stage_width, stage_height,
                    linewidth=2, edgecolor='white', facecolor=color, alpha=0.8
                )
                ax.add_patch(rect)
                
                # Adiciona texto do estágio
                stage_name = stage['name'].split('(')[0].strip()  # Pega só o nome principal
                ax.text(
                    funnel_width / 2, y + stage_height / 2,
                    stage_name,
                    ha='center', va='center',
                    fontsize=14, fontweight='bold',
                    color='white', wrap=True
                )
                
                # Adiciona setas entre estágios
                if i < len(stages) - 1:
                    arrow_y = y - 0.2
                    ax.annotate('', xy=(funnel_width/2, arrow_y - 0.3), 
                               xytext=(funnel_width/2, arrow_y),
                               arrowprops=dict(arrowstyle='->', lw=3, color='#333333'))
            
            # Título
            ax.text(funnel_width / 2, funnel_height + 0.5, 'FUNIL DE VENDAS',
                   ha='center', va='center', fontsize=24, fontweight='bold',
                   color='#333333')
            
            # Configurações do gráfico
            ax.set_xlim(0, funnel_width)
            ax.set_ylim(0, funnel_height + 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Salva em buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='PNG', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
            
            # Converte para base64
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logger.info(f"✅ Gráfico de fallback gerado: {len(image_base64)} caracteres")
            return image_base64
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar gráfico de fallback: {e}")
            return self._generate_minimal_funnel()
    
    def _generate_minimal_funnel(self) -> str:
        """
        Gera gráfico mínimo em caso de erro total
        """
        try:
            logger.info("🎨 Gerando gráfico mínimo de emergência...")
            
            # Cria imagem simples 1080x1080
            img = Image.new('RGB', (1080, 1080), color='#f8f9fa')
            draw = ImageDraw.Draw(img)
            
            # Tenta carregar fonte
            try:
                font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
            except:
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()
            
            # Desenha título
            title = "FUNIL DE VENDAS"
            bbox = draw.textbbox((0, 0), title, font=font_title)
            text_width = bbox[2] - bbox[0]
            text_x = 540 - text_width // 2
            draw.text((text_x, 100), title, fill='#333333', font=font_title)
            
            # Desenha estágios do funil
            stages = ["TOPO - ATRAÇÃO", "MEIO - CONSIDERAÇÃO", "FUNDO - AÇÃO"]
            colors = ['#4A90E2', '#7ED321', '#F5A623']
            
            for i, (stage, color) in enumerate(zip(stages, colors)):
                # Calcula posição e tamanho
                y = 250 + i * 200
                width = 600 - i * 150
                x = 540 - width // 2
                height = 120
                
                # Desenha retângulo
                draw.rectangle([x, y, x + width, y + height], fill=color, outline='white', width=3)
                
                # Desenha texto
                bbox = draw.textbbox((0, 0), stage, font=font_text)
                text_width = bbox[2] - bbox[0]
                text_x = 540 - text_width // 2
                text_y = y + height // 2 - 15
                draw.text((text_x, text_y), stage, fill='white', font=font_text)
                
                # Desenha seta
                if i < len(stages) - 1:
                    arrow_y = y + height + 20
                    draw.polygon([
                        (540 - 20, arrow_y),
                        (540 + 20, arrow_y),
                        (540, arrow_y + 40)
                    ], fill='#666666')
            
            # Converte para base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
            
        except Exception as e:
            logger.error(f"❌ Erro crítico ao gerar gráfico mínimo: {e}")
            return ""
    
    async def generate_sales_funnel_chart(self, funnel_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera gráfico de funil de vendas usando Gemini/OpenRouter + fallback
        """
        logger.info("🎨 Gerando gráfico de funil de vendas...")
        
        # Cria prompt detalhado
        prompt = self._create_funnel_prompt(funnel_data)
        logger.info(f"📝 Prompt criado: {prompt[:200]}...")
        
        # Tenta gerar com Gemini Direct primeiro
        image_base64 = await self._generate_with_gemini_direct(prompt)
        
        if not image_base64:
            logger.info("🔄 Gemini não disponível, tentando OpenRouter...")
            # Fallback para OpenRouter
            image_base64 = await self._generate_with_openrouter(prompt)
        
        if not image_base64:
            logger.info("🔄 APIs não disponíveis, gerando gráfico de fallback...")
            # Fallback para geração local
            image_base64 = self._generate_fallback_funnel(funnel_data)
        
        if image_base64:
            resultado = {
                'success': True,
                'chart_base64': image_base64,
                'chart_data_url': f'data:image/png;base64,{image_base64}',
                'size': '1080x1080',
                'format': 'PNG',
                'funnel_stages': len(funnel_data.get('stages', self.default_funnel_stages)),
                'generated_at': datetime.now().isoformat(),
                'method': 'ai_generated' if image_base64 else 'fallback'
            }
            logger.info("✅ Gráfico de funil gerado com sucesso")
            return resultado
        else:
            logger.error("❌ Falha total ao gerar gráfico de funil")
            return {
                'success': False,
                'error': 'Falha ao gerar gráfico com todos os métodos disponíveis',
                'generated_at': datetime.now().isoformat()
            }
    
    def create_custom_funnel_data(self, segment: str, target_audience: str, 
                                 product: str = None) -> Dict[str, Any]:
        """
        Cria dados customizados do funil baseado no segmento e público-alvo
        """
        logger.info(f"🎯 Criando funil customizado para: {segment}")
        
        # Mapeia segmentos para estágios específicos
        if 'marketing' in segment.lower() or 'digital' in segment.lower():
            stages = [
                {
                    'name': 'TOPO DO FUNIL - AWARENESS',
                    'description': 'Atrair leads qualificados através de conteúdo relevante',
                    'content': 'Blog posts, SEO, redes sociais, webinars, e-books gratuitos',
                    'channels': 'Google Ads, Facebook Ads, LinkedIn, YouTube',
                    'color': '#4A90E2'
                },
                {
                    'name': 'MEIO DO FUNIL - CONSIDERATION',
                    'description': 'Nutrir leads e demonstrar valor da solução',
                    'content': 'Email marketing, demos, cases de sucesso, trials gratuitos',
                    'channels': 'Email sequences, retargeting, inside sales',
                    'color': '#7ED321'
                },
                {
                    'name': 'FUNDO DO FUNIL - DECISION',
                    'description': 'Converter leads em clientes pagantes',
                    'content': 'Propostas personalizadas, negociação, fechamento',
                    'channels': 'Sales calls, contratos, onboarding',
                    'color': '#F5A623'
                }
            ]
        elif 'ecommerce' in segment.lower() or 'loja' in segment.lower():
            stages = [
                {
                    'name': 'DESCOBERTA - AWARENESS',
                    'description': 'Atrair visitantes para a loja online',
                    'content': 'SEO, anúncios pagos, influenciadores, conteúdo viral',
                    'channels': 'Google Shopping, Facebook Ads, Instagram, TikTok',
                    'color': '#4A90E2'
                },
                {
                    'name': 'INTERESSE - CONSIDERATION',
                    'description': 'Engajar visitantes e gerar interesse nos produtos',
                    'content': 'Páginas de produto, reviews, comparações, wishlist',
                    'channels': 'Email marketing, push notifications, remarketing',
                    'color': '#7ED321'
                },
                {
                    'name': 'COMPRA - PURCHASE',
                    'description': 'Converter visitantes em compradores',
                    'content': 'Checkout otimizado, ofertas especiais, urgência',
                    'channels': 'Carrinho abandonado, cupons, frete grátis',
                    'color': '#F5A623'
                },
                {
                    'name': 'RETENÇÃO - LOYALTY',
                    'description': 'Fidelizar clientes e gerar recompras',
                    'content': 'Programa de fidelidade, upsell, cross-sell',
                    'channels': 'Email pós-venda, SMS, programa VIP',
                    'color': '#D0021B'
                }
            ]
        else:
            # Funil genérico para outros segmentos
            stages = self.default_funnel_stages
        
        return {
            'segment': segment,
            'target_audience': target_audience,
            'product': product,
            'stages': stages,
            'created_at': datetime.now().isoformat()
        }

# Função de conveniência para uso externo
async def generate_sales_funnel_chart(funnel_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função de conveniência para gerar gráfico de funil
    """
    async with SalesFunnelChartGenerator() as generator:
        return await generator.generate_sales_funnel_chart(funnel_data)

# Instância global para uso direto
sales_funnel_generator = SalesFunnelChartGenerator()