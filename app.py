"""ClaudeTrader — Interface Streamlit para o Analista de Investimentos B3"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import config

load_dotenv()

# ── Adiciona mcp-b3-news ao path ──────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent / "mcp-b3-news"))

try:
    from server import (
        atualizar_decisao,
        buscar_noticias as _buscar_noticias,
        buscar_noticias_acao as _buscar_noticias_acao,
        buscar_noticias_mercado as _buscar_noticias_mercado,
        buscar_noticias_setor as _buscar_noticias_setor,
        listar_decisoes,
        obter_resumo_mercado as _obter_resumo_mercado,
        resumo_performance,
        salvar_decisao,
    )

    B3_NEWS_OK = True
except ImportError as e:
    B3_NEWS_OK = False
    st.error(f"mcp-b3-news não encontrado: {e}")

try:
    import fundamentus
    FUNDAMENTUS_OK = True
except ImportError:
    FUNDAMENTUS_OK = False

try:
    import yfinance as yf
    import numpy as np
    import pandas as pd
    YFINANCE_OK = True
except ImportError:
    YFINANCE_OK = False

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.WARNING)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClaudeTrader — Analista B3",
    page_icon="📈",
    layout="wide",
)

# ── Modelos disponíveis ───────────────────────────────────────────────────────
# Prefixo "groq/" → usa Groq API (GROQ_API_KEY)
# Demais          → usa OpenRouter (OPEN_ROUTER)
MODELOS = {
    # ── Groq ──────────────────────────────────────────────────────────────────
    "⚡ Llama 3.3 70B (Groq)":      "groq/llama-3.3-70b-versatile",
    # ── OpenRouter premium ────────────────────────────────────────────────────
    "💎 Gemini 2.0 Flash":          "google/gemini-2.0-flash-001",
    "💎 Claude Sonnet 4.6":         "anthropic/claude-sonnet-4-6",
    "💎 GPT-4o":                    "openai/gpt-4o",
}

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""Você é um analista de swing trading da B3. Data: {datetime.now().strftime('%d/%m/%Y')}. Responda em português.

TOOLS: chame executar_screening para screening; analisar_acao(ticker) para ação individual; salvar_decisao SEMPRE após recomendar COMPRAR/MONITORAR/DESCARTAR.

Ao receber dados do executar_screening, gere relatório com estas seções exatas:

# Screening B3 — [data]
**Data:** [data] | **Universo analisado:** [N com gatilho] ([N aprovadas fundamentalista])
---
## Contexto de Mercado
[narrativa: RSI médio, tendência dominante, recomendação de tamanho de posição]
---
## Ranking Top 10 — Gatilhos de Entrada
### VERDE — Alta Convicção (Score >= 5.0)
| # | Ticker | Cotação | Gatilho | Tendência | RSI | ROE% | Mrg.EBIT% | Mrg.Liq% | Dív/Patr | P/VP | Var7d% | Var15d% | Score |
|---|--------|---------|---------|-----------|-----|------|-----------|----------|----------|------|--------|---------|-------|
[uma linha por ativo VERDE]
### AMARELO — Monitorar com Confirmação (Score 4.5–4.9)
| # | Ticker | Cotação | Gatilho | RSI | ROE% | Mrg.EBIT% | Score |
|---|--------|---------|---------|-----|------|-----------|-------|
[uma linha por ativo AMARELO]
---
## Destaques por Ativo
[Para top 5 VERDE + top 2 AMARELO: **TICKER — Nome Real da Empresa (Score X.XX)** seguido de parágrafo com pontos fortes, RSI, gatilho, risco e stop sugerido]
---
## Alertas Operacionais
[lista numerada com os alertas do campo ALERTAS dos dados]
---
## Metodologia
- **Filtro fundamentalista:** ROE>15%, Mrg.EBIT>10%, Mrg.Liq>10%, Dív/Patr<3x, P/VP>1 (Fundamentus)
- **Dados técnicos:** 3 meses yfinance, RSI(14) Wilder, gatilhos nos 3 últimos candles
- **Score:** Alta+3/Neutro+1, RSI 40-60+2, RSI<70+1, ROE normalizado"""

# ── Definição dos tools no formato OpenAI/OpenRouter ─────────────────────────
def _tool(name: str, description: str, parameters: dict) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters,
        },
    }


