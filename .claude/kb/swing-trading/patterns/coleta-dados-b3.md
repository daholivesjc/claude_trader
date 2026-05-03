> **MCP Validated:** 2026-03-14

# Padrão: Coleta de Dados Históricos da B3

Padrão completo para obter dados OHLCV de ações brasileiras via Yahoo Finance, extraído da função `coleta_dados_historicos()` e das células do `SwingTrade.ipynb`.

---

## Visão Geral

O padrão resolve dois problemas específicos do mercado brasileiro:

1. **Sufixo `.SA`:** O Yahoo Finance requer o sufixo `.SA` para ações da B3 (ex: `PETR4.SA`, não `PETR4`).
2. **Dados de fim de semana:** O yfinance pode retornar linhas com datas de sábado/domingo em alguns casos; o padrão remove explicitamente.

---

## Padrão 1: Coleta em Lote (Função Reutilizável)

Usado quando se tem um DataFrame do `fundamentus` como universo de entrada.

```python
import yfinance as yf
import pandas as pd
import time

def coleta_dados_historicos(df: pd.DataFrame, periodo: str = "1mo") -> pd.DataFrame:
    """
    Coleta dados OHLCV históricos para todas as ações do DataFrame.

    Args:
        df: DataFrame do fundamentus (índice = tickers sem sufixo .SA).
        periodo: Período do yfinance. Válidos: 1mo, 3mo, 6mo, 12mo, 1y, 2y, 5y.

    Returns:
        DataFrame concatenado com colunas: date, close, high, low, open, volume, ticker.
    """
    # Adiciona sufixo .SA exigido pelo Yahoo Finance para ações brasileiras
    acoes_ibov_yfinance = [acoes + ".SA" for acoes in df.index]

    df_list = []

    for ticker in acoes_ibov_yfinance:
        try:
            df_ohlcv = yf.download(ticker, period=periodo, progress=False)

            if df_ohlcv.shape[0] > 0:
                # Normaliza o índice e renomeia colunas para padrão interno
                df_ohlcv.reset_index(inplace=True)
                df_ohlcv.columns = ["date", "close", "high", "low", "open", "volume"]

                # Adiciona coluna de identificação (sem o sufixo .SA)
                df_ohlcv["ticker"] = ticker.split(".")[0]

                # Remove fins de semana (dayofweek: 0=segunda ... 4=sexta, 5=sábado, 6=domingo)
                df_ohlcv['date'] = pd.to_datetime(df_ohlcv['date'])
                df_ohlcv['day_of_week'] = df_ohlcv['date'].dt.dayofweek
                df_ohlcv = df_ohlcv[df_ohlcv['day_of_week'] < 5]
                df_ohlcv = df_ohlcv.drop(columns=['day_of_week'])

                df_list.append(df_ohlcv)

        except Exception as e:
            print(f"Ticker {ticker} not listed. Error: {e}")
            time.sleep(2)  # Backoff para evitar rate limiting
            continue

    return pd.concat(df_list)
```

---

## Padrão 2: Coleta Direta por Lista (Inline)

Usado no notebook principal quando a entrada é uma lista de tickers (não um DataFrame).

```python
df_list = []

for ticker in tickers:  # tickers: lista de strings sem sufixo .SA
    try:
        df_ohlcv = yf.download(ticker + ".SA", period="12mo", progress=False)

        if df_ohlcv.shape[0] > 0:
            df_ohlcv.reset_index(inplace=True)
            df_ohlcv.columns = ["date", "close", "high", "low", "open", "volume"]
            df_ohlcv["ticker"] = ticker.split(".")[0]

            df_ohlcv['date'] = pd.to_datetime(df_ohlcv['date'])
            df_ohlcv['day_of_week'] = df_ohlcv['date'].dt.dayofweek
            df_ohlcv = df_ohlcv[df_ohlcv['day_of_week'] < 5]
            df_ohlcv = df_ohlcv.drop(columns=['day_of_week'])

            df_list.append(df_ohlcv)

    except Exception as e:
        print(f"Ticker {ticker} not listed. Error: {e}")
        time.sleep(2)
        continue

df_join = pd.concat(df_list)
```

---

## Estrutura do DataFrame Resultante

| Coluna | Dtype | Descrição |
|--------|-------|-----------|
| `date` | `datetime64[ns]` | Data do pregão |
| `close` | `float64` | Preço de fechamento (ajustado) |
| `high` | `float64` | Máxima do dia |
| `low` | `float64` | Mínima do dia |
| `open` | `float64` | Abertura |
| `volume` | `int64` | Volume negociado |
| `ticker` | `object` | Código da ação (sem `.SA`) |

**Resultado típico com 401 tickers / 12 meses:** ~98.077 linhas, ~6 MB em memória.

---

## Renomeação de Colunas — Detalhe Importante

O yfinance retorna colunas com nomes diferentes dependendo da versão:

```python
# Após reset_index(), o yfinance retorna ordem:
# ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']  (versões mais recentes)
# A renomeação posicional normaliza para o padrão interno:
df_ohlcv.columns = ["date", "close", "high", "low", "open", "volume"]
```

O notebook define `auto_adjust=True` por padrão (mudança de comportamento do yfinance documentada nas saídas: "YF.download() has changed argument auto_adjust default to True"). Os preços retornados são ajustados por dividendos e splits.

---

## Filtro de Fim de Semana

```python
# dayofweek retorna: 0=segunda, 1=terça, 2=quarta, 3=quinta, 4=sexta
#                    5=sábado, 6=domingo
df_ohlcv['day_of_week'] = df_ohlcv['date'].dt.dayofweek
df_ohlcv = df_ohlcv[df_ohlcv['day_of_week'] < 5]  # mantém apenas dias úteis
df_ohlcv = df_ohlcv.drop(columns=['day_of_week'])  # limpa coluna temporária
```

---

## Tratamento de Erros

| Situação | Comportamento |
|----------|--------------|
| Ticker delistado | yfinance lança `YFPricesMissingError`; o `except` captura, imprime e continua |
| DataFrame vazio | `shape[0] > 0` previne `concat` de DataFrames vazios |
| Rate limiting | `time.sleep(2)` após exceção |
| Ticker não encontrado | Ignorado silenciosamente após log |

---

## Períodos Suportados pelo yfinance

```
"1mo", "2mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
Intradía: "1d", "5d" (com interval="1m", "5m", etc.)
```

O notebook usa `"12mo"` — equivalente a `"1y"`.

---

## Referências Cruzadas

- Universo de tickers coletados: [concepts/pipeline-screener.md](../concepts/pipeline-screener.md)
- Uso dos dados históricos no cálculo de RSI: [patterns/calculo-rsi-wilder.md](calculo-rsi-wilder.md)
- Indicadores calculados sobre esses dados: [concepts/indicadores-tecnicos.md](../concepts/indicadores-tecnicos.md)
