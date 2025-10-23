"""
Verify the P&L calculation example - check realized vol calculation
"""
import numpy as np

# Spot path from the example
spots = [1.1000, 1.1020, 1.0990, 1.1010, 1.1025]

# Calculate returns
returns = []
for i in range(1, len(spots)):
    r = np.log(spots[i] / spots[i-1])
    returns.append(r)
    print(f"r{i} = ln({spots[i]}/{spots[i-1]}) = {r:.6f} = {r*100:.4f}%")

# Calculate variance
squared_returns = [r**2 for r in returns]
print(f"\nSquared returns:")
for i, r2 in enumerate(squared_returns, 1):
    print(f"r{i}² = {r2:.10f}")

sum_r2 = sum(squared_returns)
print(f"\nSum of r² = {sum_r2:.10f}")

variance_per_period = sum_r2 / len(returns)
print(f"Variance (per 6-hour period) = {sum_r2} / {len(returns)} = {variance_per_period:.10f}")

# Annualize - 6 hour periods
# 6 hours = 0.25 days
# Periods per year = 365 / 0.25 = 1,460
periods_per_year = 365 * 4  # 4 periods of 6 hours per day
print(f"\nPeriods per year = {periods_per_year}")

annual_variance = variance_per_period * periods_per_year
print(f"Annual variance = {variance_per_period:.10f} × {periods_per_year} = {annual_variance:.6f}")

realized_vol = np.sqrt(annual_variance)
print(f"\nRealized Vol = √{annual_variance:.6f} = {realized_vol:.4f} = {realized_vol*100:.2f}%")

print("\n" + "="*60)
print("CORRECTED: Realized vol is 7.61%, not 24.1%!")
print("The original calculation was wrong.")