TOOLS = [
    _tool("obter_resumo_mercado",
          "Retorna resumo do mercado: IBOVESPA, dólar e manchetes do dia. Use no início de qualquer sessão.",
          {"type": "object", "properties": {}}),

    _tool("buscar_noticias_acao", "Notícias de uma ação da B3.",
          {"type": "object", "required": ["ticker"], "properties": {
              "ticker": {"type": "string"}, "limite": {"type": "integer", "default": 5}}}),

    _tool("buscar_noticias_mercado", "Notícias gerais do mercado brasileiro.",
          {"type": "object", "properties": {"limite": {"type": "integer", "default": 5}}}),

    _tool("buscar_noticias", "Busca notícias por palavra-chave.",
          {"type": "object", "required": ["query"], "properties": {
              "query": {"type": "string"}, "limite": {"type": "integer", "default": 5}}}),

    _tool("buscar_noticias_setor", "Notícias de um setor da B3.",
          {"type": "object", "required": ["setor"], "properties": {
              "setor": {"type": "string"}, "limite": {"type": "integer", "default": 5}}}),

    _tool("executar_screening", "Screening B3: fundamentalista + técnico. Retorna ranking com gatilhos.",
          {"type": "object", "properties": {
              "periodo": {"type": "string", "default": "3mo"},
              "limite_tecnicos": {"type": "integer", "default": 60}}}),

    _tool("analisar_acao", "Análise técnica e fundamentalista de uma ação (RSI, EMAs, gatilho).",
          {"type": "object", "required": ["ticker"], "properties": {
              "ticker": {"type": "string"}, "periodo": {"type": "string", "default": "3mo"}}}),

    _tool("salvar_decisao", "Salva decisão COMPRAR/MONITORAR/DESCARTAR. Chamar sempre após recomendar.",
          {"type": "object", "required": ["ticker", "acao", "preco_entrada", "gatilho", "justificativa", "confianca"],
           "properties": {
              "ticker": {"type": "string"}, "acao": {"type": "string"},
              "preco_entrada": {"type": "number"}, "gatilho": {"type": "string"},
              "justificativa": {"type": "string"}, "confianca": {"type": "number"},
              "stop_loss": {"type": "number"}, "setor": {"type": "string"},
              "tendencia": {"type": "string"}, "rsi": {"type": "number"}, "roe": {"type": "number"}}}),

    _tool("listar_decisoes", "Lista histórico de decisões salvas.",
          {"type": "object", "properties": {
              "ticker": {"type": "string"}, "status": {"type": "string"},
              "acao": {"type": "string"}, "limite": {"type": "integer", "default": 20}}}),

    _tool("atualizar_decisao", "Atualiza decisão com preço atual e status (FECHADA/STOP_ATINGIDO).",
          {"type": "object", "required": ["decisao_id", "preco_atual"], "properties": {
              "decisao_id": {"type": "integer"}, "preco_atual": {"type": "number"},
              "status": {"type": "string"}, "nota": {"type": "string"}}}),

    _tool("resumo_performance", "Relatório de performance das decisões.",
          {"type": "object", "properties": {}}),
]

# ── Funções de análise técnica ────────────────────────────────────────────────


def _calcular_rsi_wilder(closes: pd.Series, period: int = 14) -> float:
    closes = closes.dropna()
    if len(closes) < period + 1:
        return float("nan")

    deltas = closes.diff().dropna()
    gains = deltas.where(deltas > 0, 0.0)
    losses = -deltas.where(deltas < 0, 0.0)

    avg_gain = gains.iloc[:period].mean()
    avg_loss = losses.iloc[:period].mean()

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains.iloc[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses.iloc[i]) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def _calcular_ema(closes: pd.Series, period: int) -> float | None:
    if len(closes) < period:
        return None
    return float(closes.ewm(span=period, adjust=False).mean().iloc[-1])


def _calcular_tendencia(closes: pd.Series) -> str:
    ema8 = _calcular_ema(closes, 8)
    ema80 = _calcular_ema(closes, 80)
    sma200 = float(closes.rolling(200).mean().iloc[-1]) if len(closes) >= 200 else None

    if ema8 is None or ema80 is None:
        return "Nenhuma"

    if sma200 is not None:
        if ema8 > ema80 > sma200:
            return "Alta"
        if ema8 < ema80 < sma200:
            return "Baixa"

    if ema8 > ema80:
        return "Alta" if sma200 is None else "Neutro/Lateral"
    if ema8 < ema80:
        return "Baixa" if sma200 is None else "Neutro/Lateral"
    return "Neutro/Lateral"


def _detectar_gatilho(df: pd.DataFrame) -> str:
    if len(df) < 3:
        return "Nenhum"

    l0 = float(df["Low"].iloc[-1])
    l1 = float(df["Low"].iloc[-2])
    l2 = float(df["Low"].iloc[-3])
    h0 = float(df["High"].iloc[-1])
    h1 = float(df["High"].iloc[-2])

    if l0 < l1 < l2:
        return "Dave Landry"
    if l0 > l1 < l2:
        return "1-2-3"
    if l0 > l1 and h0 < h1:
        return "Inside Candle"
    return "Nenhum"


