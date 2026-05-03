"""
MCP Server — Notícias do Mercado Financeiro Brasileiro (B3) + Memória de Decisões

Fontes de notícias:
  - InfoMoney      (infomoney.com.br)   — RSS + scraping por ação
  - Valor Econômico (valor.com.br)      — RSS gratuito
  - Investing.com BR                    — busca de notícias
  - Status Invest   (statusinvest.com.br) — dados e notícias por ação

Memória de decisões:
  - Armazena recomendações em JSON no diretório DECISIONS_DIR
  - Permite consultar histórico, validar e auditar decisões passadas
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import feedparser
import httpx
from bs4 import BeautifulSoup
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# ─────────────────────────────── constants ───────────────────────────────────

# ─────────────────────────────── decisions storage ───────────────────────────

DECISIONS_DIR = Path(
    os.environ.get(
        "B3_DECISIONS_DIR",
        Path(__file__).parent.parent / ".claude" / "memory" / "investment-decisions",
    )
)
DECISIONS_DIR.mkdir(parents=True, exist_ok=True)
DECISIONS_FILE = DECISIONS_DIR / "decisions.json"


def _load_decisions() -> list[dict]:
    if not DECISIONS_FILE.exists():
        return []
    try:
        return json.loads(DECISIONS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _save_decisions(decisions: list[dict]) -> None:
    DECISIONS_FILE.write_text(
        json.dumps(decisions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _next_id(decisions: list[dict]) -> int:
    return max((d.get("id", 0) for d in decisions), default=0) + 1


# ─────────────────────────────── constants ───────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}

TIMEOUT = httpx.Timeout(15.0)

# RSS feeds confiáveis — acesso gratuito, sem paywall
RSS_FEEDS = {
    "infomoney_mercados": "https://www.infomoney.com.br/mercados/feed/",
    "infomoney_acoes":    "https://www.infomoney.com.br/acoes/feed/",
    "infomoney_economia": "https://www.infomoney.com.br/economia/feed/",
    "infomoney_geral":    "https://www.infomoney.com.br/feed/",
    "valor_economico":    "https://valor.globo.com/rss/financas/",
    "investing_br":       "https://br.investing.com/rss/news.rss",
    "b3_noticias":        "https://www.b3.com.br/pt_br/noticias/rss.htm",
}

# ─────────────────────────────── helpers ─────────────────────────────────────


def _clean_html(text: str) -> str:
    """Remove tags HTML e normaliza espaços."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def _fmt_date(entry: Any) -> str:
    if hasattr(entry, "published"):
        return entry.published
    if hasattr(entry, "updated"):
        return entry.updated
    return "Data desconhecida"


def _parse_feed(url: str, limite: int) -> list[dict]:
    """Lê um feed RSS e retorna lista de itens normalizados."""
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:limite]:
        items.append(
            {
                "titulo": _clean_html(entry.get("title", "")),
                "resumo": _clean_html(entry.get("summary", entry.get("description", ""))),
                "link":   entry.get("link", ""),
                "data":   _fmt_date(entry),
                "fonte":  feed.feed.get("title", url),
            }
        )
    return items


def _fmt_noticias(items: list[dict], titulo_secao: str) -> str:
    if not items:
        return f"## {titulo_secao}\nNenhuma notícia encontrada.\n"

    linhas = [f"## {titulo_secao}\n"]
    for i, n in enumerate(items, 1):
        linhas.append(f"### {i}. {n['titulo']}")
        linhas.append(f"**Fonte:** {n['fonte']} | **Data:** {n['data']}")
        if n["resumo"]:
            linhas.append(f"{n['resumo'][:400]}{'...' if len(n['resumo']) > 400 else ''}")
        linhas.append(f"**Link:** {n['link']}")
        linhas.append("")
    return "\n".join(linhas)


# ─────────────────────────────── tools ───────────────────────────────────────


