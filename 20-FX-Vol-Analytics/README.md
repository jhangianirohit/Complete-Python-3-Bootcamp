# FX Volatility Trading Analytics Prototype

## P&L Delta-Hedging Mockup (Call, 1-Day Tenor)
Using the required long-option perspective and r = 0, the example below follows a 100 million USD notional EURUSD call with strike 1.1000, initial spot 1.1000, implied volatility 10% (annualised), tenor 24 hours, and hedging every six hours. Spot path (in USD per EUR): 1.1000 → 1.1050 → 1.0950 → 1.1020 → 1.1070.

| Time (h) | Spot | Tau (yrs) | Sigma eff. | Delta | Spot Δ | Hedge P&L (USD) | Cum. Hedge P&L (USD) | Option MTM (USD) | Running P&L (USD) |
|---------:|------|-----------|------------|-------|--------|-----------------|----------------------|------------------|-------------------|
| 0        | 1.1000 | 0.002740 | 0.1000 | 0.5010 | – | – | – | 229,697.26 | -229,697.26 |
| 6        | 1.1050 | 0.002055 | 0.0857 | 0.8420 | +0.0050 | -250,522.04 | -250,522.04 | 409,694.28 | -70,525.02 |
| 12       | 1.0950 | 0.001370 | 0.0700 | 0.1095 | -0.0100 | +842,008.15 | +591,486.11 | 78,515.23 | +440,304.08 |
| 18       | 1.1020 | 0.000685 | 0.0495 | 0.7566 | +0.0070 | -76,666.83 | +514,819.28 | 267,153.96 | +552,275.98 |
| 24       | 1.1070 | 0        | – | 1.0000 | +0.0050 | -378,299.47 | +136,519.81 | 700,000.00 | **+606,822.54** |

- **Premium paid at t=0:** 0.00229697 × 100m = 229,697.26 USD
- **Hedge gains/losses:** Sum of step P&Ls (–250,522.04 + 842,008.15 – 76,666.83 – 378,299.47) = +136,519.81 USD
- **Intrinsic value at expiry:** max(1.1070 – 1.1000, 0) × 100m = 700,000.00 USD
- **Total P&L:** -Premium + Hedge P&L + Intrinsic = -229,697.26 + 136,519.81 + 700,000.00 = **+606,822.54 USD**
- **P&L(t) illustration:** `P&L(t) = -Premium_paid + Cumulative_hedge_P&L(t) + Option_MTM(t)`

The numbers above were validated with a short Python calculation (see development notes in `chunk c3d558†L1-L26`).

### Realised Volatility Example
With four six-hour log returns from the same path, variance = 4.1078e-05 and the annualised realised vol is:

```
σ_realised = sqrt(var × 365 × 24 / 24) = 12.24%
```

(See calculation output `chunk 85b7b1†L1-L10`).

### Notional Standardisation Logic
- Quote currency is USD (e.g. EURUSD, GBPUSD): **use 100 million USD notional**; P&L reported in USD.
- Base currency is USD (e.g. USDJPY, USDCHF): **use 100 million units of the quote currency** (JPY, CHF, etc.). P&L is produced in that quote currency and displayed as unitless for cross-comparison.
- Cross pairs without USD (e.g. AUDCHF, EURJPY): **use 100 million units of the quote currency**. Calculations occur in that currency, results shown as unitless multiples of the 100m-equivalent notionals.

These rules align every trade near a 100 million USD exposure so that P&L figures remain comparable across currency pairs.

---

The remainder of this README explains how to run the in-browser prototype once built.

## Running the Prototype
1. Open `index.html` in any modern browser (Chrome, Edge, Firefox, Safari). No server is required—the app runs entirely in the browser.
2. Upload the spot time-series workbook:
   - First sheet only is processed.
   - Include a column named `timestamp` (Excel datetime or ISO string) and one column per currency pair (e.g. `EURUSD`, `USDJPY`).
   - Provide at least the time range that covers the tenors you wish to analyse.
3. Upload the implied volatility workbook:
   - First sheet only is processed.
   - Required columns (case-insensitive): `pair`, `option_type` (`Call`/`Put`), `tenor_hours` (or `tenor_days`), `strike_label`, `implied_vol` (decimal, 0.10 = 10%).
   - Optional: `strike` (explicit strike) or `delta_target` (to back out the strike).
   - Any additional commentary columns are ignored.
4. Choose the currency pairs and strike buckets to analyse (leave empty to take all), select hedging frequency (10, 30, or 60 minutes), and pick the variance decay model.
5. Click **Run P&L Simulation** to generate the dashboard. Click any P&L cell to view its path-decomposition chart.
6. Download the Excel report for the full hedge-by-hedge breakdown and summary table.

### Variance Decay Options
- **Standard √t decay:** σ(t) = σ₀ × √(t_remaining / t_total).
- **Flat:** Keeps σ constant throughout the life of the trade.
- **Event-weighted window:** Allocate a chosen share of total variance to a specific hour-window (e.g. central-bank announcement). The remaining variance is distributed proportionally outside the window; the engine recomputes σ(t) from the residual variance budget.

### Output Overview
- **P&L heatmap:** Currency vs strike/tenor grid colour-coded by total P&L (per 100m notional).
- **P&L rankings:** Top and bottom five trades.
- **Volatility comparison:** Implied vs realised σ, with flags where P&L contradicts the vol differential (e.g. realised > implied but trade loses money).
- **Interactive chart:** Premium, hedge P&L, option MTM, and total P&L lines over time.
- **Excel export:** `Summary` (per-trade metrics) and `HedgePaths` (hedge-by-hedge records with timestamps, deltas, MTM, and cumulative P&L).

### Notes and Assumptions
- Risk-free and foreign rates are fixed at zero, matching the short-dated setup.
- Hedging is discrete at the chosen frequency and ignores transaction costs.
- Spot prices are assumed to be clean post any Monday-market filtering; pre-processing should remove stale values.
- If spot data ends before a tenor expires, that trade is flagged and excluded.
- All P&L values are shown both in the underlying currency (per the notional convention) and implicitly as a unitless number by dividing by 100 million.

### Future Enhancements
- Incorporate transaction costs and slippage controls.
- Allow custom strikes in delta or absolute terms directly inside the UI.
- Persist historical runs for longitudinal analysis.
- Add gamma-weighted realised volatility metrics.
- Connect to upstream APIs (Bloomberg, internal data lakes) once permissions are available.