def _flatten_df(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def _baixar_ohlcv(ticker: str, periodo: str) -> pd.DataFrame | None:
    try:
        df = yf.download(f"{ticker}.SA", period=periodo, progress=False, auto_adjust=True)
        if df.empty:
            return None
        df = _flatten_df(df)
        df = df[df.index.dayofweek < 5]
        return df
    except Exception:
        return None


# ── Implementação dos tools ───────────────────────────────────────────────────


def _exec_obter_resumo_mercado() -> str:
    return asyncio.run(_obter_resumo_mercado())


def _exec_buscar_noticias_acao(ticker: str, limite: int = 5) -> str:
    return asyncio.run(_buscar_noticias_acao(ticker, limite))


def _exec_buscar_noticias_mercado(limite: int = 5) -> str:
    return asyncio.run(_buscar_noticias_mercado(limite))


def _exec_buscar_noticias(query: str, limite: int = 5) -> str:
    return asyncio.run(_buscar_noticias(query, limite))


def _exec_buscar_noticias_setor(setor: str, limite: int = 5) -> str:
    return asyncio.run(_buscar_noticias_setor(setor, limite))


def _exec_executar_screening(
    periodo: str = "3mo",
    setor: str | None = None,
    limite_tecnicos: int = 60,
) -> str:
    if not FUNDAMENTUS_OK:
        return "fundamentus não instalado."
    if not YFINANCE_OK:
        return "yfinance não instalado."

    try:
        df = fundamentus.get_resultado()
    except Exception as e:
        return f"Erro Fundamentus: {e}"

    try:
        df_filt = df[
            (df["roe"] > 0.15)
            & (df["mrgebit"] > 0.10)
            & (df["mrgliq"] > 0.10)
            & (df["divbpatr"] < 3.0)
            & (df["pvp"] > 1.0)
            & (df["liq2m"] > 100000)
        ].copy()
    except KeyError as e:
        return f"Erro de coluna: {e}"

    if df_filt.empty:
        return "Nenhuma ação aprovada no filtro fundamentalista."

    total_fund = len(df_filt)
    df_filt = df_filt.sort_values("roe", ascending=False).head(limite_tecnicos)

    candidatos: list[dict] = []
    sem_gatilho: list[dict] = []
    erros = 0

    for ticker in df_filt.index:
        try:
            df_ohlcv = _baixar_ohlcv(ticker, periodo)
            if df_ohlcv is None or len(df_ohlcv) < 20:
                erros += 1
                continue

            closes   = df_ohlcv["Close"]
            volumes  = df_ohlcv["Volume"]
            rsi      = _calcular_rsi_wilder(closes)
            tendencia = _calcular_tendencia(closes)
            gatilho  = _detectar_gatilho(df_ohlcv)

            row = df_filt.loc[ticker]
            cotacao     = round(float(closes.iloc[-1]), 2)
            roe_pct     = round(float(row["roe"])      * 100, 1)
            mrgebit_pct = round(float(row["mrgebit"])  * 100, 1)
            mrgliq_pct  = round(float(row["mrgliq"])   * 100, 1)
            divbpatr    = round(float(row["divbpatr"]),  2)
            pvp         = round(float(row["pvp"]),       2)
            liq2m       = round(float(row["liq2m"]) / 1e6, 1)

            var7d  = round(((closes.iloc[-1] / closes.iloc[-7])  - 1) * 100, 1) if len(closes) >= 7  else 0.0
            var15d = round(((closes.iloc[-1] / closes.iloc[-15]) - 1) * 100, 1) if len(closes) >= 15 else 0.0
            var30d = round(((closes.iloc[-1] / closes.iloc[-30]) - 1) * 100, 1) if len(closes) >= 30 else 0.0

            vol_medio20 = float(volumes.iloc[-20:].mean()) if len(volumes) >= 20 else float(volumes.mean())
            vol_rel = round(float(volumes.iloc[-1]) / vol_medio20, 2) if vol_medio20 > 0 else 1.0

            ema8  = _calcular_ema(closes, 8)
            ema80 = _calcular_ema(closes, 80)

            score = 0.0
            if tendencia == "Alta":
                score += 3
            elif tendencia in ("Neutro/Lateral",):
                score += 1
            if 40 <= rsi <= 60:
                score += 2
            if rsi < 70:
                score += 1
            score += min(roe_pct, 30) / 10

            record = {
                "ticker":    ticker,
                "cotacao":   cotacao,
                "gatilho":   gatilho,
                "tendencia": tendencia,
                "rsi":       round(rsi, 1),
                "roe":       roe_pct,
                "mrgebit":   mrgebit_pct,
                "mrgliq":    mrgliq_pct,
                "divbpatr":  divbpatr,
                "pvp":       pvp,
                "var7d":     var7d,
                "var15d":    var15d,
                "var30d":    var30d,
                "liq2m":     liq2m,
                "vol_rel":   vol_rel,
                "ema8":      round(ema8, 2) if ema8 else None,
                "ema80":     round(ema80, 2) if ema80 else None,
                "score":     round(score, 2),
            }

            if gatilho != "Nenhum":
                candidatos.append(record)
            else:
                sem_gatilho.append(record)

        except Exception:
            erros += 1
            continue

    if not candidatos:
        return (
            f"Nenhuma ação com gatilho ativo. "
            f"Analisadas: {len(df_filt)} | Erros: {erros}"
        )

    candidatos.sort(key=lambda r: r["score"], reverse=True)
    sem_gatilho.sort(key=lambda r: r["score"], reverse=True)

    verdes   = [r for r in candidatos if r["score"] >= 5.0]
    amarelos = [r for r in candidatos if 4.5 <= r["score"] < 5.0]

    todos_rsi   = [r["rsi"] for r in candidatos]
    rsi_medio   = round(sum(todos_rsi) / len(todos_rsi), 1) if todos_rsi else 0
    rsi_min     = round(min(todos_rsi), 1) if todos_rsi else 0
    rsi_max     = round(max(todos_rsi), 1) if todos_rsi else 0
    n_alta      = sum(1 for r in candidatos if r["tendencia"] == "Alta")
    n_neutro    = sum(1 for r in candidatos if "Neutro" in r["tendencia"])
    n_baixa     = sum(1 for r in candidatos if r["tendencia"] == "Baixa")
    n_nenhuma   = sum(1 for r in candidatos if r["tendencia"] == "Nenhuma")
    gatilhos_cnt = {}
    for r in candidatos:
        gatilhos_cnt[r["gatilho"]] = gatilhos_cnt.get(r["gatilho"], 0) + 1

    L = []
    L.append(f"DATA_SCREENING: {datetime.now().strftime('%d/%m/%Y')}")
    L.append(f"UNIVERSO: {total_fund} aprovadas no filtro fundamentalista | {len(df_filt)} analisadas tecnicamente | {len(candidatos)} com gatilho")
    L.append(f"PERIODO_DADOS: {periodo}")
    L.append("")
    L.append(f"MERCADO: RSI_medio={rsi_medio} range={rsi_min}-{rsi_max} | Alta={n_alta} Neutro={n_neutro} Baixa={n_baixa} Nenhuma={n_nenhuma}")
    L.append(f"GATILHOS: {' '.join(f'{k}={v}' for k, v in gatilhos_cnt.items())}")
    L.append("")

    L.append("VERDE(score>=5.0):")
    L.append("i|ticker|cotacao|gatilho|tend|rsi|roe|ebit|liq|div|pvp|v7d|v15d|v30d|liqM|score")
    for i, r in enumerate(verdes[:12], 1):
        L.append(
            f"{i}|{r['ticker']}|{r['cotacao']:.2f}|{r['gatilho']}|{r['tendencia']}|"
            f"{r['rsi']}|{r['roe']}|{r['mrgebit']}|{r['mrgliq']}|"
            f"{r['divbpatr']}|{r['pvp']}|{r['var7d']:+.1f}%|{r['var15d']:+.1f}%|"
            f"{r['var30d']:+.1f}%|{r['liq2m']}|{r['score']}"
        )
    L.append("")

    L.append("AMARELO(4.5<=score<5.0):")
    L.append("i|ticker|cotacao|gatilho|rsi|roe|ebit|score")
    offset = len(verdes[:12]) + 1
    for i, r in enumerate(amarelos[:8], offset):
        L.append(f"{i}|{r['ticker']}|{r['cotacao']:.2f}|{r['gatilho']}|{r['rsi']}|{r['roe']}|{r['mrgebit']}|{r['score']}")
    L.append("")

    if sem_gatilho:
        monitorar_str = " | ".join(f"{r['ticker']} RSI={r['rsi']} ROE={r['roe']}%" for r in sem_gatilho[:3])
        L.append(f"MONITORAR(sem_gatilho): {monitorar_str}")
        L.append("")

    alertas = []
    vistos: dict[str, list[str]] = {}
    for r in candidatos:
        vistos.setdefault(r["ticker"][:4], []).append(r["ticker"])
    for grupo in vistos.values():
        if len(grupo) > 1:
            alertas.append(f"Duplicados: {', '.join(grupo)}")
    baixa_liq = [r["ticker"] for r in candidatos if r["liq2m"] < 1.0]
    if baixa_liq:
        alertas.append(f"Baixa liquidez: {', '.join(baixa_liq)}")
    alto_rsi_t = [r["ticker"] for r in candidatos if r["rsi"] > 65]
    if alto_rsi_t:
        alertas.append(f"RSI>65: {', '.join(alto_rsi_t)}")
    if n_alta == 0:
        alertas.append("Nenhuma ação com tendência Alta — reduzir posição 30-50%")

    if alertas:
        L.append("ALERTAS: " + " | ".join(alertas))
        L.append("")

    L.append(f"METODOLOGIA: ROE>15% MrgEBIT>10% MrgLiq>10% Div<3x PVP>1 | {periodo} yfinance | RSI Wilder | Score=Alta+3/Neutro+1/RSI40-60+2/<70+1/ROE_norm")

    return "\n".join(L)


def _exec_analisar_acao(ticker: str, periodo: str = "3mo") -> str:
    ticker = ticker.upper().replace(".SA", "").strip()

    if not FUNDAMENTUS_OK or not YFINANCE_OK:
        return "fundamentus ou yfinance não instalados."

    df_ohlcv = _baixar_ohlcv(ticker, periodo)
    if df_ohlcv is None or len(df_ohlcv) < 10:
        return f"Sem dados históricos suficientes para {ticker}.SA no período {periodo}."

    closes = df_ohlcv["Close"]
    cotacao = float(closes.iloc[-1])
    data_cotacao = closes.index[-1].strftime("%d/%m/%Y")

    rsi = _calcular_rsi_wilder(closes)
    tendencia = _calcular_tendencia(closes)
    gatilho = _detectar_gatilho(df_ohlcv)

    ema8 = _calcular_ema(closes, 8)
    ema80 = _calcular_ema(closes, 80)
    sma200 = float(closes.rolling(200).mean().iloc[-1]) if len(closes) >= 200 else None

    var7d = round(((closes.iloc[-1] / closes.iloc[-7]) - 1) * 100, 1) if len(closes) >= 7 else None
    var15d = round(((closes.iloc[-1] / closes.iloc[-15]) - 1) * 100, 1) if len(closes) >= 15 else None
    var30d = round(((closes.iloc[-1] / closes.iloc[-30]) - 1) * 100, 1) if len(closes) >= 30 else None

    rsi_interp = "Sobrecomprado ⚠️" if rsi > 70 else ("Sobrevendido" if rsi < 30 else "Neutro")

    linhas = [f"## Análise: {ticker}\n"]
    linhas.append(f"**Cotação:** R${cotacao:.2f} | **Data:** {data_cotacao}\n")

    linhas.append("### Análise Técnica")
    linhas.append(f"- **Tendência:** {tendencia}")
    if ema8:
        linhas.append(f"  - EMA(8): R${ema8:.2f}")
    if ema80:
        linhas.append(f"  - EMA(80): R${ema80:.2f}")
    if sma200:
        linhas.append(f"  - SMA(200): R${sma200:.2f}")
    linhas.append(f"- **RSI(14):** {rsi} → {rsi_interp}")
    linhas.append(f"- **Gatilho:** {gatilho}")
    if var7d is not None:
        linhas.append(f"- **Variação:** 7d: {var7d:+.1f}% | 15d: {var15d:+.1f}% | 30d: {var30d:+.1f}%")

    try:
        df_all = fundamentus.get_resultado()
        if ticker in df_all.index:
            row = df_all.loc[ticker]
            roe_pct = float(row["roe"]) * 100
            mrgebit_pct = float(row["mrgebit"]) * 100
            mrgliq_pct = float(row["mrgliq"]) * 100
            divbpatr = float(row["divbpatr"])
            pvp = float(row["pvp"])

            def check(ok: bool) -> str:
                return "✅" if ok else "❌"

            linhas.append("\n### Filtro Fundamentalista")
            linhas.append("| Critério | Valor | Threshold | Status |")
            linhas.append("|----------|-------|-----------|--------|")
            linhas.append(f"| ROE | {roe_pct:.1f}% | > 15% | {check(roe_pct > 15)} |")
            linhas.append(f"| Margem EBIT | {mrgebit_pct:.1f}% | > 10% | {check(mrgebit_pct > 10)} |")
            linhas.append(f"| Margem Líquida | {mrgliq_pct:.1f}% | > 10% | {check(mrgliq_pct > 10)} |")
            linhas.append(f"| Dívida/Patrimônio | {divbpatr:.2f}x | < 3x | {check(divbpatr < 3)} |")
            linhas.append(f"| P/VP | {pvp:.2f}x | > 1x | {check(pvp > 1)} |")
    except Exception as e:
        linhas.append(f"\n*Dados fundamentalistas não disponíveis: {e}*")

    return "\n".join(linhas)


# ── Dispatcher de tools ───────────────────────────────────────────────────────


def execute_tool(name: str, inputs: dict) -> str:
    try:
        if name == "obter_resumo_mercado":
            return _exec_obter_resumo_mercado()
        if name == "buscar_noticias_acao":
            return _exec_buscar_noticias_acao(**inputs)
        if name == "buscar_noticias_mercado":
            return _exec_buscar_noticias_mercado(**inputs)
        if name == "buscar_noticias":
            return _exec_buscar_noticias(**inputs)
        if name == "buscar_noticias_setor":
            return _exec_buscar_noticias_setor(**inputs)
        if name == "executar_screening":
            return _exec_executar_screening(**inputs)
        if name == "analisar_acao":
            return _exec_analisar_acao(**inputs)
        if name == "salvar_decisao":
            return salvar_decisao(**inputs)
        if name == "listar_decisoes":
            return listar_decisoes(**inputs)
        if name == "atualizar_decisao":
            return atualizar_decisao(**inputs)
        if name == "resumo_performance":
            return resumo_performance()
        return f"Tool desconhecida: {name}"
    except Exception as e:
        return f"Erro ao executar '{name}': {type(e).__name__}: {e}"


# ── Helpers de API ────────────────────────────────────────────────────────────

def get_api_key(key_name: str) -> str:
    """Busca chave de API em st.secrets (Streamlit Cloud) ou variáveis de ambiente (local)."""
    try:
        return st.secrets[key_name]
    except (KeyError, FileNotFoundError):
        api_key = os.environ.get(key_name)
        if not api_key:
            st.error(f"❌ {key_name} não encontrada. Configure em Secrets do Streamlit Cloud ou no arquivo .env")
            st.stop()
        return api_key


def get_client(model: str) -> OpenAI:
    if model.startswith("groq/"):
        return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=get_api_key("GROQ_API_KEY"))
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=get_api_key("OPEN_ROUTER"))


