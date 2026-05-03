# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ClaudeTrader** é um screener de swing trading para ações da B3 que combina filtros fundamentalistas com análise técnica para identificar ações com gatilhos de entrada. O agente conversa com o usuário via Streamlit e usa um servidor MCP customizado para notícias e memória de decisões.

**Repositório:** https://github.com/daholivesjc/claude_trader

## Architecture

```text
STREAMLIT UI (app.py)
       │
       ├── Sidebar: modelo LLM + temperatura (default 0.0) + ações rápidas
       ├── Tab Chat: conversa principal com tool_calls
       ├── Tab Guia de Funcionalidades: documentação das ferramentas
       └── Tab Histórico: pares pergunta/resposta da sessão
       │
       ▼
  LLM via OpenRouter ou Groq
       │
       ▼
  Tool Execution Layer
  ├── Data Collection  → yfinance (OHLCV 3mo)
  ├── Fundamentals     → fundamentus (ROE, margens, dívida)
  ├── Technical        → RSI Wilder, EMA(8/80), SMA(200)
  └── Triggers         → Dave Landry / 1-2-3 / Inside Candle
       │
       ▼
  MCP Server (mcp-b3-news/server.py)
  ├── News             → RSS feeds (InfoMoney, Valor, Investing.com BR, B3)
  ├── Market Summary   → obter_resumo_mercado()
  └── Decision Memory  → salvar/listar/atualizar_decisao() (JSON)
       │
       ▼
  screenings/          → Weekly markdown reports
```

## Pipeline Steps

### 1. Fundamentalist Filter (`fundamentus.get_resultado()`)
Keeps only stocks meeting all criteria:
- ROE > 15%
- EBIT margin > 10%
- Net margin > 10%
- Debt/equity < 3
- P/BV (PVP) > 1
- Liquidity > R$ 100k

### 2. Technical Indicators (computed per ticker)
- **RSI(14)** — custom implementation using Wilder smoothing (recursive loop, not rolling mean)
- **Trend** — determined by EMA(8) vs EMA(80) vs SMA(200): Alta / Baixa / Neutro/Lateral / Nenhuma
- **Price variation** — 7, 15, and 30-day percentage change

### 3. Trigger Detection (`_detectar_gatilho()`)
Three mutually exclusive candlestick triggers evaluated on the last 3 candles:
- **Dave Landry (3 consecutive lower lows):** `low[0] < low[1] < low[2]`
- **1-2-3 (bounce from low):** `low[0] > low[1] < low[2]`
- **Inside Candle:** `low[0] > low[1]` AND `high[0] < high[1]`

### 4. Score
- Tendência Alta: +3 | Neutro: +1
- RSI 40–60: +2 | RSI < 70: +1
- ROE normalizado (até 30%): até +3

Classificação: Verde ≥ 5.0 · Amarelo 4.5–4.9

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI + LLM + todas as tool implementations |
| `config.py` | Configurações centralizadas (MAX_TOKENS, DEFAULT_MODEL) |
| `requirements.txt` | Dependências do projeto |
| `mcp-b3-news/server.py` | MCP server: notícias, resumo de mercado, memória de decisões |
| `mcp-b3-news/pyproject.toml` | MCP server dependencies (Python 3.12+) |
| `.mcp.json` | MCP server configuration |
| `.env` | GROQ_API_KEY e OPEN_ROUTER (local) |
| `screenings/` | Relatórios semanais em markdown |
| `scripts/generate_screening_pdf.py` | Geração de PDF dos screenings (weasyprint) |

## API Keys — Padrão st.secrets + .env

O app usa `get_api_key()` que busca em `st.secrets` primeiro (Streamlit Cloud) e cai para variáveis de ambiente (`.env` local). **Usar os mesmos secrets do ClaudeConsorcios no Streamlit Cloud.**

```python
def get_api_key(key_name: str) -> str:
    try:
        return st.secrets[key_name]
    except (KeyError, FileNotFoundError):
        api_key = os.environ.get(key_name)
        ...
```

## Temperatura

Default: **0.0** (determinístico e preciso — ideal para análises numéricas).
Slider exposto na sidebar (0.0–1.0, step 0.05). Labels: 🎯 Preciso / ⚖️ Equilibrado / 🎨 Criativo.

