import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SilverBreakoutAnalyzer:
    def __init__(self, symbol='SI=F', start_date='2000-01-01'):
        """
        Initialize the analyzer with silver futures data
        
        Args:
            symbol (str): Silver futures symbol (SI=F for continuous futures)
            start_date (str): Start date for analysis
        """
        self.symbol = symbol
        self.start_date = start_date
        self.data = None
        self.breakouts = None
        
    def fetch_data(self):
        """Fetch silver price data from Yahoo Finance"""
        print(f"Fetching {self.symbol} data from {self.start_date}...")
        
        # Get silver futures data
        ticker = yf.Ticker(self.symbol)
        self.data = ticker.history(start=self.start_date)
        
        if self.data.empty:
            print("No data found. Trying alternative symbol...")
            # Try alternative silver symbols
            alt_symbols = ['SLV', 'XAGUSD=X']
            for alt_symbol in alt_symbols:
                print(f"Trying {alt_symbol}...")
                ticker = yf.Ticker(alt_symbol)
                self.data = ticker.history(start=self.start_date)
                if not self.data.empty:
                    self.symbol = alt_symbol
                    break
        
        if self.data.empty:
            raise ValueError("Could not fetch silver data from any source")
        
        print(f"Successfully fetched {len(self.data)} days of data for {self.symbol}")
        print(f"Date range: {self.data.index[0].date()} to {self.data.index[-1].date()}")
        
        return self.data
    
    def identify_breakouts(self, threshold_pct=5.0, hold_days=2, future_days=126):
        """
        Identify breakouts that meet the criteria:
        1. Price increases by threshold_pct% in one day
        2. Holds above breakout price for hold_days days
        3. Check if higher after future_days days
        
        Args:
            threshold_pct (float): Minimum daily increase percentage
            hold_days (int): Number of days to hold above breakout price
            future_days (int): Number of days to look ahead for win/loss
        """
        if self.data is None:
            self.fetch_data()
        
        print(f"\nIdentifying breakouts with {threshold_pct}% daily increase...")
        
        # Calculate daily returns
        self.data['Daily_Return'] = self.data['Close'].pct_change() * 100
        
        # Find days with >= threshold_pct increase
        breakout_candidates = self.data[self.data['Daily_Return'] >= threshold_pct].copy()
        
        print(f"Found {len(breakout_candidates)} days with >= {threshold_pct}% increase")
        
        # Analyze each breakout candidate
        breakout_results = []
        
        for idx, row in breakout_candidates.iterrows():
            breakout_date = idx
            breakout_price = row['Low']  # Use the low of the breakout day
            breakout_return = row['Daily_Return']
            
            # Check if we have enough future data
            future_idx = self.data.index.get_loc(breakout_date) + future_days
            has_future_data = future_idx < len(self.data)
            
            # Check if price holds above breakout for hold_days
            holds_above = True
            for i in range(1, hold_days + 1):
                check_idx = self.data.index.get_loc(breakout_date) + i
                if check_idx >= len(self.data):
                    holds_above = False
                    break
                
                if self.data.iloc[check_idx]['Close'] < breakout_price:
                    holds_above = False
                    break
            
            if not holds_above:
                continue
            
            # Check future price after future_days (if we have the data)
            if has_future_data:
                future_price = self.data.iloc[future_idx]['Close']
                future_return = ((future_price - breakout_price) / breakout_price) * 100
                is_winner = future_price > breakout_price
                status = 'completed'
            else:
                # For recent breakouts without enough future data
                future_price = None
                future_return = None
                is_winner = None
                status = 'pending'
            
            # Get the hold period data for visualization
            hold_period_data = []
            for i in range(hold_days + 1):
                check_idx = self.data.index.get_loc(breakout_date) + i
                if check_idx < len(self.data):
                    hold_period_data.append({
                        'date': self.data.index[check_idx],
                        'price': self.data.iloc[check_idx]['Close']
                    })
            
            breakout_results.append({
                'breakout_date': breakout_date,
                'breakout_price': breakout_price,
                'breakout_return': breakout_return,
                'future_price': future_price,
                'future_return': future_return,
                'is_winner': is_winner,
                'status': status,
                'hold_period_data': hold_period_data
            })
        
        self.breakouts = pd.DataFrame(breakout_results)
        
        if len(self.breakouts) > 0:
            # Separate completed and pending breakouts
            completed_breakouts = self.breakouts[self.breakouts['status'] == 'completed']
            pending_breakouts = self.breakouts[self.breakouts['status'] == 'pending']
            
            print(f"\nBreakout Analysis Results:")
            print(f"Total valid breakouts: {len(self.breakouts)}")
            print(f"Completed breakouts: {len(completed_breakouts)}")
            print(f"Pending breakouts (recent, awaiting results): {len(pending_breakouts)}")
            
            if len(completed_breakouts) > 0:
                # Convert to proper boolean for arithmetic
                wins = (completed_breakouts['is_winner'] == True).sum()
                win_rate = (wins / len(completed_breakouts)) * 100
                avg_future_return = completed_breakouts['future_return'].mean()
                
                print(f"Win rate (completed only): {win_rate:.1f}% ({wins}/{len(completed_breakouts)})")
                print(f"Average future return: {avg_future_return:.1f}%")
                print(f"Average breakout return: {self.breakouts['breakout_return'].mean():.1f}%")
                
                # Show some statistics for completed breakouts
                print(f"\nFuture Return Statistics (Completed):")
                print(f"Min: {completed_breakouts['future_return'].min():.1f}%")
                print(f"Max: {completed_breakouts['future_return'].max():.1f}%")
                print(f"Std Dev: {completed_breakouts['future_return'].std():.1f}%")
            
            # Show recent breakouts
            print(f"\nRecent Breakouts (last 10):")
            recent_breakouts = self.breakouts.tail(10)
            for _, breakout in recent_breakouts.iterrows():
                if breakout['status'] == 'pending':
                    print(f"{breakout['breakout_date'].date()}: {breakout['breakout_return']:.1f}% → PENDING (awaiting {future_days} trading days)")
                else:
                    status = "WIN" if breakout['is_winner'] else "LOSS"
                    print(f"{breakout['breakout_date'].date()}: {breakout['breakout_return']:.1f}% → {breakout['future_return']:.1f}% ({status})")
        else:
            print("No valid breakouts found with the given criteria")
        
        return self.breakouts
    
    def plot_breakouts(self, figsize=(15, 10), save_path=None, threshold_pct=None):
        """Plot the price chart with breakout periods highlighted"""
        if self.breakouts is None or len(self.breakouts) == 0:
            print("No breakouts to plot")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, height_ratios=[3, 1])
        
        # Main price chart
        ax1.plot(self.data.index, self.data['Close'], color='gray', alpha=0.7, linewidth=1, label='Silver Price')
        
        # Highlight breakout periods  
        colors = []
        for _, breakout in self.breakouts.iterrows():
            if breakout['status'] == 'pending':
                colors.append('orange')  # Orange for pending breakouts
            elif breakout['is_winner']:
                colors.append('green')   # Green for wins
            else:
                colors.append('red')     # Red for losses
        
        for i, (_, breakout) in enumerate(self.breakouts.iterrows()):
            # Plot the breakout day (close price) and breakout level (low)
            close_price = self.data.loc[breakout['breakout_date'], 'Close']
            ax1.scatter(breakout['breakout_date'], close_price, 
                       color=colors[i], s=50, alpha=0.8, zorder=5)
            ax1.scatter(breakout['breakout_date'], breakout['breakout_price'], 
                       color=colors[i], s=30, alpha=0.6, zorder=5, marker='v')
            
            # Highlight the hold period
            hold_data = breakout['hold_period_data']
            if hold_data:
                hold_dates = [d['date'] for d in hold_data]
                hold_prices = [d['price'] for d in hold_data]
                ax1.plot(hold_dates, hold_prices, color=colors[i], linewidth=3, alpha=0.7)
                
                # Add annotation for the breakout
                ax1.annotate(f"{breakout['breakout_return']:.1f}%", 
                           xy=(breakout['breakout_date'], breakout['breakout_price']),
                           xytext=(10, 10), textcoords='offset points',
                           fontsize=8, alpha=0.8)
        
        if threshold_pct is None:
            threshold_pct = 5.0  # fallback for legacy calls
            
        # Calculate stats for completed breakouts only
        completed_breakouts = self.breakouts[self.breakouts['status'] == 'completed']
        pending_count = len(self.breakouts[self.breakouts['status'] == 'pending'])
        
        if len(completed_breakouts) > 0:
            median_return = completed_breakouts['future_return'].median()
            win_count = (completed_breakouts["is_winner"] == True).sum()
            win_rate = (win_count / len(completed_breakouts) * 100)
            completed_count = len(completed_breakouts)
        else:
            median_return = 0
            win_rate = 0
            win_count = 0
            completed_count = 0
            
        title_pending = f" + {pending_count} pending" if pending_count > 0 else ""
        ax1.set_title(f'Silver Breakout Analysis ({self.symbol})\n'
                     f'≥{threshold_pct:.0f}% Daily Increase → Hold Above Low → 12-Month Result\n'
                     f'Win Rate: {win_rate:.1f}% '
                     f'({win_count}/{completed_count} completed{title_pending}) | '
                     f'Median Return: {median_return:.1f}%', 
                     fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Format x-axis
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax1.xaxis.set_major_locator(mdates.YearLocator(2))
        
        # Daily returns subplot
        ax2.plot(self.data.index, self.data['Daily_Return'], color='blue', alpha=0.6, linewidth=0.8)
        ax2.axhline(y=5, color='red', linestyle='--', alpha=0.7, label='5% Threshold')
        ax2.set_ylabel('Daily Return (%)', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Format x-axis for subplot
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax2.xaxis.set_major_locator(mdates.YearLocator(2))
        
        plt.tight_layout()
        
        # Save the chart if save_path is provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {save_path}")
        
        plt.show()
        
        return fig
    
    def plot_win_rate_by_year(self, figsize=(12, 6), save_path=None):
        """Plot win rate by year"""
        if self.breakouts is None or len(self.breakouts) == 0:
            print("No breakouts to plot")
            return
        
        # Only use completed breakouts (exclude pending ones)
        completed_breakouts = self.breakouts[self.breakouts['status'] == 'completed'].copy()
        
        if len(completed_breakouts) == 0:
            print("No completed breakouts to plot")
            return
        
        # Group by year
        completed_breakouts['year'] = completed_breakouts['breakout_date'].dt.year
        yearly_stats = completed_breakouts.groupby('year').agg({
            'is_winner': ['count', 'sum']
        }).round(2)
        
        yearly_stats.columns = ['total_breakouts', 'wins']
        yearly_stats['win_rate'] = (yearly_stats['wins'] / yearly_stats['total_breakouts'] * 100).round(1)
        
        # Filter years with at least 2 breakouts
        yearly_stats = yearly_stats[yearly_stats['total_breakouts'] >= 2]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, height_ratios=[2, 1])
        
        # Win rate by year
        bars1 = ax1.bar(yearly_stats.index, yearly_stats['win_rate'], 
                       color=['green' if rate >= 50 else 'red' for rate in yearly_stats['win_rate']],
                       alpha=0.7)
        ax1.axhline(y=50, color='black', linestyle='--', alpha=0.5, label='50% Win Rate')
        ax1.set_ylabel('Win Rate (%)', fontsize=12)
        ax1.set_title('Win Rate by Year', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Add value labels on bars
        for bar, rate in zip(bars1, yearly_stats['win_rate']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{rate:.0f}%', ha='center', va='bottom', fontsize=9)
        
        # Number of breakouts by year
        bars2 = ax2.bar(yearly_stats.index, yearly_stats['total_breakouts'], 
                       color='skyblue', alpha=0.7)
        ax2.set_ylabel('Number of Breakouts', fontsize=12)
        ax2.set_xlabel('Year', fontsize=12)
        ax2.set_title('Number of Breakouts by Year', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, count in zip(bars2, yearly_stats['total_breakouts']):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count:.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        # Save the chart if save_path is provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {save_path}")
        
        plt.show()
        
        return fig
    
    def export_results(self, filename='silver_breakout_results.csv'):
        """Export breakout results to CSV"""
        if self.breakouts is not None and len(self.breakouts) > 0:
            export_data = self.breakouts.copy()
            export_data['breakout_date'] = export_data['breakout_date'].dt.date
            export_data = export_data.drop('hold_period_data', axis=1)
            export_data.to_csv(filename, index=False)
            print(f"Results exported to {filename}")
        else:
            print("No results to export")

    def generate_parameter_sweep_table(self, thresholds=[3.0, 4.0, 5.0, 6.0, 7.0], save_path=None):
        """Generate a table showing results for different threshold values"""
        if self.data is None:
            self.fetch_data()
        
        print(f"\nGenerating parameter sweep table for thresholds: {thresholds}")
        
        results = []
        
        for threshold in thresholds:
            breakouts = self.identify_breakouts(
                threshold_pct=threshold,
                hold_days=2,
                future_days=126
            )
            
            if breakouts is not None and len(breakouts) > 0:
                win_rate = (breakouts['is_winner'].sum() / len(breakouts)) * 100
                avg_return = breakouts['future_return'].mean()
                median_return = breakouts['future_return'].median()
                min_return = breakouts['future_return'].min()
                max_return = breakouts['future_return'].max()
                std_return = breakouts['future_return'].std()
                
                results.append({
                    'threshold_pct': threshold,
                    'total_breakouts': len(breakouts),
                    'wins': breakouts['is_winner'].sum(),
                    'win_rate': win_rate,
                    'avg_return': avg_return,
                    'median_return': median_return,
                    'min_return': min_return,
                    'max_return': max_return,
                    'std_return': std_return
                })
            else:
                results.append({
                    'threshold_pct': threshold,
                    'total_breakouts': 0,
                    'wins': 0,
                    'win_rate': 0.0,
                    'avg_return': 0.0,
                    'median_return': 0.0,
                    'min_return': 0.0,
                    'max_return': 0.0,
                    'std_return': 0.0
                })
        
        # Create DataFrame
        sweep_df = pd.DataFrame(results)
        
        # Print table
        print("\nParameter Sweep Results:")
        print("=" * 80)
        print(f"{'Threshold':>10} | {'Breakouts':>10} | {'Win Rate':>10} | {'Avg Return':>12} | {'Median':>8} | {'Min':>8} | {'Max':>8}")
        print("-" * 80)
        
        for _, row in sweep_df.iterrows():
            print(f"{row['threshold_pct']:10.1f} | {row['total_breakouts']:10.0f} | {row['win_rate']:10.1f}% | {row['avg_return']:12.1f}% | {row['median_return']:8.1f}% | {row['min_return']:8.1f}% | {row['max_return']:8.1f}%")
        
        # Save to CSV if path provided
        if save_path:
            sweep_df.to_csv(save_path, index=False)
            print(f"\nParameter sweep table saved to: {save_path}")
        
        return sweep_df

    def save_table_as_image(self, df, save_path, title=None):
        """Save a DataFrame as a PNG image using matplotlib"""
        import matplotlib.pyplot as plt
        from matplotlib.table import Table
        
        fig, ax = plt.subplots(figsize=(min(20, 2 + 2*len(df.columns)), 1 + 0.5*len(df)))
        ax.axis('off')
        
        # Table title
        if title:
            plt.title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Render table
        table = ax.table(
            cellText=df.round(2).values,
            colLabels=df.columns,
            loc='center',
            cellLoc='center',
            colLoc='center',
        )
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.2)
        
        # Style header
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_fontsize(13)
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#cccccc')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Table image saved to: {save_path}")

def main():
    """Main function to run the analysis"""
    print("=" * 60)
    print("SILVER BREAKOUT ANALYSIS")
    print("=" * 60)
    print("Analyzing historical probability that:")
    print("1. Silver goes up ≥5% in one day")
    print("2. Holds above that breakout price for 2 days")
    print("3. Is higher 6 months (126 trading days) later")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SilverBreakoutAnalyzer(symbol='SI=F', start_date='2010-01-01')
    
    try:
        # Fetch data
        analyzer.fetch_data()
        
        # Identify breakouts
        breakouts = analyzer.identify_breakouts(
            threshold_pct=5.0,
            hold_days=2,
            future_days=126
        )
        
        if breakouts is not None and len(breakouts) > 0:
            # Create visualizations
            print("\n" + "=" * 60)
            print("GENERATING CHARTS...")
            print("=" * 60)
            
            # Main breakout chart
            analyzer.plot_breakouts()
            
            # Win rate by year
            analyzer.plot_win_rate_by_year()
            
            # Export results
            analyzer.export_results()
            
            print("\n" + "=" * 60)
            print("ANALYSIS COMPLETE!")
            print("=" * 60)
        else:
            print("\nNo valid breakouts found. Try adjusting the parameters:")
            print("- Lower the threshold percentage")
            print("- Reduce the hold period")
            print("- Use a different date range")
    
    except Exception as e:
        print(f"Error during analysis: {e}")
        print("Trying alternative approach...")
        
        # Try with different parameters
        try:
            analyzer = SilverBreakoutAnalyzer(symbol='SLV', start_date='2015-01-01')
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
        except Exception as e2:
            print(f"Alternative approach also failed: {e2}")

if __name__ == "__main__":
    main() 