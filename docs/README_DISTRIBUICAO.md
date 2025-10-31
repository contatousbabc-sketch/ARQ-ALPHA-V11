# ARQ-ALPHA-V9 - Sistema de Análise Ultra-Detalhada

## 🚀 Instalação Automática para Windows

### Para Usuários Finais (Recomendado)

**OPÇÃO 1: Instalador Executável (Mais Fácil)**
1. Baixe `ARQ-ALPHA-V9-Instalador.exe`
2. **Execute como Administrador** (botão direito → "Executar como administrador")
3. Aguarde a instalação completa (15-30 minutos)
4. Siga as instruções na tela
5. Execute `iniciar_arq_alpha.bat` para iniciar o sistema

**OPÇÃO 2: Script Python**
1. Instale Python 3.11+ de https://python.org/downloads/
2. Execute `instalador_automatico.py`
3. Aguarde a instalação completa

### O que o Instalador Faz Automaticamente

✅ **Instala Python 3.11+** (se não estiver instalado)  
✅ **Instala Node.js 20+** (para Playwright)  
✅ **Instala Visual Studio Build Tools** (para compilação)  
✅ **Configura variáveis de ambiente PATH**  
✅ **Instala todas as dependências Python** (50+ pacotes)  
✅ **Instala Playwright + Chromium** (navegador automatizado)  
✅ **Cria scripts de inicialização**  
✅ **Configura sistema de logging**  
✅ **Executa testes de verificação**  

### Requisitos do Sistema

- **SO**: Windows 10/11 (64-bit)
- **RAM**: 4GB mínimo, 8GB recomendado
- **Espaço**: 2GB livres (após instalação completa)
- **Internet**: Conexão estável necessária
- **Privilégios**: Administrador (para instalação)

## 🎯 Recursos Principais

### 3 Etapas de Workflow Automatizado

1. **Coleta Massiva Real**
   - Busca em múltiplas APIs simultaneamente
   - Rotação automática de provedores
   - Extração de conteúdo viral
   - Captura automática de screenshots

2. **Síntese com IA Ativa**
   - Análise por múltiplos modelos de IA
   - Buscas online ativas para validação
   - Enriquecimento de informações
   - Síntese estruturada em JSON

3. **Geração de 16 Módulos**
   - Relatório final ultra-detalhado
   - 16 módulos especializados
   - Mais de 25 páginas de análise
   - Compilação automática

### Verificação AI Avançada

🧠 **Análise de Sentimento** - Detecta polaridade emocional  
🔍 **Detecção de Viés** - Identifica tendências  
✅ **Validação LLM** - Verificação por IA  
📊 **Filtros Avançados** - Qualidade dos dados  

### Sistema de Logging em Tempo Real

📝 **Logs detalhados** de cada operação  
⏰ **Timestamps precisos** para rastreamento  
🔧 **Códigos executados** capturados  
📊 **Dados extras** para debugging  
💾 **Arquivos de sessão** específicos  

## 🔧 Configuração Inicial

### 1. Chaves de API Necessárias

Você precisará configurar as seguintes chaves de API:

```env
# APIs de IA (pelo menos uma obrigatória)
OPENAI_API_KEY=sk-...                    # GPT-4, GPT-3.5
ANTHROPIC_API_KEY=sk-ant-...             # Claude 3
GOOGLE_API_KEY=AIza...                   # Gemini Pro

# APIs de Busca (pelo menos uma obrigatória)
SERPER_API_KEY=...                       # Google Search
JINA_API_KEY=jina_...                    # Extração de conteúdo
EXA_API_KEY=...                          # Busca semântica

# APIs Opcionais (melhoram resultados)
FIRECRAWL_API_KEY=fc-...                 # Web scraping
SUPADATA_API_KEY=...                     # Dados estruturados
APIFY_API_KEY=apify_api_...              # Automação web
RAPIDAPI_KEY=...                         # APIs diversas
```

### 2. Como Obter as Chaves

**OpenAI**: https://platform.openai.com/api-keys  
**Anthropic**: https://console.anthropic.com/  
**Google AI**: https://makersuite.google.com/app/apikey  
**Serper**: https://serper.dev/  
**Jina AI**: https://jina.ai/  

### 3. Configurar Arquivo .env

1. Copie `.env.example` para `.env`
2. Edite `.env` com suas chaves de API
3. Salve o arquivo

## 🚀 Como Usar

### 1. Iniciar o Sistema

