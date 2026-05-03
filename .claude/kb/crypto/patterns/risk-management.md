> **MCP Validated:** 2026-03-14

# Crypto Risk Management

## Core Principle

Risk management in crypto is more critical than in equities due to:
- Higher volatility (BTC: 60-100% annualized vs 20-40% for B3 blue chips)
- 24/7 trading (risks materialize overnight and on weekends)
- Liquidation risk in futures/margin (position wiped out, not just marked down)
- Exchange risk (platform insolvency, hacks)
- Regulatory risk (sudden restrictions on exchanges)

## Position Sizing

### Fixed Risk Per Trade Model

The most reliable method. Risk a fixed percentage of total capital per trade.

```
Position Size = (Account × Risk%) / (Entry - Stop Loss)

Example:
Account: R$ 50,000
Risk per trade: 2% = R$ 1,000
Entry: R$ 280,000 (BTC equivalent in BRL)
Stop: R$ 267,000
Risk per BTC: R$ 13,000
Position: R$ 1,000 / R$ 13,000 = 0.077 BTC
Position value: 0.077 × R$ 280,000 = R$ 21,560 (43% of account, fine)
```

### Risk Tiers by Account Size and Experience

| Tier | Risk/Trade | Max Concurrent | Leverage |
|------|-----------|----------------|---------|
| Conservative | 1% | 3 positions | None (spot only) |
| Moderate | 2% | 5 positions | Max 3x futures |
| Aggressive | 3% | 8 positions | Max 10x futures |

Recommended for Brazilian retail traders: Conservative to Moderate.

## Stop Loss Placement

### For Spot Trading

- Place stop below the most recent structural swing low
- Add 1% buffer below the structural level to avoid false triggers on wicks
- Use daily closes as your reference, not intraday wicks
- Stop loss orders: use Stop-Limit (not Stop-Market) to control slippage

### For Futures/Margin

- Stop must account for funding rate cost over holding period
- Use isolated margin mode to cap maximum loss to the position's collateral
- **Never** use cross-margin for swing trades (total account at risk)

### Crypto Stop Loss Widths

Typical stop sizes by asset (daily chart):

| Asset | Min Stop Width | Reason |
|-------|--------------|--------|
| BTC | 3-5% | Institutional, tighter ranges |
| ETH | 4-7% | Slightly more volatile |
| SOL | 6-10% | Higher beta |
| Altcoins | 8-15% | High volatility |
| B3 ETFs (BITH11) | 3-5% | Tracks BTC with B3 spread |

## Liquidation Risk (Futures and Margin)

### How Liquidation Works

When your margin falls below the maintenance margin level, the exchange
forcibly closes your position at the current market price.

```
Liquidation Price (Long) ≈ Entry × (1 - Initial Margin Rate + Maintenance Margin Rate)

10x BTC Long at $50,000:
Initial Margin Rate = 1/10 = 10%
Maintenance Margin Rate ≈ 0.5%
Liquidation ≈ $50,000 × (1 - 0.10 + 0.005) = $45,250
```

A 9.5% adverse move = full position lost.

### Avoiding Liquidation

1. Use isolated margin (never cross margin for speculative positions)
2. Keep leverage low (2-3x for swing, never >20x for any trade)
3. Set hard stops well before liquidation price
4. Monitor positions at least once daily
5. Have alerts set for -5% from entry

### Cascade Liquidation Risk

When price drops sharply, many stop losses trigger simultaneously, pushing price
further down, which triggers more liquidations. This creates flash crashes.
- BTC has experienced 20-30% intraday drops during cascade events
- These events are more common during: funding rate spikes, major news, low liquidity hours (weekends)

## Portfolio-Level Risk

### Correlation Management

BTC and altcoins are highly correlated. Having 5 long crypto positions
is NOT equivalent to diversification — it is essentially 5x BTC exposure.

| Portfolio State | Risk Level |
|----------------|-----------|
| 1 BTC + 4 altcoins longs | Very concentrated (all move together) |
| BTC long + USDT stablecoin | Hedged |
| BTC long + BTC short (futures) | Delta-neutral hedge |
| BITH11 + stocks (B3) | Partial diversification |

### Max Drawdown Management

- Set maximum portfolio drawdown threshold (e.g., 20%)
- If portfolio drops 20%, pause trading, reassess market regime
- Never add to losing positions (averaging down in crypto can be fatal)

## Exchange Risk

Risk of losing funds due to exchange failure, not market moves.

| Risk Type | Mitigation |
|-----------|-----------|
| Exchange hack | Keep only trading capital on exchange; move profits to cold wallet |
| Exchange insolvency | Diversify across 2+ exchanges; use regulated Brazilian exchanges |
| Withdrawal restrictions | Test withdrawals periodically; keep emergency fiat accessible |
| Regulatory shutdown | Prefer BCB-authorized exchanges for core holdings |

**Brazilian specific:** BTG Pactual and B3 ETFs eliminate exchange risk for the
custody layer. Consider using Binance only for active trades, not long-term storage.

## Tax-Aware Risk Management

Brazilian traders must factor taxes into risk/reward calculations:

```
Net Profit = Gross Gain × (1 - 0.175)   [at 17.5% CGT rate, 2026]

Trade: +R$ 10,000 gross → R$ 8,250 net
Trade: -R$ 5,000 loss → can offset future gains (direct crypto)

Effective R:R must account for taxes:
Gross 2:1 R:R → Net ≈ 1.65:1 after 17.5% tax
```

Always provision for tax payments in DARF before withdrawing trading profits.

## Risk Management Checklist

Before entering any crypto trade:
```
[ ] Stop loss defined and placed at order entry
[ ] Position size calculated (max 2% portfolio risk)
[ ] Leverage checked (prefer spot, max 3x for swing)
[ ] Funding rate acceptable (< 0.05%/8h)
[ ] BTC regime confirmed (bullish or neutral, not bearish)
[ ] Exchange risk acceptable (not > 30% of portfolio on single exchange)
[ ] Tax provision updated
```