async def buscar_noticias_mercado(limite: int = 10) -> str:
    """
    Retorna as últimas notícias gerais do mercado financeiro brasileiro.
    Combina InfoMoney (mercados + economia) e Valor Econômico.
    """
    feeds_a_usar = [
        RSS_FEEDS["infomoney_mercados"],
        RSS_FEEDS["infomoney_economia"],
        RSS_FEEDS["valor_economico"],
    ]

    items: list[dict] = []
    for url in feeds_a_usar:
        try:
            items.extend(_parse_feed(url, limite))
        except Exception:
            continue

    # Deduplica por título e limita
    vistos: set[str] = set()
    unicos: list[dict] = []
    for item in items:
        chave = item["titulo"].lower()[:60]
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(item)
        if len(unicos) >= limite:
            break

    unicos = unicos[:limite]
    return _fmt_noticias(unicos, f"Notícias do Mercado Financeiro Brasileiro — {datetime.now().strftime('%d/%m/%Y %H:%M')}")


async def buscar_noticias_acao(ticker: str, limite: int = 10) -> str:
    """
    Busca notícias de uma ação específica da B3.
    Usa InfoMoney (página da ação) e Status Invest.

    Args:
        ticker: Código da ação sem sufixo (ex: PETR4, WEGE3, ITUB4)
        limite: Número máximo de notícias (padrão 10)
    """
    ticker = ticker.upper().replace(".SA", "").strip()
    results: list[dict] = []

    async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT, follow_redirects=True) as client:

        # ── InfoMoney: página da ação ──────────────────────────────────────
        try:
            url_im = f"https://www.infomoney.com.br/{ticker.lower()}/"
            resp = await client.get(url_im)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                # Notícias na sidebar / feed da ação
                for article in soup.select("article.item-news, div.card-news, div.news-item")[:limite]:
                    titulo_tag = article.select_one("h3, h4, .title, a")
                    link_tag   = article.select_one("a[href]")
                    data_tag   = article.select_one("time, .date, .meta-date")
                    resumo_tag = article.select_one("p, .description, .excerpt")

                    titulo = _clean_html(titulo_tag.get_text()) if titulo_tag else ""
                    link   = link_tag["href"] if link_tag else url_im
                    if link and not link.startswith("http"):
                        link = "https://www.infomoney.com.br" + link
                    data   = data_tag.get_text(strip=True) if data_tag else ""
                    resumo = _clean_html(resumo_tag.get_text()) if resumo_tag else ""

                    if titulo:
                        results.append({"titulo": titulo, "resumo": resumo, "link": link, "data": data, "fonte": "InfoMoney"})
        except Exception:
            pass

        # ── Status Invest: notícias da ação ───────────────────────────────
        try:
            url_si = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
            resp = await client.get(url_si)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                for article in soup.select("div.news-item, div.item-news, li.news")[:limite]:
                    titulo_tag = article.select_one("a, h3, h4")
                    data_tag   = article.select_one("span.date, time")
                    titulo = _clean_html(titulo_tag.get_text()) if titulo_tag else ""
                    link   = titulo_tag.get("href", "") if titulo_tag else ""
                    if link and not link.startswith("http"):
                        link = "https://statusinvest.com.br" + link
                    data = data_tag.get_text(strip=True) if data_tag else ""

                    if titulo and titulo not in [r["titulo"] for r in results]:
                        results.append({"titulo": titulo, "resumo": "", "link": link, "data": data, "fonte": "Status Invest"})
        except Exception:
            pass

    # ── Fallback: busca no feed geral da InfoMoney ─────────────────────────
    if not results:
        try:
            todos = _parse_feed(RSS_FEEDS["infomoney_acoes"], 50)
            ticker_lower = ticker.lower()
            results = [
                n for n in todos
                if ticker_lower in n["titulo"].lower() or ticker_lower in n["resumo"].lower()
            ][:limite]
        except Exception:
            pass

    results = results[:limite]
    return _fmt_noticias(results, f"Notícias: {ticker} — {datetime.now().strftime('%d/%m/%Y %H:%M')}")


