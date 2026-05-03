> **MCP Validated:** 2026-03-14

# Crypto Knowledge Base

Domain reference for cryptocurrency and digital asset trading, focused on swing trading
with coverage of Brazilian market specifics (B3 ETFs, BTG Pactual, Receita Federal).

---

## Navigation

| Section | File | Purpose |
|---------|------|---------|
| Bitcoin fundamentals | `concepts/bitcoin.md` | BTC mechanics, halving, network metrics |
| Digital asset types | `concepts/digital-assets.md` | Altcoins, stablecoins, DeFi tokens |
| Exchanges | `concepts/exchanges.md` | Binance vs BTG Pactual comparison |
| Brazilian market | `concepts/brazilian-market.md` | B3 ETFs, Receita Federal tax rules |
| Market structure | `concepts/market-structure.md` | Order books, liquidity, funding rates |
| Swing trading | `patterns/swing-trading-crypto.md` | Entry/exit patterns for 2-14 day holds |
| Risk management | `patterns/risk-management.md` | Position sizing, stop loss, liquidation |
| Technical analysis | `patterns/technical-analysis.md` | RSI, EMA, Bollinger Bands for crypto |
| DCA strategy | `patterns/dca-strategy.md` | Dollar-cost averaging implementation |
| Asset taxonomy | `specs/asset-taxonomy.yaml` | Machine-readable classification |
| Quick reference | `quick-reference.md` | Cheat sheet for active trading |

---

## Domain Overview

### Key Asset Classes

| Class | Examples | Use Case |
|-------|----------|----------|
| Layer 1 | BTC, ETH, SOL, ADA | Store of value, base infrastructure |
| Stablecoins | USDT, USDC, BUSD | Capital preservation, hedging |
| DeFi tokens | UNI, AAVE, LINK | Protocol governance, yield |
| B3 ETFs | BITH11, QBTC11 | Regulated BTC exposure (Brazil) |

### Exchanges Available to Brazilian Traders

| Exchange | Type | Access | Regulation |
|----------|------|--------|------------|
| Binance | Global CEX | Direct | CVM/BCB monitored |
| BTG Pactual | Brazilian bank | App/platform | CVM regulated |
| B3 | Stock exchange | Broker | CVM regulated |
| Mercado Bitcoin | Brazilian CEX | Direct | BCB authorized |

### Brazilian Regulatory Summary (2026)

- Capital gains tax: **17.5%** flat on profits (from Jan 2026)
- Monthly reporting required when sales > **R$ 35,000**
- Holdings > **R$ 5,000** must be declared in IRPF
- VASPs must be authorized by Banco Central do Brasil (BCB)

---

## Integration with ClaudeTrader

This domain complements the B3 stock screener. The investment analyst agent uses
crypto concepts to compare crypto correlations with B3 equity movements and evaluate
crypto ETF liquidity (BITH11, QBTC11) alongside traditional stocks.

**Entry points for agent use:**
1. Start with `quick-reference.md` for fast lookups
2. Deep dive into `concepts/` for foundational understanding
3. Apply `patterns/` during screening decisions
