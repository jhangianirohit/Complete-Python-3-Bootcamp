# FX Volatility Trading Analytics System

## Overview

A web-based analytics tool for calculating P&L from **buying** FX options and delta-hedging them. This tool helps you determine which options are actually profitable to buy, accounting for where volatility occurs relative to the strike (gamma effect), path dependency, and actual hedging cashflows.

## Key Features

✅ **P&L-Focused Analysis** - Primary metric for trading decisions
✅ **Zero Interest Rate** - Simplified for short-dated options (r=0)
✅ **Standardized Notionals** - 100 million USD equivalent across all pairs
✅ **Black-Scholes Pricing** - With proper delta calculations
✅ **Delta-Hedging Simulation** - Configurable frequency (10min to 6h)
✅ **Interactive Charts** - Click any P&L cell to see evolution
✅ **Excel Export** - Detailed results and P&L paths
✅ **Multi-Currency Support** - Handles USD pairs and crosses

---

## Getting Started

### 1. Open the Tool

Simply open `fx_volatility_analytics.html` in any modern web browser:

```bash
# Option 1: Double-click the HTML file
# Option 2: Open from command line
open fx_volatility_analytics.html  # macOS
xdg-open fx_volatility_analytics.html  # Linux
start fx_volatility_analytics.html  # Windows
```

### 2. Prepare Your Data Files

You need **two Excel files**:

#### File 1: Spot Price Data (`sample_spot_prices.xlsx` format)

| Timestamp | EURUSD | USDJPY | GBPUSD | ... |
|-----------|--------|--------|--------|-----|
| 2025-10-20 00:00:00 | 1.1000 | 150.00 | 1.2700 | ... |
| 2025-10-20 00:10:00 | 1.1005 | 150.15 | 1.2705 | ... |
| ... | ... | ... | ... | ... |

**Requirements:**
- First column: `Timestamp` (datetime format)
- Subsequent columns: Currency pair names (e.g., EURUSD, USDJPY)
- Frequency: 10-minute intervals recommended
- Duration: 1 hour to 1 week of data
- Clean data: No missing values, Bloomberg Monday data cleaned

#### File 2: Implied Volatility Data (`sample_implied_vols.xlsx` format)

| Pair | Strike | Tenor | ImpliedVol |
|------|--------|-------|------------|
| EURUSD | ATM | 1D | 11.30 |
| EURUSD | 25DP | 1D | 12.15 |
| EURUSD | 25DC | 1D | 11.91 |
| ... | ... | ... | ... |

**Requirements:**
- `Pair`: Currency pair name (must match spot data columns)
- `Strike`: Strike type (ATM, 25DP, 25DC, 10DP, 10DC)
- `Tenor`: Time to expiry (1D, 1W, 2W, 1M)
- `ImpliedVol`: Volatility in percentage (e.g., 11.30 for 11.30%)

### 3. Upload and Configure

1. **Upload Files:**
   - Click "Upload Spot Price Data" and select your spot file
   - Click "Upload Implied Volatility Data" and select your vol file
   - Both boxes will turn green when files are loaded ✓

2. **Configure Settings:**
   - **Hedge Frequency**: 10 min, 30 min, 1 hour, or 6 hours
   - **Option Type**: Call, Put, or Both
   - **Strikes**: Select which strikes to analyze (ATM, 25-delta, 10-delta)
   - **Tenors**: Select which tenors to analyze (1D, 1W, etc.)

3. **Run Analysis:**
   - Click "Calculate P&L Analysis"
   - Wait for calculations to complete
   - View results in interactive dashboard

---

## Understanding the Results

### Tab 1: P&L Analysis (PRIMARY)

This is your main view showing actual trading profitability.

**Summary Cards:**
- **Total P&L**: Aggregate P&L across all analyzed trades
- **Average P&L per Trade**: Mean performance
- **Profitable Trades**: Win rate (X out of Y trades)
- **Avg Realized Vol**: Average volatility actually experienced

**P&L Table:**
Shows each trade with breakdown:
- **Premium Paid**: Initial cost of buying the option
- **Hedge P&L**: Cumulative profit/loss from delta hedging
- **Intrinsic Value**: Final payoff at expiry
- **Total P&L**: = -Premium + Hedge P&L + Intrinsic Value

**Interactive Feature:** Click any row to see P&L evolution over time!

### Tab 2: Volatility Comparison (SECONDARY)

Shows realized vs implied volatility scatter plot.

**Key Insight:**
- Points above the diagonal: Realized > Implied (volatility higher than expected)
- Green points: Profitable trades
- Red points: Losing trades

**Important:** High realized vol doesn't guarantee profit! If spot moves away from strike (low gamma region), you can have high vol but negative P&L.

### Tab 3: P&L Rankings

Shows:
- **Top 5 Profitable Trades**: Best performers
- **Bottom 5 Trades**: Worst performers