async def buscar_noticias(query: str, limite: int = 10) -> str:
    """
    Busca notícias por palavra-chave no mercado financeiro brasileiro.
    Pesquisa em InfoMoney e Investing.com BR.

    Args:
        query: Termo de busca (ex: "Petrobras dividendos", "SELIC", "resultados Itaú")
        limite: Número máximo de resultados (padrão 10)
    """
    results: list[dict] = []

    async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT, follow_redirects=True) as client:

        # ── InfoMoney: busca ───────────────────────────────────────────────
        try:
            url = f"https://www.infomoney.com.br/?s={quote_plus(query)}"
            resp = await client.get(url)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                for article in soup.select("article, div.search-result, div.card-news")[:limite]:
                    titulo_tag = article.select_one("h2, h3, h4, .title")
                    link_tag   = article.select_one("a[href]")
                    data_tag   = article.select_one("time, .date, .meta-date")
                    resumo_tag = article.select_one("p, .excerpt, .description")

                    titulo = _clean_html(titulo_tag.get_text()) if titulo_tag else ""
                    link   = link_tag["href"] if link_tag else ""
                    if link and not link.startswith("http"):
                        link = "https://www.infomoney.com.br" + link
                    data   = data_tag.get_text(strip=True) if data_tag else ""
                    resumo = _clean_html(resumo_tag.get_text()) if resumo_tag else ""

                    if titulo:
                        results.append({"titulo": titulo, "resumo": resumo, "link": link, "data": data, "fonte": "InfoMoney"})
        except Exception:
            pass

        # ── Investing.com BR: busca ────────────────────────────────────────
        try:
            url = f"https://br.investing.com/search/?q={quote_plus(query)}&tab=news"
            resp = await client.get(url)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                for article in soup.select("article.js-article-item, div.articleItem")[:limite]:
                    titulo_tag = article.select_one("a.title, h3, .articleTitle")
                    data_tag   = article.select_one("span.date, time")
                    descr_tag  = article.select_one("p, .articleSummary")

                    titulo = _clean_html(titulo_tag.get_text()) if titulo_tag else ""
                    link   = titulo_tag.get("href", "") if titulo_tag else ""
                    if link and not link.startswith("http"):
                        link = "https://br.investing.com" + link
                    data   = data_tag.get_text(strip=True) if data_tag else ""
                    resumo = _clean_html(descr_tag.get_text()) if descr_tag else ""

                    if titulo and titulo not in [r["titulo"] for r in results]:
                        results.append({"titulo": titulo, "resumo": resumo, "link": link, "data": data, "fonte": "Investing.com BR"})
        except Exception:
            pass

    # ── Fallback: filtrar nos RSS feeds carregados ─────────────────────────
    if not results:
        try:
            query_lower = query.lower()
            feed_items = _parse_feed(RSS_FEEDS["infomoney_geral"], 100)
            results = [
                n for n in feed_items
                if any(w in n["titulo"].lower() or w in n["resumo"].lower() for w in query_lower.split())
            ][:limite]
        except Exception:
            pass

    results = results[:limite]
    return _fmt_noticias(results, f'Busca: "{query}" — {datetime.now().strftime("%d/%m/%Y %H:%M")}')


