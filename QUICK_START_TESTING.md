# Quick Start Testing Guide

## Files Available for Testing

### Simple Test Files (RECOMMENDED FOR FIRST TEST)
Use these minimal files to verify the tool works:

1. **simple_spot_prices.xlsx** (or .csv)
   - Single currency pair: EURUSD
   - 24 hours of data (145 rows)
   - 10-minute frequency
   - ~10% realized volatility

2. **simple_implied_vols.xlsx** (or .csv)
   - Just EURUSD
   - 3 strikes: ATM, 25DP, 25DC
   - 1D tenor only
   - 10% implied vol (ATM)

### Full Test Files (FOR COMPREHENSIVE TESTING)
Use these for testing multiple pairs:

1. **sample_spot_prices.xlsx**
   - 6 currency pairs (EURUSD, USDJPY, GBPUSD, AUDUSD, USDCAD, USDCHF)
   - 24 hours of data (144 rows)
   - 10-minute frequency

2. **sample_implied_vols.xlsx**
   - All 6 pairs
   - 5 strikes (ATM, 25DP, 25DC, 10DP, 10DC)
   - 2 tenors (1D, 1W)
   - 60 total rows

---

## Step-by-Step Testing

### Step 1: Open the Tool
```bash
# Simply double-click this file:
fx_volatility_analytics.html

# Or use a local server if file:// protocol has issues:
python -m http.server 8000
# Then open: http://localhost:8000/fx_volatility_analytics.html
```

### Step 2: Open Browser Console
**IMPORTANT:** Open your browser's developer console to see detailed logs!

- **Chrome/Edge:** Press F12 or Ctrl+Shift+J (Cmd+Option+J on Mac)
- **Firefox:** Press F12 or Ctrl+Shift+K (Cmd+Option+K on Mac)
- **Safari:** Enable Develop menu first, then Cmd+Option+C

You should see console output when uploading files:
```
Spot file selected: simple_spot_prices.xlsx
Processing spot file...
Spot data loaded: 145 rows
Columns: ['Timestamp', 'EURUSD']
First row: {Timestamp: '2025-10-20 09:00:00', EURUSD: 1.1}
```

### Step 3: Upload Simple Test Files

1. **Click "Upload Spot Price Data"**
   - Select: `simple_spot_prices.xlsx`
   - Box should turn green with "✓ Loaded 145 rows"
   - Check console for detailed logs

2. **Click "Upload Implied Volatility Data"**
   - Select: `simple_implied_vols.xlsx`
   - Box should turn green with "✓ Loaded 3 rows"
   - Check console for detailed logs

3. **Check "Calculate" Button**
   - Should now be enabled (not grayed out)
   - If not enabled, check console for errors

### Step 4: Configure Settings

Use these settings for first test:
- **Hedge Frequency:** 10 minutes
- **Option Type:** Both (Call & Put)
- **Strikes:** Select ATM (hold Ctrl/Cmd to select multiple)
- **Tenors:** Select 1D

### Step 5: Run Analysis

1. Click "Calculate P&L Analysis"
2. Wait for "Calculating..." message
3. Results should appear in ~2-5 seconds
4. Check console if it takes longer or fails

### Step 6: Verify Results

Expected results for EURUSD ATM Call with simple test data:
- **Premium:** ~$200,000 (for 100M USD notional)
- **Realized Vol:** ~11% (data generated with ~10% target)
- **P&L:** Should be positive or slightly negative depending on spot path

### Step 7: Interactive Features

1. **Click any row in P&L table**
   - Should open modal showing P&L evolution chart
   - Should show 4 lines: Total P&L, Hedge P&L, Option MTM, Premium

2. **Switch between tabs:**
   - P&L Analysis (primary)
   - Volatility Comparison (scatter plot)
   - P&L Rankings (top/bottom trades)

3. **Export to Excel:**
   - Click "Export Results to Excel"
   - Should download: FX_Volatility_Analysis.xlsx
   - Open in Excel to verify

---

## Troubleshooting

### Issue: Files Not Uploading

**Check Console for Errors:**
```
Error: XLSX library not loaded. Check internet connection.
```
**Solution:** Ensure you have internet connection (CDN libraries need to load)

**Check Console for:**
```
Spot file selected: simple_spot_prices.xlsx
```
**If you DON'T see this:** File input is not working. Try:
1. Click directly on the upload box text
2. Refresh the page
3. Try a different browser
4. Check file permissions

### Issue: "Calculate" Button Not Enabled

**Console should show:**
```
Spot data loaded: 145 rows
Vol data loaded: 3 rows
```