def chat(client: OpenAI, messages: list[dict], model: str, temperature: float = 0.0) -> tuple[str, list[dict]]:
    tool_log: list[dict] = []
    api_model = model.removeprefix("groq/")
    full_messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    while True:
        response = client.chat.completions.create(
            model=api_model,
            messages=full_messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=config.MAX_TOKENS,
            temperature=temperature,
        )

        choice = response.choices[0]
        msg = choice.message

        if choice.finish_reason == "stop" or not msg.tool_calls:
            text = msg.content or ""
            messages.append({"role": "assistant", "content": text})
            return text, tool_log

        assistant_dict: dict = {
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ],
        }
        messages.append(assistant_dict)
        full_messages.append(assistant_dict)

        for tc in msg.tool_calls:
            inputs = json.loads(tc.function.arguments)
            tool_log.append({"name": tc.function.name, "input": inputs})
            result = execute_tool(tc.function.name, inputs)
            tool_result = {"role": "tool", "tool_call_id": tc.id, "content": result}
            messages.append(tool_result)
            full_messages.append(tool_result)


# ── Guia de Funcionalidades ───────────────────────────────────────────────────

def _render_guia() -> None:
    st.markdown("## 📚 Guia de Funcionalidades")
    st.markdown(
        "O **ClaudeTrader** combina filtros fundamentalistas, análise técnica (RSI Wilder, EMAs, gatilhos) "
        "e notícias em tempo real para identificar oportunidades de swing trade na B3. "
        "Basta descrever seu caso no chat — o analista identifica automaticamente qual ferramenta usar."
    )

    st.divider()

    with st.expander("📊 Screening B3 — ranking completo de gatilhos de entrada", expanded=True):
        st.markdown(
            """
**O que faz:** Aplica filtro fundamentalista em toda a B3, depois análise técnica nas aprovadas, e retorna ranking por score com gatilhos de entrada.

**Pipeline:**
1. Filtra por ROE > 15%, Mrg.EBIT > 10%, Mrg.Líquida > 10%, Dív/Patr < 3x, P/VP > 1
2. Baixa 3 meses de OHLCV via yfinance para as top ROE
3. Calcula RSI Wilder(14), EMAs (8/80) e SMA(200)
4. Detecta gatilhos nos últimos 3 candles
5. Calcula score e classifica Verde (≥ 5.0) ou Amarelo (4.5–4.9)

**Score:**

| Critério | Pontos |
|---|---|
| Tendência Alta (EMA8 > EMA80 > SMA200) | +3 |
| Tendência Neutro/Lateral | +1 |
| RSI entre 40 e 60 | +2 |
| RSI abaixo de 70 | +1 |
| ROE normalizado (até 30%) | +0 a +3 |

**Quando usar:** Toda semana para identificar as melhores oportunidades de entrada.

**Exemplo de pergunta:**
> *"Faça um screening completo da B3 agora."*
"""
        )

    with st.expander("🔍 Análise Individual — mergulhe em uma ação específica"):
        st.markdown(
            """
**O que faz:** Análise técnica e fundamentalista completa de uma ação, com tendência, RSI, gatilho e todos os indicadores fundamentalistas.

**Indicadores técnicos:**
- **RSI(14) Wilder** — sobrecomprado (> 70), neutro (30–70), sobrevendido (< 30)
- **EMA(8) e EMA(80)** — direção da tendência de curto e médio prazo
- **SMA(200)** — tendência de longo prazo (quando disponível)
- **Gatilho** — Dave Landry, 1-2-3 ou Inside Candle nos últimos 3 candles
- **Variação** — 7, 15 e 30 dias

**Gatilhos detectados:**

| Gatilho | Padrão (últimos 3 candles) | Significado |
|---|---|---|
| Dave Landry | Mínima[0] < Mínima[1] < Mínima[2] | 3 mínimas consecutivamente mais baixas |
| 1-2-3 | Mínima[0] > Mínima[1] < Mínima[2] | Fundo com recuperação |
| Inside Candle | Mín[0] > Mín[1] e Máx[0] < Máx[1] | Candle dentro do anterior |

**Quando usar:** Antes de tomar uma decisão de compra ou para monitorar uma posição específica.

**Exemplo de pergunta:**
> *"Analise WEGE3 para mim."*
> *"Como está PETR4 tecnicamente?"*
"""
        )

    with st.expander("📰 Notícias — mercado, ações e setores em tempo real"):
        st.markdown(
            """
**O que faz:** Busca notícias financeiras via RSS de InfoMoney, Valor Econômico, Investing.com BR e B3 Notícias.

**Tipos de busca disponíveis:**

| Ferramenta | Uso | Exemplo |
|---|---|---|
| Resumo de mercado | Visão geral do dia | "Qual o resumo do mercado hoje?" |
| Notícias por ação | Notícias de um ticker | "Notícias de VALE3" |
| Notícias por setor | Setor específico | "O que está acontecendo no setor bancário?" |
| Busca por palavra-chave | Tema livre | "Notícias sobre juros e Selic" |
| Notícias gerais | Manchetes do momento | "Principais notícias do mercado" |

**Quando usar:** Antes de uma decisão de compra, para verificar se há eventos corporativos ou macroeconômicos relevantes.

**Exemplo de pergunta:**
> *"Tem alguma notícia ruim sobre ITUB4 que explique a queda?"*
"""
        )

    with st.expander("💾 Registro de Decisões — acompanhe suas operações"):
        st.markdown(
            """
**O que faz:** Salva, lista e atualiza decisões de COMPRAR / MONITORAR / DESCARTAR com preço, gatilho, stop sugerido e justificativa. O analista salva automaticamente após cada recomendação.

**Campos registrados:**
- Ticker, ação (COMPRAR/MONITORAR/DESCARTAR), preço de entrada
- Gatilho detectado, tendência, RSI, ROE
- Stop loss sugerido, setor, justificativa
- Confiança (0–10)

**Operações disponíveis:**

| Operação | Exemplo |
|---|---|
| Salvar decisão | Automático após recomendação |
| Listar decisões | "Liste minhas posições abertas" |
| Filtrar por ticker | "Mostre histórico de WEGE3" |
| Atualizar (fechada/stop) | "Fechei PETR4 a R$ 38,50" |

**Armazenamento:** `.claude/memory/investment-decisions/decisions.json`

**Exemplo de pergunta:**
> *"Liste minhas posições abertas."*
> *"Stop atingido em ITUB4 a R$ 32,00."*
"""
        )

    with st.expander("📈 Performance — resultado das suas decisões"):
        st.markdown(
            """
**O que faz:** Gera relatório consolidado de todas as decisões registradas, com resultado por operação e resumo geral.

**O relatório inclui:**
- Total de operações por ação (COMPRAR / MONITORAR / DESCARTAR)
- Operações fechadas vs abertas
- Resultado percentual das operações encerradas
- Alertas de stop atingido

**Quando usar:** Periodicamente para avaliar a taxa de acerto e calibrar a estratégia de entrada.

**Exemplo de pergunta:**
> *"Mostre meu relatório de performance."*
> *"Como estão minhas operações da última semana?"*
"""
        )

    st.divider()

    st.markdown("### ⚙️ Ferramentas — Quando São Acionadas Automaticamente")
    st.info(
        "O analista aciona as ferramentas **automaticamente** quando você fornece os dados necessários. "
        "Você não precisa saber o nome da ferramenta — basta descrever o que quer."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dados que acionam cada ferramenta:**")
        st.markdown(
            """
- **Screening** → "faça um screening" ou "quais ações têm gatilho hoje"
- **Análise individual** → ticker + "analise" ou "como está"
- **Notícias** → ticker/setor + "notícias" ou "o que está acontecendo"
- **Salvar decisão** → após recomendar COMPRAR/MONITORAR/DESCARTAR (automático)
- **Listar decisões** → "posições abertas" ou "histórico de X"
- **Performance** → "relatório de performance" ou "resultado das operações"
"""
        )
    with col2:
        st.markdown("**O que o analista entrega:**")
        st.markdown(
            """
- Ranking VERDE/AMARELO com score e gatilho
- Análise técnica completa (RSI, EMAs, tendência, variações)
- Filtro fundamentalista com thresholds
- Notícias contextuais por ação/setor
- Registro automático de decisões com stop sugerido
- Relatório de performance consolidado
"""
        )

    st.divider()

    st.markdown("### 📌 Regras Operacionais")
    st.warning(
        "**Stop loss é obrigatório.** Toda decisão de COMPRAR deve ter stop definido. "
        "Se o analista não sugerir, peça explicitamente antes de entrar na operação."
    )
    st.markdown(
        """
1. Use temperatura 0.0 para análises — respostas determinísticas e precisas
2. Faça screening semanalmente, de preferência na segunda-feira antes da abertura
3. Confirme o gatilho no gráfico antes de executar a ordem
4. RSI > 70 indica sobrecompra — evite entrar em posições novas
5. Reduza posição em 30–50% quando nenhuma ação estiver em tendência de alta
"""
    )


# ── Histórico de Interações ───────────────────────────────────────────────────

def _render_historico(messages: list[dict]) -> None:
    st.markdown("## 🕐 Histórico de Interações")

    interacoes = [m for m in messages if m["role"] in ("user", "assistant")]
    if not interacoes:
        st.info("Nenhuma interação registrada nesta sessão. Inicie uma conversa na aba Chat.")
        return

    total_user = sum(1 for m in interacoes if m["role"] == "user")
    total_tools = sum(len(m.get("tool_log", [])) for m in interacoes if m["role"] == "assistant")

    col1, col2, col3 = st.columns(3)
    col1.metric("Mensagens", len(interacoes))
    col2.metric("Perguntas", total_user)
    col3.metric("Ferramentas utilizadas", total_tools)

    st.divider()

    pares: list[tuple[dict, dict | None]] = []
    i = 0
    while i < len(interacoes):
        if interacoes[i]["role"] == "user":
            pergunta = interacoes[i]
            resposta = interacoes[i + 1] if i + 1 < len(interacoes) and interacoes[i + 1]["role"] == "assistant" else None
            pares.append((pergunta, resposta))
            i += 2 if resposta else 1
        else:
            i += 1

    for idx, (pergunta, resposta) in enumerate(reversed(pares), 1):
        n = len(pares) - idx + 1
        ferramentas = resposta.get("tool_log", []) if resposta else []
        label = f"**#{n}** — {pergunta['content'][:80]}{'…' if len(pergunta['content']) > 80 else ''}"
        if ferramentas:
            label += f"  🔧 *{len(ferramentas)} ferramenta(s)*"

        with st.expander(label):
            st.markdown("**Pergunta:**")
            st.markdown(f"> {pergunta['content']}")

            if resposta:
                st.markdown("**Resposta:**")
                st.markdown(resposta["content"])

                if ferramentas:
                    st.markdown("**Ferramentas utilizadas:**")
                    for t in ferramentas:
                        st.code(
                            f"{t['name']}({json.dumps(t['input'], ensure_ascii=False, indent=2)})",
                            language="python",
                        )
            else:
                st.warning("Resposta não disponível.")

    st.divider()
    if st.button("📋 Copiar histórico como texto", key="copy_hist"):
        linhas = []
        for idx, (p, r) in enumerate(pares, 1):
            linhas.append(f"## Interação {idx}")
            linhas.append(f"**Pergunta:** {p['content']}")
            if r:
                linhas.append(f"**Resposta:** {r['content']}")
            linhas.append("")
        st.text_area("Histórico em texto:", value="\n".join(linhas), height=300, key="hist_text")


# ── UI ────────────────────────────────────────────────────────────────────────


def main() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "quick_action" not in st.session_state:
        st.session_state.quick_action = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "selected_model_name" not in st.session_state:
        st.session_state.selected_model_name = "💎 Gemini 2.0 Flash"
    if "temperatura" not in st.session_state:
        st.session_state.temperatura = 0.0

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.title("📈 ClaudeTrader")
        st.caption("Analista de Swing Trade B3")

        st.divider()

        st.markdown("### Modelo LLM")
        selected_model_name = st.selectbox(
            "Escolha o modelo:",
            options=list(MODELOS.keys()),
            index=list(MODELOS.keys()).index(st.session_state.selected_model_name),
            key="model_selector",
        )
        st.session_state.selected_model_name = selected_model_name
        selected_model = MODELOS[selected_model_name]

        st.markdown("### Temperatura")
        temperatura = st.slider(
            "Criatividade / precisão:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperatura,
            step=0.05,
            key="temp_slider",
            help=(
                "0.0 = respostas determinísticas e precisas (ideal para análises)\n"
                "0.5 = equilíbrio entre precisão e fluidez\n"
                "1.0 = respostas mais criativas e variadas"
            ),
        )
        st.session_state.temperatura = temperatura
        _label_temp = "🎯 Preciso" if temperatura <= 0.2 else ("⚖️ Equilibrado" if temperatura <= 0.6 else "🎨 Criativo")
        st.caption(f"{_label_temp} — temperatura {temperatura:.2f}")

        st.divider()

        st.markdown("### Ações Rápidas")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Screening", use_container_width=True):
                st.session_state.quick_action = "Faça um screening completo da B3 agora."
        with col2:
            if st.button("📰 Mercado", use_container_width=True):
                st.session_state.quick_action = "Qual o resumo do mercado hoje?"

        col3, col4 = st.columns(2)
        with col3:
            if st.button("📋 Posições", use_container_width=True):
                st.session_state.quick_action = "Liste minhas posições abertas."
        with col4:
            if st.button("📈 Performance", use_container_width=True):
                st.session_state.quick_action = "Mostre meu relatório de performance."

        st.divider()

        st.markdown("### Exemplos de Perguntas")
        st.markdown(
            """
- *Analise WEGE3 para mim*
- *Ações do setor de energia com gatilho*
- *Fechei PETR4 a R$38,50*
- *Stop atingido em ITUB4*
- *Quais ações da lista TAEE posso comprar?*
"""
        )

        st.divider()

        if st.button("🗑️ Limpar conversa", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

        st.divider()
        st.markdown("**Status**")
        st.markdown(f"{'✅' if FUNDAMENTUS_OK else '❌'} fundamentus")
        st.markdown(f"{'✅' if YFINANCE_OK else '❌'} yfinance")
        st.markdown(f"{'✅' if B3_NEWS_OK else '❌'} mcp-b3-news")
        st.caption(f"Modelo: {selected_model_name}  \nData: {datetime.now().strftime('%d/%m/%Y')}")

    # ── Header ────────────────────────────────────────────────────────────────
    st.title("📈 ClaudeTrader — Analista B3")
    st.caption(
        "Combina filtros fundamentalistas, análise técnica (RSI Wilder, EMAs, gatilhos) "
        "e notícias em tempo real para identificar oportunidades de swing trade na B3."
    )

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_chat, tab_guia, tab_hist = st.tabs(["💬 Chat", "📚 Guia de Funcionalidades", "🕐 Histórico"])

    with tab_guia:
        _render_guia()

    with tab_hist:
        _render_historico(st.session_state.messages)

    with tab_chat:
        if not st.session_state.messages:
            with st.chat_message("assistant"):
                st.markdown(
                    "Olá! Sou o **ClaudeTrader**, seu analista de swing trade especializado na B3.\n\n"
                    "Posso:\n"
                    "- 📊 Fazer **screening completo** da B3 com filtros fundamentalistas + gatilhos técnicos\n"
                    "- 🔍 **Analisar ações individuais** (RSI, tendência, gatilho, fundamentos)\n"
                    "- 📰 Buscar **notícias** de ações e setores\n"
                    "- 💾 Registrar e acompanhar suas **decisões de investimento**\n\n"
                    "Como posso ajudar hoje? Pode perguntar sobre uma ação específica ou pedir um screening."
                )

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("tool_log"):
                    with st.expander(f"🔧 {len(msg['tool_log'])} ferramenta(s) utilizada(s)"):
                        for t in msg["tool_log"]:
                            st.code(f"{t['name']}({json.dumps(t['input'], ensure_ascii=False)})", language="python")

        user_input = st.chat_input("Digite sua pergunta sobre ações da B3...")

        if st.session_state.quick_action:
            user_input = st.session_state.quick_action
            st.session_state.quick_action = None

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.chat_messages.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                with st.spinner("Analisando..."):
                    try:
                        client = get_client(selected_model)
                        response_text, tool_log = chat(
                            client,
                            st.session_state.chat_messages,
                            selected_model,
                            temperature=st.session_state.temperatura,
                        )
                    except Exception as e:
                        response_text = f"Erro ao comunicar com a API: {type(e).__name__}: {e}"
                        tool_log = []

                st.markdown(response_text)

                if tool_log:
                    with st.expander(f"🔧 {len(tool_log)} ferramenta(s) utilizada(s)"):
                        for t in tool_log:
                            st.code(
                                f"{t['name']}({json.dumps(t['input'], ensure_ascii=False)})",
                                language="python",
                            )

            st.session_state.messages.append(
                {"role": "assistant", "content": response_text, "tool_log": tool_log}
            )


if __name__ == "__main__":
    main()