async def obter_resumo_mercado() -> str:
    """
    Retorna um resumo do estado atual do mercado: IBOVESPA, dólar,
    juros e principais notícias do dia.
    """
    partes: list[str] = [f"# Resumo do Mercado — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"]

    async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT, follow_redirects=True) as client:

        # ── Dados do Ibovespa e Dólar via Investing.com BR ─────────────────
        try:
            resp = await client.get("https://br.investing.com/")
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                # Pega os índices do header
                indices = soup.select("div.marketSummaryInner, div.header-market-data, .market-header")
                if indices:
                    partes.append("## Indicadores\n")
                    for idx in indices[:6]:
                        nome  = idx.select_one(".instrumentName, .name")
                        valor = idx.select_one(".last, .value, .price")
                        var   = idx.select_one(".changePer, .change, .percent")
                        if nome and valor:
                            sinal = "📈" if "+" in (var.get_text() if var else "") else "📉"
                            partes.append(
                                f"- **{nome.get_text(strip=True)}:** "
                                f"{valor.get_text(strip=True)} "
                                f"{sinal} {var.get_text(strip=True) if var else ''}"
                            )
                    partes.append("")
        except Exception:
            pass

        # ── Cotação IBOV via Status Invest ─────────────────────────────────
        if len(partes) == 1:  # fallback se Investing.com não retornou dados
            try:
                resp = await client.get("https://statusinvest.com.br/indices/ibovespa")
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "lxml")
                    valor_tag = soup.select_one("strong.value, .value, h3.value")
                    var_tag   = soup.select_one("span.diff, .change")
                    if valor_tag:
                        partes.append("## Indicadores\n")
                        partes.append(f"- **IBOVESPA:** {valor_tag.get_text(strip=True)} {var_tag.get_text(strip=True) if var_tag else ''}\n")
            except Exception:
                pass

    # ── Manchetes do dia ───────────────────────────────────────────────────
    try:
        items = _parse_feed(RSS_FEEDS["infomoney_mercados"], 5)
        if items:
            partes.append("## Manchetes de Hoje (InfoMoney)")
            for n in items:
                partes.append(f"- [{n['titulo']}]({n['link']}) — {n['data']}")
            partes.append("")
    except Exception:
        pass

    try:
        items = _parse_feed(RSS_FEEDS["valor_economico"], 5)
        if items:
            partes.append("## Manchetes de Hoje (Valor Econômico)")
            for n in items:
                partes.append(f"- [{n['titulo']}]({n['link']}) — {n['data']}")
            partes.append("")
    except Exception:
        pass

    return "\n".join(partes) if len(partes) > 1 else "Não foi possível obter dados do mercado no momento."


async def buscar_noticias_setor(setor: str, limite: int = 10) -> str:
    """
    Busca notícias de um setor específico da B3.

    Setores válidos (B3):
      Financeiro, Petróleo e Gás, Energia Elétrica, Saneamento,
      Mineração, Siderurgia, Agronegócio, Varejo, Saúde,
      Tecnologia, Telecomunicações, Construção Civil, Transportes,
      Bancos, Seguros, Consumo

    Args:
        setor: Nome do setor (ex: "Energia Elétrica", "Bancos", "Agronegócio")
        limite: Número máximo de notícias (padrão 10)
    """
    return await buscar_noticias(setor, limite)


# ─────────────────────────────── decision tools ──────────────────────────────


def salvar_decisao(
    ticker: str,
    acao: str,
    preco_entrada: float,
    gatilho: str,
    justificativa: str,
    confianca: float,
    stop_loss: float | None = None,
    setor: str | None = None,
    tendencia: str | None = None,
    rsi: float | None = None,
    roe: float | None = None,
) -> str:
    """
    Salva uma decisão de investimento no histórico persistente.

    Args:
        ticker:        Código da ação (ex: WEGE3)
        acao:          COMPRAR | MONITORAR | DESCARTAR
        preco_entrada: Preço no momento da análise
        gatilho:       Dave Landry | 1-2-3 | Inside Candle | Nenhum
        justificativa: Texto livre com a razão da decisão
        confianca:     Score de 0.0 a 1.0
        stop_loss:     Preço de stop sugerido (opcional)
        setor:         Setor da empresa (opcional)
        tendencia:     Alta | Baixa | Neutro | Nenhuma (opcional)
        rsi:           Valor do RSI(14) no momento (opcional)
        roe:           ROE da empresa em percentual (opcional)
    """
    ticker = ticker.upper().replace(".SA", "").strip()
    decisions = _load_decisions()

    record: dict = {
        "id":            _next_id(decisions),
        "ticker":        ticker,
        "acao":          acao.upper(),
        "preco_entrada": preco_entrada,
        "preco_atual":   None,
        "resultado_pct": None,
        "status":        "ABERTA",
        "gatilho":       gatilho,
        "justificativa": justificativa,
        "confianca":     round(confianca, 3),
        "stop_loss":     stop_loss,
        "setor":         setor,
        "tendencia":     tendencia,
        "rsi":           rsi,
        "roe":           roe,
        "data_decisao":  datetime.now().isoformat(timespec="seconds"),
        "data_fechamento": None,
        "notas":         [],
    }

    decisions.append(record)
    _save_decisions(decisions)

    return (
        f"✅ Decisão #{record['id']} salva.\n"
        f"**{ticker}** — {acao} @ R${preco_entrada:.2f} | "
        f"Gatilho: {gatilho} | Confiança: {confianca:.0%} | "
        f"Stop: {'R$' + str(stop_loss) if stop_loss else 'não definido'}\n"
        f"Arquivo: {DECISIONS_FILE}"
    )