**Opção A**: Execute `iniciar_arq_alpha.bat`  
**Opção B**: Execute `python run.py`  
**Opção C**: Navegue até a pasta e execute no terminal

### 2. Acessar Interface

Abra seu navegador em: **http://localhost:12000**

### 3. Configurar Análise

1. **Segmento de Mercado**: Ex: "Inteligência Artificial"
2. **Produto/Serviço**: Ex: "Sistema de logging em tempo real"
3. **Preço**: Valor em R$
4. **Objetivo de Receita**: Meta financeira
5. **Público-Alvo**: Descrição detalhada
6. **Contexto Adicional**: Informações extras

### 4. Executar Workflow

1. **Clique "INICIAR COLETA MASSIVA"** (Etapa 1)
2. **Aguarde conclusão** (5-15 minutos)
3. **Clique "INICIAR SÍNTESE IA"** (Etapa 2)
4. **Aguarde conclusão** (10-20 minutos)
5. **Clique "VERIFICAR COM IA"** (Verificação)
6. **Clique "GERAR MÓDULOS"** (Etapa 3)
7. **Aguarde relatório final** (15-30 minutos)

## 📊 Resultados

### Tipos de Saída

- **Visão Geral**: Dashboard interativo
- **16 Módulos**: Análises especializadas
- **Screenshots**: Capturas automáticas
- **Dados Coletados**: Informações brutas
- **Logs**: Rastreamento completo

### Formatos Disponíveis

- **JSON**: Dados estruturados
- **HTML**: Relatórios visuais
- **PNG**: Screenshots e gráficos
- **TXT**: Logs detalhados

## 🔧 Solução de Problemas

### Instalação

**Erro: "Python não encontrado"**
- Execute o instalador como Administrador
- Reinicie o terminal após instalação

**Erro: "Dependências falharam"**
- Execute: `python verificar_dependencias.py`
- Reinstale com: `pip install -r requirements.txt`

**Erro: "Playwright não funciona"**
- Execute: `python -m playwright install chromium`
- Verifique conexão com internet

### Execução

**Erro: "Chaves de API inválidas"**
- Verifique arquivo `.env`
- Confirme chaves corretas
- Teste chaves individualmente

**Erro: "Análise não inicia"**
- Verifique conexão com internet
- Confirme todas as dependências
- Reinicie o sistema

**Performance lenta**
- Feche outras aplicações
- Use parâmetros mais específicos
- Aguarde mais tempo

### Logs e Debugging

**Localização dos Logs**:
- `app_runtime.log` - Log principal
- `log_session_*.txt` - Logs de sessão
- `src/services/viral_integration.log` - Logs específicos

**Verificação Rápida**:
Execute `scripts/verificacao_rapida.bat`

## 📁 Estrutura de Arquivos

```
ARQ-ALPHA-V9/
├── run.py                          # Arquivo principal
├── instalador_automatico.py        # Instalador completo
├── criar_executavel.bat           # Gerador de executável
├── iniciar_arq_alpha.bat          # Script de inicialização
├── verificar_dependencias.py      # Verificador de deps
├── requirements.txt               # Dependências Python
├── .env.example                   # Exemplo de configuração
├── src/                          # Código fonte
│   ├── routes/                   # Rotas Flask
│   ├── services/                 # Serviços principais
│   ├── static/                   # Arquivos estáticos
│   └── templates/                # Templates HTML
├── external_ai_verifier/         # Módulo de verificação IA
├── docs/                         # Documentação
├── scripts/                      # Scripts auxiliares
└── logs/                         # Arquivos de log
```

## 🆘 Suporte

### Verificações Automáticas

1. **Dependências**: `python verificar_dependencias.py`
2. **Sistema**: `scripts/verificacao_rapida.bat`
3. **Atualização**: `scripts/atualizar_sistema.bat`

### Informações do Sistema

- **Versão**: 9.0.0
- **Build**: 2025-10-31
- **Python**: 3.11+
- **Node.js**: 18+

### Contato

Para suporte técnico:
- Consulte os logs detalhados
- Verifique a documentação completa
- Execute scripts de verificação

---

## 🎉 Pronto para Usar!

O ARQ-ALPHA-V9 está configurado para análises profissionais de mercado com IA avançada. 

**Acesse**: http://localhost:12000  
**Execute**: `iniciar_arq_alpha.bat`  
**Configure**: Suas chaves de API no arquivo `.env`  

**Boa análise! 🚀**