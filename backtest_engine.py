#!/usr/bin/env python3
"""
历史回测引擎 - 验证大师策略有效性

⚠️ 重要免责声明 / IMPORTANT DISCLAIMER:

本回测引擎存在以下局限性，结果仅供参考，不构成投资建议：

1. 【前视偏差风险 Look-ahead Bias】
   - 当前实现使用AI基于历史数据"重新生成"信号
   - 并非真实的历史信号回放，存在信息泄露风险
   - 实际历史表现可能与回测结果存在显著差异

2. 【模拟信号非真实策略】
   - 大师"策略"本质是基于当前AI模型的模拟
   - 无法复现大师在真实历史环境中的决策过程
   - 无法考虑当时的信息环境、情绪、流动性等因素

3. 【过拟合风险】
   - 基于历史数据优化的参数可能在未来失效
   - 市场环境变化可能导致策略表现急剧恶化

4. 【数据质量限制】
   - 使用简化模拟数据或单一数据源
   - 未考虑交易滑点、手续费、流动性冲击等

建议：将此回测作为"概念验证"和"框架测试"工具，
      而非绩效评估依据。真实投资决策需结合更多因素。

功能:
- 用2015-2025历史数据验证每位大师
- 计算胜率、夏普比率、最大回撤
- 对比不同大师在同一时期的表现
- 生成回测报告
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import os


@dataclass
class Trade:
    """单笔交易记录"""
    entry_date: datetime
    exit_date: Optional[datetime]
    symbol: str
    entry_price: float
    exit_price: Optional[float]
    signal: str  # bullish/bearish
    confidence: int
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None


@dataclass
class BacktestResult:
    """回测结果"""
    master_name: str
    start_date: str
    end_date: str
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    avg_return: float
    total_return: float
    annualized_return: float
    sharpe_ratio: float
    max_drawdown: float
    max_drawdown_duration: int
    trades: List[Trade]
    equity_curve: List[Tuple[str, float]]  # (date, equity)


class HistoricalDataLoader:
    """
    历史数据加载器
    从OKX获取历史K线数据
    """
    
    def __init__(self, data_dir: str = "./historical_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def load_data(self, symbol: str, start: str, end: str, 
                  timeframe: str = "1D") -> Optional[pd.DataFrame]:
        """
        加载历史数据
        
        Args:
            symbol: 标的代码
            start: 开始日期 (YYYY-MM-DD)
            end: 结束日期 (YYYY-MM-DD)
            timeframe: 时间周期
        """
        # 检查本地缓存
        cache_file = f"{self.data_dir}/{symbol}_{timeframe}_{start}_{end}.csv"
        
        if os.path.exists(cache_file):
            print(f"📂 从缓存加载: {symbol}")
            return pd.read_csv(cache_file, parse_dates=['timestamp'])
        
        # 从API获取 (简化版，实际应该调用OKX API)
        print(f"🌐 从API获取: {symbol}")
        df = self._fetch_from_api(symbol, start, end, timeframe)
        
        if df is not None:
            df.to_csv(cache_file, index=False)
        
        return df
    
    def _fetch_from_api(self, symbol: str, start: str, end: str, 
                        timeframe: str) -> Optional[pd.DataFrame]:
        """从OKX API获取历史数据"""
        # 这里简化处理，实际应该调用OKX的history-candles接口
        # 需要处理分页、限流等
        
        # 模拟数据生成 (用于测试)
        dates = pd.date_range(start=start, end=end, freq='D')
        np.random.seed(42)
        
        data = {
            'timestamp': dates,
            'open': 100 + np.random.randn(len(dates)).cumsum(),
            'high': 100 + np.random.randn(len(dates)).cumsum() + 5,
            'low': 100 + np.random.randn(len(dates)).cumsum() - 5,
            'close': 100 + np.random.randn(len(dates)).cumsum(),
            'volume': np.random.randint(1000000, 10000000, len(dates))
        }
        
        return pd.DataFrame(data)


class MasterBacktest:
    """
    大师策略回测引擎
    """
    
    def __init__(self):
        self.data_loader = HistoricalDataLoader()
        self.initial_capital = 100000  # 初始资金
    
    def run(self, master_name: str, symbol: str, 
            start: str, end: str, timeframe: str = "1D") -> BacktestResult:
        """
        运行单大师回测
        
        示例:
            result = backtest.run("buffett", "AAPL", "2020-01", "2024-12")
        """
        print(f"\n🔄 回测: {master_name} | {symbol} | {start} ~ {end}")
        
        # 加载数据
        df = self.data_loader.load_data(symbol, start, end, timeframe)
        if df is None or df.empty:
            raise ValueError(f"无法获取数据: {symbol}")
        
        # 加载大师模型
        master = self._load_master(master_name)
        if not master:
            raise ValueError(f"未知大师: {master_name}")
        
        # 运行回测
        trades = []
        equity = self.initial_capital
        equity_curve = [(df.iloc[0]['timestamp'].strftime('%Y-%m-%d'), equity)]
        
        position = None  # 当前持仓
        
        for i in range(20, len(df)):  # 从第20根开始，确保有足够历史数据
            current = df.iloc[i]
            history = df.iloc[:i+1]
            
            # 构建分析数据
            data = self._prepare_data(history)
            
            # 获取大师信号
            signal = master.analyze(data)
            
            # 交易逻辑
            if signal['signal'] == 'bullish' and position is None:
                # 买入
                position = Trade(
                    entry_date=current['timestamp'],
                    exit_date=None,
                    symbol=symbol,
                    entry_price=current['close'],
                    exit_price=None,
                    signal='bullish',
                    confidence=signal['confidence']
                )
                
            elif signal['signal'] == 'bearish' and position is not None:
                # 卖出
                position.exit_date = current['timestamp']
                position.exit_price = current['close']
                position.pnl = (position.exit_price - position.entry_price)
                position.pnl_pct = position.pnl / position.entry_price * 100
                
                # 更新权益
                equity *= (1 + position.pnl_pct / 100)
                equity_curve.append((current['timestamp'].strftime('%Y-%m-%d'), equity))
                
                trades.append(position)
                position = None
        
        # 关闭最后一笔持仓
        if position is not None:
            position.exit_date = df.iloc[-1]['timestamp']
            position.exit_price = df.iloc[-1]['close']
            position.pnl = (position.exit_price - position.entry_price)
            position.pnl_pct = position.pnl / position.entry_price * 100
            
            equity *= (1 + position.pnl_pct / 100)
            trades.append(position)
        
        # 计算回测指标
        return self._calculate_metrics(master_name, start, end, trades, equity_curve)
    
    def _load_master(self, master_name: str):
        """加载大师模型"""
        # 简化版，实际应该动态导入
        # 这里返回模拟的大师类
        
        class MockMaster:
            def analyze(self, data):
                # 简单的移动均线策略作为示例
                if len(data) < 20:
                    return {'signal': 'neutral', 'confidence': 50}
                
                ma20 = sum([d['close'] for d in data[-20:]]) / 20
                ma60 = sum([d['close'] for d in data[-60:]]) / 60 if len(data) >= 60 else ma20
                
                if ma20 > ma60 * 1.02:  # 多头排列
                    return {'signal': 'bullish', 'confidence': 70}
                elif ma20 < ma60 * 0.98:  # 空头排列
                    return {'signal': 'bearish', 'confidence': 70}
                else:
                    return {'signal': 'neutral', 'confidence': 50}
        
        return MockMaster()
    
    def _prepare_data(self, df: pd.DataFrame) -> Dict:
        """准备分析数据"""
        data = []
        for _, row in df.iterrows():
            data.append({
                'timestamp': row['timestamp'],
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            })
        return {'price_history': data, 'current': data[-1]}
    
    def _calculate_metrics(self, master_name: str, start: str, end: str,
                          trades: List[Trade], equity_curve: List) -> BacktestResult:
        """计算回测指标"""
        
        if not trades:
            return BacktestResult(
                master_name=master_name,
                start_date=start,
                end_date=end,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0,
                avg_return=0,
                total_return=0,
                annualized_return=0,
                sharpe_ratio=0,
                max_drawdown=0,
                max_drawdown_duration=0,
                trades=[],
                equity_curve=equity_curve
            )
        
        winning_trades = [t for t in trades if t.pnl and t.pnl > 0]
        losing_trades = [t for t in trades if t.pnl and t.pnl <= 0]
        
        returns = [t.pnl_pct for t in trades if t.pnl_pct is not None]
        
        # 计算最大回撤
        max_drawdown = 0
        max_drawdown_duration = 0
        peak = equity_curve[0][1]
        peak_date = equity_curve[0][0]
        
        for date, equity in equity_curve:
            if equity > peak:
                peak = equity
                peak_date = date
            
            drawdown = (peak - equity) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                # 计算回撤持续时间
                max_drawdown_duration = (datetime.strptime(date, '%Y-%m-%d') - 
                                        datetime.strptime(peak_date, '%Y-%m-%d')).days
        
        # 年化收益
        start_date = datetime.strptime(start, '%Y-%m')
        end_date = datetime.strptime(end, '%Y-%m')
        years = (end_date - start_date).days / 365.25
        
        final_equity = equity_curve[-1][1]
        total_return = (final_equity - self.initial_capital) / self.initial_capital
        annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 夏普比率 (简化版)
        if returns:
            avg_return = np.mean(returns)
            std_return = np.std(returns)
            sharpe_ratio = (avg_return / std_return) * np.sqrt(252) if std_return > 0 else 0
        else:
            avg_return = 0
            sharpe_ratio = 0
        
        return BacktestResult(
            master_name=master_name,
            start_date=start,
            end_date=end,
            total_trades=len(trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            win_rate=len(winning_trades) / len(trades) * 100 if trades else 0,
            avg_return=avg_return,
            total_return=total_return * 100,
            annualized_return=annualized_return * 100,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown * 100,
            max_drawdown_duration=max_drawdown_duration,
            trades=trades,
            equity_curve=equity_curve
        )
    
    def compare_masters(self, masters: List[str], symbol: str, 
                        start: str, end: str) -> Dict[str, BacktestResult]:
        """
        对比多位大师
        
        示例:
            results = backtest.compare_masters(
                ["buffett", "wood", "dalio"], 
                "NVDA", 
                "2020-01", 
                "2024-12"
            )
        """
        results = {}
        
        for master in masters:
            try:
                result = self.run(master, symbol, start, end)
                results[master] = result
            except Exception as e:
                print(f"⚠️  {master} 回测失败: {e}")
        
        return results
    
    def generate_report(self, result: BacktestResult) -> str:
        """生成回测报告"""
        report = f"""
{'='*60}
📊 {result.master_name} 回测报告
{'='*60}
回测区间: {result.start_date} ~ {result.end_date}

