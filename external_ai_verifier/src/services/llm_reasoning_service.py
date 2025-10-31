#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - External LLM Reasoning Service
Serviço de raciocínio com LLMs para análise aprofundada
COM ROTAÇÃO DE API KEYS
"""

import logging
import os
import time
import random
from typing import Dict, Any, Optional, List

# Try to import LLM clients, fallback gracefully
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)

class ExternalLLMReasoningService:
    """Serviço de raciocínio com LLMs externo independente com rotação de API keys"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa o serviço de LLM"""
        self.config = config.get('llm_reasoning', {})
        self.enabled = self.config.get('enabled', True)
        self.provider = self.config.get('provider', 'gemini').lower()
        self.model = self.config.get('model', 'gemini-2.0-flash-exp')
        self.max_tokens = self.config.get('max_tokens', 1000)
        self.temperature = self.config.get('temperature', 0.3)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.6)
        
        # Parâmetros para retry de cota
        self.max_retries_on_quota_error = self.config.get('max_retries_on_quota_error', 3)
        self.base_retry_delay = self.config.get('base_retry_delay', 1.0)
        self.max_retry_delay = self.config.get('max_retry_delay', 60.0)
        
        # ✅ NOVO: Sistema de rotação de API keys
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        self.key_failure_count = {}  # Rastreia falhas por chave
        self.max_key_failures = 3  # Máximo de falhas antes de desabilitar chave
        
        self.client = None
        self._initialize_llm_client()
        
        logger.info(f"✅ External LLM Reasoning Service inicializado (Provider: {self.provider}, Keys disponíveis: {len(self.api_keys)}, Available: {self.client is not None})")
    
    def _load_api_keys(self) -> List[str]:
        """Carrega todas as API keys disponíveis do ambiente"""
        keys = []
        
        if self.provider == 'gemini':
            # Tenta carregar GEMINI_API_KEY e GEMINI_API_KEY_1, GEMINI_API_KEY_2, etc.
            base_key = os.getenv('GEMINI_API_KEY')
            if base_key:
                keys.append(base_key)
            
            # Tenta carregar chaves numeradas
            index = 1
            while True:
                key = os.getenv(f'GEMINI_API_KEY_{index}')
                if key:
                    keys.append(key)
                    index += 1
                else:
                    break
                    
        elif self.provider == 'openai':
            base_key = os.getenv('OPENAI_API_KEY')
            if base_key:
                keys.append(base_key)
            
            index = 1
            while True:
                key = os.getenv(f'OPENAI_API_KEY_{index}')
                if key:
                    keys.append(key)
                    index += 1
                else:
                    break
        
        # Remove duplicatas mantendo a ordem
        keys = list(dict.fromkeys(keys))
        
        if keys:
            logger.info(f"🔑 {len(keys)} API key(s) carregadas para {self.provider}")
        else:
            logger.warning(f"⚠️ Nenhuma API key encontrada para {self.provider}")
        
        return keys
    
    def _get_next_api_key(self) -> Optional[str]:
        """Obtém a próxima API key disponível na rotação"""
        if not self.api_keys:
            return None
        
        # Filtra chaves que não atingiram o limite de falhas
        available_keys = [
            (i, key) for i, key in enumerate(self.api_keys)
            if self.key_failure_count.get(i, 0) < self.max_key_failures
        ]
        
        if not available_keys:
            logger.error("❌ Todas as API keys atingiram o limite de falhas")
            return None
        
        # Rotaciona para a próxima chave disponível
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        
        # Garante que a chave selecionada está disponível
        while self.key_failure_count.get(self.current_key_index, 0) >= self.max_key_failures:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        
        selected_key = self.api_keys[self.current_key_index]
        logger.debug(f"🔄 Usando API key #{self.current_key_index + 1} de {len(self.api_keys)}")
        
        return selected_key
    
    def _mark_key_failure(self):
        """Marca uma falha na chave atual"""
        self.key_failure_count[self.current_key_index] = \
            self.key_failure_count.get(self.current_key_index, 0) + 1
        
        failures = self.key_failure_count[self.current_key_index]
        logger.warning(f"⚠️ API key #{self.current_key_index + 1} falhou {failures}/{self.max_key_failures} vezes")
        
        if failures >= self.max_key_failures:
            logger.error(f"❌ API key #{self.current_key_index + 1} desabilitada (muitas falhas)")
    
    def _reset_key_failure(self):
        """Reseta contador de falhas da chave atual (sucesso)"""
        if self.current_key_index in self.key_failure_count:
            self.key_failure_count[self.current_key_index] = 0
    
    def _initialize_llm_client(self):
        """Inicializa o cliente LLM baseado no provider configurado"""
        try:
            if not self.api_keys:
                logger.warning(f"⚠️ Nenhuma API key disponível para {self.provider}")
                return
            
            if self.provider == 'gemini' and GEMINI_AVAILABLE:
                api_key = self._get_next_api_key()
                if api_key:
                    genai.configure(api_key=api_key)
                    self.client = genai.GenerativeModel(self.model)
                    logger.info(f"✅ Gemini client inicializado: {self.model} (Key #{self.current_key_index + 1})")
                    
            elif self.provider == 'openai' and OPENAI_AVAILABLE:
                api_key = self._get_next_api_key()
                if api_key:
                    openai.api_key = api_key
                    self.client = openai
                    logger.info(f"✅ OpenAI client inicializado: {self.model} (Key #{self.current_key_index + 1})")
            else:
                logger.warning(f"⚠️ Provider '{self.provider}' não disponível ou não configurado")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar LLM client: {e}")
            self.client = None
    
    def _rotate_to_next_key(self) -> bool:
        """Rotaciona para a próxima chave disponível"""
        try:
            next_key = self._get_next_api_key()
            if not next_key:
                return False
            
            if self.provider == 'gemini' and GEMINI_AVAILABLE:
                genai.configure(api_key=next_key)
                self.client = genai.GenerativeModel(self.model)
                logger.info(f"🔄 Rotacionado para API key #{self.current_key_index + 1}")
                return True
                
            elif self.provider == 'openai' and OPENAI_AVAILABLE:
                openai.api_key = next_key
                self.client = openai
                logger.info(f"🔄 Rotacionado para API key #{self.current_key_index + 1}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao rotacionar API key: {e}")
            return False
    
    def analyze_with_llm(self, text: str, context: str = "") -> Dict[str, Any]:
        """
        Analisa o texto com LLM para raciocínio aprofundado
        
        Args:
            text (str): Texto para análise
            context (str): Contexto adicional
            
        Returns:
            Dict[str, Any]: Resultados da análise LLM
        """
        if not self.enabled or not self.client or not text or not text.strip():
            return self._get_default_result()
        
        try:
            # Prepare prompt for analysis
            prompt = self._create_analysis_prompt(text, context)
            
            # Get LLM response
            if self.provider == 'gemini':
                response = self._analyze_with_gemini_with_retry(prompt)
            elif self.provider == 'openai':
                response = self._analyze_with_openai(prompt)
            else:
                return self._get_default_result()
            
            # Parse and structure response
            analysis_result = self._parse_llm_response(response, text)
            
            # Marca sucesso da chave
            self._reset_key_failure()
            
            logger.debug(f"LLM analysis completed: confidence={analysis_result.get('llm_confidence', 0):.3f}")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Erro na análise LLM: {e}")
            return self._get_default_result()
    
    def _analyze_with_gemini_with_retry(self, prompt: str) -> str:
        """Análise com Gemini com lógica de retry e rotação de keys"""
        last_exception = None
        delay = self.base_retry_delay
        keys_tried = set()

        for attempt in range(self.max_retries_on_quota_error + 1):
            try:
                response = self.client.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=self.max_tokens,
                        temperature=self.temperature
                    )
                )
                return response.text
                
            except Exception as e:
                last_exception = e
                error_message = str(e).lower()
                
                # Verifica se é um erro de cota
                if "429" in error_message or "quota" in error_message or "rate limit" in error_message:
                    keys_tried.add(self.current_key_index)
                    
                    # Marca falha da chave atual
                    self._mark_key_failure()
                    
                    # Tenta rotacionar para próxima chave se ainda há tentativas
                    if attempt < self.max_retries_on_quota_error:
                        if len(keys_tried) < len(self.api_keys):
                            logger.warning(f"Erro de cota no Gemini (tentativa {attempt + 1}), rotacionando para próxima API key...")
                            
                            if self._rotate_to_next_key():
                                # Pequeno delay antes de tentar com nova chave
                                time.sleep(1.0)
                                continue
                            else:
                                logger.error("❌ Não há mais API keys disponíveis para rotação")
                                break
                        else:
                            logger.warning(f"Erro de cota no Gemini (tentativa {attempt + 1}), aguardando {delay:.1f}s...")
                            time.sleep(delay)
                            delay = min(self.base_retry_delay * (2 ** attempt) + random.uniform(0, 1), self.max_retry_delay)
                    else:
                        logger.error(f"Limite de tentativas excedido para erro de cota no Gemini")
                        break
                else:
                    # Se não for erro de cota, não faz retry
                    logger.error(f"Erro não relacionado a cota no Gemini: {e}")
                    raise

        # Se chegou aqui, todas as tentativas falharam
        if last_exception:
            raise last_exception

        raise Exception("Falha ao chamar Gemini após tentativas de retry para cota excedida.")

    def _create_analysis_prompt(self, text: str, context: str = "") -> str:
        """Cria o prompt para análise LLM"""
        base_prompt = f"""Analise o seguinte texto de forma crítica e objetiva:

TEXTO PARA ANÁLISE:
"{text}"

{f'CONTEXTO ADICIONAL: {context}' if context else ''}

Por favor, forneça uma análise estruturada considerando:

1. QUALIDADE DO CONTEÚDO (0-10):
   - Clareza e coerência
   - Fundamentação das afirmações
   - Presença de evidências

2. CONFIABILIDADE (0-10):
   - Presença de fontes ou referências
   - Linguagem objetiva vs. subjetiva
   - Sinais de credibilidade

3. VIÉS/PARCIALIDADE (0-10, onde 0=neutro, 10=muito tendencioso):
   - Linguagem emotiva ou manipulativa
   - Apresentação unilateral de fatos
   - Generalizações ou estereótipos

4. RISCO DE DESINFORMAÇÃO (0-10):
   - Afirmações sem evidências
   - Padrões típicos de desinformação
   - Inconsistências factuais

Forneça sua resposta no seguinte formato:
QUALIDADE: [pontuação]/10 - [breve justificativa]
CONFIABILIDADE: [pontuação]/10 - [breve justificativa]  
VIÉS: [pontuação]/10 - [breve justificativa]
DESINFORMAÇÃO: [pontuação]/10 - [breve justificativa]
RECOMENDAÇÃO: [APROVAR/REJEITAR/REVISÃO_MANUAL] - [razão principal]
CONFIANÇA_ANÁLISE: [0-100]% - [justificativa da confiança]"""

        return base_prompt
    
    def _analyze_with_openai(self, prompt: str) -> str:
        """Análise com OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro no OpenAI: {e}")
            raise
    
    def _parse_llm_response(self, response: str, original_text: str) -> Dict[str, Any]:
        """Parse da resposta LLM para formato estruturado"""
        try:
            import re
            
            result = {
                'llm_response': response,
                'quality_score': 5.0,
                'reliability_score': 5.0,
                'bias_score': 5.0,
                'disinformation_score': 5.0,
                'llm_recommendation': 'REVISÃO_MANUAL',
                'llm_confidence': 0.5,
                'analysis_reasoning': '',
                'provider': self.provider,
                'model': self.model,
                'api_key_used': self.current_key_index + 1
            }
            
            patterns = {
                'quality_score': r'QUALIDADE:\s*([0-9]+(?:\.[0-9]+)?)',
                'reliability_score': r'CONFIABILIDADE:\s*([0-9]+(?:\.[0-9]+)?)',
                'bias_score': r'VIÉS:\s*([0-9]+(?:\.[0-9]+)?)',
                'disinformation_score': r'DESINFORMAÇÃO:\s*([0-9]+(?:\.[0-9]+)?)',
                'llm_recommendation': r'RECOMENDAÇÃO:\s*(APROVAR|REJEITAR|REVISÃO_MANUAL)',
                'llm_confidence': r'CONFIANÇA_ANÁLISE:\s*([0-9]+)%?'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    if key == 'llm_confidence':
                        result[key] = min(float(match.group(1)) / 100.0, 1.0)
                    elif key == 'llm_recommendation':
                        result[key] = match.group(1).upper()
                    else:
                        score = min(float(match.group(1)) / 10.0, 1.0)
                        result[key] = score
            
            reasoning_parts = []
            for line in response.split('\n'):
                if ' - ' in line and any(keyword in line.upper() for keyword in ['QUALIDADE', 'CONFIABILIDADE', 'VIÉS', 'DESINFORMAÇÃO']):
                    reasoning_parts.append(line.split(' - ', 1)[-1])
            
            result['analysis_reasoning'] = ' | '.join(reasoning_parts)
            result['llm_confidence'] = self._validate_llm_confidence(result)
            
            return result
            
        except Exception as e:
            logger.warning(f"Erro no parsing da resposta LLM: {e}")
            return {
                'llm_response': response,
                'quality_score': 0.5,
                'reliability_score': 0.5,
                'bias_score': 0.5,
                'disinformation_score': 0.5,
                'llm_recommendation': 'REVISÃO_MANUAL',
                'llm_confidence': 0.3,
                'analysis_reasoning': 'Erro no parsing da resposta',
                'provider': self.provider,
                'model': self.model,
                'api_key_used': self.current_key_index + 1
            }
    
    def _validate_llm_confidence(self, result: Dict[str, Any]) -> float:
        """Valida e ajusta a confiança baseada na consistência da análise"""
        try:
            quality = result.get('quality_score', 0.5)
            reliability = result.get('reliability_score', 0.5) 
            bias = result.get('bias_score', 0.5)
            disinformation = result.get('disinformation_score', 0.5)
            recommendation = result.get('llm_recommendation', 'REVISÃO_MANUAL')
            base_confidence = result.get('llm_confidence', 0.5)
            
            avg_positive_scores = (quality + reliability) / 2.0
            avg_negative_scores = (bias + disinformation) / 2.0
            
            expected_approval = avg_positive_scores > 0.7 and avg_negative_scores < 0.4
            expected_rejection = avg_positive_scores < 0.4 or avg_negative_scores > 0.6
            
            consistency_bonus = 0.0
            if recommendation == 'APROVAR' and expected_approval:
                consistency_bonus = 0.1
            elif recommendation == 'REJEITAR' and expected_rejection:
                consistency_bonus = 0.1
            elif recommendation == 'REVISÃO_MANUAL':
                consistency_bonus = 0.05
            
            adjusted_confidence = min(base_confidence + consistency_bonus, 1.0)
            adjusted_confidence = max(adjusted_confidence, 0.1)
            
            return adjusted_confidence
            
        except Exception as e:
            logger.warning(f"Erro na validação de confiança: {e}")
            return 0.5
    
    def _get_default_result(self) -> Dict[str, Any]:
        """Retorna resultado padrão quando LLM não está disponível"""
        return {
            'llm_response': 'LLM não disponível ou configurado',
            'quality_score': 0.5,
            'reliability_score': 0.5,
            'bias_score': 0.5,
            'disinformation_score': 0.5,
            'llm_recommendation': 'REVISÃO_MANUAL',
            'llm_confidence': 0.1,
            'analysis_reasoning': 'Análise LLM não disponível',
            'provider': self.provider,
            'model': self.model,
            'api_key_used': 0
        }
    
    def get_keys_status(self) -> Dict[str, Any]:
        """Retorna status das API keys"""
        return {
            'total_keys': len(self.api_keys),
            'current_key_index': self.current_key_index + 1,
            'key_failures': {
                f"key_{i+1}": self.key_failure_count.get(i, 0)
                for i in range(len(self.api_keys))
            },
            'available_keys': len([
                i for i in range(len(self.api_keys))
                if self.key_failure_count.get(i, 0) < self.max_key_failures
            ])
        }