def listar_decisoes(
    ticker: str | None = None,
    status: str | None = None,
    acao: str | None = None,
    limite: int = 20,
) -> str:
    """
    Lista decisões de investimento armazenadas.

    Args:
        ticker: Filtrar por ação (opcional)
        status: ABERTA | FECHADA | STOP_ATINGIDO (opcional)
        acao:   COMPRAR | MONITORAR | DESCARTAR (opcional)
        limite: Número máximo de resultados (padrão 20)
    """
    decisions = _load_decisions()

    if not decisions:
        return "Nenhuma decisão registrada ainda."

    filtered = decisions
    if ticker:
        t = ticker.upper().replace(".SA", "")
        filtered = [d for d in filtered if d["ticker"] == t]
    if status:
        filtered = [d for d in filtered if d.get("status", "").upper() == status.upper()]
    if acao:
        filtered = [d for d in filtered if d.get("acao", "").upper() == acao.upper()]

    filtered = filtered[-limite:]  # mais recentes

    if not filtered:
        return "Nenhuma decisão encontrada com os filtros informados."

    linhas = [f"## Histórico de Decisões ({len(filtered)} registros)\n"]
    for d in reversed(filtered):
        resultado = ""
        if d.get("resultado_pct") is not None:
            sinal = "📈" if d["resultado_pct"] >= 0 else "📉"
            resultado = f" | Resultado: {sinal} {d['resultado_pct']:+.1f}%"

        status_icon = {"ABERTA": "🟡", "FECHADA": "✅", "STOP_ATINGIDO": "🛑"}.get(
            d.get("status", ""), "❓"
        )

        linhas.append(
            f"### #{d['id']} — {d['ticker']} | {status_icon} {d.get('status','?')} | "
            f"{d.get('acao','?')} @ R${d['preco_entrada']:.2f}{resultado}"
        )
        linhas.append(
            f"**Data:** {d['data_decisao'][:10]} | "
            f"**Gatilho:** {d.get('gatilho','?')} | "
            f"**Confiança:** {d.get('confianca', 0):.0%} | "
            f"**Tendência:** {d.get('tendencia','?')} | "
            f"**RSI:** {d.get('rsi','?')} | "
            f"**ROE:** {str(d.get('roe','?')) + '%' if d.get('roe') else '?'}"
        )
        if d.get("justificativa"):
            linhas.append(f"**Justificativa:** {d['justificativa']}")
        if d.get("notas"):
            linhas.append(f"**Notas:** {' | '.join(d['notas'])}")
        linhas.append("")

    return "\n".join(linhas)


