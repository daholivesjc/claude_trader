> **MCP Validated:** 2026-03-14

# Crypto Market Structure

## Order Book Mechanics

The order book is a real-time list of buy (bid) and sell (ask) orders at each price level.

```text
ASK (sell orders)
  $50,200  │ 2.5 BTC
  $50,100  │ 5.1 BTC
  $50,050  │ 1.2 BTC  ← Best ask (lowest sell)
────────────────────── spread
  $50,000  │ 3.8 BTC  ← Best bid (highest buy)
  $49,950  │ 8.2 BTC
  $49,800  │ 12.0 BTC
BID (buy orders)
```

**Spread:** Difference between best ask and best bid. Tighter spread = higher liquidity.
- BTC/USDT on Binance: ~$1-5 spread (very liquid)
- BITH11 on B3: variable, typically R$ 0.01-0.05 per cota

## Liquidity Concepts

| Concept | Definition | Trading Implication |
|---------|-----------|---------------------|
| Bid-ask spread | Cost to enter + exit immediately | Narrow spread = cheaper trading |
| Market depth | Volume available at each price level | Deep book = less slippage |
| Slippage | Difference between expected and actual fill | Higher for large orders |
| Market impact | Price movement caused by your order | Relevant for large positions |

## Market Cap and Volume

**Market Cap:** Current price × circulating supply
- Bitcoin dominance (BTC.D) = BTC market cap / total crypto market cap
- Used to assess capital rotation between BTC and altcoins

**Volume:** Total traded value in a period (24h standard in crypto)
- Volume > 1.5x average: breakout confirmation signal
- Volume declining during uptrend: potential reversal warning
- Crypto trades 24/7 (unlike B3 which closes at 17h BRT)

## Volatility in Crypto

Crypto is significantly more volatile than B3 stocks:

| Asset Class | Typical Annual Volatility |
|-------------|--------------------------|
| Ibovespa stocks (blue chip) | 20-40% |
| Bitcoin (BTC) | 60-100% |
| Ethereum (ETH) | 80-120% |
| Altcoins (top 20) | 100-200% |
| Small cap altcoins | 200%+ |

**Practical implication:** Position sizing must be smaller for crypto than for B3 stocks
to maintain equivalent portfolio risk exposure.

## Funding Rates (Perpetual Futures)

Funding rates are periodic payments between long and short traders in perpetual futures.
They keep the futures price anchored to the spot price.

| Rate | Condition | Implication |
|------|-----------|-------------|
| Positive (+) | Market bullish | Longs pay shorts every 8h |
| Negative (-) | Market bearish | Shorts pay longs every 8h |
| Very high (+0.1%/8h) | Overheated longs | Potential cascading long liquidations |
| Very negative (-0.1%/8h) | Overheated shorts | Potential short squeeze |

**Annualized cost:** 0.01%/8h × 3 × 365 = 10.95% annual cost for holding a perpetual long.

## Liquidation Risk

In margin/futures trading, positions are liquidated when margin falls below maintenance level.

```text
Liquidation Price (long) = Entry Price × (1 - 1/Leverage + Maintenance Margin Rate)

Example: 10x long on BTC at $50,000
Liquidation ≈ $50,000 × (1 - 0.1 + 0.005) ≈ $45,250
```

**Cascade liquidations:** When price drops, long positions liquidate, pushing price further down,
triggering more liquidations. This creates sharp, sudden drops ("cascade wicks").

## Market Regimes

| Regime | Characteristics | Strategy |
|--------|----------------|----------|
| Bull trend | Higher highs and higher lows, BTC.D often falling | Buy dips, ride trend |
| Bear trend | Lower highs and lower lows, high correlation drops | Reduce exposure, hedge |
| Sideways (range) | Price bouncing between support/resistance | Buy support, sell resistance |
| High volatility | Wide daily ranges, news-driven | Reduce position size |

## Key Market Dynamics Unique to Crypto

1. **24/7 trading:** No overnight gap risk management via position limits
2. **No circuit breakers:** Price can move 30%+ in hours without halt
3. **Global correlation:** US news affects Asian and Brazilian markets instantly
4. **Exchange risk:** Exchange hacks or insolvency (e.g., FTX 2022) can cause total loss
5. **Macro sensitivity:** Fed rate decisions, USD strength affect BTC significantly
6. **Halving cycles:** 4-year supply cycles create repeating bull/bear patterns

## Order Flow and Market Makers

- Market makers provide liquidity with limit orders (paid lower maker fees)
- Retail traders are typically takers (pay higher taker fees)
- Whale orders (>100 BTC) create visible imbalances in the order book
- Dark pools and OTC desks execute large trades without impacting spot price
