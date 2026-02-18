#!/usr/bin/env python3
"""
AI Hedge Fund - Backtesting Module
Backtest investment strategies on historical data
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ai_hedge_fund_advanced import AIHedgeFundAdvanced, DataFetcher

@dataclass
class Trade:
    """Individual trade record"""
    date: str
    ticker: str
    action: str  # BUY, SELL
    shares: float
    price: float
    value: float
    commission: float
    reason: str

@dataclass
class PortfolioSnapshot:
    """Portfolio state at a point in time"""
    date: str
    cash: float
    positions: Dict[str, Dict]  # ticker -> {shares, value, weight}
    total_value: float
    daily_return: float
    cumulative_return: float
    benchmark_value: float
    benchmark_return: float

@dataclass
class BacktestResult:
    """Complete backtest results"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_value: float
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    benchmark_return: float
    alpha: float
    beta: float
    win_rate: float
    profit_factor: float
    num_trades: int
    trades: List[Trade]
    equity_curve: List[PortfolioSnapshot]
    monthly_returns: List[Dict]
    sector_performance: Dict[str, float]

class Backtester:
    """Backtest investment strategies"""
    
    def __init__(self, initial_capital: float = 100000, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission  # 0.1% per trade
        self.data_fetcher = DataFetcher()
    
    def run_backtest(self, tickers: List[str], 
                     start_date: str, 
                     end_date: str,
                     strategy: str = "ai_consensus",
                     rebalance_freq: str = "monthly") -> BacktestResult:
        """
        Run backtest on historical data
        
        Args:
            tickers: Universe of stocks to consider
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            strategy: "ai_consensus", "equal_weight", "momentum", "value"
            rebalance_freq: "weekly", "monthly", "quarterly"
        """
        print(f"\n📊 Running backtest: {strategy}")
        print(f"   Period: {start_date} to {end_date}")
        print(f"   Universe: {len(tickers)} stocks\n")
        
        # Fetch historical data
        price_data = self._fetch_historical_data(tickers, start_date, end_date)
        benchmark_data = self._fetch_benchmark_data(start_date, end_date)
        
        if not price_data:
            raise ValueError("Could not fetch price data")
        
        # Initialize portfolio
        portfolio = {
            'cash': self.initial_capital,
            'positions': {},  # ticker -> shares
            'value_history': []
        }
        
        trades = []
        equity_curve = []
        
        # Generate rebalance dates
        dates = self._generate_dates(start_date, end_date, rebalance_freq)
        
        # Run simulation
        for i, date in enumerate(dates):
            current_prices = self._get_prices_on_date(price_data, date)
            
            if not current_prices:
                continue
            
            # Calculate current portfolio value
            portfolio_value = self._calculate_portfolio_value(portfolio, current_prices)
            
            # Get benchmark value
            benchmark_value = benchmark_data.get(date, self.initial_capital)
            
            # Record snapshot
            snapshot = PortfolioSnapshot(
                date=date,
                cash=portfolio['cash'],
                positions=self._get_position_details(portfolio, current_prices),
                total_value=portfolio_value,
                daily_return=0,  # Will calculate later
                cumulative_return=(portfolio_value - self.initial_capital) / self.initial_capital,
                benchmark_value=benchmark_value,
                benchmark_return=(benchmark_value - self.initial_capital) / self.initial_capital
            )
            equity_curve.append(snapshot)
            
            # Rebalance on schedule
            if self._should_rebalance(date, rebalance_freq, i):
                print(f"📅 Rebalancing on {date}...", file=sys.stderr)
                
                # Get strategy signals
                if strategy == "ai_consensus":
                    signals = self._get_ai_signals(tickers, date)
                elif strategy == "equal_weight":
                    signals = {t: {'signal': 'neutral', 'weight': 1.0/len(tickers)} for t in tickers}
                elif strategy == "momentum":
                    signals = self._get_momentum_signals(price_data, tickers, date)
                elif strategy == "value":
                    signals = self._get_value_signals(tickers, date)
                else:
                    signals = {}
                
                # Execute rebalancing
                new_trades = self._rebalance_portfolio(portfolio, signals, current_prices, date)
                trades.extend(new_trades)
        
        # Calculate performance metrics
        return self._calculate_performance(equity_curve, trades, benchmark_data, strategy)
    
    def _fetch_historical_data(self, tickers: List[str], start: str, end: str) -> Dict:
        """Fetch historical price data"""
        import yfinance as yf
        
        data = {}
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(start=start, end=end)
                if not hist.empty:
                    data[ticker] = hist['Close'].to_dict()
            except Exception as e:
                print(f"Warning: Could not fetch {ticker}: {e}", file=sys.stderr)
        
        return data
    
    def _fetch_benchmark_data(self, start: str, end: str, benchmark: str = "SPY") -> Dict:
        """Fetch benchmark data (default S&P 500)"""
        import yfinance as yf
        
        try:
            spy = yf.Ticker(benchmark)
            hist = spy.history(start=start, end=end)
            
            # Normalize to initial capital
            initial_price = hist['Close'].iloc[0]
            shares = self.initial_capital / initial_price
            
            return {
                date.strftime('%Y-%m-%d'): price * shares 
                for date, price in hist['Close'].items()
            }
        except Exception as e:
            print(f"Warning: Could not fetch benchmark: {e}", file=sys.stderr)
            return {}
    
    def _generate_dates(self, start: str, end: str, freq: str) -> List[str]:
        """Generate trading dates"""
        dates = pd.date_range(start=start, end=end, freq='B')  # Business days
        return [d.strftime('%Y-%m-%d') for d in dates]
    
    def _should_rebalance(self, date: str, freq: str, index: int) -> bool:
        """Check if should rebalance on this date"""
        if index == 0:
            return True  # Initial allocation
        
        # Simple logic: rebalance on first day of period
        if freq == "monthly":
            return date.endswith('-01')
        elif freq == "weekly":
            return index % 5 == 0
        elif freq == "quarterly":
            return date.endswith('-01') and date[5:7] in ['01', '04', '07', '10']
        
        return False
    
    def _get_ai_signals(self, tickers: List[str], date: str) -> Dict:
        """Get AI consensus signals for all tickers"""
        hedge_fund = AIHedgeFundAdvanced(use_subagents=False)
        signals = {}
        
        for ticker in tickers[:5]:  # Limit to avoid rate limits
            try:
                result = hedge_fund.analyze(ticker)
                
                # Convert signal to weight
                if result.signal == "bullish":
                    weight = 0.15 + (result.confidence / 100) * 0.10  # 15-25%
                elif result.signal == "neutral":
                    weight = 0.05
                else:
                    weight = 0
                
                signals[ticker] = {
                    'signal': result.signal,
                    'confidence': result.confidence,
                    'weight': weight
                }
            except:
                signals[ticker] = {'signal': 'neutral', 'weight': 0.05}
        
        # Normalize weights
        total_weight = sum(s['weight'] for s in signals.values())
        if total_weight > 0:
            for ticker in signals:
                signals[ticker]['weight'] /= total_weight
        
        return signals
    
    def _get_momentum_signals(self, price_data: Dict, tickers: List[str], date: str) -> Dict:
        """Get momentum-based signals"""
        signals = {}
        
        for ticker in tickers:
            if ticker not in price_data:
                continue
            
            prices = price_data[ticker]
            dates = sorted(prices.keys())
            
            if len(dates) < 60:
                continue
            
            # Calculate 3-month and 6-month returns
            current_idx = dates.index(date) if date in dates else len(dates) - 1
            if current_idx < 60:
                continue
            
            current_price = prices[dates[current_idx]]
            price_3m = prices[dates[current_idx - 63]]  # ~3 months
            price_6m = prices[dates[current_idx - 126]]  # ~6 months
            
            ret_3m = (current_price - price_3m) / price_3m
            ret_6m = (current_price - price_6m) / price_6m
            
            # Momentum score
            momentum = ret_3m * 0.6 + ret_6m * 0.4
            
            signals[ticker] = {
                'signal': 'bullish' if momentum > 0.05 else 'bearish' if momentum < -0.05 else 'neutral',
                'weight': max(0, momentum + 0.1)  # Shift to positive
            }
        
        # Normalize
        total = sum(s['weight'] for s in signals.values())
        if total > 0:
            for t in signals:
                signals[t]['weight'] /= total
        
        return signals
    
    def _get_value_signals(self, tickers: List[str], date: str) -> Dict:
        """Get value-based signals (simplified)"""
        signals = {}
        
        for ticker in tickers:
            try:
                data = self.data_fetcher.get_comprehensive_data(ticker)
                pe = data.get('pe_ratio', 0) or 100
                pb = data.get('pb_ratio', 0) or 10
                
                # Value score (lower is better)
                value_score = (1 / (pe + 1)) * 0.5 + (1 / (pb + 1)) * 0.5
                
                signals[ticker] = {
                    'signal': 'bullish' if pe < 15 else 'neutral',
                    'weight': value_score
                }
            except:
                signals[ticker] = {'signal': 'neutral', 'weight': 0.05}
        
        # Normalize
        total = sum(s['weight'] for s in signals.values())
        if total > 0:
            for t in signals:
                signals[t]['weight'] /= total
        
        return signals
    
    def _rebalance_portfolio(self, portfolio: Dict, signals: Dict, 
                            prices: Dict, date: str) -> List[Trade]:
        """Execute portfolio rebalancing"""
        trades = []
        
        # Calculate current values
        total_value = portfolio['cash']
        for ticker, shares in portfolio['positions'].items():
            if ticker in prices:
                total_value += shares * prices[ticker]
        
        # Calculate target allocations
        target_allocations = {}
        for ticker, signal in signals.items():
            if signal['weight'] > 0 and ticker in prices:
                target_allocations[ticker] = signal['weight']
        
        # Sell positions that are no longer in signals
        for ticker in list(portfolio['positions'].keys()):
            if ticker not in target_allocations and ticker in prices:
                shares = portfolio['positions'][ticker]
                price = prices[ticker]
                value = shares * price
                commission = value * self.commission
                
                portfolio['cash'] += value - commission
                del portfolio['positions'][ticker]
                
                trades.append(Trade(
                    date=date, ticker=ticker, action='SELL',
                    shares=shares, price=price, value=value,
                    commission=commission, reason='Not in target allocation'
                ))
        
        # Buy target allocations
        for ticker, target_weight in target_allocations.items():
            if ticker not in prices:
                continue
            
            target_value = total_value * target_weight
            current_shares = portfolio['positions'].get(ticker, 0)
            current_value = current_shares * prices[ticker]
            
            value_diff = target_value - current_value
            
            # Only trade if significant difference (>1%)
            if abs(value_diff) > total_value * 0.01:
                if value_diff > 0:  # Buy
                    price = prices[ticker]
                    shares_to_buy = value_diff / price
                    commission = value_diff * self.commission
                    
                    if portfolio['cash'] >= value_diff + commission:
                        portfolio['positions'][ticker] = current_shares + shares_to_buy
                        portfolio['cash'] -= value_diff + commission
                        
                        trades.append(Trade(
                            date=date, ticker=ticker, action='BUY',
                            shares=shares_to_buy, price=price, value=value_diff,
                            commission=commission, reason=f'Target weight {target_weight:.1%}'
                        ))
                else:  # Sell
                    price = prices[ticker]
                    shares_to_sell = abs(value_diff) / price
                    commission = abs(value_diff) * self.commission
                    
                    if current_shares >= shares_to_sell:
                        portfolio['positions'][ticker] = current_shares - shares_to_sell
                        if portfolio['positions'][ticker] < 0.001:
                            del portfolio['positions'][ticker]
                        portfolio['cash'] += abs(value_diff) - commission
                        
                        trades.append(Trade(
                            date=date, ticker=ticker, action='SELL',
                            shares=shares_to_sell, price=price, value=abs(value_diff),
                            commission=commission, reason='Rebalancing'
                        ))
        
        return trades
    
    def _calculate_portfolio_value(self, portfolio: Dict, prices: Dict) -> float:
        """Calculate total portfolio value"""
        value = portfolio['cash']
        for ticker, shares in portfolio['positions'].items():
            if ticker in prices:
                value += shares * prices[ticker]
        return value
    
    def _get_prices_on_date(self, price_data: Dict, date: str) -> Dict:
        """Get all prices on a specific date"""
        prices = {}
        for ticker, data in price_data.items():
            # Find closest date
            if date in data:
                prices[ticker] = data[date]
            else:
                # Find nearest previous date
                dates = sorted(data.keys())
                for d in reversed(dates):
                    if d <= date:
                        prices[ticker] = data[d]
                        break
        return prices
    
    def _get_position_details(self, portfolio: Dict, prices: Dict) -> Dict:
        """Get detailed position information"""
        details = {}
        for ticker, shares in portfolio['positions'].items():
            if ticker in prices:
                value = shares * prices[ticker]
                details[ticker] = {
                    'shares': shares,
                    'value': value,
                    'weight': 0  # Will calculate later
                }
        return details
    
    def _calculate_performance(self, equity_curve: List[PortfolioSnapshot], 
                              trades: List[Trade],
                              benchmark_data: Dict,
                              strategy: str) -> BacktestResult:
        """Calculate performance metrics"""
        
        if not equity_curve:
            raise ValueError("No equity curve data")
        
        # Calculate daily returns
        values = [s.total_value for s in equity_curve]
        daily_returns = [(values[i] - values[i-1]) / values[i-1] 
                        for i in range(1, len(values))]
        
        # Basic metrics
        final_value = values[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital
        
        # Annualized return
        num_years = len(equity_curve) / 252  # Trading days
        annualized_return = (final_value / self.initial_capital) ** (1/num_years) - 1 if num_years > 0 else 0
        
        # Volatility
        volatility = np.std(daily_returns) * np.sqrt(252) if daily_returns else 0
        
        # Sharpe ratio
        sharpe = (annualized_return - 0.04) / volatility if volatility > 0 else 0
        
        # Max drawdown
        cumulative = [1 + r for r in np.cumsum(daily_returns)] if daily_returns else [1]
        running_max = np.maximum.accumulate(cumulative)
        drawdowns = [(c - m) / m for c, m in zip(cumulative, running_max)]
        max_drawdown = min(drawdowns) if drawdowns else 0
        
        # Benchmark comparison
        if benchmark_data:
            benchmark_values = list(benchmark_data.values())
            if len(benchmark_values) >= 2:
                benchmark_return = (benchmark_values[-1] - benchmark_values[0]) / benchmark_values[0]
            else:
                benchmark_return = 0
        else:
            benchmark_return = 0
        
        # Alpha and Beta (simplified)
        alpha = annualized_return - (0.04 + 1.0 * (benchmark_return - 0.04))
        beta = 1.0  # Simplified
        
        # Win rate
        winning_trades = [t for t in trades if t.action == 'SELL' and t.value > t.shares * t.price * 0.99]
        win_rate = len(winning_trades) / len([t for t in trades if t.action == 'SELL']) if trades else 0
        
        # Profit factor
        gross_profit = sum(t.value for t in trades if t.action == 'SELL')
        gross_loss = sum(t.value for t in trades if t.action == 'BUY')
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        return BacktestResult(
            strategy_name=strategy,
            start_date=equity_curve[0].date,
            end_date=equity_curve[-1].date,
            initial_capital=self.initial_capital,
            final_value=final_value,
            total_return=total_return,
            annualized_return=annualized_return,
            volatility=volatility,
            sharpe_ratio=sharpe,
            max_drawdown=max_drawdown,
            benchmark_return=benchmark_return,
            alpha=alpha,
            beta=beta,
            win_rate=win_rate,
            profit_factor=profit_factor,
            num_trades=len(trades),
            trades=trades,
            equity_curve=equity_curve,
            monthly_returns=[],  # TODO
            sector_performance={}  # TODO
        )

def format_backtest_report(result: BacktestResult) -> str:
    """Format backtest results for display"""
    lines = [
        f"\n{'='*80}",
        f"📊 Backtest Results: {result.strategy_name}",
        f"{'='*80}",
        f"Period: {result.start_date} to {result.end_date}",
        "",
        "💰 Performance Summary:",
        "-" * 40,
        f"  Initial Capital:        ${result.initial_capital:,.0f}",
        f"  Final Value:            ${result.final_value:,.0f}",
        f"  Total Return:           {result.total_return:>8.1%}",
        f"  Annualized Return:      {result.annualized_return:>8.1%}",
        f"  Benchmark Return:       {result.benchmark_return:>8.1%}",
        "",
        "📈 Risk Metrics:",
        "-" * 40,
        f"  Volatility:             {result.volatility:>8.1%}",
        f"  Sharpe Ratio:           {result.sharpe_ratio:>8.2f}",
        f"  Max Drawdown:           {result.max_drawdown:>8.1%}",
        f"  Alpha:                  {result.alpha:>8.1%}",
        f"  Beta:                   {result.beta:>8.2f}",
        "",
        "🔄 Trading Statistics:",
        "-" * 40,
        f"  Total Trades:           {result.num_trades}",
        f"  Win Rate:               {result.win_rate:>8.1%}",
        f"  Profit Factor:          {result.profit_factor:>8.2f}",
        ""
    ]
    
    # Recent trades
    if result.trades:
        lines.extend([
            "📋 Recent Trades:",
            "-" * 80,
            f"{'Date':<12} {'Ticker':<8} {'Action':<6} {'Shares':>10} {'Price':>10} {'Value':>12}"
        ])
        for trade in result.trades[-10:]:
            lines.append(
                f"{trade.date:<12} {trade.ticker:<8} {trade.action:<6} "
                f"{trade.shares:>10.2f} ${trade.price:>9.2f} ${trade.value:>11,.0f}"
            )
        lines.append("")
    
    lines.append(f"{'='*80}\n")
    
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Hedge Fund - Backtest")
    parser.add_argument("tickers", help="Comma-separated stock tickers")
    parser.add_argument("--start", "-s", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", "-e", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--strategy", "-st", default="ai_consensus",
                       choices=["ai_consensus", "equal_weight", "momentum", "value"],
                       help="Strategy to backtest")
    parser.add_argument("--rebalance", "-r", default="monthly",
                       choices=["weekly", "monthly", "quarterly"],
                       help="Rebalancing frequency")
    parser.add_argument("--capital", "-c", type=float, default=100000,
                       help="Initial capital")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    tickers = [t.strip().upper() for t in args.tickers.split(",")]
    
    backtester = Backtester(initial_capital=args.capital)
    
    try:
        result = backtester.run_backtest(
            tickers=tickers,
            start_date=args.start,
            end_date=args.end,
            strategy=args.strategy,
            rebalance_freq=args.rebalance
        )
        
        if args.json:
            # Convert to dict for JSON
            result_dict = {
                "strategy": result.strategy_name,
                "period": {"start": result.start_date, "end": result.end_date},
                "performance": {
                    "initial_capital": result.initial_capital,
                    "final_value": result.final_value,
                    "total_return": result.total_return,
                    "annualized_return": result.annualized_return,
                    "benchmark_return": result.benchmark_return
                },
                "risk": {
                    "volatility": result.volatility,
                    "sharpe_ratio": result.sharpe_ratio,
                    "max_drawdown": result.max_drawdown,
                    "alpha": result.alpha,
                    "beta": result.beta
                },
                "trading": {
                    "num_trades": result.num_trades,
                    "win_rate": result.win_rate,
                    "profit_factor": result.profit_factor
                }
            }
            print(json.dumps(result_dict, indent=2))
        else:
            print(format_backtest_report(result))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()