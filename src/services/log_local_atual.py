#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Log Local Atual - Sistema de Log em Tempo Real para Windows
Cria e atualiza arquivo de log específico por sessão na raiz do app
Monitora e salva todos os logs de execução em tempo real
OTIMIZADO PARA WINDOWS LOCAL
"""

import os
import sys
import json
import logging
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List
import time
import queue
import traceback
import platform

class LogLocalAtual:
    """
    Sistema de log local em tempo real que cria arquivos de log específicos por sessão
    """
    
    def __init__(self, app_root_path: str = None):
        """
        Inicializa o sistema de log local para Windows
        
        Args:
            app_root_path: Caminho raiz do app (se None, detecta automaticamente)
        """
        # Detecta automaticamente o caminho raiz do app
        if app_root_path is None:
            current_dir = os.path.abspath(__file__)
            # Sobe até encontrar a pasta ARQ-ALPHA-V9 ou similar
            while True:
                parent_dir = os.path.dirname(current_dir)
                if parent_dir == current_dir:  # Chegou na raiz
                    # Se não encontrou, usa o diretório atual
                    self.app_root = os.getcwd()
                    break
                if any(name in os.path.basename(parent_dir).upper() for name in ['ARQ-ALPHA', 'ARQ_ALPHA']):
                    self.app_root = parent_dir
                    break
                current_dir = parent_dir
        else:
            self.app_root = os.path.abspath(app_root_path)
        
        # Configurações
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.log_queue = queue.Queue()
        self.is_running = False
        self.worker_thread = None
        self.lock = threading.Lock()
        self.is_windows = platform.system().lower() == 'windows'
        
        # Logger interno
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Inicia o worker thread
        self.start_worker()
        
        print(f"✅ Log Local Atual inicializado para {platform.system()}")
        print(f"📁 Diretório raiz: {self.app_root}")
        
        # Cria diretório se não existir
        if not os.path.exists(self.app_root):
            os.makedirs(self.app_root, exist_ok=True)
    
    def start_worker(self):
        """Inicia o thread worker para processar logs"""
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.worker_thread.start()
            print("🔄 Worker thread de log iniciado")
    
    def stop_worker(self):
        """Para o worker thread"""
        self.is_running = False
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2)
            print("⏹️ Worker thread de log parado")
    
    def _worker_loop(self):
        """Loop principal do worker thread"""
        while self.is_running:
            try:
                # Processa logs na fila
                try:
                    log_entry = self.log_queue.get(timeout=0.5)
                    self._write_log_entry(log_entry)
                    self.log_queue.task_done()
                except queue.Empty:
                    continue
                    
            except Exception as e:
                print(f"❌ Erro no worker loop: {e}")
                time.sleep(1)
    
    def create_session_log(self, session_id: str, session_info: Dict[str, Any] = None) -> str:
        """
        Cria um novo arquivo de log para uma sessão
        
        Args:
            session_id: ID da sessão
            session_info: Informações adicionais da sessão
            
        Returns:
            Caminho do arquivo de log criado
        """
        try:
            # Nome do arquivo de log
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"log_{session_id}_{timestamp}.txt"
            log_path = os.path.join(self.app_root, log_filename)
            
            # Informações da sessão
            session_data = {
                'session_id': session_id,
                'log_file': log_path,
                'created_at': datetime.now().isoformat(),
                'info': session_info or {},
                'entries_count': 0
            }
            
            with self.lock:
                self.active_sessions[session_id] = session_data
            
            # Cria arquivo inicial
            header = self._create_log_header(session_id, session_info)
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(header)
            
            print(f"📝 Log criado para sessão {session_id}: {log_filename}")
            
            # Log inicial
            self.add_log_entry(session_id, "SISTEMA", "INFO", f"Log iniciado para sessão {session_id}")
            
            return log_path
            
        except Exception as e:
            print(f"❌ Erro ao criar log para sessão {session_id}: {e}")
            return ""
    
    def _create_log_header(self, session_id: str, session_info: Dict[str, Any] = None) -> str:
        """Cria o cabeçalho do arquivo de log"""
        header = f"""
{'='*80}
                    ARQ-ALPHA-V9 - LOG DE EXECUÇÃO EM TEMPO REAL
{'='*80}
SESSÃO: {session_id}
INICIADO EM: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
ARQUIVO: {self.active_sessions.get(session_id, {}).get('log_file', 'N/A')}
{'='*80}

