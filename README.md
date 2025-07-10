# Silver Breakout Analysis

A comprehensive yfinance-based script that analyzes silver's historical breakout patterns and calculates the probability of successful breakouts.

## What This Script Does

The script identifies and analyzes historical instances where:

1. **Silver goes up ≥5% in one day** (breakout day)
2. **Holds above that breakout price for the next 2 days** (confirmation period)
3. **Is higher 6 months (~126 trading days) later** (success criteria)

It then calculates the **win rate** - the percentage of times silver was higher 6 months after a valid breakout.

## Features

- 📊 **Historical Analysis**: Analyzes silver price data from 2000 to present
- 🎯 **Breakout Identification**: Finds days with ≥5% daily increases
- ✅ **Confirmation Check**: Verifies 2-day hold above breakout price
- 📈 **Win Rate Calculation**: Determines success rate over 6 months
- 📉 **Visualization**: Creates charts showing breakout periods and results
- 📋 **Data Export**: Exports results to CSV for further analysis
- 🔄 **Multiple Symbols**: Tries different silver symbols (SI=F, SLV, XAGUSD=X)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Or install manually:**
   ```bash
   pip install yfinance pandas numpy matplotlib
   ```

## Usage

### Quick Start

Run the analysis with default parameters:

```bash
python run_analysis.py
```

### Advanced Usage

Use the main script directly for custom parameters:

```python
from silver_breakout_analysis import SilverBreakoutAnalyzer

# Initialize analyzer
analyzer = SilverBreakoutAnalyzer(symbol='SI=F', start_date='2000-01-01')

# Fetch data
analyzer.fetch_data()

# Run analysis with custom parameters
breakouts = analyzer.identify_breakouts(
    threshold_pct=5.0,    # Minimum daily increase
    hold_days=2,          # Days to hold above breakout
    future_days=126       # Days to look ahead
)

# Generate charts
analyzer.plot_breakouts()
analyzer.plot_win_rate_by_year()

# Export results
analyzer.export_results('my_results.csv')
```

## Output

The script generates:

1. **Console Output**: Summary statistics and recent breakouts
2. **Main Chart**: Price chart with breakout periods highlighted (saved as `output/silver_breakouts.png`)
   - Green dots/lines = successful breakouts (higher after 6 months)
   - Red dots/lines = failed breakouts (lower after 6 months)
3. **Win Rate Chart**: Yearly breakdown of success rates (saved as `output/silver_winrate_by_year.png`)
4. **CSV File**: Detailed results for further analysis

## Example Output

```
============================================================
SILVER BREAKOUT ANALYSIS
============================================================
Analyzing historical probability that:
1. Silver goes up ≥5% in one day
2. Holds above that breakout price for 2 days
3. Is higher 6 months (126 trading days) later
============================================================

Fetching SI=F data from 2010-01-01...
Successfully fetched 3,456 days of data for SI=F
Date range: 2010-01-04 to 2024-01-15

Identifying breakouts with 5.0% daily increase...
Found 47 days with >= 5.0% increase

Breakout Analysis Results:
Total valid breakouts: 23
Win rate: 65.2% (15/23)
Average future return: 8.7%
Average breakout return: 7.2%

Future Return Statistics:
Min: -15.3%
Max: 45.2%
Std Dev: 12.8%

Recent Breakouts (last 10):
2023-03-17: 6.2% → 12.4% (WIN)
2023-01-09: 5.8% → -3.1% (LOSS)
2022-11-11: 7.1% → 18.9% (WIN)
...
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `threshold_pct` | 5.0 | Minimum daily percentage increase |
| `hold_days` | 2 | Days price must hold above breakout |
| `future_days` | 126 | Days to look ahead (6 months) |
| `symbol` | 'SI=F' | Silver symbol (SI=F, SLV, XAGUSD=X) |
| `start_date` | '2010-01-01' | Start date for analysis |

## Files

- `silver_breakout_analysis.py` - Main analysis class
- `run_analysis.py` - Simple runner script
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `silver_breakout_results.csv` - Generated results (after running)

## Troubleshooting

### No Data Found
- Check internet connection
- Try different symbols (SLV, XAGUSD=X)
- Use different date ranges

### No Breakouts Found
- Lower the threshold percentage (e.g., 3% instead of 5%)
- Reduce hold period (e.g., 1 day instead of 2)
- Use longer date range

### Chart Display Issues
- Ensure matplotlib backend is properly configured
- Try running in Jupyter notebook for better display

## Technical Details

- **Data Source**: Yahoo Finance via yfinance
- **Analysis Period**: 2000-present (configurable)
- **Trading Days**: Uses actual trading days (not calendar days)
- **Price Data**: Uses closing prices for analysis
- **Success Criteria**: Simple binary (higher/lower after 6 months)

## Disclaimer

This script is for educational and research purposes only. Past performance does not guarantee future results. Always do your own research and consider consulting with financial professionals before making investment decisions. 