📈 收益指标
  总收益率: {result.total_return:+.2f}%
  年化收益: {result.annualized_return:+.2f}%
  夏普比率: {result.sharpe_ratio:.2f}

📉 风险指标
  最大回撤: {result.max_drawdown:.2f}%
  回撤天数: {result.max_drawdown_duration}天

🎯 交易统计
  总交易数: {result.total_trades}
  盈利交易: {result.winning_trades}
  亏损交易: {result.losing_trades}
  胜率: {result.win_rate:.1f}%
  平均收益: {result.avg_return:.2f}%

{'='*60}
"""
        return report


def run_backtest(master: str, symbol: str, start: str, end: str):
    """便捷函数：运行单次回测"""
    engine = MasterBacktest()
    result = engine.run(master, symbol, start, end)
    print(engine.generate_report(result))
    return result


def compare_masters(masters: List[str], symbol: str, start: str, end: str):
    """便捷函数：对比多位大师"""
    engine = MasterBacktest()
    results = engine.compare_masters(masters, symbol, start, end)
    
    # 排名
    print(f"\n🏆 大师排名: {symbol} | {start} ~ {end}")
    print("="*60)
    
    sorted_results = sorted(
        results.items(), 
        key=lambda x: x[1].annualized_return, 
        reverse=True
    )
    
    for i, (master, result) in enumerate(sorted_results, 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
        print(f"{medal} {master:20} | 年化: {result.annualized_return:+6.1f}% | "
              f"最大回撤: {result.max_drawdown:5.1f}% | 胜率: {result.win_rate:4.1f}%")


if __name__ == "__main__":
    # 测试
    print("🧪 回测引擎测试")
    
    # 单大师回测
    # run_backtest("buffett", "AAPL", "2020-01", "2024-12")
    
    # 多大师对比
    compare_masters(
        ["buffett", "wood", "dalio", "druckenmiller"],
        "NVDA",
        "2020-01",
        "2024-12"
    )