"""
        
        if session_info:
            header += "INFORMAÇÕES DA SESSÃO:\n"
            for key, value in session_info.items():
                header += f"  {key}: {value}\n"
            header += f"{'='*80}\n\n"
        
        return header
    
    def add_log_entry(self, session_id: str, component: str, level: str, message: str, 
                     code_executed: str = None, extra_data: Dict[str, Any] = None):
        """
        Adiciona uma entrada de log para uma sessão específica
        
        Args:
            session_id: ID da sessão
            component: Componente que gerou o log (ex: "ETAPA1", "SYNTHESIS", "AI_VERIFIER")
            level: Nível do log (INFO, WARNING, ERROR, DEBUG)
            message: Mensagem do log
            code_executed: Código que foi executado (opcional)
            extra_data: Dados extras (opcional)
        """
        if session_id not in self.active_sessions:
            print(f"⚠️ Sessão {session_id} não encontrada. Criando automaticamente...")
            self.create_session_log(session_id)
        
        log_entry = {
            'session_id': session_id,
            'timestamp': datetime.now(),
            'component': component,
            'level': level,
            'message': message,
            'code_executed': code_executed,
            'extra_data': extra_data or {}
        }
        
        # Adiciona à fila para processamento assíncrono
        self.log_queue.put(log_entry)
    
    def _write_log_entry(self, log_entry: Dict[str, Any]):
        """Escreve uma entrada de log no arquivo"""
        try:
            session_id = log_entry['session_id']
            
            if session_id not in self.active_sessions:
                return
            
            session_data = self.active_sessions[session_id]
            log_path = session_data['log_file']
            
            # Formata a entrada
            timestamp_str = log_entry['timestamp'].strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
            
            # Linha principal
            log_line = f"[{timestamp_str}] [{log_entry['level']:7}] [{log_entry['component']:15}] {log_entry['message']}\n"
            
            # Código executado (se houver)
            code_section = ""
            if log_entry['code_executed']:
                code_section = f"""
{'─'*60}
CÓDIGO EXECUTADO:
{log_entry['code_executed']}
{'─'*60}
"""
            
            # Dados extras (se houver)
            extra_section = ""
            if log_entry['extra_data']:
                extra_section = f"""
