# Guia de Uso — Agente Analista de Investimentos B3

> Documentação completa do agente `investment-analyst` para análise de ações da Bolsa Brasileira.

---

## Sumário

1. [O que é o agente](#1-o-que-é-o-agente)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Como ativar o agente](#3-como-ativar-o-agente)
4. [Casos de uso](#4-casos-de-uso)
   - [4.1 Screening completo do mercado](#41-screening-completo-do-mercado)
   - [4.2 Análise de uma ação específica](#42-análise-de-uma-ação-específica)
   - [4.3 Filtrar por setor](#43-filtrar-por-setor)
   - [4.4 Análise por período personalizado](#44-análise-por-período-personalizado)
   - [4.5 Consultar histórico de decisões](#45-consultar-histórico-de-decisões)
   - [4.6 Fechar ou atualizar uma posição](#46-fechar-ou-atualizar-uma-posição)
   - [4.7 Relatório de performance](#47-relatório-de-performance)
5. [Como o agente analisa](#5-como-o-agente-analisa)
   - [5.1 Filtro fundamentalista](#51-filtro-fundamentalista)
   - [5.2 Análise técnica](#52-análise-técnica)
   - [5.3 Notícias de mercado](#53-notícias-de-mercado)
   - [5.4 Score de confiança](#54-score-de-confiança)
6. [Entendendo as recomendações](#6-entendendo-as-recomendações)
7. [Memória de decisões](#7-memória-de-decisões)
8. [Fontes de dados](#8-fontes-de-dados)
9. [Perguntas frequentes](#9-perguntas-frequentes)

---

## 1. O que é o agente

O **investment-analyst** é um agente especializado em swing trading de ações brasileiras (B3). Ele combina três camadas de análise em uma resposta integrada:

| Camada | O que faz |
|--------|-----------|
| **Fundamentalista** | Filtra empresas por ROE, margens, dívida e valor patrimonial |
| **Técnica** | Identifica tendência (EMA/SMA) e gatilhos de entrada (Dave Landry, 1-2-3, Inside Candle) |
| **Notícias** | Consulta InfoMoney, Valor Econômico e Investing.com BR em tempo real |
| **Memória** | Registra todas as recomendações e rastreia resultados ao longo do tempo |

> **Filosofia:** Selecionar bons negócios (fundamentalista) e entrar no momento técnico certo (gatilho), evitando armadilhas identificadas pelo contexto de notícias.

---

## 2. Pré-requisitos

### Dependências Python

```bash
# Instalar todas as dependências de uma vez
pip install ot-module yfinance fundamentus ta mcp httpx feedparser beautifulsoup4 lxml
```

### Estrutura necessária

```
ClaudeTrader/
├── .mcp.json                                    ← MCP server registrado
├── mcp-b3-news/
│   └── server.py                                ← Servidor de notícias + memória
└── .claude/
    ├── kb/swing-trading/                         ← Base de conhecimento
    └── memory/investment-decisions/
        └── decisions.json                        ← Histórico de decisões
```

O arquivo `.mcp.json` já está configurado e aponta para `mcp-b3-news/server.py`. Nenhuma configuração adicional é necessária.

---

## 3. Como ativar o agente

O agente é ativado automaticamente pelo Claude Code quando você faz perguntas sobre o mercado financeiro brasileiro. Você também pode chamá-lo diretamente:

```
# Ativação implícita (Claude decide sozinho)
"Quais ações estão com bom gatilho essa semana?"
"Analisa WEGE3 pra mim"
"Como foram minhas recomendações do mês passado?"

# Ativação explícita
"Use o investment-analyst para analisar o setor de energia"
```

---

## 4. Casos de Uso

### 4.1 Screening Completo do Mercado

Analisa todas as ~400 ações da B3 e retorna as que passam no filtro fundamentalista e possuem gatilho técnico ativo.

**Exemplos de prompt:**

```
"Quais ações da B3 estão com bom setup para compra hoje?"
"Me mostra as melhores oportunidades da semana"
"Faz um screening completo do mercado"
```

**O agente vai perguntar:**
1. Qual período analisar? (padrão: última semana)
2. Quer filtrar por algum setor?
3. Filtro conservador ou pode flexibilizar algum critério?

**Exemplo de saída:**

```
## Oportunidades Identificadas — 14/03/2026 (12 ações)

### Semáforo VERDE — Comprar
| Ativo | Empresa           | Setor           | Cotação  | Gatilho     | Tendência | RSI  | ROE  |
|-------|-------------------|-----------------|----------|-------------|-----------|------|------|
| WEGE3 | WEG S.A.          | Bens Industriais| R$38,20  | Dave Landry | Alta      | 52.3 | 28%  |
| ITUB4 | Itaú Unibanco     | Financeiro      | R$34,50  | Inside C.   | Alta      | 48.1 | 21%  |

### Semáforo AMARELO — Monitorar
| BBAS3 | Banco do Brasil   | Financeiro      | R$28,10  | Nenhum      | Alta      | 44.0 | 19%  |

### Contexto de Mercado
- IBOVESPA: 128.450 pts (+0,8%)
- Notícia de destaque: "Selic mantida em 13,25% — mercado reage positivamente"
- Setor em destaque: Financeiro (5 empresas com gatilho ativo)
```

---

### 4.2 Análise de uma Ação Específica

Análise completa de um único ticker, incluindo fundamentos, técnica, notícias e histórico de decisões anteriores.

**Exemplos de prompt:**

```
"Analisa PETR4 pra mim"
"O que você acha de VALE3 agora?"
"Me dá um relatório completo de MGLU3"
"ITUB4 está bom para comprar?"
```

**Exemplo de saída:**

```
## Análise: WEGE3 — WEG S.A.
Setor: Bens Industriais | Data: 14/03/2026 | Cotação: R$38,20

### Histórico de Decisões
#3 — WEGE3 | COMPRAR @ R$35,10 | 2026-02-15 → Fechada +8,8%
Última análise confirmou tese de alta — modificador aplicado: +0.05

### Notícias Recentes
🟢 "WEG bate recorde de receita no 4T25" — InfoMoney, 10/03/2026

### Semáforo Fundamentalista
| Critério       | Valor | Threshold | Status |
|----------------|-------|-----------|--------|
| ROE            | 28%   | >= 15%    | ✓      |
| Margem EBIT    | 18%   | >= 10%    | ✓      |
| Margem Líquida | 15%   | >= 10%    | ✓      |
| Dívida/Patrim. | 0.2x  | < 3x      | ✓      |
| P/VP           | 8.1x  | > 1x      | ✓      |

### Análise Técnica
- Tendência: Alta (EMA8: 37,80 > EMA80: 35,20 > SMA200: 31,50)
- RSI(14): 52.3 → Zona neutra favorável
- Gatilho: Dave Landry Pullback (3 mínimas consecutivas decrescentes)
- Variação: 7d: +2.1% | 15d: +4.3% | 30d: +8.8%

### Veredicto
COMPRAR
Empresa de alta qualidade em tendência consolidada. Pullback controlado com RSI
em zona ideal. Histórico positivo na memória confirma a tese.

Confiança: 0.97 | Stop sugerido: R$36,50 | Entrada: R$38,20
Decisão salva — ID #7
```

---

### 4.3 Filtrar por Setor

Analisa apenas as empresas de um setor específico, útil quando você tem convicção sobre um tema macro.

**Exemplos de prompt:**

```
"Analisa ações do setor bancário"
"Quais empresas de energia elétrica estão boas?"
"Me mostra oportunidades no agronegócio"
"Screening só no setor de saúde"
```

**Setores disponíveis na B3:**

| Setor | Exemplos de empresas |
|-------|---------------------|
| Financeiro e Outros | ITUB4, BBDC4, BBAS3, B3SA3 |
| Petróleo, Gás e Biocombustíveis | PETR4, VBBR3 |
| Utilidade Pública | EGIE3, CPFE3, SAPR4 |
| Materiais Básicos | VALE3, CSNA3, GGBR4 |
| Consumo Não Cíclico | ABEV3, BEEF3, PCAR3 |
| Consumo Cíclico | MGLU3, LREN3, CYRE3 |
| Saúde | RDOR3, HAPV3, FLRY3 |
| Tecnologia da Informação | TOTVS3, LWSA3 |
| Telecomunicações | VIVT3, TIMS3 |
| Construção Civil | CYRE3, MRVE3, EVEN3 |
| Bens Industriais | WEGE3, ROMI3 |

Quando você pede análise por setor sem especificar, o agente lista os setores com contagem de empresas aprovadas e pergunta qual você quer:

```
## Setores com Empresas Aprovadas no Filtro Fundamentalista

| # | Setor                      | Empresas Aprovadas |
|---|----------------------------|--------------------|
| 1 | Financeiro e Outros        | 28                 |
| 2 | Consumo Não Cíclico        | 18                 |
| 3 | Bens Industriais           | 12                 |
| 4 | Utilidade Pública          | 11                 |
...

Qual setor você quer analisar?
```

---

### 4.4 Análise por Período Personalizado

Por padrão o agente usa os últimos 7 dias para identificar gatilhos. Você pode especificar outro período.

**Exemplos de prompt:**

```
"Analisa VALE3 nos últimos 3 meses"
"Screening do mercado no último mês"
"Quais ações tinham gatilho na semana passada?"
"Analisa PETR4 de janeiro até março de 2026"
```

**Períodos aceitos:**

| Você diz | Parâmetro usado |
|----------|----------------|
| "última semana" / "7 dias" | `period="7d"` |
| "último mês" / "30 dias" | `period="1mo"` |
| "3 meses" | `period="3mo"` |
| "6 meses" | `period="6mo"` |
| "1 ano" / "12 meses" | `period="1y"` |

> **Dica:** Para EMAs precisas (EMA80, SMA200), o agente sempre baixa pelo menos 12 meses de histórico internamente, mesmo que você peça análise de um período menor. Isso garante que as médias móveis longas sejam calculadas corretamente.

---

### 4.5 Consultar Histórico de Decisões

Consulte todas as decisões já registradas, filtrando por ação, status ou tipo de recomendação.

**Exemplos de prompt:**

```
"Mostra todas as minhas posições em aberto"
"Quais foram as recomendações de COMPRAR este mês?"
"Histórico de decisões de WEGE3"
"Mostra as últimas 10 recomendações"
"Tem alguma posição que atingiu o stop?"
```

**Exemplos de saída:**

```
## Histórico de Decisões (3 registros)

### #7 — WEGE3 | 🟡 ABERTA | COMPRAR @ R$38,20
Data: 2026-03-14 | Gatilho: Dave Landry | Confiança: 97% | Tendência: Alta | RSI: 52.3 | ROE: 28%
Justificativa: Empresa de alta qualidade em tendência consolidada...

### #6 — PETR4 | ✅ FECHADA | COMPRAR @ R$37,50 | Resultado: 📈 +6.1%
Data: 2026-03-05 | Gatilho: 1-2-3 | Confiança: 91% | Tendência: Alta | RSI: 45.0 | ROE: 18%

### #5 — MGLU3 | 🛑 STOP_ATINGIDO | COMPRAR @ R$12,10 | Resultado: 📉 -8.3%
Data: 2026-02-20 | Gatilho: Inside Candle | Confiança: 82% | Tendência: Neutro | RSI: 58.0 | ROE: 12%
Notas: 22/02/2026: Stop atingido após notícia negativa de resultado
```

---

### 4.6 Fechar ou Atualizar uma Posição

Informe ao agente quando você fechar uma posição ou quando o stop for atingido. Ele registra o resultado automaticamente.

**Exemplos de prompt:**

```
"Fechei WEGE3 hoje a R$42,50 — registra aí"
"PETR4 atingiu o stop a R$35,80"
"Vendi ITUB4 por R$38,20, lucro realizado"
"Atualiza minha posição de VALE3, tá valendo R$85,00 agora"
"Saí de todas as posições do setor financeiro"
```

O agente vai:
1. Identificar o ID da decisão pelo ticker
2. Calcular o resultado percentual automaticamente
3. Registrar o status (FECHADA ou STOP_ATINGIDO)
4. Perguntar se quer adicionar uma nota sobre a decisão

```
✅ Decisão #7 atualizada.
WEGE3: R$38,20 → R$42,50 | 📈 +11.3% | Status: FECHADA
```

---

### 4.7 Relatório de Performance

Avalie a qualidade das recomendações ao longo do tempo.

**Exemplos de prompt:**

```
"Como foi minha performance?"
"Qual minha taxa de acerto?"
"Qual gatilho dá mais certo pra mim?"
"Relatório completo de todas as decisões"
"Como estão minhas posições abertas?"
```

**Exemplo de saída:**

```
# Relatório de Performance — Decisões de Investimento

Total de decisões: 15
Em aberto: 3 | Fechadas: 10 | Stop atingido: 2

## Desempenho Geral
- Taxa de acerto: 70%
- Retorno médio: +4.8%
- Total positivas: 7 (média: +8.2%)
- Total negativas: 3 (média: -5.1%)

Melhor decisão: #6 PETR4 (+18.5%) — 2026-02-10
Pior decisão:   #5 MGLU3 (-8.3%)  — 2026-02-20

## Acerto por Gatilho
- Dave Landry:   5/7  (71%) — média +5.1%
- 1-2-3:         3/4  (75%) — média +6.2%
- Inside Candle: 2/5  (40%) — média -0.8%

## Posições em Aberto
- #7 WEGE3 @ R$38,20 | 2026-03-14 | Dave Landry
- #8 ITUB4 @ R$34,50 | 2026-03-14 | Inside Candle
- #9 BBAS3 @ R$28,10 | 2026-03-14 | 1-2-3
```

> **Insight útil:** Se Inside Candle tiver baixa taxa de acerto para você, o agente passará a aplicar um modificador de confiança negativo para esse padrão em futuras análises.

---

## 5. Como o Agente Analisa

### 5.1 Filtro Fundamentalista

Antes de qualquer análise técnica, a empresa precisa passar em **todos os 5 critérios**:

| Critério | Threshold | O que significa |
|----------|-----------|-----------------|
| **ROE** | > 15% | A empresa gera pelo menos R$0,15 de lucro para cada R$1 de patrimônio |
| **Margem EBIT** | > 10% | Pelo menos 10% da receita vira lucro operacional |
| **Margem Líquida** | > 10% | Pelo menos 10% da receita sobra após todos os custos |
| **Dívida / Patrimônio** | < 3x | A dívida total é menor que 3 vezes o patrimônio líquido |
| **P/VP** | > 1x | O mercado paga mais do que o valor patrimonial (sinal de valor reconhecido) |

**Semáforo fundamentalista:**
- 🟢 **VERDE** — Passou em todos os 5 critérios
- 🟡 **AMARELO** — Passou em 3 ou 4 critérios
- 🔴 **VERMELHO** — Menos de 3 critérios → descartada imediatamente

### 5.2 Análise Técnica

Após passar no filtro fundamentalista, são calculados:

**Tendência (EMA/SMA):**
```
Alta:           EMA(8) > EMA(80) > SMA(200)   ← empilhamento crescente
Baixa:          EMA(8) < EMA(80) < SMA(200)   ← empilhamento decrescente
Neutro/Lateral: EMA(8) entre EMA(80) e SMA(200)
Nenhuma:        demais configurações
```

**RSI(14) — Zonas de interpretação:**

| Faixa | Interpretação |
|-------|---------------|
| > 70 | Sobrecomprado — aguardar pullback antes de entrar |
| 50–70 | Momentum de alta — zona favorável |
| 40–60 | **Zona ideal de entrada** |
| 30–50 | Momentum de baixa |
| < 30 | Sobrevendido — possível reversão |

**Gatilhos de entrada (verificados nos últimos 3 candles):**

| Gatilho | Condição | Quando usar |
|---------|----------|-------------|
| **Dave Landry** | 3 mínimas consecutivas decrescentes | Pullback em tendência de alta consolidada |
| **1-2-3 de Ross** | Mínima[0] > Mínima[1] < Mínima[2] | Reversão de tendência confirmada |
| **Inside Candle** | Mínima[0] > Mínima[1] E Máxima[0] < Máxima[1] | Compressão de volatilidade antes de rompimento |

### 5.3 Notícias de Mercado

O agente consulta automaticamente:

| Fonte | Tipo de conteúdo |
|-------|-----------------|
| **InfoMoney** | Notícias gerais do mercado, por ação e busca |
| **Valor Econômico** | Manchetes de finanças e economia |
| **Investing.com BR** | Busca por tema e indicadores |
| **Status Invest** | Notícias corporativas por ticker |

As notícias influenciam o score de confiança: notícias positivas adicionam +0.05, notícias negativas relevantes subtraem -0.10.

### 5.4 Score de Confiança

Cada recomendação tem um score de 0.0 a 1.0, calculado assim:

```
Score base:  0.75 (padrão)

Modificadores positivos:
  + 0.10  Tendência de alta confirmada (EMA8 > EMA80 > SMA200)
  + 0.10  Gatilho alinhado com a tendência
  + 0.05  RSI entre 40-60 (zona ideal de entrada)
  + 0.05  Notícias positivas recentes
  + 0.05  Histórico de acerto nesse ticker na memória

Modificadores negativos:
  - 0.15  RSI > 70 (sobrecomprado)
  - 0.15  Dívida/EBITDA > 3x
  - 0.10  Notícias negativas relevantes
  - 0.10  Histórico de erro nesse ticker na memória
  - 0.20  Dados históricos insuficientes (< 12 meses)
  - 0.05  Setor cíclico (commodities)
```

**Interpretação:**
- `>= 0.95` → Alta convicção, COMPRAR
- `0.90–0.94` → Boa convicção, COMPRAR com cautela
- `0.80–0.89` → Convicção moderada, MONITORAR
- `< 0.80` → Baixa convicção, aguardar ou DESCARTAR

---

## 6. Entendendo as Recomendações

### Semáforo Final

| Resultado | Condições |
|-----------|-----------|
| **COMPRAR** | Fundamentalista VERDE + Tendência Alta + Gatilho ativo + RSI < 65 + sem notícias negativas críticas |
| **MONITORAR** | Fundamentalista VERDE + Tendência Alta mas sem gatilho, ou Tendência Neutra com RSI < 50 |
| **DESCARTAR** | Fundamentalista VERMELHO, ou Tendência de Baixa com RSI > 60, ou Dívida > 3x EBITDA |

### Stop Loss

Quando o agente recomenda COMPRAR, ele sempre sugere um stop loss:

| Gatilho | Stop sugerido |
|---------|--------------|
| Dave Landry | Abaixo da mínima do pullback |
| 1-2-3 | Abaixo do Ponto 3 (terceiro fundo) |
| Inside Candle | Abaixo da mínima do candle interno |

### Alertas Automáticos

O agente sempre avisa quando:
- **Setor cíclico**: a queda de receita pode ser do ciclo da commodity, não da empresa
- **ROE > 40%**: verificar se não é alavancagem artificial mascarando risco
- **Gatilho sem tendência confirmada**: risco elevado de falso sinal

---

## 7. Memória de Decisões

Todas as recomendações são salvas automaticamente em:

```
.claude/memory/investment-decisions/decisions.json
```

### Estrutura de uma decisão salva

```json
{
  "id": 7,
  "ticker": "WEGE3",
  "acao": "COMPRAR",
  "preco_entrada": 38.20,
  "preco_atual": null,
  "resultado_pct": null,
  "status": "ABERTA",
  "gatilho": "Dave Landry",
  "justificativa": "Empresa de alta qualidade em tendência consolidada...",
  "confianca": 0.97,
  "stop_loss": 36.50,
  "setor": "Bens Industriais",
  "tendencia": "Alta",
  "rsi": 52.3,
  "roe": 28.0,
  "data_decisao": "2026-03-14T10:35:00",
  "data_fechamento": null,
  "notas": []
}
```

### Status possíveis

| Status | Ícone | Significado |
|--------|-------|-------------|
| `ABERTA` | 🟡 | Posição ainda ativa, sem resultado final |
| `FECHADA` | ✅ | Posição encerrada com lucro ou prejuízo |
| `STOP_ATINGIDO` | 🛑 | Stop loss foi acionado |

### Como a memória melhora as análises futuras

Na próxima vez que você pedir análise de WEGE3, o agente vai:

1. Carregar o histórico de decisões para esse ticker
2. Mostrar os resultados anteriores
3. Aplicar modificadores no score de confiança:
   - Se o histórico tem mais acertos → +0.05
   - Se o histórico tem mais erros → -0.10
4. Informar explicitamente: _"Analisamos WEGE3 em 14/03/2026 — resultado: +11.3%"_

---

## 8. Fontes de Dados

| Fonte | Dados | Acesso |
|-------|-------|--------|
| **Fundamentus** (fundamentus.com.br) | ROE, margens, dívida, P/VP, receita | Gratuito via biblioteca Python |
| **Yahoo Finance** (yfinance) | OHLCV histórico, 12 meses | Gratuito via API |
| **dadosdemercado.com.br** | Lista completa de tickers B3 (~400) | Gratuito via scraping |
| **InfoMoney** (infomoney.com.br) | Notícias de mercado e por ação | Gratuito via RSS + scraping |
| **Valor Econômico** (valor.globo.com) | Manchetes financeiras | Gratuito via RSS |
| **Investing.com BR** | Busca de notícias por tema | Gratuito via scraping |
| **Status Invest** (statusinvest.com.br) | Notícias corporativas por ticker | Gratuito via scraping |

> **Importante:** O agente usa apenas fontes gratuitas e públicas. Nenhuma API paga ou chave de acesso é necessária.

---

## 9. Perguntas Frequentes

**Q: O agente garante retorno positivo?**
> Não. O agente aplica metodologia consistente e registra decisões para aprendizado, mas mercado financeiro envolve risco. Use as recomendações como ponto de partida para sua própria avaliação.

**Q: Por que o agente pergunta sobre o período antes de analisar?**
> Gatilhos de curto prazo (Inside Candle, Dave Landry) são mais relevantes para entradas imediatas. Gatilhos de médio prazo (1-2-3) requerem mais contexto histórico. A pergunta garante que a análise seja adequada ao seu horizonte.

**Q: O que significa "Tendência: Neutro/Lateral"?**
> Significa que as EMAs não estão em empilhamento claro. Nem alta nem baixa definida. O agente vai recomendar MONITORAR, não COMPRAR, e aguardar uma definição de tendência.

**Q: Por que o agente usa RSI com Wilder smoothing em vez do padrão?**
> O RSI de Wilder usa suavização recursiva (`avg_gain[i] = (avg_gain[i-1] × 13 + gain[i]) / 14`), que preserva memória exponencial de todas as velas. O rolling mean descarta velas fora da janela. Wilder é o método original e mais preciso para séries curtas.

**Q: Posso pedir análise de um ticker que não está na B3?**
> O agente é especializado na B3. Tickers precisam ter cotação no Yahoo Finance com sufixo `.SA` (ex: WEGE3.SA). Ações americanas ou de outras bolsas não são suportadas.

**Q: O arquivo `decisions.json` pode ser editado manualmente?**
> Sim, é um JSON simples. Mas prefira usar os comandos do agente para garantir consistência dos campos e IDs.

**Q: O que acontece se uma notícia estiver indisponível?**
> O servidor de notícias tem fallback para RSS quando o scraping falha. Se nenhuma fonte responder, o agente prossegue com a análise e informa que as notícias não puderam ser verificadas — o score de confiança não recebe o modificador positivo nesse caso.

---

*Documentação gerada em 2026-03-14 | Versão do agente: 2.0.0*
