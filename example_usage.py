#!/usr/bin/env python3
"""
Example usage of the Silver Breakout Analyzer
Demonstrates different ways to use the analyzer with custom parameters
"""

from silver_breakout_analysis import SilverBreakoutAnalyzer

def example_1_basic_analysis():
    """Basic analysis with default parameters"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Analysis (Default Parameters)")
    print("=" * 60)
    
    analyzer = SilverBreakoutAnalyzer(symbol='SI=F', start_date='2000-01-01')
    analyzer.fetch_data()
    
    breakouts = analyzer.identify_breakouts(
        threshold_pct=5.0,    # 5% daily increase
        hold_days=2,          # Hold for 2 days
        future_days=126       # Check 6 months later
    )
    
    if breakouts is not None and len(breakouts) > 0:
        analyzer.plot_breakouts()
        analyzer.plot_win_rate_by_year()
        analyzer.export_results('basic_analysis_results.csv')

def example_2_more_lenient_criteria():
    """Analysis with more lenient criteria"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: More Lenient Criteria")
    print("=" * 60)
    
    analyzer = SilverBreakoutAnalyzer(symbol='SI=F', start_date='2000-01-01')
    analyzer.fetch_data()
    
    breakouts = analyzer.identify_breakouts(
        threshold_pct=3.0,    # Lower threshold: 3% daily increase
        hold_days=1,          # Shorter hold: 1 day
        future_days=126       # Still check 6 months later
    )
    
    if breakouts is not None and len(breakouts) > 0:
        analyzer.plot_breakouts()
        analyzer.plot_win_rate_by_year()
        analyzer.export_results('lenient_analysis_results.csv')

def example_3_shorter_timeframe():
    """Analysis with shorter future timeframe"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Shorter Timeframe (3 months)")
    print("=" * 60)
    
    analyzer = SilverBreakoutAnalyzer(symbol='SI=F', start_date='2015-01-01')
    analyzer.fetch_data()
    
    breakouts = analyzer.identify_breakouts(
        threshold_pct=5.0,    # 5% daily increase
        hold_days=2,          # Hold for 2 days
        future_days=63        # Check 3 months later (63 trading days)
    )
    
    if breakouts is not None and len(breakouts) > 0:
        analyzer.plot_breakouts()
        analyzer.plot_win_rate_by_year()
        analyzer.export_results('short_timeframe_results.csv')

def example_4_custom_analysis():
    """Custom analysis with different silver symbol"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Custom Analysis (SLV ETF)")
    print("=" * 60)
    
    analyzer = SilverBreakoutAnalyzer(symbol='SLV', start_date='2015-01-01')
    analyzer.fetch_data()
    
    breakouts = analyzer.identify_breakouts(
        threshold_pct=4.0,    # 4% daily increase
        hold_days=2,          # Hold for 2 days
        future_days=126       # Check 6 months later
    )
    
    if breakouts is not None and len(breakouts) > 0:
        analyzer.plot_breakouts()
        analyzer.plot_win_rate_by_year()
        analyzer.export_results('slv_analysis_results.csv')

def example_5_parameter_sweep():
    """Sweep through different threshold values"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Parameter Sweep")
    print("=" * 60)
    
    analyzer = SilverBreakoutAnalyzer(symbol='SI=F', start_date='2000-01-01')
    analyzer.fetch_data()
    
    thresholds = [3.0, 4.0, 5.0, 6.0, 7.0]
    
    print("Threshold | Breakouts | Win Rate | Avg Return")
    print("-" * 45)
    
    for threshold in thresholds:
        breakouts = analyzer.identify_breakouts(
            threshold_pct=threshold,
            hold_days=2,
            future_days=126
        )
        
        if breakouts is not None and len(breakouts) > 0:
            win_rate = (breakouts['is_winner'].sum() / len(breakouts)) * 100
            avg_return = breakouts['future_return'].mean()
            print(f"{threshold:9.1f} | {len(breakouts):9d} | {win_rate:8.1f}% | {avg_return:9.1f}%")
        else:
            print(f"{threshold:9.1f} | {0:9d} | {0:8.1f}% | {0:9.1f}%")

def main():
    """Run all examples"""
    print("🎯 SILVER BREAKOUT ANALYSIS - EXAMPLES")
    print("=" * 60)
    print("This script demonstrates different ways to use the analyzer.")
    print("Each example will generate charts and CSV files.")
    print("=" * 60)
    
    try:
        # Run examples
        example_1_basic_analysis()
        example_2_more_lenient_criteria()
        example_3_shorter_timeframe()
        example_4_custom_analysis()
        example_5_parameter_sweep()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed!")
        print("Check the generated CSV files and charts.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Try running the basic analysis first to ensure everything works.")

if __name__ == "__main__":
    main() 