> **MCP Validated:** 2026-03-14

# Technical Analysis for Crypto

## Overview

Technical analysis in crypto uses the same indicators as equities but requires
adjustments for 24/7 trading, higher volatility, and the absence of fundamentalist
filters (for pure crypto — B3 ETFs are an exception).

## RSI (Relative Strength Index)

**Period:** 14 (standard) | **Smoothing:** Wilder (same as ClaudeTrader's equity RSI)

```
RSI = 100 - (100 / (1 + RS))
RS = Average Gain / Average Loss (Wilder smoothing)
```

### Crypto RSI Thresholds

| RSI Zone | Signal | Action |
|----------|--------|--------|
| < 25 | Extremely oversold | Strong long consideration |
| 25-35 | Oversold | Prepare for entry, wait trigger |
| 35-50 | Bearish momentum | Avoid longs |
| 50-65 | Bullish momentum | Trend continuation |
| 65-75 | Approaching overbought | Reduce new longs, watch exits |
| > 75 | Overbought | Take profit, avoid new longs |

**Crypto adjustment:** Standard equity thresholds (30/70) still apply but crypto
can remain oversold/overbought longer. Use RSI divergence for stronger signals:
- **Bullish divergence:** Price makes lower low, RSI makes higher low → reversal
- **Bearish divergence:** Price makes higher high, RSI makes lower high → reversal

### RSI Implementation (Wilder — matches ClaudeTrader)

```python
def compute_rsi_wilder(closes: pd.Series, period: int = 14) -> pd.Series:
    delta = closes.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Initial average using simple mean
    avg_gain = gain.iloc[:period].mean()
    avg_loss = loss.iloc[:period].mean()

    gains, losses = [avg_gain], [avg_loss]
    for i in range(period, len(delta)):
        avg_gain = (avg_gain * (period - 1) + gain.iloc[i]) / period
        avg_loss = (avg_loss * (period - 1) + loss.iloc[i]) / period
        gains.append(avg_gain)
        losses.append(avg_loss)

    rs = pd.Series(gains) / pd.Series(losses)
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

## Exponential Moving Averages (EMA)

### Key EMAs for Crypto

| EMA | Role | Timeframe |
|-----|------|-----------|
| EMA 8 | Fast trend direction | Daily |
| EMA 21 | Swing trader's trend line | Daily |
| EMA 50 | Medium-term trend | Daily |
| EMA 200 | Bull/bear regime filter | Daily |

### Trend Classification (mirrors ClaudeTrader logic)

```python
def classify_trend(ema8, ema50, sma200):
    if ema8 > ema50 and ema50 > sma200:
        return "Alta"
    elif ema8 < ema50 and ema50 < sma200:
        return "Baixa"
    elif abs(ema8 - ema50) / sma200 < 0.02:
        return "Neutro/Lateral"
    else:
        return "Nenhuma"
```

### Golden and Death Cross

- **Golden Cross:** EMA50 crosses above EMA200 → macro bullish signal
  - Historically precedes multi-month BTC rallies
  - Backtested avg BTC return +50% over following 6 months
- **Death Cross:** EMA50 crosses below EMA200 → macro bearish signal
  - High false positive rate — use only as regime filter, not primary signal

## Bollinger Bands

**Parameters:** 20-period SMA, ±2 standard deviations

### Interpretation

| Scenario | Signal | Action |
|----------|--------|--------|
| Price at lower band + RSI < 35 | Oversold, mean-reversion | Long entry |
| Price at upper band + RSI > 65 | Overbought | Take profit or avoid entry |
| Band squeeze (width < 5%) | Low volatility → breakout pending | Await directional confirmation |
| Band expansion | Trending market | Trade with trend |

### Bollinger Band Width Formula

```
BB Width = (Upper Band - Lower Band) / Middle Band × 100

< 5%: Squeeze (breakout pending)
5-15%: Normal range
> 20%: High volatility, trending
```

**Mean-reversion strategy:** Backtests show ~4% average monthly return for BTC
when entering at lower band with confirming RSI < 30. Stop below recent swing low.

## Support and Resistance

### Identifying Key Levels

1. **Previous highs/lows:** Most reliable S/R in crypto (same as equities)
2. **Round numbers:** $50,000, $100,000, $200,000 for BTC act as psychological S/R
3. **Previous ATH:** Strongest resistance until broken; then becomes support
4. **EMA levels:** Dynamic S/R that moves with price
5. **Volume profile (VPVR):** High-volume nodes act as S/R

### S/R in Practice

```
Entry near support: Place limit buy 0.5-1% above support
Stop: 1-2% below support (accounts for wick)
Target: Next resistance level
```

## Candlestick Patterns

### Most Reliable for Crypto (Daily Chart)

| Pattern | Signal | Reliability |
|---------|--------|-------------|
| Hammer at support | Bullish reversal | High |
| Shooting star at resistance | Bearish reversal | High |
| Engulfing bullish | Reversal | High if on key level |
| Doji | Indecision, possible reversal | Medium (needs confirmation) |
| Morning star (3 candles) | Strong reversal | High |
| Inside candle (NR7) | Consolidation → breakout | High (ClaudeTrader trigger) |

**Dave Landry (3 lower lows) and 1-2-3:** Covered in `patterns/swing-trading-crypto.md`.
These same patterns work in crypto daily charts.

## Multi-Indicator Confirmation

The strongest entries combine multiple signals:

```text
TIER 1 SETUP (all 4 present):
  [x] EMA50 > EMA200 (bullish regime)
  [x] RSI 35-50 (oversold recovery zone)
  [x] Price at EMA21 or key support
  [x] Trigger candle (Dave Landry / 1-2-3 / Inside)

TIER 2 SETUP (3 of 4 present):
  [x] Bullish regime
  [x] RSI in range
  [ ] Not at exact support (close to EMA21)
  [x] Trigger present

SKIP (missing regime or trigger):
  [ ] Bearish regime (EMA50 < EMA200)
  [ ] No trigger candle
```

## Volume Analysis

Crypto volume should be analyzed alongside price:

| Volume Pattern | Price Pattern | Interpretation |
|---------------|---------------|----------------|
| Declining | Declining (pullback) | Healthy correction, buy the dip |
| Rising | Rising (breakout) | Strong confirmation |
| Rising | Declining | Distribution, potential top |
| Declining | Rising | Weak rally, likely to fail |

**Data source note:** For Binance assets, use exchange volume. For BITH11/B3 ETFs,
use B3 financial volume (note: lower volume than spot, but more regulated).

## Indicator Parameters Summary

| Indicator | Parameter | Crypto Adjustment vs Equities |
|-----------|-----------|-------------------------------|
| RSI | 14 periods, Wilder | Same period, wider thresholds |
| EMA fast | 8 | Same |
| EMA swing | 21 | Use instead of 20 SMA |
| EMA trend | 50 | Same |
| SMA macro | 200 | Same |
| Bollinger | 20 SMA, 2 SD | Same parameters |
| Volume MA | 20 periods | Same |
