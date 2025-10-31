# 📝 GUIA DE INTEGRAÇÃO - Log Local Atual para Windows

## 🎯 Objetivo
Sistema de log em tempo real que cria arquivos `.txt` na raiz do app com nome `log_nome_da_sessão_timestamp.txt`, salvando e atualizando logs de execução em tempo real, como se fosse a tela do terminal mostrando as etapas, códigos executados, etc.

## 📁 Localização
- **Arquivo Principal**: `src/services/log_local_atual.py`
- **Exemplo de Integração**: `src/services/log_integration_example.py`
- **Logs Gerados**: Raiz do ARQ-ALPHA-V9 (ex: `log_session_123_20251031_182509.txt`)

## 🚀 Como Usar

### 1. Importação Básica
```python
from services.log_local_atual import (
    get_log_local, 
    create_session_log, 
    log_info, 
    log_error, 
    log_warning,
    finalize_session_log
)
```

### 2. Criando Log de Sessão
```python
# Cria log para uma nova sessão
session_id = "session_12345"
log_path = create_session_log(session_id, {
    'tipo': 'enhanced_workflow',
    'usuario': 'sistema',
    'versao': 'ARQ-ALPHA-V9'
})
```

### 3. Adicionando Logs Durante Execução
```python
# Log simples
log_info(session_id, "ETAPA1", "Iniciando coleta de dados")

# Log com sistema completo
log_system = get_log_local()

# Log de início de etapa
log_system.log_etapa_iniciada(session_id, 1, "Coleta de Dados", {
    'fontes': ['google', 'bing'],
    'max_results': 50
})

# Log de código executado
log_system.log_codigo_executado(
    session_id, "COLETA", 
    "results = search_web(query)\nprint(f'Coletados {len(results)} resultados')",
    resultado={'total': 150}
)

# Log de chamada API
log_system.log_api_call(
    session_id, "COLETA", "google_api",
    parametros={'q': 'mercado', 'num': 50},
    tempo_resposta=1.5
)

# Log de arquivo processado
log_system.log_arquivo_processado(
    session_id, "SYNTHESIS", "dados_consolidados.json",
    "ESCRITA", {'items': 150}
)

# Log de conclusão de etapa
log_system.log_etapa_concluida(session_id, 1, "Coleta de Dados", 
    {'total_coletado': 150}, tempo_execucao=5.2)
```

### 4. Finalizando Sessão
```python
# Finaliza o log com resumo
finalize_session_log(session_id, {
    'status': 'SUCESSO',
    'etapas_concluidas': 3,
    'tempo_total': '15.8s',
    'items_processados': 150
})
```

## 🔧 Integração com Rotas Flask

### Exemplo em `routes/enhanced_workflow.py`:
```python
from services.log_local_atual import get_log_local, create_session_log

@app.route('/api/workflow/start', methods=['POST'])
def start_workflow():
    # Gera session_id
    session_id = f"session_{int(time.time())}"
    
    # Cria log da sessão
    create_session_log(session_id, {
        'route': '/api/workflow/start',
        'method': 'POST',
        'ip': request.remote_addr
    })
    
    log_system = get_log_local()
    
    # Log de início
    log_system.add_log_entry(
        session_id, "WORKFLOW", "INFO",
        "🚀 Workflow iniciado via API",
        extra_data={'parametros': request.json}
    )
    
    try:
        # Seu código aqui...
        
        # Log de sucesso
        log_system.add_log_entry(
            session_id, "WORKFLOW", "INFO",
            "✅ Workflow concluído com sucesso"
        )
        
        return jsonify({'success': True, 'session_id': session_id})
        
    except Exception as e:
        # Log de erro
        log_system.add_log_entry(
            session_id, "WORKFLOW", "ERROR",
            f"❌ Erro no workflow: {str(e)}"
        )
        return jsonify({'success': False, 'error': str(e)})
```

## 🔧 Integração com Serviços

### Exemplo em `services/enhanced_synthesis_engine.py`:
```python
from services.log_local_atual import get_log_local

class EnhancedSynthesisEngine:
    def process_data(self, session_id, data):
        log_system = get_log_local()
        
        # Log início do processamento
        log_system.add_log_entry(
            session_id, "SYNTHESIS", "INFO",
            f"🔄 Processando {len(data)} items"
        )
        
        # Log código executado
        log_system.log_codigo_executado(
            session_id, "SYNTHESIS",
            """
# Processamento de síntese
for item in data:
    processed_item = self.analyze_item(item)
    results.append(processed_item)
""",
            resultado={'items_processados': len(data)}
        )
        
        # Seu código de processamento aqui...
        
        return results
```

