> **MCP Validated:** 2026-03-14

# Swing Trading / Bolsa Brasileira (B3)

Domínio de conhecimento sobre investimento em ações na B3, análise fundamentalista e técnica para swing trading.

---

## Visão Geral

Este domínio cobre os fundamentos para seleção de ações e operações de swing trading no mercado brasileiro, integrando análise fundamentalista (qualidade do negócio) com análise técnica (momento de entrada).

**Princípio central:** No longo prazo, a cotação de uma ação tende a acompanhar os resultados da empresa. No curto prazo, fatores irracionais dominam. A estratégia é selecionar bons negócios e entrar em momentos técnicos favoráveis.

---

## Conceitos

| Conceito | Arquivo | Descrição |
|----------|---------|-----------|
| Por que ações sobem e caem | [concepts/por-que-acoes-sobem-e-caem.md](concepts/por-que-acoes-sobem-e-caem.md) | Oferta, demanda e fundamentos |
| Análise fundamentalista | [concepts/analise-fundamentalista.md](concepts/analise-fundamentalista.md) | Como avaliar a qualidade de um negócio |
| Métricas financeiras | [concepts/metricas-financeiras.md](concepts/metricas-financeiras.md) | ROE, margens, dívida, receita, lucro |
| Análise técnica | [concepts/analise-tecnica.md](concepts/analise-tecnica.md) | Tendências, padrões, Pring |
| Gatilhos de entrada | [concepts/gatilhos-entrada.md](concepts/gatilhos-entrada.md) | Dave Landry, 1-2-3, Inside Candle |
| Indicadores técnicos | [concepts/indicadores-tecnicos.md](concepts/indicadores-tecnicos.md) | RSI(14) Wilder, EMA(8/80), SMA(200), classificação de tendência |
| Pipeline do screener | [concepts/pipeline-screener.md](concepts/pipeline-screener.md) | Arquitetura completa dos 5 estágios do SwingTrade.ipynb |

## Padrões

| Padrão | Arquivo | Descrição |
|--------|---------|-----------|
| Screener fundamentalista | [patterns/screener-fundamentalista.md](patterns/screener-fundamentalista.md) | 5 passos para filtrar ações |
| Dollar Cost Averaging | [patterns/dollar-cost-averaging.md](patterns/dollar-cost-averaging.md) | Compra mensal sistemática |
| Leitura de cotação | [patterns/leitura-cotacao.md](patterns/leitura-cotacao.md) | Como ler dados de uma ação |
| Cálculo RSI Wilder | [patterns/calculo-rsi-wilder.md](patterns/calculo-rsi-wilder.md) | Implementação recursiva do RSI com suavização original de Wilder |
| Coleta de dados B3 | [patterns/coleta-dados-b3.md](patterns/coleta-dados-b3.md) | yfinance + sufixo .SA + filtro de fim de semana |

---

## Fontes de Dados

- **Fundamentus.com.br** — dados fundamentalistas de empresas brasileiras
- **B3** — dados oficiais de mercado
- Ferramenta citada nas aulas: site de fundamentos com mais de 6.000 ativos

---

## Contexto de Uso

Este KB foi criado para alimentar o `SwingTrade.ipynb` com lógica de seleção e gatilhos de entrada baseados nas aulas transcritas e no livro "Análise Técnica Explicada" de Martin J. Pring (5a edição).