def atualizar_decisao(
    decisao_id: int,
    preco_atual: float,
    status: str | None = None,
    nota: str | None = None,
) -> str:
    """
    Atualiza uma decisão com o preço atual e calcula o resultado percentual.

    Args:
        decisao_id:  ID da decisão (obter via listar_decisoes)
        preco_atual: Preço atual da ação
        status:      ABERTA | FECHADA | STOP_ATINGIDO (opcional)
        nota:        Observação livre para registrar no histórico (opcional)
    """
    decisions = _load_decisions()
    target = next((d for d in decisions if d["id"] == decisao_id), None)

    if not target:
        return f"Decisão #{decisao_id} não encontrada."

    preco_entrada = target["preco_entrada"]
    resultado_pct = ((preco_atual - preco_entrada) / preco_entrada) * 100

    target["preco_atual"]   = preco_atual
    target["resultado_pct"] = round(resultado_pct, 2)

    if status:
        target["status"] = status.upper()
        if status.upper() in ("FECHADA", "STOP_ATINGIDO"):
            target["data_fechamento"] = datetime.now().isoformat(timespec="seconds")

    if nota:
        target["notas"].append(f"{datetime.now().strftime('%d/%m/%Y')}: {nota}")

    _save_decisions(decisions)

    sinal = "📈" if resultado_pct >= 0 else "📉"
    return (
        f"✅ Decisão #{decisao_id} atualizada.\n"
        f"**{target['ticker']}:** R${preco_entrada:.2f} → R${preco_atual:.2f} "
        f"| {sinal} {resultado_pct:+.1f}% | Status: {target.get('status','?')}"
    )


def resumo_performance() -> str:
    """
    Gera um relatório de performance de todas as decisões registradas:
    acertos vs erros, retorno médio, melhor/pior decisão.
    """
    decisions = _load_decisions()

    if not decisions:
        return "Nenhuma decisão registrada ainda."

    fechadas = [d for d in decisions if d.get("resultado_pct") is not None]
    abertas  = [d for d in decisions if d.get("status") == "ABERTA"]
    stops    = [d for d in decisions if d.get("status") == "STOP_ATINGIDO"]

    linhas = ["# Relatório de Performance — Decisões de Investimento\n"]
    linhas.append(f"**Total de decisões:** {len(decisions)}")
    linhas.append(f"**Em aberto:** {len(abertas)} | **Fechadas:** {len(fechadas)} | **Stop atingido:** {len(stops)}\n")

    if fechadas:
        retornos   = [d["resultado_pct"] for d in fechadas]
        positivas  = [r for r in retornos if r >= 0]
        negativas  = [r for r in retornos if r < 0]
        media      = sum(retornos) / len(retornos)
        taxa_acerto = len(positivas) / len(retornos) * 100

        melhor = max(fechadas, key=lambda d: d["resultado_pct"])
        pior   = min(fechadas, key=lambda d: d["resultado_pct"])

        linhas.append("## Desempenho Geral")
        linhas.append(f"- **Taxa de acerto:** {taxa_acerto:.1f}%")
        linhas.append(f"- **Retorno médio:** {media:+.1f}%")
        linhas.append(f"- **Total positivas:** {len(positivas)} (média: {sum(positivas)/len(positivas):+.1f}%)" if positivas else "- **Total positivas:** 0")
        linhas.append(f"- **Total negativas:** {len(negativas)} (média: {sum(negativas)/len(negativas):+.1f}%)" if negativas else "- **Total negativas:** 0")
        linhas.append(
            f"\n**Melhor decisão:** #{melhor['id']} {melhor['ticker']} "
            f"({melhor['resultado_pct']:+.1f}%) — {melhor['data_decisao'][:10]}"
        )
        linhas.append(
            f"**Pior decisão:** #{pior['id']} {pior['ticker']} "
            f"({pior['resultado_pct']:+.1f}%) — {pior['data_decisao'][:10]}"
        )

        # Por gatilho
        linhas.append("\n## Acerto por Gatilho")
        gatilhos: dict[str, list[float]] = {}
        for d in fechadas:
            g = d.get("gatilho", "Desconhecido")
            gatilhos.setdefault(g, []).append(d["resultado_pct"])
        for g, vals in sorted(gatilhos.items()):
            acertos = sum(1 for v in vals if v >= 0)
            linhas.append(
                f"- **{g}:** {acertos}/{len(vals)} acertos | "
                f"média {sum(vals)/len(vals):+.1f}%"
            )

    if abertas:
        linhas.append("\n## Posições em Aberto")
        for d in abertas:
            linhas.append(
                f"- #{d['id']} **{d['ticker']}** @ R${d['preco_entrada']:.2f} "
                f"| {d['data_decisao'][:10]} | {d.get('gatilho','?')}"
            )

    return "\n".join(linhas)


