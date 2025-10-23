"""
Create simple, minimal test files for easier debugging
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Creating SIMPLE test files with minimal data...")

# ============================================
# 1. Simple Spot File - Just EURUSD, 24 hours
# ============================================

# Generate spot path with KNOWN 10% volatility
np.random.seed(123)

start_time = datetime(2025, 10, 20, 9, 0)  # Start 9 AM
time_points = 145  # 24 hours with 10-minute intervals (144 periods)
timestamps = [start_time + timedelta(minutes=10*i) for i in range(time_points)]

# Generate EURUSD with exactly 10% annual volatility
S0 = 1.1000
annual_vol = 0.10
ten_min_vol = annual_vol / np.sqrt(365 * 24 * 6)  # = 0.0436%

print(f"Target annual vol: {annual_vol*100:.2f}%")
print(f"10-minute vol: {ten_min_vol*100:.4f}%")

# Generate returns
returns = np.random.normal(0, ten_min_vol, time_points - 1)

# Build price series
prices = [S0]
for ret in returns:
    prices.append(prices[-1] * np.exp(ret))

# Verify realized vol
actual_returns = np.diff(np.log(prices))
variance = np.var(actual_returns, ddof=1)
periods_per_year = 365 * 24 * 6
realized_vol = np.sqrt(variance * periods_per_year)
print(f"Actual realized vol: {realized_vol*100:.2f}%")

# Create DataFrame
df_spot = pd.DataFrame({
    'Timestamp': timestamps,
    'EURUSD': prices
})

# Save as both Excel and CSV
df_spot.to_excel('/home/user/Complete-Python-3-Bootcamp/simple_spot_prices.xlsx', index=False)
df_spot.to_csv('/home/user/Complete-Python-3-Bootcamp/simple_spot_prices.csv', index=False)

print(f"✓ Created simple_spot_prices.xlsx and .csv")
print(f"  - {len(df_spot)} rows")
print(f"  - Spot range: {df_spot['EURUSD'].min():.4f} to {df_spot['EURUSD'].max():.4f}")

# ============================================
# 2. Simple Vol File - Just EURUSD, 1D tenor
# ============================================

df_vol = pd.DataFrame([
    {'Pair': 'EURUSD', 'Strike': 'ATM', 'Tenor': '1D', 'ImpliedVol': 10.0},
    {'Pair': 'EURUSD', 'Strike': '25DP', 'Tenor': '1D', 'ImpliedVol': 11.5},
    {'Pair': 'EURUSD', 'Strike': '25DC', 'Tenor': '1D', 'ImpliedVol': 10.5},
])

df_vol.to_excel('/home/user/Complete-Python-3-Bootcamp/simple_implied_vols.xlsx', index=False)
df_vol.to_csv('/home/user/Complete-Python-3-Bootcamp/simple_implied_vols.csv', index=False)

print(f"✓ Created simple_implied_vols.xlsx and .csv")
print(f"  - {len(df_vol)} rows")
print(f"  - Strikes: ATM, 25DP, 25DC")

print("\n" + "="*60)
print("SIMPLE TEST FILES CREATED:")
print("  1. simple_spot_prices.xlsx / .csv")
print("  2. simple_implied_vols.xlsx / .csv")
print("\nThese are minimal files with:")
print("  - Just EURUSD (single pair)")
print("  - 24 hours of 10-minute data")
print("  - 10% volatility (verified)")
print("  - 3 strikes only")
print("\nUse these to test the HTML interface!")

# Show first few rows
print("\n" + "="*60)
print("SPOT FILE (first 5 rows):")
print(df_spot.head())

print("\nVOL FILE (all rows):")
print(df_vol)

# Create a verification script
print("\n" + "="*60)
print("Expected Results (for ATM call, 24h expiry, 10min hedging):")
print(f"  - Initial spot: {S0:.4f}")
print(f"  - Strike (ATM): {S0:.4f}")
print(f"  - Implied vol: 10.0%")
print(f"  - Realized vol: ~{realized_vol*100:.2f}%")
print(f"  - Notional: 100M USD = {100000000/S0:,.0f} EUR")
