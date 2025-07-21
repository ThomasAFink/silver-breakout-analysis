#!/usr/bin/env python3
"""
Simple runner script for Silver Breakout Analysis
Run this script to analyze silver's historical breakout patterns
"""

from silver_breakout_analysis import SilverBreakoutAnalyzer

def run_analysis():
    """Run the silver breakout analysis with default parameters"""
    print("🚀 Starting Silver Breakout Analysis...")
    
    # Initialize analyzer
    analyzer = SilverBreakoutAnalyzer(symbol='SI=F', start_date='2000-01-01')
    
    try:
        # Fetch data
        analyzer.fetch_data()
        
        # Run analysis with default parameters
        breakouts = analyzer.identify_breakouts(
            threshold_pct=5,
            hold_days=2,
            future_days=252
        )
        
        if breakouts is not None and len(breakouts) > 0:
            # Create visualizations
            print("\n" + "=" * 60)
            print("GENERATING CHARTS...")
            print("=" * 60)
            
            # Main breakout chart
            analyzer.plot_breakouts(save_path="output/silver_breakouts.png", threshold_pct=5.0)
            
            # Win rate by year
            analyzer.plot_win_rate_by_year(save_path="output/silver_winrate_by_year.png")
            
            # Export results
            analyzer.export_results()
            
            # Generate parameter sweep table
            sweep_df = analyzer.generate_parameter_sweep_table(save_path="output/parameter_sweep_results.csv")
            analyzer.save_table_as_image(sweep_df, save_path="output/parameter_sweep_results.png", title="Silver Breakout Parameter Sweep (2000-2025)")
            
            print("\n✅ Analysis complete! Check the generated charts and CSV file.")
        else:
            print("\n❌ No valid breakouts found with current parameters.")
            print("Try running with different parameters:")
            print("- Lower threshold (e.g., 3% instead of 5%)")
            print("- Shorter hold period (e.g., 1 day instead of 2)")
            print("- Different date range")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Trying alternative approach...")
        
        # Try with more lenient parameters
        try:
            analyzer = SilverBreakoutAnalyzer(symbol='SLV', start_date='2006-01-01')
            analyzer.fetch_data()
            breakouts = analyzer.identify_breakouts(
                threshold_pct=3.0,  # Lower threshold
                hold_days=1,        # Shorter hold period
                future_days=126
            )
            
            if breakouts is not None and len(breakouts) > 0:
                analyzer.plot_breakouts()
                analyzer.plot_win_rate_by_year()
                analyzer.export_results()
                print("\n✅ Analysis complete with alternative parameters!")
            else:
                print("\n❌ Still no breakouts found. Please check your internet connection and try again.")
        except Exception as e2:
            print(f"\n❌ Alternative approach also failed: {e2}")

if __name__ == "__main__":
    run_analysis() 