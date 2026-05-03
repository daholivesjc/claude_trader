> **MCP Validated:** 2026-03-14

# Indicadores Técnicos

Indicadores implementados no `SwingTrade.ipynb` para análise de tendência e momentum.

---

## RSI (Relative Strength Index) — Período 14

### Conceito

O RSI mede a velocidade e magnitude das variações de preço. Varia de 0 a 100. Leituras acima de 70 indicam sobrecompra; abaixo de 30, sobrevenda.

### Implementação: Wilder Smoothing (Recursiva)

O notebook usa `calculate_rsi_new()`, que implementa o suavizamento original de J. Welles Wilder — **não** usa média móvel simples (`rolling mean`).

**Diferença crítica:**

| Método | Fórmula média | Resultado |
|--------|--------------|-----------|
| Rolling mean (simplificado) | `sum(ganhos[-14]) / 14` | Suprime a persistência de ganhos/perdas passados |
| Wilder smoothing (correto) | `((avg_anterior * 13) + ganho_atual) / 14` | Mantém memória exponencial do histórico |

O rolling mean trata cada janela de 14 períodos como independente. O Wilder smoothing acumula a história completa de forma recursiva, produzindo RSI mais suave e confiável.

### Cálculo Passo a Passo

```
1. change[i]   = close[i] - close[i-1]
2. gain[i]     = change[i]  se change > 0, senão 0
3. loss[i]     = |change[i]| se change < 0, senão 0
4. Média inicial (bootstrapping):
   avg_gain[first] = rolling_mean(gain, 14)  ← usado apenas uma vez
   avg_loss[first] = rolling_mean(loss, 14)
5. Loop recursivo para i > first:
   avg_gain[i] = ((avg_gain[i-1] * 13) + gain[i]) / 14
   avg_loss[i] = ((avg_loss[i-1] * 13) + loss[i]) / 14
6. RS[i]  = avg_gain[i] / avg_loss[i]
7. RSI[i] = 100 - (100 / (1 + RS[i]))
```

### Edge Cases

- `first_valid_index` é identificado antes do loop; se `None` ou `len(df) <= first`, retorna `np.nan`
- Linha 0 tem `gain = NaN` e `loss = NaN` (sem candle anterior)
- A função retorna apenas o **último valor** do RSI (escalar), não a série completa

---

## Médias Móveis

### EMA(8) — EMA Curta

Exponential Moving Average de 8 períodos. Calculada via `ta.trend.ema_indicator(close, window=8)`. Captura movimento de preço de curto prazo. Usada como proxy da tendência imediata.

### EMA(80) — EMA Longa

Exponential Moving Average de 80 períodos. Calculada via `ta.trend.ema_indicator(close, window=80)`. Captura movimento de médio prazo. Serve como filtro de tendência intermediária.

### SMA(200) — Média de Longo Prazo

Simple Moving Average de 200 períodos. Calculada via `ta.trend.sma_indicator(close, window=200)`. Referência clássica de tendência primária. Acima dela: mercado em alta estrutural. Abaixo: mercado em baixa estrutural.

**Nota:** O notebook também contém `calculate_ema_200_manual()` com implementação manual da EMA(200) (fator de suavização = 2/201), mas a função `get_trend()` usa `sma_indicator` da biblioteca `ta`.

---

## Classificação de Tendência

A função `get_trend(dataframe, periodos)` retorna `(tendencia, variacao)`.

### Condições Exatas

```
EMA_curta  = EMA(8)  do último candle
EMA_longa  = EMA(80) do último candle
EMA_longa200 = SMA(200) do último candle

SE   EMA_curta > EMA_longa  E  EMA_longa > EMA_longa200  → "Alta"
ELIF EMA_curta < EMA_longa  E  EMA_longa < EMA_longa200  → "Baixa"
ELIF (EMA_longa > EMA_curta < EMA_longa200)              → "Neutro/Lateral"
     OU (EMA_longa < EMA_curta > EMA_longa200)
ELSE                                                      → "Nenhuma"
```

### Interpretação Visual

```
Alta:          EMA200 < EMA80 < EMA8   (empilhamento crescente)
Baixa:         EMA8 < EMA80 < EMA200   (empilhamento decrescente)
Neutro/Lateral: EMA8 no meio (sanduíche) ou acima de ambas as longas
Nenhuma:       configuração não enquadrada nas anteriores
```

---

## Variação de Preço (7, 15, 30 dias)

A função `calcular_variacao_preco(df, dias)` calcula a variação percentual do fechamento.

### Algoritmo

```
1. data_recente = df['date'].max()
2. close_atual  = close na data_recente (por ticker)
3. data_alvo    = data_recente - timedelta(days=dias)
4. close_anterior = close na data mais próxima de data_alvo
   (usa abs(date - data_alvo) e idxmin por ticker — tolerante a feriados)
5. variacao = ((close_atual - close_anterior) / close_anterior) * 100
```

### Saída no build_table()

O campo `Variacao` em `build_table()` usa `periodos=7` por padrão na chamada do screener principal. Representa a variação percentual nos últimos 7 dias de pregão.

---

## Referências Cruzadas

- Gatilhos de entrada que usam esses indicadores: [concepts/gatilhos-entrada.md](gatilhos-entrada.md)
- Pipeline que orquestra o cálculo: [concepts/pipeline-screener.md](pipeline-screener.md)
- Implementação da coleta de dados históricos: [patterns/coleta-dados-b3.md](../patterns/coleta-dados-b3.md)
- Implementação detalhada do RSI Wilder: [patterns/calculo-rsi-wilder.md](../patterns/calculo-rsi-wilder.md)
