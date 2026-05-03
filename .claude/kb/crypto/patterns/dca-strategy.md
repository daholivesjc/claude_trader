> **MCP Validated:** 2026-03-14

# Dollar-Cost Averaging (DCA) for Crypto

## What is DCA

Dollar-Cost Averaging (DCA) — in Portuguese, Aporte Mensal or Investimento Periodico —
is the practice of investing a fixed amount at regular intervals regardless of price.

This eliminates the need to time the market and reduces the average cost over time
during bear markets. The ClaudeTrader project already documents DCA for B3 stocks;
this pattern applies the same logic to crypto.

## Why DCA Works in Crypto

Crypto's cyclical nature (halving cycles, 4-year bull/bear patterns) makes DCA
particularly effective:

- Buying during bear markets accumulates more units at lower prices
- The long-term uptrend of BTC and ETH rewards consistent buyers
- Eliminates emotional decision-making during volatile periods
- No need to predict tops or bottoms

## DCA Implementation

### Basic DCA

```python
# Pseudo-code: monthly fixed-amount DCA
def dca_monthly(asset, amount_brl, frequency="monthly"):
    """
    asset: "BTC", "ETH", or B3 ETF like "BITH11"
    amount_brl: fixed BRL amount per period
    frequency: monthly, weekly, biweekly
    """
    current_price = get_current_price(asset)
    units_purchased = amount_brl / current_price
    update_position(asset, units_purchased, amount_brl)
    record_purchase(date=today(), asset=asset, brl=amount_brl, units=units_purchased)
```

### Value Averaging (Enhanced DCA)

Value averaging adjusts the purchase amount based on how far below target growth
the portfolio has fallen. If portfolio underperforms, buy more; if it overperforms, buy less.

```
Monthly target: portfolio grows by R$ 500/month
Current value: R$ 9,200 (target was R$ 10,000 after 20 months)
Gap: R$ 800 below target
Purchase this month: R$ 800 (instead of regular R$ 500)
```

Value averaging typically outperforms basic DCA but requires more cash reserves.

## DCA Schedule Options

| Frequency | Suitable For | Pros | Cons |
|-----------|-------------|------|------|
| Daily | Large portfolios (>R$ 100k) | Maximum smoothing | High fee cost |
| Weekly | Active investors | Good smoothing | Moderate fee cost |
| Monthly | Most retail investors | Low fees, simple | Less smoothing |
| On dip (-10%) | Technical DCA | Buys at better prices | Timing risk |

**Brazil note:** For B3 ETFs (BITH11, QBTC11), monthly purchases on first trading
day align with typical salary payment cycles and simplify tax tracking.

## DCA for Crypto: Asset Allocation

Recommended DCA allocation for Brazilian retail investor (moderate risk):

| Asset | Allocation | Rationale |
|-------|-----------|-----------|
| BTC (via BITH11 or direct) | 60% | Store of value, lowest risk in crypto |
| ETH (via ETHE11 or direct) | 30% | Smart contract platform, strong fundamentals |
| Diversified crypto index | 10% | HASH11 or basket exposure |

**Conservative version:** 100% BTC (BITH11/QBTC11) via B3 ETFs — fully regulated,
no foreign exchange required, tax treatment mirrors stocks.

## DCA Tax Implications (Brazil)

### Cost Basis Tracking (FIFO)

Receita Federal requires FIFO (First In, First Out) method for crypto disposals.

```
Purchases:
  Jan 2025: 0.05 BTC at R$ 250,000 (cost: R$ 12,500)
  Feb 2025: 0.05 BTC at R$ 280,000 (cost: R$ 14,000)

Sale: 0.05 BTC at R$ 320,000 (proceeds: R$ 16,000)
Cost basis (FIFO): R$ 12,500 (Jan purchase)
Gain: R$ 3,500
Tax (17.5%): R$ 612.50 → pay via DARF
```

### B3 ETF Simplification

When using BITH11/QBTC11 via a Brazilian broker:
- Broker automatically tracks average cost basis
- Informe de Rendimentos provided annually
- No FIFO calculation needed (broker handles it)
- Tax declaration follows standard renda variavel rules

## DCA vs Swing Trading: When to Use Each

| Scenario | DCA | Swing Trade |
|----------|-----|-------------|
| Long-term wealth building | Yes | No |
| Market timing uncertainty | Yes | No |
| Bear market accumulation | Yes | Partial |
| Bull market momentum | No | Yes |
| Capital < R$ 10,000 | Yes (fees matter) | Only large positions |
| Time available < 1h/week | Yes | No |

## Combining DCA with ClaudeTrader

The ClaudeTrader screener can enhance DCA by:
1. Pausing DCA buys when RSI > 70 on weekly chart (overbought)
2. Doubling DCA amount when trigger conditions met (tactical top-up)
3. Using DCA as baseline; adding swing trades on confirmed setups

```text
Portfolio structure example:
  Base layer (60%): DCA into BITH11 monthly — never sold
  Active layer (40%): Swing trades on Binance BTC/ETH with ClaudeTrader signals
```

## Practical DCA Tools for Brazilian Investors

| Platform | Method | Automation |
|----------|--------|-----------|
| BTG Pactual | Schedule recurring BTC purchase in app | Yes |
| Mercado Bitcoin | Recurring buy orders | Yes |
| B3 ETFs via broker | Monthly order via home broker | Manual |
| Binance | Recurring buy feature (auto-invest) | Yes |

**Recommendation:** Automate DCA through BTG Pactual or Mercado Bitcoin for
the regulated layer. Keep Binance active layer for discretionary swing trades.

## DCA Performance Tracking

Track these metrics monthly:
- Average cost basis (BRL per BTC or ETH)
- Total units accumulated
- Current portfolio value in BRL
- Unrealized gain/loss
- Tax provision (17.5% of all gains)

Review quarterly: if average cost basis > current price for 6+ months, reassess thesis.
