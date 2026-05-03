> **MCP Validated:** 2026-03-14

# Gatilhos de Entrada

Padrões técnicos de curto prazo usados para determinar o momento de compra após a seleção fundamentalista. Estes gatilhos são os utilizados no `SwingTrade.ipynb`.

---

## Contexto de Uso

Os gatilhos de entrada só devem ser aplicados após:
1. A ação ter passado pelo screener fundamentalista (5 critérios)
2. A tendência primária e intermediária ser confirmada como de alta
3. O setup de pullback estar configurado (preço recuando em tendência de alta)

Gatilho = sinal de que o recuo terminou e a tendência vai retomar.

---

## Gatilho 1: Dave Landry Pullback

### Descrição
Padrão de pullback em tendência de alta estabelecida. Desenvolvido por Dave Landry, especializado em swing trading de curto prazo.

### Condições
1. Ação em tendência de alta confirmada (mínimos e máximos crescentes)
2. Pullback de 2 a 5 candles consecutivos de queda (recuo controlado)
3. Candle de reversão: fechamento acima da máxima do candle anterior
4. Volume pode aumentar no dia do sinal

### Sinal de Entrada
Compra no rompimento da máxima do candle de reversão (ou no fechamento desse candle).

### Stop Loss
Abaixo da mínima do pullback (fundo formado durante o recuo).

### Lógica
O pullback em tendência de alta é a oportunidade de entrar com risco definido. O mercado recuou, exauriu os vendedores, e os compradores retomam o controle.

```
Alta → ... → Pullback (2-5 candles vermelhos) → Candle de reversão → ENTRADA
                                                                       Stop = fundo do pullback
```

---

## Gatilho 2: Padrão 1-2-3 de Joe Ross

### Descrição
Padrão de reversão de tendência identificado por Joe Ross. Captura o início de uma nova tendência após a conclusão da reversão.

### Condições para 1-2-3 de Baixa para Alta (entrada comprada)
1. **Ponto 1:** Fundo significativo da tendência de baixa
2. **Ponto 2:** Rally até um topo (reação intermediária)
3. **Ponto 3:** Novo fundo, ACIMA do Ponto 1 (fundo mais alto)
4. **Entrada:** Rompimento acima do Ponto 2 (confirmação)

### Sinal de Entrada
Compra no rompimento do nível do Ponto 2 (topo entre os dois fundos).

### Stop Loss
Abaixo do Ponto 3.

### Lógica (conexão com Pring)
O 1-2-3 é a confirmação da progressão pico-e-vale de Pring: fundo acima do fundo anterior + topo acima do topo anterior = reversão de tendência confirmada.

```
Tendência de baixa:
  Topo 2 ................ ENTRADA (rompimento)
         \      /P3\   /
          \    /    \ /
           \  /
            P1 (fundo)     Stop = abaixo P3
```

---

## Gatilho 3: Inside Candle (Candle Interno)

### Descrição
Padrão de compressão de volatilidade seguido de rompimento direcional.

### Definição
Um Inside Candle é um candle cuja **máxima é menor** que a máxima do candle anterior E cuja **mínima é maior** que a mínima do candle anterior. O candle está completamente "dentro" do candle anterior.

### Condições para Entrada Comprada
1. Tendência de alta estabelecida
2. Formação de Inside Candle (compressão)
3. Rompimento da máxima do Inside Candle no candle seguinte

### Sinal de Entrada
Compra stop na máxima do Inside Candle + 1 tick (ordem OCO).

### Stop Loss
Abaixo da mínima do Inside Candle.

### Lógica
O Inside Candle representa equilíbrio temporário entre compradores e vendedores (compressão). O rompimento da máxima indica que os compradores venceram a batalha e a tendência deve continuar.

```
Candle Mãe: |-------|  (range amplo)
Inside:        |---|    (range menor, dentro do anterior)
Entrada:            →   (rompimento da máxima do inside)
Stop:          ↓        (mínima do inside candle)
```

---

## Comparativo dos Gatilhos

| Gatilho | Quando usar | Agressividade | Frequência |
|---------|-------------|---------------|------------|
| Dave Landry Pullback | Tendência consolidada | Moderada | Alta |
| 1-2-3 Ross | Reversão de tendência | Mais conservador | Média |
| Inside Candle | Consolidação em tendência | Mais agressivo | Alta |

---

## Princípio de Confirmação

Nenhum gatilho deve ser usado isoladamente. Confirme sempre com:
- Direção da tendência primária (Pring)
- Volume no rompimento (ideal: acima da média)
- Posição em relação a suporte/resistência
- Fundamentos da empresa (screener passou?)

---

## Referência

Fonte: `SwingTrade.ipynb` (implementação dos gatilhos); Dave Landry — "Dave Landry on Swing Trading"; Joe Ross — "Trading by the Book"; Pring — "Análise Técnica Explicada" (Cap. 1, progressão pico-e-vale).
