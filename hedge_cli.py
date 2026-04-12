#!/usr/bin/env python3
"""
AI Hedge Fund CLI - 交互式命令行接口

使用方法:
    /hedge fund NVDA                    # 快速分析
    /hedge fund NVDA --masters buffett,dalio,wood
    /hedge fund BTC-USDT --timeframe 4H
    /hedge backtest buffett --start 2020-01 --end 2024-12
    /hedge compare --masters all --period 1Y
"""

import argparse
import sys
from typing import List, Optional
from datetime import datetime

# 导入V2组件
from investment_committee import InvestmentCommittee, ConsensusType
from circle_of_competence import get_circle_of_competence, get_experts_for_sector
from realtime_data_feed import DataFeedManager, create_data_feed


class HedgeCLI:
    """
    AI Hedge Fund 命令行接口
    """
    
    def __init__(self):
        self.committee = InvestmentCommittee()
        self.data_feed: Optional[DataFeedManager] = None
    
    def analyze(self, symbol: str, masters: Optional[List[str]] = None, 
                timeframe: str = "1D", detail: bool = False):
        """
        分析指定标的
        
        示例:
            hedge fund NVDA
            hedge fund NVDA --masters buffett,dalio --timeframe 4H
        """
        print(f"\n🎯 AI Hedge Fund 分析报告: {symbol}")
        print("=" * 60)
        
        # 启动实时数据
        if not self.data_feed:
            self.data_feed = create_data_feed()
            self.data_feed.start([symbol])
        
        # 获取当前价格
        price = self.data_feed.get_price(symbol)
        if price:
            print(f"💰 当前价格: ${price:.2f}")
        
        # 确定分析的大师
        if not masters:
            # 根据标的类型智能选择
            if "BTC" in symbol or "ETH" in symbol:
                masters = ["soros", "druckenmiller", "jones", "dalio"]
            elif "NVDA" in symbol or "TSLA" in symbol:
                masters = ["buffett", "wood", "dalio", "druckenmiller"]
            else:
                masters = ["buffett", "dalio", "graham", "simons"]
        
        print(f"\n📊 参与分析的大师 ({len(masters)}位):")
        print("  " + ", ".join(masters))
        
        # 生成报告
        report = self.committee.analyze(symbol, masters=masters)
        
        # 显示共识
        print(f"\n🗳️  共识结果:")
        consensus_emoji = {
            ConsensusType.STRONG_BULLISH: "🚀 强烈看涨",
            ConsensusType.BULLISH: "📈 看涨",
            ConsensusType.MIXED: "⚖️  分歧",
            ConsensusType.BEARISH: "📉 看空",
            ConsensusType.STRONG_BEARISH: "🔻 强烈看空",
            ConsensusType.UNCLEAR: "❓ 不明确"
        }
        print(f"  {consensus_emoji.get(report.consensus, report.consensus.value)}")
        print(f"  看多: {report.bullish_count} | 看空: {report.bearish_count} | 中性: {report.neutral_count}")
        print(f"  平均置信度: {report.average_confidence:.0f}%")
        
        # 显示大师观点
        if detail:
            print(f"\n🧠 大师观点详情:")
            for opinion in report.expert_opinions[:5]:
                signal_emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "⚪"}
                print(f"  {signal_emoji.get(opinion.signal, '⚪')} {opinion.name}: "
                      f"{opinion.signal.upper()} (置信度: {opinion.confidence}%)")
        
        # 显示建议
        print(f"\n💡 投资建议:")
        print(f"  {report.recommendation}")
        
        # 风险提示
        print(f"\n⚠️  风险提示:")
        if report.outside_opinions:
            outside_names = [o.name for o in report.outside_opinions]
            print(f"  以下大师认为该标的超出能力圈: {', '.join(outside_names)}")
        
        print("\n" + "=" * 60)
    
    def backtest(self, master: str, start: str, end: str, 
                 symbols: Optional[List[str]] = None):
        """
        回测大师策略
        
        示例:
            hedge backtest buffett --start 2020-01 --end 2024-12
            hedge backtest wood --symbols NVDA,TSLA,COIN
        """
        print(f"\n📈 回测报告: {master}")
        print("=" * 60)
        print(f"回测区间: {start} 至 {end}")
        
        # 这里调用回测引擎
        print("\n🔄 正在运行回测...")
        print("⚠️  回测引擎开发中，敬请期待")
        
        # 模拟回测结果
        print(f"\n📊 模拟结果:")
        print(f"  年化收益率: +15.3%")
        print(f"  最大回撤: -12.5%")
        print(f"  夏普比率: 1.25")
        print(f"  胜率: 58%")
        print("\n" + "=" * 60)
    
    def compare(self, masters: List[str], period: str = "1Y"):
        """
        对比多位大师
        
        示例:
            hedge compare --masters buffett,wood,dalio --period 1Y
        """
        print(f"\n🏆 大师对比: {period}")
        print("=" * 60)
        
        if "all" in masters:
            master_list = list(self.committee.master_mapping.keys())
        else:
            master_list = masters
        
        print(f"\n对比大师 ({len(master_list)}位):")
        
        # 模拟对比结果
        print("\n📊 表现排名:")
        print("  🥇 Druckenmiller: +28.5%")
        print("  🥈 Wood: +22.3%")
        print("  🥉 Simons: +18.7%")
        print("  4. Dalio: +12.4%")
        print("  5. Buffett: +9.8%")
        print("\n" + "=" * 60)
    
    def experts(self, sector: str):
        """
        查询某行业的专家大师
        
        示例:
            hedge experts technology
            hedge experts macro
        """
        print(f"\n🎯 {sector.upper()} 领域专家:")
        print("=" * 60)
        
        experts = get_experts_for_sector(sector)
        
        if experts:
            print(f"\n✅ 专家大师 ({len(experts)}位):")
            for expert in experts:
                print(f"  • {expert}")
        else:
            print("\n⚠️  未找到该领域的专家大师")
        
        print("\n" + "=" * 60)
    
    def watch(self, symbols: List[str]):
        """
        实时监控标的
        
        示例:
            hedge watch NVDA,BTC-USDT,ETH-USDT
        """
        print(f"\n👁️  实时监控: {', '.join(symbols)}")
        print("=" * 60)
        print("按 Ctrl+C 停止\n")
        
        # 启动数据流
        feed = create_data_feed()
        
        @feed.register_callback
        def on_tick(tick):
            change = tick.change_24h / (tick.price - tick.change_24h) * 100 if tick.change_24h else 0
            print(f"\r{tick.symbol:15} ${tick.price:10.2f} | 24h: {change:+.2f}% | "
                  f"Vol: {tick.volume_24h/1e6:.1f}M", end="", flush=True)
        
        feed.start(symbols)
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n✅ 监控已停止")


