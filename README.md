# ClaudeTrader — Analista de Swing Trading para B3

> Um screener inteligente que combina filtros fundamentalistas com análise técnica avançada para identificar oportunidades de swing trade na Bolsa de Valores Brasileira (B3).

## Visão Geral

**ClaudeTrader** é uma aplicação Streamlit que integra um agente de IA (via OpenRouter/Groq) com ferramentas de análise técnica e fundamentalista para o mercado de ações brasileiro. O sistema executa screenings automatizados, analisa ações individuais, busca notícias relevantes em tempo real e acompanha o histórico de decisões de investimento.

### Diferenciais

- **Análise Fundamentalista Automática:** Filtra ações com ROE, margens e alavancagem saudáveis
- **Indicadores Técnicos Precisos:** RSI Wilder(14), EMAs (8/80) e SMA(200) com detecção de gatilhos
- **Gatilhos de Entrada:** Dave Landry, 1-2-3 e Inside Candle nos últimos 3 candles
- **Notícias em Tempo Real:** Integração com RSS de InfoMoney, Valor Econômico, Investing.com BR e B3
- **Registro de Decisões:** Histórico persistente com cálculo de performance
- **Agente LLM Autônomo:** O analista aciona ferramentas automaticamente conforme a conversa
- **Temperatura Configurável:** Respostas determinísticas (0.0) para análises ou criativas (1.0) para narrativas

## Características Principais

### 📊 Screening B3 Completo

Aplica pipeline de análise em toda a B3:

1. Filtro fundamentalista (ROE > 15%, Mrg.EBIT > 10%, Mrg.Líquida > 10%, Dív/Patr < 3x, P/VP > 1)
2. Download de 3 meses de OHLCV via yfinance
3. Cálculo de RSI Wilder(14), EMAs (8/80) e SMA(200)
4. Detecção de gatilhos nos últimos 3 candles
5. Ranking por score (Verde ≥ 5.0 | Amarelo 4.5–4.9)

### 🔍 Análise Individual de Ações

Para uma ação específica:
- Tendência (Alta/Baixa/Neutro/Lateral)
- RSI com interpretação (Sobrecomprado/Neutro/Sobrevendido)
- Médias móveis (EMA8, EMA80, SMA200)
- Gatilho detectado
- Variações (7d, 15d, 30d)
- Validação contra filtro fundamentalista

### 📰 Notícias e Contexto de Mercado

- Resumo do mercado (IBOVESPA, dólar, manchetes)
- Notícias por ação
- Notícias por setor
- Busca por palavra-chave
- Notícias gerais do mercado

### 💾 Registro e Acompanhamento de Decisões

Salva automaticamente cada recomendação:
- Ticker, ação (COMPRAR/MONITORAR/DESCARTAR)
- Preço de entrada, gatilho, tendência
- RSI, ROE, stop loss sugerido
- Confiança (0–1.0)
- Justificativa

Permite atualizar preço atual, registrar fechamentos e calcular performance consolidada.

## Pré-requisitos

### Sistema Operacional
- Linux, macOS ou Windows
- Python 3.11+

### Dependências Externas
- **Conta de API:** OpenRouter ou Groq
- **Dados:** yfinance (automático) e Fundamentus (automático)

### Chaves de API Necessárias
- `GROQ_API_KEY` — Para usar Llama 3.3 70B (ativo)
- `OPEN_ROUTER` — Para Gemini 2.0 Flash, Claude Sonnet 4.6, GPT-4o (recomendado)

## Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/daholivesjc/claude_trader.git
cd claude_trader
```

### 2. Crie um Ambiente Virtual

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Chaves de API

**Localmente** (arquivo `.env`):
```bash
GROQ_API_KEY=your_groq_api_key
OPEN_ROUTER=your_openrouter_api_key
```

**No Streamlit Cloud** (Secrets):
1. Acesse a dashboard de seu app Streamlit
2. Vá para **Settings > Secrets**
3. Adicione as mesmas variáveis acima

Alternativamente, reutilize os secrets do ClaudeConsorcios se tiver permissão.

### 5. (Opcional) Geração de PDFs

Se quiser gerar PDFs dos screenings (via `scripts/generate_screening_pdf.py`), certifique-se de que tem `weasyprint` instalado (já incluído em `requirements.txt`).

## Como Executar

### Localmente

```bash
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`.

### No Streamlit Cloud

1. Envie o repositório para GitHub
2. Crie um novo app em [streamlit.io](https://streamlit.io)
3. Conecte ao seu repositório GitHub
4. Configure os **Secrets** (GROQ_API_KEY, OPEN_ROUTER)
5. Deploy

## Uso Rápido

### Exemplo 1: Screening Semanal

1. Na sidebar, clique em **"📊 Screening"** (ou digite na conversa)
2. O analista executa o screening completo
3. Receba ranking VERDE/AMARELO com score
4. Clique em ações para mais detalhes
5. O analista salva automaticamente qualquer recomendação

### Exemplo 2: Análise Individual

1. Digite na conversa: *"Analise WEGE3"*
2. O analista chama a ferramenta `analisar_acao`
3. Receba análise técnica completa + validação fundamentalista
4. Se recomendar, digitar: *"COMPRAR WEGE3 a R$ X"*
5. O analista salva a decisão automaticamente

### Exemplo 3: Consultar Posições Abertas

1. Clique em **"📋 Posições"** na sidebar
2. O analista lista todas as decisões ABERTA
3. Atualize: *"Fechei PETR4 a R$ 38,50"*
4. O analista calcula resultado e fecha a posição

## Estrutura do Projeto

```
claude_trader/
├── app.py                          # Aplicação Streamlit principal
├── config.py                       # Configurações centralizadas
├── requirements.txt                # Dependências Python
│
├── mcp-b3-news/                    # MCP Server customizado
│   ├── server.py                   # Implementação (news + memory)
│   ├── pyproject.toml              # Dependências do server
│   └── .mcp.json                   # Configuração MCP
│
├── screenings/                     # Relatórios semanais em markdown
│   ├── 2026-03-17-screening.md
│   ├── 2026-03-14-screening.md
│   └── ...
│
├── scripts/                        # Utilitários
│   └── generate_screening_pdf.py   # Gera PDF dos screenings
│
├── docs/                           # Documentação de referência
│   ├── INVESTMENT_ANALYST_GUIDE.md # Guia do analista
│   ├── 01-Porque uma acao sobre ou cai.txt
│   ├── 02-Quando comprar acoes.txt
│   └── ...
│
├── lib/                            # Bibliotecas customizadas (opcional)
│
├── .claude/                        # Claude Code ecosystem
│   ├── agents/                     # Agentes especializados
│   │   └── domain/
│   │       ├── investment-analyst.md
│   │       └── crypto-analyst.md
│   ├── kb/                         # Knowledge Base (10 domínios)
│   │   ├── swing-trading/
│   │   ├── crypto/
│   │   └── ...
│   ├── sdd/                        # Spec-Driven Development docs
│   └── memory/                     # Decisões persistentes
│       └── investment-decisions/decisions.json
│
├── .env                            # Variáveis de ambiente (local)
├── .gitignore
├── CLAUDE.md                       # Guia para Claude Code
└── README.md                       # Este arquivo
```

## Ferramentas Disponíveis (6 principais)

### 1. **executar_screening**
Executa screening completo da B3 com filtro fundamentalista + técnico.

```python
Entrada: período (padrão "3mo"), limite_tecnicos (padrão 60)
Saída: Ranking VERDE/AMARELO com scores e gatilhos
```

Quando usar: Toda semana, preferencialmente segunda-feira antes da abertura.

### 2. **analisar_acao**
Análise técnica e fundamentalista de uma ação específica.

```python
Entrada: ticker (ex: WEGE3), período (padrão "3mo")
Saída: Tendência, RSI, EMAs, SMA, gatilho, validação fundamentalista
```

Quando usar: Antes de tomar uma decisão de compra ou monitorar uma posição.

### 3. **buscar_noticias_acao**
Notícias recentes de um ticker específico.

```python
Entrada: ticker, limite (padrão 5)
Saída: Lista de notícias com título, resumo, link, data
Fontes: InfoMoney, Status Invest
```

### 4. **salvar_decisao**
Registra uma recomendação de COMPRAR/MONITORAR/DESCARTAR.

```python
Entrada: ticker, ação, preço_entrada, gatilho, justificativa, confiança
Saída: ID da decisão + confirmação
Armazenamento: .claude/memory/investment-decisions/decisions.json
```

**Chamado automaticamente** após o analista recomendar.

### 5. **listar_decisoes**
Consulta histórico de decisões com filtros opcionais.

```python
Entrada: ticker (opt), status (opt), ação (opt), limite (padrão 20)
Saída: Tabela com todas as decisões registradas
```

Estatutos: ABERTA, FECHADA, STOP_ATINGIDO

### 6. **resumo_performance**
Relatório consolidado de todas as decisões.

```python
Saída: Taxa de acerto, retorno médio, melhor/pior decisão, acerto por gatilho
```

## Indicadores Técnicos Explicados

### RSI Wilder(14)

**Implementação:** Loop recursivo (não rolling window) para precisão em séries curtas.

```
RSI = 100 - (100 / (1 + RS))
onde RS = Média de Ganhos / Média de Perdas

Interpretação:
  RSI > 70    → Sobrecomprado ⚠️ (evitar entrar)
  30 < RSI ≤ 70 → Neutro
  RSI < 30    → Sobrevendido (oportunidade)