## Key Data Sources

| Source | Library / Protocol | Data |
|--------|-------------------|------|
| Yahoo Finance | `yfinance` | OHLCV history (3mo, daily) |
| Fundamentus | `fundamentus` | ROE, margins, debt, P/BV |
| InfoMoney, Valor Econômico, Investing.com BR, B3 | RSS via `mcp-b3-news` | Financial news |

## MCP Server — `mcp-b3-news`

Async MCP server que roda junto ao app Streamlit.

**News Tools:**
- `buscar_noticias_mercado(limite)` — Notícias gerais do mercado
- `buscar_noticias_acao(ticker, limite)` — Notícias de um ticker
- `buscar_noticias(query, limite)` — Busca por palavra-chave
- `buscar_noticias_setor(setor, limite)` — Busca por setor
- `obter_resumo_mercado()` — Resumo com cache de 1 hora

**Decision Memory Tools (persistent JSON):**
- `salvar_decisao(ticker, acao, ...)` — Salva decisão COMPRAR/MONITORAR/DESCARTAR
- `listar_decisoes(filtros)` — Lista histórico
- `atualizar_decisao(decisao_id, preco_atual, ...)` — Fecha operação ou registra stop
- `resumo_performance()` — Relatório consolidado

**Storage:** `.claude/memory/investment-decisions/decisions.json`

## Tabs da Interface

| Tab | Conteúdo |
|-----|----------|
| 💬 Chat | Conversa principal com tool_calls e expansor de ferramentas |
| 📚 Guia de Funcionalidades | Documentação de cada ferramenta com exemplos de uso |
| 🕐 Histórico | Pares pergunta/resposta com métricas e exportação em texto |

## Domain Agents

| Agent | File | Purpose |
|-------|------|---------|
| `investment-analyst` | `.claude/agents/domain/investment-analyst.md` | Weekly B3 swing trading screening with MCP tools |
| `crypto-analyst` | `.claude/agents/domain/crypto-analyst.md` | Bitcoin, ETH, altcoins, B3 ETFs, Binance, BTG, Toro |

## Knowledge Base (10 Domains)

| Domain | Concepts | Patterns | Notes |
|--------|----------|----------|-------|
| **swing-trading** | 7 | 5 | RSI, EMAs, gatilhos, B3 |
| **crypto** | 5 | 4 | BTC/ETH, ETFs B3, on-chain |
| **pydantic** | 4 | 4 | Validation, computed fields |
| **gcp** | 6 | 5 | GCP serverless |
| **gemini** | 6 | 6 | Gemini multimodal LLM |
| **langfuse** | 6 | 6 | LLMOps observability |
| **terraform** | 6 | 6 | IaC for GCP |
| **terragrunt** | 6 | 5 | Multi-environment orchestration |
| **crewai** | 6 | 6 | Multi-agent AI |
| **openrouter** | 5 | 5 | Unified LLM API gateway |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `GROQ_API_KEY` | Groq API key (modelos ⚡) |
| `OPEN_ROUTER` | OpenRouter API key (modelos 🆓 e 💎) |
| `B3_DECISIONS_DIR` | Path para o JSON de decisões (definido em `.mcp.json`) |

## Important Notes

- Tickers da B3 precisam do sufixo `.SA` para yfinance (ex: `PETR4.SA`)
- RSI usa **loop recursivo de Wilder** — não rolling window — para precisão em séries curtas
- Temperatura padrão **0.0** para análises quantitativas; suba para narrativas/explicações
- Secrets do Streamlit Cloud devem ser os **mesmos do ClaudeConsorcios** (`GROQ_API_KEY`, `OPEN_ROUTER`)
- Neo4j e Docker foram **removidos** — app não tem dependências de banco de dados externo

## Version History

| Date | Changes |
|------|---------|
| 2026-05-03 | Remove Neo4j/Docker; add temperatura (default 0.0); add tabs Guia + Histórico; add get_api_key() com st.secrets; update CLAUDE.md |
| 2026-03-17 | Added crypto-analyst agent; swing-trading and crypto KB domains; MCP server details |
| Initial | ClaudeTrader screener B3 — pipeline steps, data sources, investment analyst agent |
