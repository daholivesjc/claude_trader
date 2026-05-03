> **MCP Validated:** 2026-03-14

# Crypto Swing Trading Patterns

## Overview

Swing trading in crypto targets moves of 2-14 days, capturing 10-30%+ moves in trending assets.
Unlike B3 stocks (which follow business hours), crypto trades 24/7, requiring defined
monitoring windows and automated alerts rather than constant screen watching.

## Core Swing Trading Framework

### Setup Requirements (All Must Be True)

```text
1. TREND FILTER        EMA50 > EMA200 (daily chart) = bullish regime
2. MOMENTUM            RSI 14 between 35-60 (room to run)
3. PULLBACK            Price retesting EMA21 or key support
4. TRIGGER             Candlestick reversal pattern on trigger candle
5. VOLUME              Volume declining on pullback (healthy correction)
```

### The Three Trigger Patterns

These match the ClaudeTrader triggers already used for B3 stocks:

**Dave Landry (3 consecutive lower lows):**
```
low[0] < low[1] < low[2]   ← 3 days of lower lows
Entry: Break above high[0] on 4th candle
Stop: Below low[0]
```

**1-2-3 Bounce (low bounce):**
```
low[0] > low[1] < low[2]   ← Swing low formed
Entry: Break above high[0]
Stop: Below low[1]
```

**Inside Candle (consolidation before move):**
```
low[0] > low[1] AND high[0] < high[1]   ← Inside bar
Entry: Break above high[1] (outside bar high)
Stop: Below low[1]
```

## Timeframe Selection

| Timeframe | Hold Period | Best For |
|-----------|-------------|---------|
| 4H chart triggers | 2-5 days | Active traders |
| Daily chart triggers | 5-14 days | Standard swing |
| Weekly chart triggers | 2-6 weeks | Position trading |

For ClaudeTrader screener: use **daily chart** consistent with B3 stock approach.

## Asset Selection for Swing Trading

Rank crypto assets by suitability for swing trading:

| Tier | Assets | Reasoning |
|------|--------|-----------|
| 1 (Best) | BTC, ETH | Highest liquidity, predictable TA |
| 2 (Good) | SOL, BNB, ADA, AVAX | Deep liquidity, established |
| 3 (Risky) | DeFi tokens (UNI, AAVE) | Higher volatility, news-driven |
| Avoid | Meme coins, low-cap altcoins | Manipulation, low liquidity |

**Brazil-specific:** BITH11, QBTC11 can be swing traded on B3 during market hours
using the same ClaudeTrader trigger logic applied to stocks.

## Entry and Exit Strategy

### Entry

- Enter on confirmed trigger (daily close or next day open)
- Use limit order near key support or EMA for better fill
- Never chase: if price runs 5%+ before entry, skip the setup

### Profit Target

| Method | Calculation | Best For |
|--------|------------|---------|
| Fixed R:R | Target = Entry + 2x (Entry - Stop) | Consistent approach |
| Resistance level | Previous high or ATH | Structural exits |
| Trailing stop | Trail stop below each new higher low | Trend continuation |
| Partial exits | Take 50% at 1:1 R:R, trail remainder | Reduces risk, keeps upside |

### Stop Loss

- Place below the swing low that defines the setup
- Buffer: stop 0.5-1% below the structural low (accounts for wicks)
- Hard rule: never move stop in the wrong direction

## Crypto-Specific Swing Adjustments

Versus B3 stocks, crypto swing trading requires:

1. **Wider stops:** Crypto wicks 3-5% routinely. Use daily close for stop logic, not intraday wick.
2. **Smaller positions:** Same portfolio risk but larger percentage stop = smaller position size.
3. **Weekend awareness:** Crypto trades weekends. Avoid entering Friday afternoon (reduced liquidity).
4. **Funding rate check:** For futures positions, calculate holding cost of daily funding.
5. **News sensitivity:** Central bank meetings, SEC decisions, exchange hacks cause sudden gaps.

## Screening Logic (Adapting ClaudeTrader)

To screen crypto for swing setups, apply the same pipeline:

```python
# Pseudo-code extending ClaudeTrader logic
assets = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"]
# OR for B3 ETFs: ["BITH11.SA", "QBTC11.SA", "ETHE11.SA"]

for asset in assets:
    ohlcv = fetch_12m_daily(asset)
    rsi = compute_rsi_wilder(ohlcv, period=14)
    ema8 = ema(ohlcv, 8)
    ema50 = ema(ohlcv, 50)
    ema200 = ema(ohlcv, 200)
    trend = "Alta" if ema8 > ema50 > ema200 else "Baixa"
    trigger = detect_trigger(ohlcv)  # Same Dave Landry / 1-2-3 / Inside logic

    if trend == "Alta" and trigger and rsi < 65:
        screener_output.append(asset)
```

## Common Mistakes to Avoid

| Mistake | Consequence | Fix |
|---------|------------|-----|
| Buying during funding rate spike | Paying daily fees eats into profit | Check funding before entry |
| Ignoring BTC.D trend | Altcoin longs fail in BTC dominance rise | Filter by BTC regime |
| Overleveraging | Single 10% move causes liquidation | Max 3x for swing, 1x preferred |
| Trading meme coins with swing logic | No technical integrity | Stick to Tier 1 and 2 assets |
| Not accounting for weekend gaps | Stop triggered at worse price | Use stop-limit not stop-market |