```

**Score:** +2 se 40 ≤ RSI ≤ 60 | +1 se RSI < 70

### EMAs (8 e 80) e SMA(200)

**Tendência:**
- **Alta:** EMA8 > EMA80 > SMA200 (+3 pontos)
- **Neutro/Lateral:** EMA8 > EMA80 (sem SMA200 confirmando) (+1 ponto)
- **Baixa:** EMA8 < EMA80 < SMA200

### Gatilhos de Entrada (nos últimos 3 candles)

| Gatilho | Padrão | Interpretação |
|---------|--------|---------------|
| **Dave Landry** | Mín[0] < Mín[1] < Mín[2] | 3 mínimas consecutivamente mais baixas |
| **1-2-3** | Mín[0] > Mín[1] < Mín[2] | Recuperação após fundo |
| **Inside Candle** | Mín[0] > Mín[1] E Máx[0] < Máx[1] | Contração de volatilidade |

## Modelos LLM Suportados

| Modelo | API | Latência | Custo | Recomendado |
|--------|-----|----------|-------|-------------|
| Llama 3.3 70B (Groq) | Groq | ⚡ Rápido | 💰 Econômico | Para análises rápidas |
| Gemini 2.0 Flash | OpenRouter | ⚡ Rápido | 💎 Premium | Padrão — melhor qualidade |
| Claude Sonnet 4.6 | OpenRouter | 📊 Médio | 💎 Premium | Respostas estruturadas |
| GPT-4o | OpenRouter | 📊 Médio | 💎 Premium | Narrativas complexas |

**Padrão:** Gemini 2.0 Flash (melhor equilíbrio de velocidade e qualidade)

**Temperatura:** 0.0 (preciso) → ideal para análises quantitativas

## Fontes de Dados e APIs

### Preços e OHLCV
- **yfinance:** Download automático de 3 meses de histórico (diário)
- Compatível com tickers `.SA` (ex: `PETR4.SA`)

### Dados Fundamentalistas
- **Fundamentus:** ROE, margens (EBIT, líquida), dívida/patrimônio, P/VP, liquidez

### Notícias
- **RSS Feeds:**
  - InfoMoney (mercados, ações, economia)
  - Valor Econômico (financeiro)
  - Investing.com BR (notícias gerais)
  - B3 Notícias (oficial)
- **Web Scraping:**
  - InfoMoney (página da ação)
  - Status Invest (dados e notícias)

### Modelos de Linguagem
- **OpenRouter:** Gateway unificado para Gemini, Claude, GPT-4o
- **Groq:** API dedicada para Llama 3.3

## MCP Server (mcp-b3-news)

**O que é:** Um servidor MCP (Model Context Protocol) customizado que fornece notícias do mercado financeiro brasileiro e gerenciamento persistente de decisões de investimento.

### Ferramentas Disponíveis

**Notícias:**
- `buscar_noticias_mercado(limite)` — Notícias gerais
- `buscar_noticias_acao(ticker, limite)` — Por ação
- `buscar_noticias(query, limite)` — Por palavra-chave
- `buscar_noticias_setor(setor, limite)` — Por setor
- `obter_resumo_mercado()` — IBOV, dólar, juros, manchetes

**Decisões (Memória Persistente):**
- `salvar_decisao(...)` — Registra recomendação
- `listar_decisoes(...)` — Consulta histórico
- `atualizar_decisao(...)` — Atualiza preço/status
- `resumo_performance()` — Relatório consolidado

### Armazenamento
- **Arquivo:** `.claude/memory/investment-decisions/decisions.json`
- **Formato:** JSON com array de decisões
- **Persistência:** Automática entre sessões

### Requisitos do Server
- Python 3.12+
- Dependências: mcp, httpx, feedparser, beautifulsoup4, lxml

## Configuração de Ambiente

### Variáveis de Ambiente (`.env`)

```bash
# APIs de LLM
GROQ_API_KEY=sk_xxxx...              # Groq
OPEN_ROUTER=sk-or_xxxx...            # OpenRouter

# Opcional
B3_DECISIONS_DIR=/path/to/decisions  # Padrão: .claude/memory/investment-decisions
```

### Streamlit Secrets (Cloud)

Na dashboard do Streamlit, configure:
```
GROQ_API_KEY
OPEN_ROUTER
```

## Exemplos de Uso

### Screening Semanal

```
Você: "Faça um screening completo da B3 agora."

ClaudeTrader:
✓ Executa screening
✓ Retorna ranking VERDE/AMARELO
✓ Para top 5 VERDE + top 2 AMARELO, mostra análise detalhada
✓ Salva automaticamente qualquer recomendação de COMPRAR
```

### Análise Individual

```
Você: "Analise WEGE3 para mim. Vale a pena comprar?"

