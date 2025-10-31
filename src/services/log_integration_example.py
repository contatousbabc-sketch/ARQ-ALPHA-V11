#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Integração do Log Local Atual com o Sistema ARQ-ALPHA-V9
Demonstra como usar o sistema de log em tempo real nas rotas e serviços
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any

# Importa o sistema de log
from services.log_local_atual import get_log_local, create_session_log, log_info, log_error

def exemplo_integracao_workflow():
    """
    Exemplo de como integrar o log local com o workflow do ARQ-ALPHA-V9
    """
    
    print("🔗 EXEMPLO DE INTEGRAÇÃO - Log Local Atual com ARQ-ALPHA-V9")
    print("=" * 70)
    
    # Simula uma sessão real
    session_id = f"session_{int(datetime.now().timestamp())}"
    
    # 1. CRIA LOG DA SESSÃO
    log_path = create_session_log(session_id, {
        'tipo_workflow': 'enhanced_workflow',
        'usuario': 'sistema',
        'timestamp_inicio': datetime.now().isoformat(),
        'versao_app': 'ARQ-ALPHA-V9'
    })
    
    print(f"📝 Log criado: {os.path.basename(log_path)}")
    
    # 2. SIMULA ETAPA 1 - COLETA DE DADOS
    log_system = get_log_local()
    
    log_system.log_etapa_iniciada(session_id, 1, "Coleta de Dados Web", {
        'fontes': ['google', 'bing', 'duckduckgo'],
        'query': 'análise de mercado',
        'max_results': 50
    })
    
    # Simula processamento
    import time
    time.sleep(0.5)
    
    # Log de código executado
    log_system.log_codigo_executado(
        session_id, "COLETA_DADOS", 
        """
# Código de coleta de dados
search_engines = ['google', 'bing', 'duckduckgo']
results = []
for engine in search_engines:
    engine_results = search_web(engine, query, max_results=50)
    results.extend(engine_results)
    log_info(session_id, 'COLETA_DADOS', f'Coletados {len(engine_results)} resultados de {engine}')
""",
        resultado={'total_coletado': 150, 'fontes_ativas': 3}
    )
    
    # Log de API calls
    log_system.log_api_call(
        session_id, "COLETA_DADOS", "google_search_api",
        parametros={'q': 'análise de mercado', 'num': 50},
        tempo_resposta=1.2
    )
    
    log_system.log_api_call(
        session_id, "COLETA_DADOS", "bing_search_api",
        parametros={'q': 'análise de mercado', 'count': 50},
        tempo_resposta=0.8
    )
    
    # Finaliza etapa 1
    log_system.log_etapa_concluida(session_id, 1, "Coleta de Dados Web", {
        'total_resultados': 150,
        'fontes_processadas': 3,
        'tempo_total': 2.5
    }, tempo_execucao=2.5)
    
    # 3. SIMULA ETAPA 2 - SÍNTESE
    log_system.log_etapa_iniciada(session_id, 2, "Síntese e Análise", {
        'engine': 'enhanced_synthesis_engine',
        'items_para_processar': 150
    })
    
    time.sleep(0.3)
    
    # Log de processamento de arquivo
    log_system.log_arquivo_processado(
        session_id, "SYNTHESIS", 
        f"relatorios_intermediarios/workflow/{session_id}/etapa1_concluida.json",
        "LEITURA", {'items_carregados': 150}
    )
    
    # Log de código de síntese
    log_system.log_codigo_executado(
        session_id, "SYNTHESIS",
        """
# Processamento de síntese
synthesis_engine = EnhancedSynthesisEngine()
consolidated_data = synthesis_engine.process_items(items)
analysis_result = synthesis_engine.generate_analysis(consolidated_data)
""",
        resultado={'items_processados': 150, 'analise_gerada': True}
    )
    
    # Finaliza etapa 2
    log_system.log_etapa_concluida(session_id, 2, "Síntese e Análise", {
        'arquivo_gerado': f'sintese_deep_market_analysis.json',
        'qualidade_analise': 0.95
    }, tempo_execucao=5.2)
    
    # 4. SIMULA ETAPA 3 - VERIFICAÇÃO AI
    log_system.log_etapa_iniciada(session_id, 3, "Verificação AI Externa", {
        'modulo': 'external_ai_verifier',
        'items_para_verificar': 150
    })
    
    time.sleep(0.2)
    
    # Log de integração com módulo externo
    log_system.add_log_entry(
        session_id, "AI_VERIFIER", "INFO",
        "🤖 Iniciando verificação com External AI Verifier",
        extra_data={
            'modulo_path': 'external_ai_verifier/src',
            'config_loaded': True,
            'apis_disponveis': ['gemini', 'openai']
        }
    )
    
    # Log de API AI
    log_system.log_api_call(
        session_id, "AI_VERIFIER", "gemini_api",
        parametros={'model': 'gemini-2.0-flash-exp', 'items': 150},
        tempo_resposta=8.5
    )
    
    # Log de arquivo gerado
    log_system.log_arquivo_processado(
        session_id, "AI_VERIFIER",
        f"relatorios_intermediarios/workflow/{session_id}/verificacao_ai_resultado.json",
        "ESCRITA", {
            'items_verificados': 150,
            'bias_detectado': 5,
            'confiabilidade_media': 0.87
        }
    )
    
    # Finaliza etapa 3
    log_system.log_etapa_concluida(session_id, 3, "Verificação AI Externa", {
        'items_verificados': 150,
        'bias_detectado': 5,
        'desinformacao_detectada': 2,
        'confiabilidade_media': 0.87
    }, tempo_execucao=9.1)
    
    # 5. FINALIZA SESSÃO
    log_system.finalize_session_log(session_id, {
        'status_final': 'SUCESSO',
        'etapas_concluidas': 3,
        'tempo_total': '17.8s',
        'items_processados': 150,
        'qualidade_final': 0.91,
        'arquivos_gerados': 3
    })
    
    print(f"✅ Exemplo de integração concluído!")
    print(f"📁 Arquivo de log: {os.path.basename(log_path)}")
    print(f"📊 Sessão: {session_id}")

