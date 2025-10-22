"""
Generate sample Excel files for FX Volatility Trading Analytics
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# ============================================
# 1. Generate Spot Price Data (24 hours, 10-minute frequency)
# ============================================

print("Generating spot price data...")

# Time range: 24 hours with 10-minute intervals
start_time = datetime(2025, 10, 20, 0, 0)
time_points = 144  # 24 hours * 6 per hour
timestamps = [start_time + timedelta(minutes=10*i) for i in range(time_points)]

# Currency pairs with realistic initial spots
pairs = {
    'EURUSD': 1.1000,
    'USDJPY': 150.00,
    'GBPUSD': 1.2700,
    'AUDUSD': 0.6500,
    'USDCAD': 1.3800,
    'USDCHF': 0.9000
}

# Generate realistic spot price movements
spot_data = {'Timestamp': timestamps}

for pair, initial_spot in pairs.items():
    # Generate returns with realistic volatility (10-15% annualized)
    annual_vol = np.random.uniform(0.10, 0.15)
    ten_min_vol = annual_vol / np.sqrt(365 * 24 * 6)

    # Generate returns with some mean reversion
    returns = np.random.normal(0, ten_min_vol, time_points - 1)

    # Add some trend and mean reversion
    prices = [initial_spot]
    for i in range(time_points - 1):
        # Mean reversion factor
        mean_reversion = -0.02 * (prices[-1] - initial_spot) / initial_spot
        ret = returns[i] + mean_reversion
        new_price = prices[-1] * np.exp(ret)
        prices.append(new_price)

    spot_data[pair] = prices

# Create DataFrame
df_spots = pd.DataFrame(spot_data)

# Save to Excel
df_spots.to_excel('/home/user/Complete-Python-3-Bootcamp/sample_spot_prices.xlsx', index=False)
print(f"✓ Created sample_spot_prices.xlsx with {len(df_spots)} rows and {len(pairs)} currency pairs")

# Print sample data
print("\nSample spot data (first 5 rows):")
print(df_spots.head())
print("\nSpot price ranges:")
for pair in pairs.keys():
    print(f"  {pair}: {df_spots[pair].min():.4f} to {df_spots[pair].max():.4f}")

# ============================================
# 2. Generate Implied Volatility Data
# ============================================

print("\n" + "="*60)
print("Generating implied volatility data...")

vol_data = []

strikes = ['ATM', '25DP', '25DC', '10DP', '10DC']
tenors = ['1D', '1W']

for pair in pairs.keys():
    for tenor in tenors:
        # Base ATM volatility (realistic levels for different tenors)
        if tenor == '1D':
            atm_vol = np.random.uniform(8, 12)  # 8-12% for overnight
        else:  # 1W
            atm_vol = np.random.uniform(10, 15)  # 10-15% for 1 week

        for strike in strikes:
            # Add volatility smile/skew
            if strike == 'ATM':
                vol = atm_vol
            elif strike == '25DP':
                vol = atm_vol + np.random.uniform(0.5, 1.5)  # Put skew
            elif strike == '25DC':
                vol = atm_vol + np.random.uniform(0.2, 0.8)  # Call skew (lower)
            elif strike == '10DP':
                vol = atm_vol + np.random.uniform(1.5, 3.0)  # Larger put skew
            elif strike == '10DC':
                vol = atm_vol + np.random.uniform(0.5, 1.5)  # Larger call skew

            vol_data.append({
                'Pair': pair,
                'Strike': strike,
                'Tenor': tenor,
                'ImpliedVol': round(vol, 2)
            })

# Create DataFrame
df_vols = pd.DataFrame(vol_data)

# Save to Excel
df_vols.to_excel('/home/user/Complete-Python-3-Bootcamp/sample_implied_vols.xlsx', index=False)
print(f"✓ Created sample_implied_vols.xlsx with {len(df_vols)} rows")

# Print sample data
print("\nSample implied vol data (first 10 rows):")
print(df_vols.head(10))

print("\n" + "="*60)
print("Implied vol summary by tenor:")
print(df_vols.groupby('Tenor')['ImpliedVol'].agg(['min', 'mean', 'max']))

print("\n" + "="*60)
print("✓ Sample data generation complete!")
print("\nFiles created:")
print("  1. sample_spot_prices.xlsx - 24 hours of 10-minute spot data")
print("  2. sample_implied_vols.xlsx - Implied vols for all strikes and tenors")
print("\nYou can now upload these files to the FX Volatility Analytics tool.")