ClaudeTrader:
✓ Chama analisar_acao
✓ Mostra: Cotação, tendência, RSI, EMAs, gatilho
✓ Valida contra filtro fundamentalista
✓ Recomenda ou descarta com justificativa
✓ Salva a decisão automaticamente
```

### Notícias e Contexto

```
Você: "Tem alguma notícia ruim sobre ITUB4?"

ClaudeTrader:
✓ Busca notícias recentes de ITUB4
✓ Apresenta manchetes com datas
✓ Contextualiza com análise técnica
```

### Acompanhamento de Posição

```
Você: "Fechei PETR4 a R$ 38,50."

ClaudeTrader:
✓ Atualiza a decisão com preço atual
✓ Calcula resultado: "+5.2%" ou "-2.1%"
✓ Marca como FECHADA
```

## Deployment

### Streamlit Cloud (Recomendado)

1. Envie o repositório para GitHub
2. Vá a [streamlit.io](https://streamlit.io)
3. Clique em **"New app"** e conecte ao seu repo
4. Configure os Secrets na dashboard
5. Deploy automático

**URL:** `https://<seu-username>-claude-trader.streamlit.app`

### Localmente (Desenvolvimento)

```bash
source .venv/bin/activate
streamlit run app.py
```

Acesse `http://localhost:8501`

### Docker (Opcional)

Crie um `Dockerfile` se quiser containerizar (não incluído neste projeto).

## Tabs da Interface

### 💬 Chat (Principal)
Conversa interativa com o analista. As ferramentas são acionadas automaticamente conforme você digita.

### 📚 Guia de Funcionalidades
Documentação completa das 6 ferramentas com exemplos de uso, interpretação de gatilhos, regras operacionais.

### 🕐 Histórico
Pares pergunta/resposta da sessão atual com métricas (total de mensagens, ferramentas utilizadas). Exportação em texto.

## Regras Operacionais

1. **Use temperatura 0.0** para análises — respostas determinísticas e precisas
2. **Faça screening semanalmente**, preferencialmente segunda-feira antes da abertura
3. **Confirme o gatilho no gráfico** antes de executar a ordem
4. **RSI > 70** indica sobrecompra — evite entrar em posições novas
5. **Reduza posição 30–50%** quando nenhuma ação estiver em tendência Alta
6. **Stop loss é obrigatório** — toda decisão de COMPRAR deve ter stop definido

## Troubleshooting

### Erro: "GROQ_API_KEY não encontrada"

**Solução:** Configure a variável de ambiente:
```bash
export GROQ_API_KEY=sk_...
# ou adicione a .env
```

No Streamlit Cloud, vá em **Settings > Secrets** e adicione a chave.

### Erro: "fundamentus não instalado"

**Solução:** Reinstale as dependências:
```bash
pip install -r requirements.txt --upgrade
```

### Erro: "Nenhuma ação com gatilho ativo"

**Explicação:** O mercado não apresentou gatilhos de entrada essa semana. Isso é normal. Use a aba **Guia** para entender os padrões buscados.

### Erro ao buscar notícias

**Solução:** Verifique conexão com Internet. Os feeds RSS podem estar temporariamente indisponíveis. O sistema tenta multiple fallbacks automaticamente.

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaMelhoria`)
3. Commit com mensagem descritiva (`git commit -m "Adiciona novo indicador"`)
4. Push para a branch (`git push origin feature/MinhaMelhoria`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença [MIT](LICENSE). Veja o arquivo `LICENSE` para detalhes.

## Suporte

- **Documentação:** Veja o arquivo `CLAUDE.md` para detalhes técnicos
- **Problemas:** Abra uma issue no GitHub
- **Contato:** daniel.holiveira@gmail.com

## Versão

**Versão Atual:** 2.0.0 (mai/2026)

**Histórico:**
- v2.0.0 — Remoção de Neo4j/Docker; temperatura 0.0; tabs Guia + Histórico; get_api_key() com st.secrets
- v1.0.0 — Screener B3 inicial; pipeline fundamentalista + técnico; MCP server notícias

## Roadmap

- [ ] Integração com more brokers (não apenas yfinance)
- [ ] Backtest automático de estratégias
- [ ] Alertas por email/Telegram quando gatilhos são detectados
- [ ] Dashboard de performance com gráficos
- [ ] Análise de setores consolidados
- [ ] Recomendações por tamanho de capital (até R$ 5k, R$ 5k–50k, etc)

## Links Úteis

- **Repositório GitHub:** https://github.com/daholivesjc/claude_trader
- **Documentação Técnica:** [CLAUDE.md](CLAUDE.md)
- **Investimento (Referência):** [docs/INVESTMENT_ANALYST_GUIDE.md](docs/INVESTMENT_ANALYST_GUIDE.md)
- **Streamlit Docs:** https://docs.streamlit.io
- **MCP Specification:** https://spec.modelcontextprotocol.io
