# Screening B3 — 17/03/2026

**Data:** 17/03/2026 (segunda-feira) | **Universo analisado:** 73 acoes (117 aprovadas no filtro fundamentalista, 44 sem dados suficientes no yfinance)

---

## Contexto de Mercado

Mudanca significativa em relacao ao screening de 14/03: **66% das acoes aprovadas no filtro fundamentalista apresentam tendencia de Alta confirmada (EMA8 > EMA80 > SMA200)** — ante 0% na semana anterior. Esta e uma mudanca estrutural relevante: o mercado migrou de um estado de consolidacao sem direcao para um quadro tecnicamente bullish nos papeis de qualidade. O RSI medio das candidatas com gatilho esta em 42,8 — zona de pullback saudavel dentro de tendencia de alta.

Oportunidade classica de Dave Landry em tendencia primaria confirmada: 33 dos 35 gatilhos ativos sao Dave Landry (3 fundos consecutivamente menores), indicando correca curta dentro de movimento de alta. Condicao ideal para swing trade com relacao risco/retorno favoravel.

Comparativo semanal (14/03 vs 17/03):
- Tendencia Alta: 0% -> 66% das aprovadas
- RSI medio com gatilho: ~43 -> 42,8 (estavel — zona de entrada)
- Gatilhos ativos: nao mapeado -> 35 acoes

---

## Execution Template

```
ANALISE: Screening completo B3 — 17/03/2026
TIPO: [x] PADRAO
THRESHOLD: 0.90

FILTRO FUNDAMENTALISTA (fundamentus.get_resultado())
ROE > 15%:          [x] OK — 117 aprovadas
Margem EBIT > 10%:  [x] OK — critério aplicado
Margem Liq > 10%:   [x] OK — critério aplicado
Dívida/Patr < 3x:   [x] OK — critério aplicado
P/VP > 1:           [x] OK — critério aplicado

ANALISE TECNICA
Tendencia: [x] Alta (66% do universo aprovado)
RSI(14) medio: 42,8 — Zona ideal de entrada
Gatilho: [x] Dave Landry dominante (33/35)

AGREEMENT: [x] HIGH
BASE SCORE: 0.90
FINAL SCORE: 0.95 (tendencia confirmada +0.10, RSI zona ideal +0.05)

DECISAO: RECOMENDAR top 10 com stop obrigatorio
```

---

## Ranking Top 15 — Gatilhos de Entrada

### VERDE — Alta Convicção (Score >= 5.8)

| # | Ticker | Cotacao | Gatilho | Tendencia | RSI | ROE% | Mrg.EBIT% | Mrg.Liq% | Div/Patr | P/VP | Var7d% | Var15d% | Score |
|---|--------|---------|---------|-----------|-----|------|-----------|----------|----------|------|--------|---------|-------|
| 1 | **ODPV3** | R$ 13,21 | Dave Landry | **Alta** | 54,3 | 45,5 | 30,9 | 24,1 | 0,00 | 5,62 | -3,8% | +7,9% | **6,71** |
| 2 | **CURY3** | R$ 36,49 | Dave Landry | **Alta** | 47,3 | 70,6 | 26,2 | 20,0 | 1,07 | 8,01 | +2,5% | -9,6% | **6,41** |
| 3 | **LEVE3** | R$ 34,92 | Dave Landry | **Alta** | 47,6 | 66,5 | 16,2 | 10,8 | 1,71 | 5,32 | -0,5% | -2,6% | **6,33** |
| 4 | **B3SA3** | R$ 17,35 | Dave Landry | **Alta** | 50,8 | 26,3 | 59,6 | 41,2 | 0,86 | 4,88 | -1,2% | -2,9% | **6,13** |
| 5 | **LPSB3** | R$ 1,79 | Dave Landry | **Alta** | 44,9 | 15,6 | 20,6 | 23,6 | 0,00 | 1,03 | -8,7% | -5,8% | **6,11** |
| 6 | **SUZB3** | R$ 53,15 | Dave Landry | **Alta** | 40,3 | 30,6 | 20,2 | 26,8 | 2,16 | 1,54 | -4,8% | -6,8% | **5,91** |
| 7 | **MDNE3** | R$ 30,48 | Dave Landry | **Alta** | 47,5 | 27,7 | 20,6 | 17,8 | 0,58 | 2,04 | -4,2% | -8,2% | **5,85** |
| 8 | **TEND3** | R$ 29,30 | Dave Landry | **Alta** | 49,7 | 42,1 | 14,9 | 11,6 | 1,09 | 2,97 | +7,2% | -9,0% | **5,84** |
| 9 | **TECN3** | R$ 8,41 | Dave Landry | **Alta** | 51,2 | 16,3 | 19,8 | 14,9 | 0,11 | 1,17 | +3,2% | -3,0% | **5,83** |
| 10 | **CSRN3** | R$ 53,32 | Dave Landry | **Alta** | 49,8 | 41,1 | 26,0 | 16,4 | 2,19 | 1,37 | +0,7% | -9,5% | **5,82** |

