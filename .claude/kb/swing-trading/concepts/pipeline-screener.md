> **MCP Validated:** 2026-03-14

# Pipeline do Screener de Swing Trading

Arquitetura completa do pipeline implementado no `SwingTrade.ipynb` para identificar ações com gatilhos de entrada.

---

## Visão Geral do Fluxo

```
[Estágio 1]         [Estágio 2]            [Estágio 3]
Coleta de           Filtro                  Coleta de
universo     →      fundamentalista   →     dados históricos
~400 tickers        ~391 tickers            12 meses OHLCV

[Estágio 4]         [Estágio 5]
Detecção de  →      Saída final
gatilhos            ordenada por ROE
por ticker
```

---

## Estágio 1: Coleta do Universo de Tickers

**Fonte:** `https://www.dadosdemercado.com.br/acoes`

**Método:** Web scraping via função `obter_tickers(url)` da biblioteca `ot-module`.

**Resultado:** Lista com aproximadamente **401 tickers** da B3.

```python
url = "https://www.dadosdemercado.com.br/acoes"
tickers = obter_tickers(url)
# len(tickers) → 401
```

---

## Estágio 2: Filtro Fundamentalista

**Fonte:** API `fundamentus.get_resultado()` (biblioteca `fundamentus`).

**Operação:** Filtra o universo de tickers pelos critérios abaixo.

### Thresholds Exatos

| Campo | Condição | Significado |
|-------|----------|-------------|
| `roe` | `> 0.15` | ROE maior que 15% |
| `mrgebit` | `> 0.1` | Margem EBIT maior que 10% |
| `mrgliq` | `> 0.1` | Margem líquida maior que 10% |
| `divbpatr` | `< 3` | Dívida bruta / patrimônio menor que 3x |
| `pvp` | `> 1` | Preço / Valor Patrimonial maior que 1 |

```python
df_filtrado = df[
    (df.roe > 0.15) &
    (df.mrgebit > 0.1) &
    (df.mrgliq > 0.1) &
    (df.divbpatr < 3) &
    (df.pvp > 1)
]
# len(df_filtrado.index.unique()) → 391
```

**Nota sobre `pvp > 1`:** Filtra empresas onde o mercado paga acima do valor patrimonial, sinal de que o mercado reconhece valor no negócio (não apenas ativos tangíveis).

---

## Estágio 3: Coleta de Dados Históricos

**Fonte:** Yahoo Finance via `yfinance`.

**Parâmetros fixos:** `period="12mo"`, `progress=False`, sufixo `.SA`.

**Processamento por ticker:**
1. Download OHLCV
2. Reset do índice, renomeação de colunas para `["date", "close", "high", "low", "open", "volume"]`
3. Adição da coluna `ticker` (sem o sufixo `.SA`)
4. Conversão de `date` para `datetime64`
5. Remoção de fins de semana (`dayofweek < 5`)

**Resultado:** DataFrame único concatenado com ~98.077 linhas (7 colunas).

**Tratamento de erros:** Tickers delistados são silenciosamente ignorados com `time.sleep(2)` entre tentativas.

Detalhes de implementação: [patterns/coleta-dados-b3.md](../patterns/coleta-dados-b3.md)

---

## Estágio 4: Detecção de Gatilhos por Ticker

**Função:** `build_table(ticker, df_historic, periodos)`

**Para cada ticker, executa em sequência:**

1. Busca dados fundamentalistas individuais via `fundamentus.get_papel(ticker)`
2. Filtra o histórico para o ticker atual e ordena por data decrescente
3. Calcula RSI(14) com Wilder smoothing
4. Calcula tendência (Alta/Baixa/Neutro-Lateral/Nenhuma) e variação do período
5. Avalia os 3 gatilhos técnicos com base nos últimos candles

### Lógica de Prioridade dos Gatilhos

Os gatilhos são verificados em ordem de prioridade:

```
SE   low[0] < low[1] < low[2]                      → "Dave Landry"
ELIF low[0] > low[1] < low[2]                       → "123"
ELIF low[0] > low[1] E high[0] < high[1]            → "Inside Candle"
ELSE                                                 → "Nenhum"
```

Índice `[0]` = candle mais recente (após `sort_values(date, ascending=False)`).

**Guarda mínima:** Se `len(df_historic) <= 3`, retorna "Nenhum" com campos vazios.

---

## Estágio 5: Saída Final

**Construção:** Lista de dicionários convertida em DataFrame.

**Filtragem pós-processamento:** Remove todas as linhas com `Gatilho == "Nenhum"`.

**Ordenação:** Por `ROE` decrescente — as melhores empresas do ponto de vista fundamentalista aparecem primeiro.

```python
df_final = pd.DataFrame(list_dict)
df_final = df_final[df_final["Gatilho"] != "Nenhum"]
df_final = df_final.sort_values(by="ROE", ascending=False)
```

**Resultado típico:** ~165 ações com algum gatilho ativo.

**Colunas da saída:** `Ativo`, `Gatilho`, `Empresa`, `Setor`, `Cotacao`, `RSI`, `Tendencia`, `Variacao`, `Marg_Bruta`, `Marg_Liquida`, `Marg_EBIT`, `ROE`, `EBIT_12m`, `Div_Bruta`, `Div_Liquida`.

**Funções auxiliares (ot-module):** `lista_acoes_gatilho_davy_landry(df)`, `lista_acoes_gatilho_123(df)`, `lista_acoes_gatilho_inside_candle(df)` — execução isolada por tipo de gatilho.

---

## Referências Cruzadas

- Indicadores técnicos calculados: [concepts/indicadores-tecnicos.md](indicadores-tecnicos.md)
- Screener fundamentalista (conceito): [patterns/screener-fundamentalista.md](../patterns/screener-fundamentalista.md)
- Coleta de dados históricos: [patterns/coleta-dados-b3.md](../patterns/coleta-dados-b3.md)
- Gatilhos de entrada (conceito): [concepts/gatilhos-entrada.md](gatilhos-entrada.md)
