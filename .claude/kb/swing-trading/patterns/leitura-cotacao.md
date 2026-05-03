> **MCP Validated:** 2026-03-14

# Leitura de Cotação de Ações

Como interpretar os dados de cotação e informações básicas de uma ação na B3.

---

## Estrutura de um Ticker na B3

Ações brasileiras são identificadas por um código de 4 letras + 1 número:

```
VALE3   → Vale S.A., ação ordinária (ON)
VALE5   → Vale S.A., ação preferencial (PN)  [código 5]
PETR4   → Petrobras, ação preferencial
WEGE3   → WEG S.A., ação ordinária
ITUB4   → Itaú Unibanco, ação preferencial
```

**Sufixos comuns:**
- `3` = Ação Ordinária (ON) — direito a voto
- `4` = Ação Preferencial (PN) — prioridade no dividendo, sem voto
- `11` = BDR, ETF ou FII (fundo imobiliário)

---

## Tipos de Ação: ON vs. PN

| Característica | Ordinária (ON) | Preferencial (PN) |
|----------------|---------------|------------------|
| Direito a voto | Sim | Não |
| Prioridade em dividendos | Não | Sim |
| Tag Along | 100% obrigatório | Pode variar |
| Código | Termina em 3 | Termina em 4 |

**Tag Along:** Direito do acionista minoritário de receber a mesma oferta que o acionista controlador em caso de venda do controle. Ações ON sempre têm Tag Along de 100% por lei. Verificar o Tag Along de ações PN antes de comprar (algumas têm 80% ou 100%, outras menos).

---

## Dados de Cotação

### Preço e Variação
```
Cotação atual:     R$ 18,34
Variação dia:      +2,1%  (+R$ 0,38)
Abertura:          R$ 18,05
Máxima dia:        R$ 18,52
Mínima dia:        R$ 17,90
Fechamento ant.:   R$ 17,96
```

### Volume
- **Volume financeiro:** Total em reais negociado no dia
- **Volume de contratos:** Quantidade de ações negociadas
- Volume acima da média = sinal de interesse do mercado (positivo ou negativo)

### Range e Volatilidade
- **Máxima 52 semanas / Mínima 52 semanas:** contexto histórico do preço
- Ação próxima da mínima de 52 semanas + fundamentos sólidos = possível oportunidade
- Ação próxima da máxima de 52 semanas = verificar se valuation ainda é razoável

---

## Indicadores de Mercado (Valuation)

### P/L — Preço/Lucro
```
P/L = Preço por ação / Lucro por ação (últimos 12 meses)
```
- Indica quantos anos de lucro você paga pela ação
- P/L baixo pode indicar ação barata ou empresa em dificuldade
- P/L alto pode indicar expectativa de crescimento forte
- Comparar sempre com a média histórica da empresa e do setor

### P/VP — Preço/Valor Patrimonial
```
P/VP = Preço por ação / Patrimônio Líquido por ação
```
- P/VP < 1 = ação sendo negociada abaixo do valor contábil
- Pode indicar oportunidade ou empresa com perspectivas ruins

### Dividend Yield
```
DY = Dividendos pagos por ação (12m) / Preço atual × 100
```
- Percentual de retorno via dividendos
- Empresas maduras tendem a ter DY mais alto
- DY muito alto pode indicar queda do preço (atenção ao contexto)

---

## Lendo um Resumo de Empresa no Fundamentus

Ao pesquisar uma empresa no Fundamentus, os dados disponíveis incluem:

```
Nome:              Vale S.A.
Setor:             Mineração
Valor de Mercado:  R$ 380 Bi
Participação IBOV: 12%
Tag Along:         100% (ação ON)
Fundada:           1943
P/L:               6,2
P/VP:              2,1
ROE:               15,3%
Margem Líquida:    14,2%
Div. Yield:        8,5%
```

**Dados financeiros históricos (série de anos):**
- Receita Líquida
- Lucro Líquido
- EBITDA
- Dívida Bruta / Caixa

---

## Como Usar a Cotação para Timing de Entrada

Após identificar uma boa empresa pelo screener, a cotação é usada para:

1. **Identificar tendência:** Sequência de topos e fundos (análise técnica)
2. **Identificar setup:** Pullback, padrão 1-2-3, Inside Candle
3. **Definir entrada:** Nível de preço de compra (gatilho)
4. **Definir stop:** Nível de preço de saída se der errado
5. **Calcular risco/retorno:** Distância ao stop vs. distância ao alvo

```
Risco/Retorno mínimo aceitável = 1:2
(Risco de R$1 para potencial ganho de R$2)
```

---

## Ferramentas de Gráfico

- **TradingView** — gráficos avançados, gratuito com limitações
- **Profit Pro / Metastock** — plataformas de análise técnica profissional
- **Corretoras** (XP, Rico, Clear) — gráficos básicos integrados ao home broker

---

## Referência

Fonte: Doc 03 — "Cotação das ações" (transcrição de aula). Fundamentus.com.br como ferramenta de referência citada nas aulas.