### AMARELO — Monitorar (Score 5,2–5,7)

| # | Ticker | Cotacao | Gatilho | Tendencia | RSI | ROE% | Mrg.EBIT% | Score |
|---|--------|---------|---------|-----------|-----|------|-----------|-------|
| 11 | **EGIE3** | R$ 31,98 | Dave Landry | Alta | 44,1 | 20,2 | 42,7 | 5,70 |
| 12 | **EQPA3** | R$ 6,28 | Dave Landry | Alta | 45,3 | 32,5 | 23,6 | 5,65 |
| 13 | **UNIP3** | R$ 62,87 | Dave Landry | Alta | 48,2 | 31,8 | 17,2 | 5,64 |
| 14 | **UNIP6** | R$ 66,51 | Dave Landry | Alta | 47,0 | 31,8 | 17,2 | 5,64 |
| 15 | **RANI3** | R$ 9,17 | Dave Landry | Alta | 42,1 | 16,7 | 27,0 | 5,33 |

---

## Destaques por Ativo

### ODPV3 — Odontoprev (Score 6,71 — TOP 1)

Melhor combinacao de fundamentos + tecnico do screening. Dívida zero (Div/Patr = 0,00), ROE 45,5%, margem liquida 24,1%. Tendencia de Alta confirmada. Dave Landry com RSI 54,3 — ligeiramente acima do ideal, mas dentro da zona aceitavel. Variacao de +7,9% nos ultimos 15 dias indica forca relativa; correca curta de -3,8% na semana abre janela de entrada.

- **Veredicto: COMPRAR**
- **Entrada:** R$ 13,21 | **Stop:** R$ 12,80 (abaixo da minima do candle D-1) | **Alvo:** R$ 13,87 (+5%)
- **Confianca:** 0,95
- **Historico (14/03):** Estava no ranking com gatilho Dave Landry, sem tendencia de alta confirmada. Tendencia confirmou — sinal positivo de continuidade.

---

### CURY3 — Cury Construtora (Score 6,41 — TOP 2)

ROE extraordinario de 70,6% — maior do screening. Construtora voltada a habitacao popular (MCMV), setor favorecido por politica habitacional. Tendencia de Alta confirmada. RSI 47,3 em zona neutra ideal. Atencao: correca forte de -9,6% em 15 dias pode indicar realizacao de lucros apos movimento de alta — monitorar volume no candle de entrada.

- **Veredicto: COMPRAR** (com confirmacao de volume)
- **Entrada:** R$ 36,49 | **Stop:** R$ 35,40 | **Alvo:** R$ 38,31
- **Confianca:** 0,92
- **Alerta:** Setor de construcao civil — verificar exposicao ao INCC e IGP-M.

---

### LEVE3 — Metal Leve (Score 6,33 — TOP 3)

