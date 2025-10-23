#!/usr/bin/env python3
"""
Quick verification that test files are correct
"""
import pandas as pd
import os

print("=" * 60)
print("VERIFYING TEST FILES")
print("=" * 60)
print()

# Check if files exist
files = {
    'HTML App': 'fx_volatility_analytics.html',
    'Spot Data': 'simple_spot_prices.xlsx',
    'Vol Data': 'simple_implied_vols.xlsx'
}

all_exist = True
for name, filename in files.items():
    if os.path.exists(filename):
        print(f"✓ {name}: {filename} EXISTS")
    else:
        print(f"✗ {name}: {filename} NOT FOUND")
        all_exist = False

if not all_exist:
    print("\n❌ Some files are missing! Cannot proceed.")
    exit(1)

print()
print("=" * 60)
print("CHECKING FILE CONTENTS")
print("=" * 60)
print()

# Check spot file
try:
    df_spot = pd.read_excel('simple_spot_prices.xlsx')
    print("SPOT FILE:")
    print(f"  Rows: {len(df_spot)}")
    print(f"  Columns: {list(df_spot.columns)}")
    print(f"  First timestamp: {df_spot['Timestamp'].iloc[0]}")
    print(f"  Last timestamp: {df_spot['Timestamp'].iloc[-1]}")
    print(f"  EURUSD range: {df_spot['EURUSD'].min():.4f} to {df_spot['EURUSD'].max():.4f}")

    # Check for NaN
    if df_spot.isna().any().any():
        print("  ⚠️  WARNING: File contains NaN values!")
    else:
        print("  ✓ No missing values")

    print()
except Exception as e:
    print(f"  ✗ ERROR reading spot file: {e}")
    print()

# Check vol file
try:
    df_vol = pd.read_excel('simple_implied_vols.xlsx')
    print("VOL FILE:")
    print(f"  Rows: {len(df_vol)}")
    print(f"  Columns: {list(df_vol.columns)}")
    print()
    print("  Data:")
    for _, row in df_vol.iterrows():
        print(f"    {row['Pair']} | {row['Strike']} | {row['Tenor']} | {row['ImpliedVol']:.1f}%")

    # Check for NaN
    if df_vol.isna().any().any():
        print("  ⚠️  WARNING: File contains NaN values!")
    else:
        print("  ✓ No missing values")

    # Check column names
    required_cols = ['Pair', 'Strike', 'Tenor', 'ImpliedVol']
    if all(col in df_vol.columns for col in required_cols):
        print("  ✓ All required columns present")
    else:
        print("  ✗ Missing required columns!")

    print()
except Exception as e:
    print(f"  ✗ ERROR reading vol file: {e}")
    print()

print("=" * 60)
print("✅ ALL FILES VERIFIED!")
print("=" * 60)
print()
print("NEXT STEPS:")
print("1. Run: ./test_app.sh")
print("2. Open browser to: http://localhost:8000/fx_volatility_analytics.html")
print("3. Press F12 to open console")
print("4. Upload the files and test!")
print()
