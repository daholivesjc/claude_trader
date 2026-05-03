> **MCP Validated:** 2026-03-14

# Screener Fundamentalista — 5 Passos

Processo de filtragem para reduzir o universo de ~400 ações da B3 para um conjunto de 10-20 empresas de qualidade.

---

## Visão Geral

```
~400 ações B3
    ↓  Passo 1: Receita Líquida Crescente
    ↓  Passo 2: Lucro Líquido Crescente
    ↓  Passo 3: Margem de Lucro >= 15%
    ↓  Passo 4: ROE >= 15%
    ↓  Passo 5: Dívida Líquida / EBITDA <= 3x
10-20 empresas qualificadas
    ↓  Análise qualitativa + comparativo setorial
5-10 candidatas à carteira
```

---

## Passo 1: Receita Líquida Crescente

**Critério:** Receita líquida crescendo nos últimos 3 anos consecutivos.

**Como verificar (Fundamentus):**
1. Abrir o perfil da empresa
2. Ir em "Dados Financeiros"
3. Verificar coluna "Receita Líquida" (últimos 3-5 anos)
4. A linha deve ser ascendente

**Exceções aceitáveis:**
- Queda pontual por evento não recorrente (ex: crise COVID em 2020)
- Setor cíclico com queda de commodity (verificar se é cíclico ou estrutural)

**Descarta imediatamente:**
- Receita em queda 2 ou mais anos consecutivos sem explicação plausível

---

## Passo 2: Lucro Líquido Crescente (ou Positivo e Estável)

**Critério:** Lucro líquido positivo e preferencialmente crescente nos últimos 3 anos.

**Variações aceitáveis:**
- Prejuízo em 1 único ano por evento não recorrente → verificar causa
- Empresa em fase de crescimento com horizonte claro de lucratividade → posição menor

**Descarta:**
- Prejuízo recorrente em múltiplos anos (ex: GOL com prejuízo alternando com pequeno lucro)
- Empresa sem perspectiva de gerar lucro

**Atenção:** Diferenciar lucro recorrente de lucro por venda de ativo ou ganho financeiro pontual.

---

## Passo 3: Margem de Lucro >= 15%

**Critério:** Margem líquida média dos últimos 3 anos acima de 15%.

**Cálculo:**
```python
margem = (lucro_liquido / receita_liquida) * 100
```

**Por que 15%:**
- Empresas com margem acima de 15% têm poder de manobra em crises
- Podem reduzir preços temporariamente e sobreviver
- Margens baixas (<5%) deixam a empresa vulnerável a qualquer choque de custo

**Contexto por setor:**
- Varejo: margens naturalmente baixas (~5-10%) — comparar com pares do setor
- Tecnologia/Software: margens acima de 20% são comuns
- Infraestrutura: margens médias (15-25%)

**Flexibilidade:** Em setores de margens naturalmente baixas (varejo), o threshold pode ser reduzido para 8-10% desde que a empresa seja a melhor do setor.

---

## Passo 4: ROE >= 15%

**Critério:** Retorno sobre Patrimônio Líquido médio dos últimos 3 anos acima de 15%.

**Cálculo:**
```python
roe = (lucro_liquido / patrimonio_liquido) * 100
```

**O que ROE > 15% significa:** A empresa gera R$15 de lucro para cada R$100 de patrimônio. É eficiente no uso dos próprios recursos.

**Cuidado com ROE inflado por dívida:** Se a empresa tem muito leverage (dívida alta), o patrimônio líquido é baixo artificialmente, elevando o ROE. Sempre verificar junto com o Passo 5.

**Empresas excelentes de referência:**
- WEG: ROE de 17-20% consistente
- Google (referência americana): ROE ~21%
- Facebook (referência americana): ROE ~26%

---

## Passo 5: Dívida Líquida / EBITDA <= 3x

**Critério:** Relação entre dívida líquida e EBITDA abaixo de 3x.

**Cálculo:**
```python
divida_liquida = dividas_totais - caixa_disponivel
relacao = divida_liquida / ebitda
# alerta se relacao > 3
```

**Interpretação:**
```
< 0x  = empresa tem caixa líquido positivo (excelente)
0-1x  = endividamento muito baixo (ótimo)
1-2x  = endividamento saudável (bom)
2-3x  = endividamento aceitável (monitorar)
> 3x  = endividamento preocupante (sinal de alerta)
```

**Setores que podem operar com mais dívida:**
- Transmissão de energia elétrica: dívida para financiar linhas, retorno previsível
- Saneamento: projetos de longo prazo com receita regulada
- Nesses setores, analisar o perfil da dívida (prazo, custo, garantia de receita)

---

## Execução Prática

### Usando Fundamentus.com.br

```
1. Acessar fundamentus.com.br
2. Na barra superior, pesquisar pelo ticker ou nome da empresa
3. Verificar aba "Dados Financeiros" → séries históricas
4. Verificar indicadores: ROE, Margem Líquida, Dívida Bruta, Caixa, EBITDA
5. Calcular Div. Líq./EBITDA manualmente se necessário
```

### Automação no SwingTrade.ipynb

Os 5 passos podem ser automatizados via:
- API do Fundamentus (biblioteca Python `fundamentus`)
- Biblioteca `yfinance` para dados históricos de preço
- Pandas para aplicar os filtros sequencialmente

---

## Output do Screener

Após aplicar os 5 filtros, o conjunto resultante contém empresas que:
- Crescem receita
- São lucrativas e eficientes
- Têm dívida sob controle

Essas são as candidatas para análise qualitativa (Camada 2) e posterior timing técnico de entrada.

---

## Referência

Fonte: Docs 04 (5 passos), 05-09 (métricas individuais). Exercício prático mencionado com empresas Vale, WEG, Engie, GOL, Petrobras.
