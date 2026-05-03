> **MCP Validated:** 2026-03-14

# Exchanges: Binance vs BTG Pactual

## Overview

| Feature | Binance | BTG Pactual |
|---------|---------|-------------|
| Type | Global CEX | Brazilian regulated bank |
| Regulation | CVM/BCB monitored | CVM / Banco Central fully regulated |
| Products | Spot, Futures, Margin, Options | Spot crypto, crypto fund, B3 ETFs |
| Leverage | Up to 125x (futures) | Not available |
| Currencies | USDT, BTC, ETH, BNB, BRL | BRL only |
| Tax reporting | Manual (user responsibility) | Integrated (issues Informe de Rendimentos) |
| Target user | Active/global traders | Conservative Brazilian investors |

## Binance

The world's largest cryptocurrency exchange by volume (>$217B daily in 2025).

### Market Types

**Spot:** Direct purchase/sale of crypto. No leverage. Settle immediately.
- Fee: 0.10% maker / 0.10% taker (reduced with BNB payment or high volume)
- Hundreds of trading pairs, deep liquidity on BTC/USDT, ETH/USDT

**Futures (USDT-M):** Contracts settled in USDT. Up to 125x leverage on BTC.
- Standard contracts: BTC, ETH, BNB, SOL, etc.
- Funding rate every 8 hours (perpetuals)
- Fee: 0.02% maker / 0.05% taker

**Futures (COIN-M):** Contracts settled in the underlying crypto.
- Good for miners hedging BTC exposure
- Delivery futures (quarterly) and perpetuals

**Margin:** Borrow funds to trade larger positions.
- Isolated margin: collateral limited to that position
- Cross margin: entire account as collateral
- Leverage: 3x to 10x depending on asset

### Binance Order Types

| Order Type | Description | When to Use |
|------------|-------------|-------------|
| Market | Immediate fill at current price | Fast execution needed |
| Limit | Fill at specified price or better | Precise entry, adds liquidity |
| Stop-Limit | Trigger at stop, then place limit | Stop loss with slippage control |
| Stop-Market | Trigger at stop, fill at market | Stop loss, guaranteed exit |
| OCO | One Cancels Other (limit + stop) | Set profit target + stop simultaneously |
| Trailing Stop | Stop moves with price | Locking in profits on trends |

### Binance Risk Considerations

- Not regulated by Brazilian CVM — legal grey area for Brazilian users
- Withdrawals to Brazilian bank can trigger IOF on international transactions
- KYC required for full access (Brazilian CPF accepted)
- Tax reporting is user's responsibility; Binance does not issue Brazilian tax docs

## BTG Pactual

Brazil's largest investment bank offering crypto exposure through regulated channels.

### Products

| Product | Ticker / Name | Description |
|---------|--------------|-------------|
| Bitcoin ETF | BITC11 | BTG's own BTC ETF on B3 |
| Crypto wallet | BTG Crypto | Direct BTC/ETH purchase via app |
| Crypto fund | BTG Digital Assets | Actively managed crypto fund |

### BTG Pactual Crypto Wallet

- Available through BTG Pactual app (requires conta digital)
- Supported assets: BTC, ETH (may expand)
- BRL-denominated pricing
- Automatic tax reporting via Informe de Rendimentos
- Custody: custodian within Brazilian regulatory framework
- Fees: spread-based (typically 0.5-1.5% above market price)

### BITC11 (BTG's Bitcoin ETF)

- Listed on B3
- Tracks CME CF Bitcoin Reference Rate
- Traded like a stock through any Brazilian broker
- Management fee: ~0.75% p.a.
- Tax treatment: renda variavel, same as stocks

### Comparison for Brazilian Swing Traders

| Criteria | Binance | BTG Pactual / B3 ETFs |
|----------|---------|----------------------|
| Price discovery | Real-time, 24/7 | B3 hours (10h-17h) |
| Liquidity | Very high | Medium |
| Spreads | Tight (0.10%) | Wider (ETF spread + mgmt fee) |
| Tax simplicity | Complex | Simple (broker handles) |
| Leverage | Yes (futures/margin) | No |
| Regulation | Partial | Full |
| Best for | Active trading | Long-term, tax-efficient exposure |

## Mercado Bitcoin (Backup Reference)

Brazilian CEX authorized by BCB. Alternative for domestic spot trading.
- BRL pairs: BTC/BRL, ETH/BRL, SOL/BRL
- Lower liquidity than Binance but full Brazilian regulation
- Issues Informe de Rendimentos

## Toro Investimentos

Brazilian fintech broker founded in 2010, acquired by Santander Brasil (completed 2023). Operating under the Santander Corretora brand with Toro identity preserved for retail traders. Fully regulated: BCB, CVM, B3, Anbima. Target of 4 million clients by 2026.

### Crypto Products Available

| Product | Description |
|---------|-------------|
| B3 Crypto ETFs | QBTC11, HASH11 and all B3-listed crypto ETFs |
| Bitcoin Futures (BIT) | Bitcoin futures contracts traded on B3 (min margin ~R$ 45) |
| Direct crypto (expanding) | BTC, ETH, SOL + others via Santander Corretora integration (from Jan 2026) |

### Fees and Withdrawal

- Corretagem: R$ 0 on all B3 assets (equities, ETFs, futures)
- ETF management fee: charged by fund (e.g., HASH11 1.30% p.a.)
- Direct crypto spread: TBD (Santander-integrated pricing)
- Withdrawal: Native PIX/TED, no IOF friction

### Pros and Cons vs Binance and BTG

| Criteria | Toro / Santander Corretora | Binance | BTG Pactual |
|----------|---------------------------|---------|-------------|
| Regulation | Full (CVM + BCB) | Partial | Full |
| Crypto variety | Limited (ETFs + BTC futures + select direct) | 400+ assets | BTC, ETH only |
| Trading fees | R$ 0 corretagem on ETFs | 0.10% spot | Spread 0.5-1.5% |
| Leverage | B3 futures margin only | Up to 125x | None |
| Tax reporting | Automatic (broker + B3 informe) | Manual | Automatic |
| Stock + crypto same account | Yes | No | Partial (ETF only) |
| Best for | Retail investors, multi-asset portfolios | Active/global traders | Conservative investors |

## Exchange Selection Framework

```text
Brazilian swing trader decision:

Need leverage?
  YES → Binance Futures (manage tax manually)
  NO + short-term active trade (<30d)?
    YES → Binance Spot (lower fees, better liquidity)
  NO + multi-asset investor?
    YES → Toro/Santander Corretora (zero corretagem, single account)
    NO  → B3 ETF via any broker (tax simplicity, regulated)
```