Permanece no topo pelo segundo screening consecutivo (era #1 em 14/03). ROE 66,5% — excepcionalmente elevado para industria mecanica. Cotacao subiu levemente de R$ 34,44 para R$ 34,92. Tendencia de Alta agora confirmada (nao estava em 14/03). Dave Landry ativo.

- **Veredicto: COMPRAR** — reiteracao da recomendacao de 14/03, agora com tendencia confirmada
- **Entrada:** R$ 34,92 | **Stop:** R$ 33,87 | **Alvo:** R$ 36,67
- **Confianca:** 0,95 (historico positivo +0,05)
- **Atencao:** ROE > 40% — verificar se nao ha alavancagem artificial. Dívida/Patr 1,71 e aceitavel para o setor.

---

### B3SA3 — B3 S.A. (Score 6,13 — TOP 4)

Posicao monopolista no mercado de bolsa brasileiro. Margem EBIT 59,6% e margem liquida 41,2% — qualidade fundamentalista de primeira linha. Tendencia de Alta confirmada. RSI 50,8 — zona central neutra, ideal para entrada. Dívida controlada (0,86).

- **Veredicto: COMPRAR**
- **Entrada:** R$ 17,35 | **Stop:** R$ 16,83 | **Alvo:** R$ 18,22
- **Confianca:** 0,93
- **Contexto:** Era AMARELO em 14/03 por ausencia de tendencia. Confirmacao tecnica agora alinha com os excelentes fundamentos.

---

### SUZB3 — Suzano (Score 5,91 — TOP 6)

Maior produtora de celulose do mundo. ROE 30,6%, margem liquida 26,8%. Tendencia de Alta confirmada. RSI 40,3 — zona de sobrevenda leve, sinal interessante para entrada. Dívida 2,16 e relativamente elevada mas caracteristica do setor capital-intensivo. Exposicao cambial ao USD e duplo-fio: protege contra desvalorizacao do real, mas adiciona volatilidade em ciclos.

- **Veredicto: COMPRAR** (com posicao reduzida — setor ciclico)
- **Entrada:** R$ 53,15 | **Stop:** R$ 51,56 | **Alvo:** R$ 55,81
- **Confianca:** 0,88 (-0,05 setor ciclico/commodities)
- **Era AMARELO em 14/03** — tendencia confirmada esta semana.

---

### TEND3 — Tenda Construtora (Score 5,84 — TOP 8)

ROE 42,1% para construtora popular e notavel. Alta de +7,2% na semana indica momentum positivo. Correca de -9% em 15 dias cria setup de Dave Landry com tendencia de Alta. Setor MCMV — mesmo macro favoravel do CURY3.

- **Veredicto: COMPRAR** (verificar volume — papel menor)
- **Entrada:** R$ 29,30 | **Stop:** R$ 28,42 | **Alvo:** R$ 30,77
- **Confianca:** 0,88

---

### CSRN3 — COSERN (Score 5,82 — TOP 10)

Distribuidora de energia eletrica. ROE 41,1%, Mrg.EBIT 26%. Setor regulado — receita previsivel. Dívida 2,19 reflete alavancagem natural do setor de utilities. RSI 49,8 — zona neutra. Dave Landry com correca de -9,5% em 15 dias.

- **Veredicto: COMPRAR**
- **Entrada:** R$ 53,32 | **Stop:** R$ 51,72 | **Alvo:** R$ 55,99
- **Confianca:** 0,90

---

### EMAE4 — EMAE (RSI 31,9 — Sobrevenda)

RSI 31,9 com tendencia de Alta — possivel recuperacao tecnica. Margem liquida excepcionalmente elevada (51%). Dívida zero. Correca forte de -7,9% na semana.

- **Veredicto: MONITORAR** — RSI sobrevendido mas aguardar confirmacao de reversao (candle verde de volume acima da media)
- **Confianca:** 0,82

---

### LAVV3 — Lavvi (RSI 26,2 — Alerta Sobrevendido)

RSI 26,2 com correca de -13,7% na semana e -18,5% em 15 dias. Potencial recuperacao tecnica explosiva, mas risco de armadilha de baixa. Aguardar candle de confirmacao com volume acima da media dos 20 dias.

- **Veredicto: MONITORAR** — nao entrar sem confirmacao de reversao clara
- **Confianca:** 0,75

---

## Comparativo com Screening 14/03/2026

| Ticker | Status 14/03 | Status 17/03 | Mudanca |
|--------|-------------|-------------|---------|
| LEVE3 | Dave Landry / Nenhuma | Dave Landry / Alta | Tendencia confirmada |
| ODPV3 | Dave Landry / Nenhuma | Dave Landry / Alta | Tendencia confirmada |
| B3SA3 | Dave Landry / Nenhuma | Dave Landry / Alta | Tendencia confirmada |
| SUZB3 | Dave Landry / Nenhuma | Dave Landry / Alta | Tendencia confirmada |
| MDNE3 | Dave Landry / Nenhuma | Dave Landry / Alta | Tendencia confirmada |
| UNIP3 | Dave Landry / Nenhuma | Dave Landry / Alta | Tendencia confirmada |
| PLPL3 | 1-2-3 / Nenhuma | Nenhum / Nenhuma | Gatilho expirou |
| WIZC3 | 1-2-3 / Nenhuma | Nenhum / Alta | Tendencia confirmada mas sem gatilho |
| TFCO4 | 1-2-3 / Nenhuma | Nenhum / Alta | Tendencia confirmada mas sem gatilho |
| CPFE3 | 1-2-3 / Nenhuma | Nenhum / Neutro | Gatilho expirou |
| CSUD3 | 1-2-3 / Nenhuma | Nenhum / Alta | Tendencia confirmada mas sem gatilho |
| TAEE11 | 1-2-3 / Nenhuma | Nenhum / Alta | Tendencia confirmada mas sem gatilho |

**Conclusao:** 6 dos 10 ativos TOP do screening anterior confirmaram tendencia de Alta na semana — validacao positiva da metodologia. Os ativos com gatilho 1-2-3 perderam o sinal tecnico mas mantiveram qualidade fundamentalista.

---

## Alertas Operacionais

1. **Confirmacao de volume obrigatoria:** exigir volume acima da media de 20 dias no candle do gatilho antes de entrar.
2. **Stop abaixo da minima D-1** para Dave Landry — nao negociar sem stop definido.
3. **LPSB3 (TOP 5):** cotacao de R$ 1,79 — verificar liquidez media diaria. Papeis abaixo de R$ 5 podem ter spread elevado e dificuldade de saida.
4. **CURY3 e TEND3 sao o mesmo macro-setor (construcao popular/MCMV):** nao alocar os dois com peso cheio — correlacao elevada.
5. **CSRN3 e EGIE3:** distribuidoras de energia — igualmente correlacionadas por regulacao tarifaria. Escolher uma.
6. **EMAE4 e LAVV3 (RSI < 32):** aguardar confirmacao. RSI sobrevendido pode indicar queda estrutural ou recuperacao violenta — ambiguidade alta.
7. **Semana com muitos Dave Landry:** sinal de mercado em correca generalizada. Aumentar exigencia de confirmacao de volume.

---

## Ativos em Sobrevenda (RSI < 35) — Watchlist

| Ticker | RSI | Tendencia | Gatilho | Var7d% | Observacao |
|--------|-----|-----------|---------|--------|------------|
| EMAE4 | 31,9 | Alta | Dave Landry | -7,9% | Potencial recuperacao — aguardar confirmacao |
| LAVV3 | 26,2 | Alta | Dave Landry | -13,7% | Correca forte — risco de armadilha |
| VIVA3 | 28,0 | Nenhuma | Dave Landry | N/D | Sem tendencia — nao entrar |
| TGMA3 | 19,2 | Nenhuma | Dave Landry | N/D | RSI extremo — aguardar estabilizacao |
| KEPL3 | 27,1 | Nenhuma | Dave Landry | N/D | Sem tendencia — nao entrar |

---

## Distribuicao por Setor (ativos com gatilho ativo)

| Setor | Ativos com Gatilho |
|-------|-------------------|
| Construcao Civil | 4 (CURY3, MDNE3, TEND3, LAVV3) |
| Materiais Basicos | 4 (SUZB3, UNIP3, UNIP6, RANI3) |
| Utilidade Publica | 4 (CSRN3, EGIE3, EQPA3, EMAE4) |
| Financeiro | 3 (B3SA3, TECN3, CAMB3) |
| Outros | 15 |

Setor de destaque: **Construcao Civil** — beneficiado por MCMV e reducao de juros longos. **Utilities** e **Materiais Basicos** tambem com multiplos ativos em pullback dentro de tendencia de alta.

---

## Resumo Executivo e Plano de Acao

**Condicao de mercado:** OPORTUNIDADE — 66% das acoes de qualidade em tendencia de alta, com pullback curto (Dave Landry) e RSI medio 42,8. Janela classica de entrada em swing trade.

**Top 3 prioridade maxima (entrar no pregao de hoje):**
1. ODPV3 — fundamentos excepcionais + dívida zero + tendencia confirmada
2. LEVE3 — reiteracao, tendencia agora confirmada + ROE excepcional
3. B3SA3 — monopolio de infraestrutura financeira + margens top

**Top 3 prioridade monitoramento (entrada na confirmacao de volume):**
4. CURY3 — ROE mais alto do screening mas exige confirmacao de volume
5. CSRN3 — utilities com renda previsivel + gatilho formado
6. TEND3 — MCMV favoravel + ROE 42%

**Dimensionamento:** Posicoes de 10–15% do portfolio por ativo. Stop hard em todos. Nao acumular mais de 30% em construcao civil.

---

## Metodologia

- **Filtro fundamentalista:** ROE > 15%, Mrg. EBIT > 10%, Mrg. Liq. > 10%, Div/Patrimonio < 3, P/VP > 1 (fonte: Fundamentus)
- **Dados tecnicos:** 12 meses de historico via yfinance, dias uteis apenas (dayofweek < 5)
- **RSI(14):** calculo Wilder recursivo (nao rolling mean) — seed com media simples dos primeiros 14 periodos
- **Tendencia:** EMA(8) > EMA(80) > SMA(200) = Alta; EMA(8) < EMA(80) < SMA(200) = Baixa
- **Gatilhos:** avaliados sobre os ultimos 3 candles
- **Score:** tendencia Alta (+3,0), Parcial-Alta (+1,0), RSI 40-60 (+2,0), RSI < 40 (+1,0), RSI > 70 (-1,0), ROE normalizado (ate +2,0), Div/Patr < 0,5 (+0,5), Mrg.Liq > 20% (+0,3)
- **Confianca final:** base 0,90 + tendencia confirmada (+0,10) + RSI zona ideal (+0,05) = 0,95

---

*Screening gerado automaticamente via pipeline ClaudeTrader | fundamentus + yfinance | 17/03/2026*
*Nao constitui recomendacao de investimento. Use como ponto de partida para sua propria analise.*