def exemplo_integracao_routes():
    """
    Exemplo de como usar o log nas rotas Flask
    """
    
    print("\n🌐 EXEMPLO DE INTEGRAÇÃO COM ROTAS FLASK")
    print("=" * 50)
    
    # Simula uma rota de workflow
    session_id = "session_route_example"
    
    # Cria log
    create_session_log(session_id, {
        'route': '/api/workflow/start',
        'method': 'POST',
        'user_agent': 'Mozilla/5.0...',
        'ip': '127.0.0.1'
    })
    
    log_system = get_log_local()
    
    # Log de início de rota
    log_system.add_log_entry(
        session_id, "ROUTE", "INFO",
        "🌐 Rota /api/workflow/start acessada",
        extra_data={
            'method': 'POST',
            'content_type': 'application/json',
            'content_length': 256
        }
    )
    
    # Log de validação
    log_system.add_log_entry(
        session_id, "VALIDATION", "INFO",
        "✅ Parâmetros validados com sucesso",
        extra_data={
            'parametros_recebidos': ['query', 'max_results', 'sources'],
            'validacao_ok': True
        }
    )
    
    # Log de resposta
    log_system.add_log_entry(
        session_id, "ROUTE", "INFO",
        "📤 Resposta enviada com sucesso",
        extra_data={
            'status_code': 200,
            'response_size': 1024,
            'tempo_processamento': 0.15
        }
    )
    
    # Finaliza
    log_system.finalize_session_log(session_id, {
        'route_status': 'SUCCESS',
        'response_code': 200,
        'processing_time': '0.15s'
    })
    
    print(f"✅ Exemplo de rota concluído!")

if __name__ == "__main__":
    # Executa exemplos
    exemplo_integracao_workflow()
    exemplo_integracao_routes()
    
    print(f"\n📁 Arquivos de log criados na raiz do ARQ-ALPHA-V9")
    print(f"💡 Use estes exemplos para integrar o log em seu sistema!")