#!/bin/bash

echo "=================================="
echo "FX Volatility Analytics - Test Setup"
echo "=================================="
echo ""

# Check if files exist
echo "Checking test files..."
if [ -f "simple_spot_prices.xlsx" ]; then
    echo "✓ simple_spot_prices.xlsx found"
else
    echo "✗ simple_spot_prices.xlsx NOT FOUND"
    exit 1
fi

if [ -f "simple_implied_vols.xlsx" ]; then
    echo "✓ simple_implied_vols.xlsx found"
else
    echo "✗ simple_implied_vols.xlsx NOT FOUND"
    exit 1
fi

if [ -f "fx_volatility_analytics.html" ]; then
    echo "✓ fx_volatility_analytics.html found"
else
    echo "✗ fx_volatility_analytics.html NOT FOUND"
    exit 1
fi

echo ""
echo "All files found! Starting local web server..."
echo ""
echo "=================================="
echo "INSTRUCTIONS:"
echo "=================================="
echo "1. Open your web browser"
echo "2. Go to: http://localhost:8000/fx_volatility_analytics.html"
echo "3. Press F12 to open console"
echo "4. Upload simple_spot_prices.xlsx (first box)"
echo "5. Upload simple_implied_vols.xlsx (second box)"
echo "6. Click 'Calculate P&L Analysis'"
echo ""
echo "Press Ctrl+C to stop the server when done"
echo "=================================="
echo ""

# Start server
python3 -m http.server 8000
