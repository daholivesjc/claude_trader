> **MCP Validated:** 2026-03-14

# Swing Trading — Quick Reference

## 5 Filtros Fundamentalistas (Screener)

| # | Critério | Threshold | Lógica |
|---|----------|-----------|--------|
| 1 | Receita Líquida | Crescente (3 anos) | Empresa vendendo mais ano a ano |
| 2 | Lucro Líquido | Crescente ou positivo | Transformando receita em lucro |
| 3 | Margem de Lucro | >= 15% | Poder de manobra em crises |
| 4 | ROE | >= 15% | Retorno sobre patrimônio próprio |
| 5 | Divida Liq / EBITDA | <= 3x | Dívida controlada |

## Fórmulas Rápidas

```
Receita Líquida    = Vendas brutas - descontos - impostos sobre venda
Lucro Líquido      = Receita total - despesa total
Margem de Lucro %  = (Lucro Líquido / Receita Líquida) x 100
ROE %              = (Lucro Líquido / Patrimônio Líquido) x 100
Dívida Líquida     = Dívidas totais - Caixa
Div. Líq / EBITDA  = Dívida Líquida / EBITDA  (alarme: > 3x)
```

## Tendências (Pring — 3 horizontes)

| Tendência | Duração típica | Uso |
|-----------|---------------|-----|
| Primária | 9 meses a 2 anos | Direção geral do mercado |
| Intermediária | 6 semanas a 9 meses | Timing de entrada/saída |
| Curto prazo | 3 a 6 semanas | Swing trading entry |

## Gatilhos de Entrada (Análise Técnica)

| Gatilho | Sinal | Condição |
|---------|-------|----------|
| Dave Landry Pullback | Alta após retração | Tendência de alta estabelecida + pullback curto |
| 1-2-3 de Ross | Reversão confirmada | Pico abaixo do anterior + fundo acima do anterior |
| Inside Candle | Compressão + rompimento | Candle dentro do anterior + rompimento da máxima |

## DCA — Regra de Ouro

- Compre mensalmente, independente de a bolsa subir ou cair
- Em 97% dos casos supera a estratégia de "esperar o fundo"
- Errar o fundo por 2 meses já reduz performance de 70% para 3%

## Progressão Pico-e-Vale (Pring)

```
Alta:  série de topos e fundos CRESCENTES
Baixa: série de topos e fundos DECRESCENTES
Reversão de alta: primeiro fundo abaixo do anterior (ponto X)
Reversão de baixa: primeiro topo acima + fundo acima do anterior
```

## Semáforo de Qualidade

```
VERDE  = receita crescente + lucro crescente + margem > 15% + ROE > 15% + div/EBITDA < 3
AMARELO = 3-4 critérios atendidos
VERMELHO = < 3 critérios ou prejuízo recorrente
```

## Indicadores Técnicos

### RSI(14) — Thresholds de Interpretação

| Faixa | Sinal |
|-------|-------|
| > 70 | Sobrecomprado — potencial reversão de alta |
| 50–70 | Tendência de alta — momentum positivo |
| 30–50 | Tendência de baixa — momentum negativo |
| < 30 | Sobrevendido — potencial reversão de baixa |

**Método:** Wilder smoothing recursivo (`avg_gain[i] = (avg_gain[i-1] * 13 + gain[i]) / 14`)
**Diferença do rolling mean:** Wilder preserva memória exponencial; rolling mean descarta candles fora da janela.

### Regras de Tendência (get_trend)

```
EMAs usadas: EMA(8) = curta | EMA(80) = longa | SMA(200) = longa200

Alta:           EMA(8) > EMA(80) > SMA(200)   empilhamento crescente
Baixa:          EMA(8) < EMA(80) < SMA(200)   empilhamento decrescente
Neutro/Lateral: EMA(8) sanduichada entre EMA(80) e SMA(200)
                OU EMA(8) acima de ambas as longas (divergência)
Nenhuma:        demais configurações
```

### Filtro Fundamentalista — Thresholds Exatos (fundamentus)

```
roe      > 0.15   ROE acima de 15%
mrgebit  > 0.10   Margem EBIT acima de 10%
mrgliq   > 0.10   Margem líquida acima de 10%
divbpatr < 3.00   Dívida bruta / patrimônio abaixo de 3x
pvp      > 1.00   Preço / valor patrimonial acima de 1
```

### Coleta yfinance — Parâmetros B3

```python
yf.download(ticker + ".SA", period="12mo", progress=False)
# Colunas resultantes: ["date", "close", "high", "low", "open", "volume"]
# Filtro pós-download:  df[df['date'].dt.dayofweek < 5]
```