Use this to identify:
- Which currency pairs are most profitable
- Which strikes/tenors work best
- Divergences where realized > implied but P&L is negative

---

## Key Calculations Explained

### P&L at Any Time t (Before Expiry)

```
P&L(t) = -Premium_paid + Cumulative_hedge_PL(t) + Option_MTM(t)

where:
  Option_MTM(t) = Current Black-Scholes value at time t
```

### P&L at Expiry

```
P&L(T) = -Premium_paid + Cumulative_hedge_PL(T) + Intrinsic_value

where:
  Intrinsic_value = max(S_T - K, 0) for calls
  Intrinsic_value = max(K - S_T, 0) for puts
```

### Delta-Hedging P&L

At each rehedge point:
```
Hedge_PL = -Delta_position × (Spot_new - Spot_old)

where:
  Delta_position = N(d1) × Base_notional (for calls)
  Delta_position = [N(d1) - 1] × Base_notional (for puts)
```

### Realized Volatility

```
1. Calculate log returns: r_i = ln(S_i / S_{i-1})
2. Calculate variance: var = Σ(r_i²) / n
3. Annualize: realized_vol = √(var × periods_per_year)

where:
  periods_per_year = (365 × 24 × 60) / frequency_minutes
```

### Notional Handling

All trades normalized to **100 million USD equivalent**:

- **EURUSD** (quote = USD): 100 mio USD notional → ~90.91 mio EUR at spot 1.1000
- **USDJPY** (base = USD): 100 mio USD notional → 15 billion JPY at spot 150.00
- **AUDCHF** (cross): 100 mio CHF notional → ~143 mio AUD at spot 0.7000

P&L presented as unitless for cross-pair comparison.

---

## Configuration Options Explained

### Hedge Frequency

Controls how often you rebalance your delta hedge:

- **10 minutes**: Most frequent, captures gamma better, more transaction costs
- **30 minutes**: Balanced approach
- **1 hour**: Less frequent, lower transaction costs
- **6 hours**: Infrequent, mainly for testing concepts

**Recommendation:** Start with 10 minutes for short-dated options (1D), 30 minutes for longer (1W).

### Option Type

- **Call**: Profit from upward moves
- **Put**: Profit from downward moves
- **Both**: Analyze calls and puts simultaneously

### Strikes

- **ATM (At-The-Money)**: Strike = Current spot
- **25DP (25-Delta Put)**: Strike below spot, delta ≈ -0.25
- **25DC (25-Delta Call)**: Strike above spot, delta ≈ 0.25
- **10DP/10DC**: Further out-of-the-money

**Trading Insight:** ATM options have highest gamma (sensitivity to spot changes). OTM options are cheaper but need larger moves to profit.

---

## Interpreting Results: Key Scenarios

### Scenario 1: High Realized Vol, Positive P&L ✅
```
Realized Vol > Implied Vol AND Total P&L > 0
```
**Meaning:** Volatility was higher than expected AND spot oscillated near the strike (high gamma region). This is the ideal outcome for option buying.

**Example:** Bought ATM call at 1.1000, spot oscillated between 1.0980-1.1020, generating hedge profits.

### Scenario 2: High Realized Vol, Negative P&L ⚠️
```
Realized Vol > Implied Vol BUT Total P&L < 0
```
**Meaning:** Volatility was high, but spot moved away from strike (low gamma). Hedging costs exceeded option value.

**Example:** Bought ATM call at 1.1000, spot quickly moved to 1.0900 and stayed there. High volatility far from strike = poor gamma = loss.

### Scenario 3: Low Realized Vol, Positive P&L 💡
```
Realized Vol < Implied Vol BUT Total P&L > 0
```
**Meaning:** Volatility was lower than expected, but the option ended deep in-the-money (ITM).

**Example:** Bought ATM call at 1.1000, implied 10%, spot drifted to 1.1100 with low vol. Intrinsic value exceeded premium paid.

### Scenario 4: Low Realized Vol, Negative P&L ❌
```
Realized Vol < Implied Vol AND Total P&L < 0
```
**Meaning:** Volatility was low and spot didn't move enough. Paid too much premium for little movement.

**Example:** Bought ATM call at 1.1000, spot stayed around 1.1005. Premium lost due to time decay.

---

## Best Practices

### Data Quality

1. **Clean Monday Data**: Bloomberg FX data is unreliable until 5 PM NY on Monday. Filter or adjust Monday morning data.

2. **Weekend Scaling**: Friday implied vols cover 3 days (Fri-Mon) but spot market is closed. Consider scaling vols appropriately.

3. **Check for Gaps**: Ensure no missing timestamps in spot data. Fill gaps with forward-fill or interpolation.

### Analysis Workflow

1. **Start Small**: Test with 1-2 currency pairs and 24 hours of data first
2. **Validate**: Compare results against known market behavior
3. **Iterate**: Adjust hedge frequency and strikes based on results
4. **Export**: Save detailed results to Excel for further analysis