## 📊 Formato do Arquivo de Log

O arquivo gerado terá o formato:
```
================================================================================
                    ARQ-ALPHA-V9 - LOG DE EXECUÇÃO EM TEMPO REAL
================================================================================
SESSÃO: session_12345
INICIADO EM: 31/10/2025 18:25:09
ARQUIVO: C:\Users\user\Desktop\ARQ-ALPHA-V9\log_session_12345_20251031_182509.txt
================================================================================

INFORMAÇÕES DA SESSÃO:
  tipo: enhanced_workflow
  usuario: sistema
  versao: ARQ-ALPHA-V9
================================================================================

[31/10/2025 18:25:09.267] [INFO   ] [ETAPA1         ] 🚀 ETAPA 1 INICIADA: Coleta de Dados

DADOS EXTRAS:
{
  "etapa_numero": 1,
  "parametros": {
    "fontes": ["google", "bing"],
    "max_results": 50
  }
}
────────────────────────────────────────

[31/10/2025 18:25:10.123] [INFO   ] [COLETA         ] 🔧 Código executado em COLETA

────────────────────────────────────────────────────────────
CÓDIGO EXECUTADO:
results = search_web(query)
print(f'Coletados {len(results)} resultados')
────────────────────────────────────────────────────────────

DADOS EXTRAS:
{
  "resultado": "{'total': 150}",
  "codigo_tamanho": 65
}
────────────────────────────────────────

[31/10/2025 18:25:12.456] [INFO   ] [COLETA         ] 🌐 Chamada API google_api (1.50s)

================================================================================
                            SESSÃO FINALIZADA
================================================================================
SESSÃO: session_12345
FINALIZADA EM: 31/10/2025 18:25:15
DURAÇÃO TOTAL: 5.73 segundos
TOTAL DE LOGS: 8
================================================================================
```

## 🎯 Funcionalidades Principais

### ✅ Logs Automáticos
- **Início/Fim de Etapas**: Com parâmetros e resultados
- **Código Executado**: Mostra o código que foi executado
- **Chamadas de API**: Com parâmetros, tempo de resposta e erros
- **Processamento de Arquivos**: Leitura/escrita com resultados
- **Erros e Exceções**: Com stack trace completo

### ✅ Características
- **Thread-Safe**: Usa threading para não bloquear execução
- **Tempo Real**: Logs são escritos imediatamente
- **Formato Legível**: Como terminal do CMD com timestamps
- **Detalhamento Completo**: Código, dados, parâmetros, resultados
- **Sessões Independentes**: Cada sessão tem seu próprio arquivo
- **Limpeza Automática**: Remove logs antigos automaticamente

### ✅ Compatibilidade Windows
- **Caminhos Windows**: Usa `os.path` em vez de `pathlib`
- **Encoding UTF-8**: Suporte completo a caracteres especiais
- **Detecção Automática**: Encontra automaticamente a raiz do app
- **Performance Otimizada**: Thread worker para não impactar performance

## 🔧 Configuração Avançada

### Limpeza de Logs Antigos
```python
log_system = get_log_local()
log_system.cleanup_old_logs(days_old=7)  # Remove logs > 7 dias
```

### Informações de Sessões Ativas
```python
log_system = get_log_local()
active_sessions = log_system.get_active_sessions()
session_info = log_system.get_session_info(session_id)
```

## 💡 Dicas de Uso

1. **Sempre crie o log no início**: Use `create_session_log()` antes de qualquer processamento
2. **Use componentes descritivos**: "ETAPA1", "SYNTHESIS", "AI_VERIFIER", etc.
3. **Log códigos importantes**: Use `log_codigo_executado()` para códigos críticos
4. **Finalize sempre**: Use `finalize_session_log()` ao terminar
5. **Monitore performance**: O sistema é otimizado mas monitore em produção

## 🚀 Exemplo Completo de Integração

Veja o arquivo `src/services/log_integration_example.py` para um exemplo completo de como integrar o sistema com o workflow do ARQ-ALPHA-V9.

## 📁 Arquivos Relacionados

- `src/services/log_local_atual.py` - Sistema principal
- `src/services/log_integration_example.py` - Exemplos de uso
- `log_*.txt` - Arquivos de log gerados na raiz

---

**✅ SISTEMA PRONTO PARA USO NO WINDOWS!**

O sistema está completamente funcional e otimizado para Windows. Basta importar e usar conforme os exemplos acima.