DADOS EXTRAS:
{json.dumps(log_entry['extra_data'], indent=2, ensure_ascii=False)}
{'─'*40}
"""
            
            # Escreve no arquivo
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(log_line)
                if code_section:
                    f.write(code_section)
                if extra_section:
                    f.write(extra_section)
                f.write("\n")
            
            # Atualiza contador
            with self.lock:
                session_data['entries_count'] += 1
            
            # Também exibe no console para debug
            print(f"📝 [{session_id}] {log_entry['component']} - {log_entry['message']}")
            
        except Exception as e:
            print(f"❌ Erro ao escrever log: {e}")
    
    def log_etapa_iniciada(self, session_id: str, etapa_numero: int, etapa_nome: str, 
                          parametros: Dict[str, Any] = None):
        """Log específico para início de etapa"""
        message = f"🚀 ETAPA {etapa_numero} INICIADA: {etapa_nome}"
        self.add_log_entry(
            session_id=session_id,
            component=f"ETAPA{etapa_numero}",
            level="INFO",
            message=message,
            extra_data={
                'etapa_numero': etapa_numero,
                'etapa_nome': etapa_nome,
                'parametros': parametros or {},
                'status': 'iniciada'
            }
        )
    
    def log_etapa_concluida(self, session_id: str, etapa_numero: int, etapa_nome: str, 
                           resultado: Dict[str, Any] = None, tempo_execucao: float = None):
        """Log específico para conclusão de etapa"""
        tempo_str = f" em {tempo_execucao:.2f}s" if tempo_execucao else ""
        message = f"✅ ETAPA {etapa_numero} CONCLUÍDA: {etapa_nome}{tempo_str}"
        self.add_log_entry(
            session_id=session_id,
            component=f"ETAPA{etapa_numero}",
            level="INFO",
            message=message,
            extra_data={
                'etapa_numero': etapa_numero,
                'etapa_nome': etapa_nome,
                'resultado': resultado or {},
                'tempo_execucao': tempo_execucao,
                'status': 'concluida'
            }
        )
    
    def log_codigo_executado(self, session_id: str, component: str, codigo: str, 
                            resultado: Any = None, erro: str = None):
        """Log específico para código executado"""
        if erro:
            level = "ERROR"
            message = f"❌ Erro na execução de código em {component}: {erro}"
        else:
            level = "INFO"
            message = f"🔧 Código executado em {component}"
        
        self.add_log_entry(
            session_id=session_id,
            component=component,
            level=level,
            message=message,
            code_executed=codigo,
            extra_data={
                'resultado': str(resultado) if resultado else None,
                'erro': erro,
                'codigo_tamanho': len(codigo) if codigo else 0
            }
        )
    
    def log_api_call(self, session_id: str, component: str, api_name: str, 
                    parametros: Dict[str, Any] = None, resposta: Any = None, 
                    tempo_resposta: float = None, erro: str = None):
        """Log específico para chamadas de API"""
        if erro:
            level = "ERROR"
            message = f"❌ Erro na API {api_name}: {erro}"
        else:
            level = "INFO"
            tempo_str = f" ({tempo_resposta:.2f}s)" if tempo_resposta else ""
            message = f"🌐 Chamada API {api_name}{tempo_str}"
        
        self.add_log_entry(
            session_id=session_id,
            component=component,
            level=level,
            message=message,
            extra_data={
                'api_name': api_name,
                'parametros': parametros or {},
                'resposta_tamanho': len(str(resposta)) if resposta else 0,
                'tempo_resposta': tempo_resposta,
                'erro': erro
            }
        )
    
    def log_arquivo_processado(self, session_id: str, component: str, arquivo_path: str, 
                              operacao: str, resultado: Dict[str, Any] = None):
        """Log específico para processamento de arquivos"""
        message = f"📁 {operacao}: {os.path.basename(arquivo_path)}"
        self.add_log_entry(
            session_id=session_id,
            component=component,
            level="INFO",
            message=message,
            extra_data={
                'arquivo_path': arquivo_path,
                'operacao': operacao,
                'resultado': resultado or {}
            }
        )
    
    def finalize_session_log(self, session_id: str, resumo: Dict[str, Any] = None):
        """
        Finaliza o log de uma sessão
        
        Args:
            session_id: ID da sessão
            resumo: Resumo final da sessão
        """
        if session_id not in self.active_sessions:
            return
        
        try:
            session_data = self.active_sessions[session_id]
            log_path = session_data['log_file']
            
            # Resumo final
            fim_timestamp = datetime.now()
            inicio_timestamp = datetime.fromisoformat(session_data['created_at'])
            duracao_total = (fim_timestamp - inicio_timestamp).total_seconds()
            
            footer = f"""

{'='*80}
                            SESSÃO FINALIZADA
{'='*80}
SESSÃO: {session_id}
FINALIZADA EM: {fim_timestamp.strftime("%d/%m/%Y %H:%M:%S")}
DURAÇÃO TOTAL: {duracao_total:.2f} segundos
TOTAL DE LOGS: {session_data['entries_count']}
{'='*80}

