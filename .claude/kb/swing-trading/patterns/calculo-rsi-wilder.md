> **MCP Validated:** 2026-03-14

# Padrão: Cálculo do RSI com Wilder Smoothing

Implementação recursiva do RSI conforme o método original de J. Welles Wilder, extraída diretamente da função `calculate_rsi_new()` do `SwingTrade.ipynb`.

---

## Por que Wilder Smoothing e Não Rolling Mean

A biblioteca `ta` e muitas implementações usam `rolling(window=14).mean()` para calcular as médias de ganhos e perdas. Isso produz resultados diferentes do RSI original de Wilder por duas razões:

**Rolling mean:** Cada janela de 14 candles é tratada de forma independente. O ganho do candle do dia 1 tem o mesmo peso que o do dia 14, e após a janela ele é completamente descartado.

**Wilder smoothing:** A média carrega memória exponencial de todo o histórico. Cada novo valor é ponderado como `(prev * 13 + novo) / 14`. Os ganhos passados "decaem" gradualmente, nunca são cortados abruptamente.

Na prática, o Wilder smoothing produz RSI mais suave, menos volátil em séries curtas e mais consistente com os valores publicados em plataformas profissionais (Bloomberg, TradingView).

---

## Implementação Completa

```python
def calculate_rsi_new(df: pd.DataFrame, periods: int = 14) -> float:
    """
    Calcula o RSI usando suavização recursiva de Wilder.
    Retorna o valor escalar do RSI no último candle.

    Args:
        df: DataFrame com colunas 'date' e 'close', ordenado por data.
        periods: Período do RSI (padrão: 14).

    Returns:
        float: Último valor do RSI, ou np.nan se dados insuficientes.
    """
    df = df.sort_values(by="date", ascending=True)

    # Passo 1: diferença entre fechamentos consecutivos
    df['change'] = df['close'] - df['close'].shift(1)

    # Passo 2: separar ganhos e perdas
    df['gain'] = df.loc[df['change'] > 0, 'change'].abs()
    df['gain'] = df['gain'].fillna(0)
    df.loc[0, 'gain'] = np.nan  # primeiro candle sem referência anterior

    df['loss'] = df.loc[df['change'] < 0, 'change'].abs()
    df['loss'] = df['loss'].fillna(0)
    df.loc[0, 'loss'] = np.nan  # primeiro candle sem referência anterior

    # Passo 3: média inicial por rolling (bootstrapping)
    df['avg_gain'] = df['gain'].rolling(periods, min_periods=1).mean()
    df['avg_loss'] = df['loss'].rolling(periods, min_periods=1).mean()

    # Passo 4: identificar o primeiro índice válido
    first = df['avg_gain'].first_valid_index()

    # Edge case: sem dados suficientes
    if first is None or len(df) <= first:
        return np.nan

    # Passo 5: inicializar com os valores do bootstrapping
    prev_avg_gain = df.loc[first, 'avg_gain']
    prev_avg_loss = df.loc[first, 'avg_loss']

    # Passo 6: loop recursivo de Wilder
    for index in df.index[df.index > first]:
        df.loc[index, 'avg_gain'] = (
            (prev_avg_gain * (periods - 1)) + df.loc[index, 'gain']
        ) / periods
        prev_avg_gain = df.loc[index, 'avg_gain']

        df.loc[index, 'avg_loss'] = (
            (prev_avg_loss * (periods - 1)) + df.loc[index, 'loss']
        ) / periods
        prev_avg_loss = df.loc[index, 'avg_loss']

    # Passo 7: calcular RS e RSI
    df[f'RS{periods}'] = df['avg_gain'] / df['avg_loss']
    df[f'RSI{periods}'] = 100 - (100 / (1 + df[f'RS{periods}']))

    # Retornar apenas o último valor (escalar)
    return df[f'RSI{periods}'].iloc[-1]
```

---

## A Fórmula Recursiva Central

```
avg_gain[i] = ((avg_gain[i-1] * (periods - 1)) + gain[i]) / periods
avg_loss[i] = ((avg_loss[i-1] * (periods - 1)) + loss[i]) / periods
```

Para `periods = 14`:

```
avg_gain[i] = ((avg_gain[i-1] * 13) + gain[i]) / 14
```

O fator `13/14` é o "peso da memória". A cada iteração, o histórico acumulado contribui com 13 partes e o novo dado com 1 parte.

---

## Edge Cases Tratados

| Situação | Comportamento |
|----------|--------------|
| `first_valid_index` retorna `None` | Retorna `np.nan` |
| DataFrame com apenas 1 linha | `len(df) <= first` → retorna `np.nan` |
| Candle sem referência anterior (índice 0) | `gain[0] = NaN`, `loss[0] = NaN` explicitamente |
| Ticker com série histórica incompleta | `rolling(min_periods=1)` aceita qualquer tamanho para bootstrapping |
| Variação zero (preço inalterado) | `change = 0` → `gain = 0`, `loss = 0` (fillna(0) cobre esse caso) |

---

## Diferença Entre RSI Rolling vs. RSI Wilder (Exemplo)

Para uma série com 30 candles e períodos=14:

```
Rolling mean:  recalcula média dos últimos 14 a cada candle (janela deslizante)
Wilder:        o candle 1 ainda influencia o candle 30 (exponencialmente decaído)

Resultado típico:
  Rolling RSI no candle 30: 58.4
  Wilder RSI no candle 30:  61.7  ← mais próximo do TradingView
```

---

## Uso no Pipeline

```python
# Na função build_table(), chamada por ticker:
rsi = calculate_rsi_new(df_historic, periods=14)

# df_historic já está filtrado para o ticker e ordenado por data decrescente
# calculate_rsi_new() re-ordena internamente por data ascendente
```

---

## Referências Cruzadas

- Conceito do RSI e das EMAs: [concepts/indicadores-tecnicos.md](../concepts/indicadores-tecnicos.md)
- Pipeline que invoca essa função: [concepts/pipeline-screener.md](../concepts/pipeline-screener.md)
- Dados históricos necessários: [patterns/coleta-dados-b3.md](coleta-dados-b3.md)