**If missing:** Upload both files again and check console errors

### Issue: Calculation Takes Forever

**Check console for errors during calculation:**
```
Error: Cannot read property 'EURUSD' of undefined
```

**Common causes:**
1. Column names don't match between files
2. Missing 'Timestamp' column in spot file
3. Missing 'Pair', 'Strike', 'Tenor', or 'ImpliedVol' in vol file
4. Data format issues (NaN, null values)

### Issue: Results Look Wrong

**Verify your expectations:**
1. Check CORRECTED_PNL_CALCULATION.md for proper calculation methodology
2. Realized vol should be close to implied vol (~10%)
3. P&L depends on spot path and where volatility occurred
4. Small losses are normal if realized < implied

### Issue: Charts Not Showing

**Check console for:**
```
Error: Chart.js not loaded
```
**Solution:** Ensure internet connection for CDN

**Check for:**
```
Error: Canvas element not found
```
**Solution:** Refresh page, charts might not have initialized

---

## Quick Debugging Checklist

- [ ] Browser console is open (F12)
- [ ] Internet connection is active (for CDN libraries)
- [ ] Both files uploaded successfully (green checkboxes)
- [ ] Console shows "Spot data loaded: X rows"
- [ ] Console shows "Vol data loaded: Y rows"
- [ ] File column names match specifications exactly
- [ ] No JavaScript errors in console
- [ ] "Calculate" button is enabled
- [ ] Results appear after clicking Calculate

---

## Expected Console Output (Success Case)

```
Spot file selected: simple_spot_prices.xlsx
Processing spot file...
Spot data loaded: 145 rows
Columns: Timestamp,EURUSD
First row: {Timestamp: "2025-10-20 09:00:00", EURUSD: 1.1}

Vol file selected: simple_implied_vols.xlsx
Processing vol file...
Vol data loaded: 3 rows
Columns: Pair,Strike,Tenor,ImpliedVol
First row: {Pair: "EURUSD", Strike: "ATM", Tenor: "1D", ImpliedVol: 10}

[Click Calculate]

Starting analysis...
Processing EURUSD...
Calculating ATM call...
Calculating ATM put...
Analysis complete: 2 results
```

---

## File Format Verification

### Spot File (simple_spot_prices.xlsx)

**First 3 rows should look like:**
| Timestamp | EURUSD |
|-----------|--------|
| 2025-10-20 09:00:00 | 1.1000 |
| 2025-10-20 09:10:00 | 1.0995 |
| 2025-10-20 09:20:00 | 1.1000 |

**Verify:**
```bash
python -c "import pandas as pd; print(pd.read_excel('simple_spot_prices.xlsx').head())"
```

### Vol File (simple_implied_vols.xlsx)

**All rows should look like:**
| Pair | Strike | Tenor | ImpliedVol |
|------|--------|-------|------------|
| EURUSD | ATM | 1D | 10.0 |
| EURUSD | 25DP | 1D | 11.5 |
| EURUSD | 25DC | 1D | 10.5 |

**Verify:**
```bash
python -c "import pandas as pd; print(pd.read_excel('simple_implied_vols.xlsx'))"
```

---

## Alternative: Use CSV Files

If Excel files aren't working, try CSV versions:

1. **simple_spot_prices.csv** - Same data, CSV format
2. **simple_implied_vols.csv** - Same data, CSV format

**Note:** You may need to update the HTML to accept .csv files. Currently it's configured for .xlsx primarily.

---

## Next Steps After Successful Test

1. ✅ Verify calculations match expected results
2. ✅ Test with multiple currency pairs (sample_spot_prices.xlsx)
3. ✅ Test different hedge frequencies (30 min, 1 hour)
4. ✅ Test different strikes (25DP, 25DC)
5. ✅ Export results and analyze in Excel
6. ✅ Prepare your own data following the same format

---

## Getting Help

**If tests fail:**
1. Copy full console output
2. Note which step failed
3. Check CORRECTED_PNL_CALCULATION.md for expected results
4. Verify file formats exactly match specifications

**Common fixes:**
- Refresh page and try again
- Try different browser (Chrome recommended)
- Verify internet connection (for CDN libraries)
- Check file formats match specifications
- Use simple test files first before complex data

---

## Success Criteria

You'll know it's working when:
✅ Both upload boxes are green
✅ Calculate button is enabled
✅ Results appear within seconds
✅ Summary cards show statistics
✅ P&L table has rows of data
✅ Clicking rows shows P&L evolution chart
✅ Charts are visible and interactive
✅ Excel export works and contains data

Good luck testing! 🚀
