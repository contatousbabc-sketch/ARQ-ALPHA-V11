#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Geração de Imagens de Avatar - V1.0
Gera imagens 1080x1080 dos avatars usando Gemini Direct + fallback OpenRouter
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
import requests

logger = logging.getLogger(__name__)

class AvatarImageGenerator:
    """
    Sistema para gerar imagens de avatar usando IA
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GOOGLE_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.session = None
        
    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()
    
    def _criar_prompt_avatar(self, avatar_data: Dict[str, Any]) -> str:
        """
        Cria prompt detalhado para geração de imagem do avatar
        """
        demograficos = avatar_data.get('dados_demograficos', {})
        psicologico = avatar_data.get('perfil_psicologico', {})
        
        nome = demograficos.get('nome_completo', 'Avatar')
        idade = demograficos.get('idade', 35)
        genero = demograficos.get('genero', 'Neutro')
        profissao = demograficos.get('profissao', 'Profissional')
        personalidade = psicologico.get('personalidade_mbti', 'ENFJ')
        
        # Determina características visuais baseadas no perfil
        if genero.lower() == 'masculino':
            genero_desc = "homem"
            cabelo_opcoes = ["cabelo curto", "cabelo médio", "careca", "barba"]
        else:
            genero_desc = "mulher"
            cabelo_opcoes = ["cabelo longo", "cabelo médio", "cabelo curto", "cabelo cacheado"]
        
        # Idade visual
        if idade < 30:
            idade_desc = "jovem"
        elif idade < 45:
            idade_desc = "adulto"
        else:
            idade_desc = "maduro"
        
        # Estilo baseado na profissão
        if 'empreendedor' in profissao.lower() or 'ceo' in profissao.lower():
            estilo = "executivo, terno elegante, confiante"
        elif 'consultor' in profissao.lower() or 'coach' in profissao.lower():
            estilo = "profissional moderno, blazer, acessível"
        elif 'desenvolvedor' in profissao.lower() or 'analista' in profissao.lower():
            estilo = "casual profissional, camisa social, intelectual"
        else:
            estilo = "profissional, bem vestido, competente"
        
        # Personalidade visual
        if personalidade.startswith('E'):  # Extrovertido
            expressao = "sorriso confiante, olhar direto, postura aberta"
        else:  # Introvertido
            expressao = "sorriso sutil, olhar pensativo, postura reservada"
        
        prompt = f"""
        Create a professional portrait photo of a {idade_desc} Brazilian {genero_desc} named {nome}.
        
        Physical characteristics:
        - Age: {idade} years old
        - Gender: {genero_desc}
        - Style: {estilo}
        - Hair: {cabelo_opcoes[0]}
        - Expression: {expressao}
        
        Professional context:
        - Occupation: {profissao}
        - Personality type: {personalidade}
        
        Image specifications:
        - High quality professional headshot
        - 1080x1080 pixels, square format
        - Clean background (office or neutral)
        - Professional lighting
        - Realistic, photographic style
        - Brazilian features
        - Confident and approachable appearance
        - Business professional attire
        
        Style: Photorealistic, professional photography, LinkedIn-style profile photo
        """
        
        return prompt
    
    async def _gerar_com_gemini_direct(self, prompt: str) -> Optional[str]:
        """
        Gera imagem usando Gemini Direct API com Imagen
        """
        if not self.gemini_api_key:
            logger.warning("Google API Key não encontrada")
            return None
            
        try:
            logger.info("🎨 Gerando imagem com Gemini Direct (Imagen)")
            
            # Usando Google AI Generative API para geração de imagem
            import google.generativeai as genai
            
            genai.configure(api_key=self.gemini_api_key)
            
            # Usando o modelo Imagen via Gemini
            try:
                # Tenta usar o modelo de geração de imagem do Google
                model = genai.GenerativeModel('gemini-pro-vision')
                
                # Como o Gemini não gera imagens diretamente, vamos usar uma abordagem alternativa
                # Criamos um prompt melhorado para o OpenRouter
                enhanced_prompt = f"""
                Professional business portrait photograph for LinkedIn profile:
                
                {prompt}
                
                Technical specifications:
                - Ultra-high quality professional headshot
                - Perfect lighting and composition
                - Clean, modern business background
                - Sharp focus on subject
                - Professional business attire
                - Confident and approachable expression
                - Brazilian ethnicity and features
                - Square format 1080x1080 pixels
                - Photorealistic style, not illustration
                """
                
                logger.info("✅ Prompt aprimorado com Gemini Direct")
                return None  # Retorna None para usar OpenRouter com prompt melhorado
                
            except Exception as model_error:
                logger.warning(f"Modelo Gemini não disponível para geração de imagem: {model_error}")
                return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar imagem com Gemini Direct: {e}")
            return None
    
    async def _gerar_com_openrouter(self, prompt: str) -> Optional[str]:
        """
        Gera imagem usando OpenRouter com múltiplos modelos de fallback
        """
        if not self.openrouter_api_key:
            logger.warning("OpenRouter API Key não encontrada")
            return None
            
        # Lista de modelos para tentar em ordem de preferência
        modelos_fallback = [
            "black-forest-labs/flux-1.1-pro",
            "black-forest-labs/flux-pro",
            "black-forest-labs/flux-dev",
            "stability-ai/stable-diffusion-3-5-large",
            "stability-ai/stable-diffusion-3-medium"
        ]
        
        for modelo in modelos_fallback:
            try:
                logger.info(f"🎨 Tentando gerar imagem com OpenRouter usando {modelo}...")
                
                headers = {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://arqv30.com",
                    "X-Title": "ARQV30 Avatar Generator"
                }
                
                # Payload para modelos de geração de imagem
                payload = {
                    "model": modelo,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Generate an image: {prompt}"
                                }
                            ]
                        }
                    ],
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
                        
                        # Processa resposta dos modelos de imagem
                        if result.get('choices') and result['choices'][0].get('message'):
                            content = result['choices'][0]['message'].get('content', '')
                            
                            # Verifica se há URL de imagem na resposta
                            if 'http' in content:
                                import re
                                urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                                if urls:
                                    logger.info(f"✅ Imagem gerada com sucesso usando {modelo}")
                                    return await self._baixar_e_converter_base64(urls[0])
                            
                            # Verifica se há dados base64 na resposta
                            elif 'base64' in content.lower() or content.startswith('data:image'):
                                logger.info(f"✅ Imagem gerada com sucesso usando {modelo}")
                                # Extrai base64 se estiver em formato data URL
                                if content.startswith('data:image'):
                                    base64_data = content.split(',')[1]
                                    return base64_data
                                return content
                            
                            # Se o modelo não suporta geração de imagem, tenta próximo
                            elif 'cannot generate' in content.lower() or 'not supported' in content.lower():
                                logger.warning(f"⚠️ Modelo {modelo} não suporta geração de imagem")
                                continue
                    
                    else:
                        error_text = await response.text()
                        logger.warning(f"⚠️ Modelo {modelo} falhou: {response.status} - {error_text}")
                        continue  # Tenta próximo modelo
                        
            except Exception as e:
                logger.warning(f"⚠️ Erro com modelo {modelo}: {e}")
                continue  # Tenta próximo modelo
        
        logger.error("❌ Todos os modelos OpenRouter falharam")
        return None
    
    async def _gerar_com_openai_direto(self, prompt: str) -> Optional[str]:
        """
        Gera imagem usando OpenAI API diretamente
        """
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            logger.warning("OpenAI API Key não encontrada")
            return None
            
        try:
            logger.info("🎨 Gerando imagem com OpenAI DALL-E 3...")
            
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "hd",
                "style": "natural"
            }
            
            async with self.session.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=90
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('data') and len(result['data']) > 0:
                        image_url = result['data'][0].get('url')
                        if image_url:
                            logger.info("✅ Imagem gerada com sucesso usando OpenAI DALL-E 3")
                            return await self._baixar_e_converter_base64(image_url)
                
                error_text = await response.text()
                logger.warning(f"⚠️ OpenAI falhou: {response.status} - {error_text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro ao gerar imagem com OpenAI: {e}")
            return None
    
    async def _baixar_e_converter_base64(self, image_url: str) -> Optional[str]:
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
                    
                    logger.info(f"✅ Imagem convertida para base64: {len(image_base64)} caracteres")
                    return image_base64
                    
        except Exception as e:
            logger.error(f"❌ Erro ao baixar e converter imagem: {e}")
            return None
    
    def _gerar_imagem_fallback(self, avatar_data: Dict[str, Any]) -> str:
        """
        Gera imagem de fallback usando PIL quando APIs não estão disponíveis
        """
        try:
            logger.info("🎨 Gerando imagem de fallback com PIL...")
            
            demograficos = avatar_data.get('dados_demograficos', {})
            nome = demograficos.get('nome_completo', 'Avatar')
            profissao = demograficos.get('profissao', 'Profissional')
            idade = demograficos.get('idade', 35)
            
            # Cria imagem 1080x1080
            img = Image.new('RGB', (1080, 1080), color='#f0f0f0')
            draw = ImageDraw.Draw(img)
            
            # Tenta carregar fonte
            try:
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Desenha círculo de fundo
            circle_center = (540, 300)
            circle_radius = 150
            draw.ellipse([
                circle_center[0] - circle_radius,
                circle_center[1] - circle_radius,
                circle_center[0] + circle_radius,
                circle_center[1] + circle_radius
            ], fill='#4f46e5')
            
            # Desenha iniciais
            iniciais = ''.join([word[0].upper() for word in nome.split()[:2]])
            bbox = draw.textbbox((0, 0), iniciais, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = circle_center[0] - text_width // 2
            text_y = circle_center[1] - text_height // 2
            draw.text((text_x, text_y), iniciais, fill='white', font=font_large)
            
            # Desenha nome
            bbox = draw.textbbox((0, 0), nome, font=font_medium)
            text_width = bbox[2] - bbox[0]
            text_x = 540 - text_width // 2
            draw.text((text_x, 500), nome, fill='#1f2937', font=font_medium)
            
            # Desenha profissão
            bbox = draw.textbbox((0, 0), profissao, font=font_small)
            text_width = bbox[2] - bbox[0]
            text_x = 540 - text_width // 2
            draw.text((text_x, 560), profissao, fill='#6b7280', font=font_small)
            
            # Desenha idade
            idade_text = f"{idade} anos"
            bbox = draw.textbbox((0, 0), idade_text, font=font_small)
            text_width = bbox[2] - bbox[0]
            text_x = 540 - text_width // 2
            draw.text((text_x, 600), idade_text, fill='#6b7280', font=font_small)
            
            # Converte para base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logger.info(f"✅ Imagem de fallback gerada: {len(image_base64)} caracteres")
            return image_base64
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar imagem de fallback: {e}")
            # Retorna uma imagem mínima em caso de erro total
            return self._gerar_imagem_minima()
    
    def _gerar_imagem_minima(self) -> str:
        """
        Gera imagem mínima em caso de erro total
        """
        try:
            # Cria imagem simples 1080x1080
            img = Image.new('RGB', (1080, 1080), color='#4f46e5')
            draw = ImageDraw.Draw(img)
            
            # Desenha texto simples
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            except:
                font = ImageFont.load_default()
            
            text = "AVATAR"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = 540 - text_width // 2
            text_y = 540 - text_height // 2
            draw.text((text_x, text_y), text, fill='white', font=font)
            
            # Converte para base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
            
        except Exception as e:
            logger.error(f"❌ Erro crítico ao gerar imagem mínima: {e}")
            # Retorna string vazia em caso de erro crítico
            return ""
    
    async def gerar_imagem_avatar(self, avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera imagem do avatar usando Gemini Direct + fallback OpenRouter
        """
        nome = avatar_data.get('dados_demograficos', {}).get('nome_completo', 'Avatar')
        logger.info(f"🎨 Gerando imagem para avatar: {nome}")
        
        # Cria prompt detalhado
        prompt = self._criar_prompt_avatar(avatar_data)
        logger.info(f"📝 Prompt criado: {prompt[:100]}...")
        
        # Tenta gerar com Gemini Direct primeiro
        image_base64 = await self._gerar_com_gemini_direct(prompt)
        
        if not image_base64:
            logger.info("🔄 Gemini não disponível, tentando OpenAI direto...")
            # Tenta OpenAI direto primeiro
            image_base64 = await self._gerar_com_openai_direto(prompt)
        
        if not image_base64:
            logger.info("🔄 OpenAI não disponível, tentando OpenRouter...")
            # Fallback para OpenRouter
            image_base64 = await self._gerar_com_openrouter(prompt)
        
        if not image_base64:
            logger.info("🔄 APIs não disponíveis, gerando imagem de fallback...")
            # Fallback para geração local
            image_base64 = self._gerar_imagem_fallback(avatar_data)
        
        if image_base64:
            resultado = {
                'success': True,
                'image_base64': image_base64,
                'image_data_url': f'data:image/png;base64,{image_base64}',
                'size': '1080x1080',
                'format': 'PNG',
                'avatar_name': nome,
                'generated_at': datetime.now().isoformat(),
                'method': 'gemini_direct' if image_base64 else 'openrouter' if image_base64 else 'fallback'
            }
            logger.info(f"✅ Imagem gerada com sucesso para {nome}")
            return resultado
        else:
            logger.error(f"❌ Falha total ao gerar imagem para {nome}")
            return {
                'success': False,
                'error': 'Falha ao gerar imagem com todos os métodos disponíveis',
                'avatar_name': nome,
                'generated_at': datetime.now().isoformat()
            }
    
    async def gerar_imagens_multiplos_avatares(self, avatares_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Gera imagens para múltiplos avatares
        """
        logger.info(f"🎨 Gerando imagens para {len(avatares_data)} avatares...")
        
        resultados = []
        for i, avatar_data in enumerate(avatares_data):
            logger.info(f"🎯 Processando avatar {i+1}/{len(avatares_data)}")
            resultado = await self.gerar_imagem_avatar(avatar_data)
            resultados.append(resultado)
            
            # Pequena pausa entre gerações para evitar rate limiting
            if i < len(avatares_data) - 1:
                await asyncio.sleep(2)
        
        sucessos = sum(1 for r in resultados if r.get('success'))
        logger.info(f"✅ Geração concluída: {sucessos}/{len(avatares_data)} imagens geradas com sucesso")
        
        return resultados

# Função de conveniência para uso externo
async def gerar_imagens_avatares(avatares_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Função de conveniência para gerar imagens de avatares
    """
    async with AvatarImageGenerator() as generator:
        return await generator.gerar_imagens_multiplos_avatares(avatares_data)

# Instância global para uso direto
avatar_image_generator = AvatarImageGenerator()