"""
            
            if resumo:
                footer += "RESUMO DA SESSÃO:\n"
                for key, value in resumo.items():
                    footer += f"  {key}: {value}\n"
                footer += f"{'='*80}\n"
            
            # Escreve footer
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(footer)
            
            # Remove da lista de sessões ativas
            with self.lock:
                del self.active_sessions[session_id]
            
            print(f"🏁 Log finalizado para sessão {session_id}")
            print(f"📊 Total de {session_data['entries_count']} entradas em {duracao_total:.2f}s")
            
        except Exception as e:
            print(f"❌ Erro ao finalizar log da sessão {session_id}: {e}")
    
    def get_active_sessions(self) -> List[str]:
        """Retorna lista de sessões ativas"""
        with self.lock:
            return list(self.active_sessions.keys())
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retorna informações de uma sessão"""
        with self.lock:
            return self.active_sessions.get(session_id)
    
    def cleanup_old_logs(self, days_old: int = 7):
        """
        Remove logs antigos
        
        Args:
            days_old: Logs mais antigos que X dias serão removidos
        """
        try:
            cutoff_time = datetime.now().timestamp() - (days_old * 24 * 3600)
            removed_count = 0
            
            # Lista todos os arquivos de log
            for filename in os.listdir(self.app_root):
                if filename.startswith("log_") and filename.endswith(".txt"):
                    file_path = os.path.join(self.app_root, filename)
                    if os.path.isfile(file_path):
                        if os.path.getmtime(file_path) < cutoff_time:
                            os.remove(file_path)
                            removed_count += 1
            
            if removed_count > 0:
                print(f"🧹 {removed_count} logs antigos removidos (>{days_old} dias)")
            
        except Exception as e:
            print(f"❌ Erro na limpeza de logs: {e}")


# Instância global do sistema de log
_log_local_instance = None

def get_log_local() -> LogLocalAtual:
    """Retorna a instância global do sistema de log"""
    global _log_local_instance
    if _log_local_instance is None:
        _log_local_instance = LogLocalAtual()
    return _log_local_instance

def create_session_log(session_id: str, session_info: Dict[str, Any] = None) -> str:
    """Função de conveniência para criar log de sessão"""
    return get_log_local().create_session_log(session_id, session_info)

def log_info(session_id: str, component: str, message: str, **kwargs):
    """Função de conveniência para log INFO"""
    get_log_local().add_log_entry(session_id, component, "INFO", message, **kwargs)

def log_error(session_id: str, component: str, message: str, **kwargs):
    """Função de conveniência para log ERROR"""
    get_log_local().add_log_entry(session_id, component, "ERROR", message, **kwargs)

def log_warning(session_id: str, component: str, message: str, **kwargs):
    """Função de conveniência para log WARNING"""
    get_log_local().add_log_entry(session_id, component, "WARNING", message, **kwargs)

def finalize_session_log(session_id: str, resumo: Dict[str, Any] = None):
    """Função de conveniência para finalizar log de sessão"""
    get_log_local().finalize_session_log(session_id, resumo)


if __name__ == "__main__":
    # Teste do sistema
    print("🧪 Testando sistema de Log Local Atual...")
    
    # Cria instância
    log_system = LogLocalAtual()
    
    # Cria sessão de teste
    session_id = "test_session_123"
    log_path = log_system.create_session_log(session_id, {
        'tipo': 'teste_sistema',
        'usuario': 'desenvolvedor'
    })
    
    # Testa diferentes tipos de log
    log_system.log_etapa_iniciada(session_id, 1, "Teste de Sistema")
    
    log_system.add_log_entry(session_id, "TESTE", "INFO", "Testando sistema de log")
    
    log_system.log_codigo_executado(
        session_id, "TESTE", 
        "print('Hello World')\nresult = 2 + 2", 
        resultado=4
    )
    
    log_system.log_api_call(
        session_id, "TESTE", "test_api",
        parametros={'param1': 'value1'},
        tempo_resposta=0.5
    )
    
    log_system.log_etapa_concluida(session_id, 1, "Teste de Sistema", tempo_execucao=2.5)
    
    # Aguarda processamento
    time.sleep(1)
    
    # Finaliza
    log_system.finalize_session_log(session_id, {
        'status': 'sucesso',
        'testes_executados': 5
    })
    
    # Para o worker
    log_system.stop_worker()
    
    print(f"✅ Teste concluído! Arquivo criado: {log_path}")