# ─────────────────────────────── MCP server ──────────────────────────────────

app = Server("mcp-b3-news")

TOOLS: list[Tool] = [
    Tool(
        name="buscar_noticias_mercado",
        description=(
            "Retorna as últimas notícias gerais do mercado financeiro brasileiro (B3). "
            "Combina InfoMoney e Valor Econômico. Use para obter o contexto macro do mercado."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de notícias (padrão: 10, máximo: 30)",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 30,
                },
            },
        },
    ),
    Tool(
        name="buscar_noticias_acao",
        description=(
            "Busca notícias recentes de uma ação específica da B3. "
            "Use para obter contexto antes de recomendar ou analisar um ativo. "
            "Fontes: InfoMoney e Status Invest."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Código da ação sem sufixo (ex: PETR4, WEGE3, ITUB4, VALE3)",
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de notícias (padrão: 10)",
                    "default": 10,
                },
            },
            "required": ["ticker"],
        },
    ),
    Tool(
        name="buscar_noticias",
        description=(
            "Busca notícias por palavra-chave no mercado financeiro brasileiro. "
            "Use para pesquisar eventos específicos (ex: 'SELIC', 'dividendos Petrobras', "
            "'resultado Itaú', 'fusão aquisição'). Fontes: InfoMoney e Investing.com BR."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo de busca em português (ex: 'Petrobras dividendos 2024')",
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de resultados (padrão: 10)",
                    "default": 10,
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="buscar_noticias_setor",
        description=(
            "Busca notícias de um setor específico da B3. "
            "Setores: Financeiro, Petróleo e Gás, Energia Elétrica, Mineração, "
            "Agronegócio, Varejo, Saúde, Tecnologia, Telecomunicações, Construção Civil, Bancos."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "setor": {
                    "type": "string",
                    "description": "Nome do setor (ex: 'Energia Elétrica', 'Bancos', 'Agronegócio')",
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de notícias (padrão: 10)",
                    "default": 10,
                },
            },
            "required": ["setor"],
        },
    ),
    Tool(
        name="obter_resumo_mercado",
        description=(
            "Retorna resumo completo do mercado: IBOVESPA, dólar, juros e manchetes do dia. "
            "Use no início de qualquer análise para ter o contexto macro atualizado."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    # ── Memória de decisões ────────────────────────────────────────────────
    Tool(
        name="salvar_decisao",
        description=(
            "Salva uma decisão de investimento no histórico persistente. "
            "SEMPRE chame após emitir uma recomendação de COMPRAR, MONITORAR ou DESCARTAR. "
            "Permite rastrear o histórico, calcular performance e auditar decisões futuras."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "ticker":        {"type": "string",  "description": "Código da ação (ex: WEGE3)"},
                "acao":          {"type": "string",  "description": "COMPRAR | MONITORAR | DESCARTAR"},
                "preco_entrada": {"type": "number",  "description": "Preço da ação no momento da análise"},
                "gatilho":       {"type": "string",  "description": "Dave Landry | 1-2-3 | Inside Candle | Nenhum"},
                "justificativa": {"type": "string",  "description": "Razão da decisão em texto livre"},
                "confianca":     {"type": "number",  "description": "Score de 0.0 a 1.0"},
                "stop_loss":     {"type": "number",  "description": "Preço de stop sugerido (opcional)"},
                "setor":         {"type": "string",  "description": "Setor da empresa (opcional)"},
                "tendencia":     {"type": "string",  "description": "Alta | Baixa | Neutro | Nenhuma (opcional)"},
                "rsi":           {"type": "number",  "description": "Valor do RSI(14) (opcional)"},
                "roe":           {"type": "number",  "description": "ROE em percentual, ex: 22.5 (opcional)"},
            },
            "required": ["ticker", "acao", "preco_entrada", "gatilho", "justificativa", "confianca"],
        },
    ),
    Tool(
        name="listar_decisoes",
        description=(
            "Lista o histórico de decisões de investimento. "
            "Use antes de analisar um ticker para ver se já foi recomendado antes e qual foi o resultado. "
            "Filtre por ticker, status (ABERTA/FECHADA/STOP_ATINGIDO) ou ação (COMPRAR/MONITORAR/DESCARTAR)."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "ticker": {"type": "string",  "description": "Filtrar por ação (opcional)"},
                "status": {"type": "string",  "description": "ABERTA | FECHADA | STOP_ATINGIDO (opcional)"},
                "acao":   {"type": "string",  "description": "COMPRAR | MONITORAR | DESCARTAR (opcional)"},
                "limite": {"type": "integer", "description": "Máximo de resultados (padrão 20)", "default": 20},
            },
        },
    ),
    Tool(
        name="atualizar_decisao",
        description=(
            "Atualiza uma decisão existente com o preço atual, calculando o resultado percentual. "
            "Use para registrar o fechamento de uma posição ou atingimento de stop. "
            "O ID da decisão é obtido via listar_decisoes."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "decisao_id":  {"type": "integer", "description": "ID da decisão (obtido via listar_decisoes)"},
                "preco_atual": {"type": "number",  "description": "Preço atual da ação"},
                "status":      {"type": "string",  "description": "ABERTA | FECHADA | STOP_ATINGIDO (opcional)"},
                "nota":        {"type": "string",  "description": "Observação para registrar no histórico (opcional)"},
            },
            "required": ["decisao_id", "preco_atual"],
        },
    ),
    Tool(
        name="resumo_performance",
        description=(
            "Gera relatório completo de performance: taxa de acerto, retorno médio, "
            "melhor/pior decisão e acerto por tipo de gatilho. "
            "Use para avaliar a qualidade das recomendações ao longo do tempo."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "buscar_noticias_mercado":
            result = await buscar_noticias_mercado(limite=arguments.get("limite", 10))

        elif name == "buscar_noticias_acao":
            result = await buscar_noticias_acao(
                ticker=arguments["ticker"],
                limite=arguments.get("limite", 10),
            )

        elif name == "buscar_noticias":
            result = await buscar_noticias(
                query=arguments["query"],
                limite=arguments.get("limite", 10),
            )

        elif name == "buscar_noticias_setor":
            result = await buscar_noticias_setor(
                setor=arguments["setor"],
                limite=arguments.get("limite", 10),
            )

        elif name == "obter_resumo_mercado":
            result = await obter_resumo_mercado()

        elif name == "salvar_decisao":
            result = salvar_decisao(
                ticker        = arguments["ticker"],
                acao          = arguments["acao"],
                preco_entrada = arguments["preco_entrada"],
                gatilho       = arguments["gatilho"],
                justificativa = arguments["justificativa"],
                confianca     = arguments["confianca"],
                stop_loss     = arguments.get("stop_loss"),
                setor         = arguments.get("setor"),
                tendencia     = arguments.get("tendencia"),
                rsi           = arguments.get("rsi"),
                roe           = arguments.get("roe"),
            )

        elif name == "listar_decisoes":
            result = listar_decisoes(
                ticker = arguments.get("ticker"),
                status = arguments.get("status"),
                acao   = arguments.get("acao"),
                limite = arguments.get("limite", 20),
            )

        elif name == "atualizar_decisao":
            result = atualizar_decisao(
                decisao_id  = arguments["decisao_id"],
                preco_atual = arguments["preco_atual"],
                status      = arguments.get("status"),
                nota        = arguments.get("nota"),
            )

        elif name == "resumo_performance":
            result = resumo_performance()

        else:
            result = f"Ferramenta desconhecida: {name}"

    except Exception as exc:
        result = f"Erro ao executar '{name}': {type(exc).__name__}: {exc}"

    return [TextContent(type="text", text=result)]


def main() -> None:
    asyncio.run(stdio_server(app))


if __name__ == "__main__":
    main()