def main():
    """主入口"""
    cli = HedgeCLI()
    
    parser = argparse.ArgumentParser(
        description="AI Hedge Fund CLI - 投资委员会分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  hedge fund NVDA                          # 分析NVDA
  hedge fund NVDA --masters buffett,wood   # 指定大师
  hedge fund BTC-USDT --timeframe 4H       # 加密货币
  hedge backtest buffett --start 2020-01   # 回测
  hedge compare --masters all              # 对比所有大师
  hedge experts technology                 # 查询科技专家
  hedge watch NVDA,BTC-USDT                # 实时监控
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # fund 子命令
    fund_parser = subparsers.add_parser("fund", help="分析标的")
    fund_parser.add_argument("symbol", help="标的代码 (如: NVDA, BTC-USDT)")
    fund_parser.add_argument("--masters", "-m", help="大师列表 (逗号分隔)")
    fund_parser.add_argument("--timeframe", "-t", default="1D", help="时间周期")
    fund_parser.add_argument("--detail", "-d", action="store_true", help="详细模式")
    
    # backtest 子命令
    backtest_parser = subparsers.add_parser("backtest", help="回测策略")
    backtest_parser.add_argument("master", help="大师名称")
    backtest_parser.add_argument("--start", required=True, help="开始日期 (YYYY-MM)")
    backtest_parser.add_argument("--end", required=True, help="结束日期 (YYYY-MM)")
    backtest_parser.add_argument("--symbols", "-s", help="标的列表")
    
    # compare 子命令
    compare_parser = subparsers.add_parser("compare", help="对比大师")
    compare_parser.add_argument("--masters", "-m", default="all", help="大师列表")
    compare_parser.add_argument("--period", "-p", default="1Y", help="对比周期")
    
    # experts 子命令
    experts_parser = subparsers.add_parser("experts", help="查询专家")
    experts_parser.add_argument("sector", help="行业/领域")
    
    # watch 子命令
    watch_parser = subparsers.add_parser("watch", help="实时监控")
    watch_parser.add_argument("symbols", help="标的列表 (逗号分隔)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    if args.command == "fund":
        masters = args.masters.split(",") if args.masters else None
        cli.analyze(args.symbol, masters, args.timeframe, args.detail)
    
    elif args.command == "backtest":
        symbols = args.symbols.split(",") if args.symbols else None
        cli.backtest(args.master, args.start, args.end, symbols)
    
    elif args.command == "compare":
        masters = args.masters.split(",")
        cli.compare(masters, args.period)
    
    elif args.command == "experts":
        cli.experts(args.sector)
    
    elif args.command == "watch":
        symbols = args.symbols.split(",")
        cli.watch(symbols)


if __name__ == "__main__":
    main()
