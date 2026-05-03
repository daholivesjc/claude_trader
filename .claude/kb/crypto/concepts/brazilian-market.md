> **MCP Validated:** 2026-03-14

# Brazilian Crypto Market

## Regulatory Framework (2026)

### Key Regulators

| Institution | Role |
|-------------|------|
| Banco Central do Brasil (BCB) | VASP authorization, payment systems |
| CVM (Comissao de Valores Mobiliarios) | Securities regulation for crypto ETFs |
| Receita Federal do Brasil (RFB) | Tax collection and reporting |

### Virtual Asset Service Providers (VASPs)

Per BCB Comunicado No. 40.874/2023, crypto exchanges operating in Brazil must
obtain BCB authorization. Fully regulated exchanges (e.g., Mercado Bitcoin) can
operate with full BCB backing. Foreign exchanges (Binance) are monitored but
Brazilian users access them at their own regulatory risk.

## Receita Federal: Tax Rules (2026)

### New Tax Regime (from January 1, 2026)

Medida Provisoria 1.303/2025 unified crypto taxation:
- **Rate: 17.5% flat** on all capital gains from crypto (removed old BRL 35,000 exemption)
- Applies to: spot trades, futures, staking rewards, DeFi yields
- Previous rule (pre-2026): gains below R$ 35,000/month were exempt (spot only)

### Reporting Obligations

| Obligation | Threshold | Frequency |
|------------|-----------|-----------|
| Reportar vendas a RFB | > R$ 35,000/mes | Monthly (GCAP or DARF) |
| Declarar holdings no IRPF | > R$ 5,000 | Annual (IRPF - Bens e Direitos) |
| Pagar DARF | Any taxable gain | Monthly (30th of following month) |

### IRPF Declaration Codes

| Code | Asset Type |
|------|-----------|
| 8180 | Bitcoin (BTC) |
| 8182 | Ethereum (ETH) |
| 8183 | Other cryptocurrencies |
| 8190 | Stablecoins |
| 8191 | NFTs |

### Tax Calculation Example

```
Compra: 0.1 BTC por R$ 30,000
Venda: 0.1 BTC por R$ 50,000
Ganho: R$ 20,000
Imposto (17.5%): R$ 3,500
```

DARF must be paid by the last business day of the month following the sale.

### IOF on Crypto (Pending 2026)

The government is reviewing whether IOF (Imposto sobre Operacoes Financeiras)
should apply to crypto transfers classified as foreign exchange operations.
As of March 2026, this is under consultation. Monitor for updates.

## B3 Crypto ETFs

### Available ETFs

| Ticker | Asset | Gestora | Fee (a.a.) | Min Lot |
|--------|-------|---------|-----------|---------|
| BITH11 | Bitcoin | Hashdex | 1.3% | 1 cota |
| QBTC11 | Bitcoin | QR Asset | 0.75% | 1 cota |
| ETHE11 | Ethereum | Hashdex | 1.3% | 1 cota |
| HASH11 | Crypto index | Hashdex | 1.3% | 1 cota |
| BITC11 | Bitcoin | BTG Pactual | 0.75% | 1 cota |

**BITH11 Stats (reference):**
- Benchmark: Nasdaq Bitcoin Reference Price
- Open volume: >R$ 6.8M
- Average daily liquidity: >R$ 1.4M
- Available since 2021
- 13,000+ shareholders on B3

### ETF Tax Treatment

B3 crypto ETFs are treated as **renda variavel** (same as stocks):
- Swing trade: 20% on gains
- Day trade: 20% on gains (no exemption)
- Loss can be offset against future gains in same category
- Monthly gains > R$ 20,000 in renda variavel require DARF

**Key difference from direct crypto:** ETF losses can offset stock gains in the
same renda variavel bucket. Direct crypto losses cannot offset stock gains.

## Market Volume and Adoption

- Crypto transactions in Brazil: R$ 227 billion in H1 2025 (+20% YoY)
- Brazil ranks among top 10 crypto markets globally by volume
- BCB CARF implementation underway for international information exchange
- PIX integration with some crypto exchanges for BRL on-ramp

## BTG Pactual Role

BTG Pactual is Brazil's largest investment bank and a key crypto access point:
- Co-launched BITH11 with Hashdex (2021)
- Owns BITC11 (Bitcoin ETF)
- Offers direct BTC/ETH via BTG Crypto wallet (app-based)
- Issues proper tax documentation (Informe de Rendimentos)
- Provides institutional custody infrastructure

## Toro Investimentos / Santander Corretora Role

Toro Investimentos (founded 2010, acquired by Santander Brasil 2021-2023) is a key Brazilian retail broker expanding into crypto:
- Fully regulated: BCB, CVM, B3, Anbima
- Offers B3 crypto ETFs (QBTC11, HASH11) with zero brokerage fee
- Offers Bitcoin Futures (BIT) on B3 with ~R$ 45 minimum margin
- Expanding direct crypto (BTC, ETH, SOL +) via Santander Corretora integration (from Jan 2026)
- Combined ~3 million clients, targeting 4 million by 2026
- Single account for stocks, ETFs, renda fixa, FIIs, and crypto
- Issues Informe de Rendimentos for tax compliance
- Toro brand maintained for retail traders; back-office unified under Santander Corretora

## Practical Notes for ClaudeTrader

When screening B3 ETFs alongside stocks:
- Use `.SA` suffix does NOT apply to ETFs — they trade under raw ticker (BITH11, not BITH11.SA)
- ETF data available via `yfinance` using `BITH11.SA` (B3 convention requires .SA for yfinance)
- Compare BTC performance with IBOV correlation for macro context
- BITH11 liquidity is sufficient for swing trading (>R$ 1.4M/day)