### Trading Insights

1. **P&L is King**: Don't just compare realized vs implied vol. P&L tells the full story.

2. **Gamma Matters**: Options with high gamma (near ATM, short-dated) are most sensitive to spot oscillations.

3. **Path Dependency**: Two trades can have same realized vol but different P&L based on timing of moves.

4. **Strike Selection**: ATM strikes have highest gamma but cost more premium. OTM strikes are cheaper but need larger moves.

---

## Excel Export Features

Click "Export Results to Excel" to download a comprehensive workbook:

**Sheet 1: P&L Summary**
- All trades with complete P&L breakdown
- Implied vs Realized vol comparison
- Sortable and filterable

**Sheets 2-11: P&L Paths**
- Detailed evolution of top 10 trades
- Period-by-period spot, delta, option MTM, hedge P&L
- Use for deep-dive analysis

---

## Troubleshooting

### "Calculate" Button Not Enabled

- ✓ Make sure both Excel files are uploaded (green checkmarks)
- ✓ Check file formats match specifications
- ✓ Verify column names are exactly as specified

### Unexpected Results

- ✓ Check spot data frequency matches selected hedge frequency
- ✓ Verify implied vols are in percentage (not decimal)
- ✓ Ensure currency pair names match exactly between files
- ✓ Validate data has no NaN or missing values

### Browser Compatibility

Works best in:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Requires JavaScript enabled and internet connection (for CDN libraries).

---

## Sample Data

Two sample files are included for testing:

1. **sample_spot_prices.xlsx**
   - 6 currency pairs (EURUSD, USDJPY, GBPUSD, AUDUSD, USDCAD, USDCHF)
   - 24 hours of data (144 rows)
   - 10-minute frequency
   - Realistic price movements

2. **sample_implied_vols.xlsx**
   - All 6 pairs
   - 5 strike types (ATM, 25DP, 25DC, 10DP, 10DC)
   - 2 tenors (1D, 1W)
   - 60 total vol entries
   - Realistic vol levels with smile/skew

**To Test:** Upload these files and run analysis with default settings.

---

## Technical Details

### Black-Scholes Implementation

Using simplified Black-Scholes with:
- **r = 0** (zero interest rate for short-dated options)
- **q = 0** (no dividend yield for currencies)

Call option:
```
d1 = [ln(S/K) + 0.5σ²T] / (σ√T)
d2 = d1 - σ√T
Price = S × N(d1) - K × N(d2)
Delta = N(d1)
```

Put option:
```
Price = K × N(-d2) - S × N(-d1)
Delta = N(d1) - 1
```

### Performance

- Handles up to 30 currency pairs simultaneously
- Processes 1 week of 10-minute data (~1,000 points) in seconds
- Browser-based calculation (no server required)
- Results cached for instant re-export

---

## Future Enhancements (Not Yet Implemented)

- Transaction costs modeling
- Custom strike input in delta and price space
- Gamma-weighted realized volatility
- Historical data storage and backtesting
- API connections to Bloomberg/database
- Multi-period P&L attribution
- Risk metrics (VaR, Greeks tracking)

---

## Support & Feedback

**File Format Issues:**
- Check that column names match exactly (case-sensitive)
- Verify Excel files are .xlsx format (not .xls or .csv)
- Try re-saving files in Excel to ensure compatibility

**Calculation Questions:**
- Review the P&L calculation mockup in project documentation
- Check the formulas section above
- Validate with a simple manual calculation

**Feature Requests:**
- This is a Phase 1 prototype
- Advanced features (transaction costs, custom strikes) planned for Phase 2

---

## Summary: Why P&L Matters

**Traditional Approach:**
> "Realized vol was 20% vs 10% implied, so buying options was profitable."

**Reality Check:**
> "Realized vol was 20% but spot moved away from strike (low gamma), so hedging costs exceeded option value. P&L was -$50,000."

**This Tool Shows:**
- ✅ Where volatility occurred (near or far from strike)
- ✅ How gamma affected hedge costs
- ✅ Path dependency of P&L
- ✅ Actual trading profitability

**Bottom Line:** Use P&L as your primary decision metric. Volatility comparison is useful context, but P&L is what matters for trading.

---

## Quick Start Checklist

- [ ] Open `fx_volatility_analytics.html` in browser
- [ ] Upload spot price Excel file (green checkmark)
- [ ] Upload implied volatility Excel file (green checkmark)
- [ ] Select hedge frequency (start with 10 minutes)
- [ ] Select option type (start with "Both")
- [ ] Select strikes and tenors
- [ ] Click "Calculate P&L Analysis"
- [ ] Review P&L table (primary metric)
- [ ] Click rows to see P&L evolution
- [ ] Check Rankings tab for best/worst trades
- [ ] Export results to Excel for deeper analysis

**Ready to analyze volatility trading profitability!** 🚀
