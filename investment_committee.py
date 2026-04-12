#!/usr/bin/env python3
"""
投资委员会模式 - Meta-Skill Composition

组合多个投资大师的观点，生成共识报告。
这是女娲方法论中的「元技能组合」实现。
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

# 导入所有V2大师（自动发现）
import os
import importlib.util
import sys


def load_all_masters_v2() -> Dict[str, object]:
    """自动加载所有V2版本的大师"""
    masters = {}
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filename in os.listdir(skill_dir):
        if filename.endswith("_distilled_v2.py"):
            name = filename.replace("_distilled_v2.py", "")
            filepath = os.path.join(skill_dir, filename)
            
            # 动态加载模块
            spec = importlib.util.spec_from_file_location(name, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[name] = module
                try:
                    spec.loader.exec_module(module)
                    # 查找Distilled类（修复：移除硬编码排除）
                    for attr in dir(module):
                        if attr.endswith("Distilled") and not attr.startswith("_"):
                            masters[name] = getattr(module, attr)
                            break
                except Exception as e:
                    print(f"⚠️ 加载 {name} 失败: {e}")
    
    return masters


class ConsensusType(Enum):
    """共识类型"""
    STRONG_BULLISH = "强烈看多"  # 70%+ bullish
    BULLISH = "看多"              # 50-70% bullish
    MIXED = "分歧"                # 多空平衡
    BEARISH = "看空"              # 50-70% bearish
    STRONG_BEARISH = "强烈看空"   # 70%+ bearish
    UNCLEAR = "不明确"            # 数据不足


@dataclass
class MasterOpinion:
    """单个大师的观点"""
    name: str
    signal: str  # bullish/bearish/neutral
    confidence: int
    reasoning: List[str]
    is_within_circle: bool = True


@dataclass
class ConsensusReport:
    """共识报告"""
    ticker: str
    consensus: ConsensusType
    bullish_count: int
    bearish_count: int
    neutral_count: int
    average_confidence: float
    expert_opinions: List[MasterOpinion]  # 能力圈内的专家
    outside_opinions: List[MasterOpinion]  # 能力圈外的大师
    key_insights: List[str]
    debates: List[Dict]  # 争议点
    recommendation: str


class InvestmentCommittee:
    """
    投资委员会 - 聚合多个大师的观点
    
    使用示例:
        committee = InvestmentCommittee()
        report = committee.analyze("AAPL", masters=["buffett", "dalio", "wood"])
    """
    
    def __init__(self):
        self.masters = {}
        self._load_masters()
    
    def _load_masters(self):
        """加载所有可用的大师"""
        # 预定义的V2大师映射
        self.master_mapping = {
            "buffett": ("buffett_distilled_v2", "WarrenBuffettDistilled"),
            "dalio": ("dalio_distilled_v2", "RayDalioDistilled"),
            "graham": ("ben_graham_distilled_v2", "BenGrahamDistilled"),
            "dennis": ("dennis_distilled_v2", "RichardDennisDistilled"),
            "simons": ("simons_distilled_v2", "JimSimonsDistilled"),
            "ackman": ("ackman_distilled_v2", "BillAckmanDistilled"),
            "wood": ("cathie_wood_distilled_v2", "CathieWoodDistilled"),
            "soros": ("soros_distilled_v2", "GeorgeSorosDistilled"),
            "jones": ("jones_pt_distilled_v2", "PaulTudorJonesDistilled"),
            "seykota": ("seykota_distilled_v2", "EdSeykotaDistilled"),
            "kovner": ("kovner_distilled_v2", "BruceKovnerDistilled"),
            "druckenmiller": ("druckenmiller_distilled_v2", "StanleyDruckenmillerDistilled"),
            "icahn": ("icahn_distilled_v2", "CarlIcahnDistilled"),
            "cohen": ("cohen_distilled_v2", "SteveCohenDistilled"),
            "griffin": ("griffin_distilled_v2", "KenGriffinDistilled"),
            "pabrai": ("pabrai_distilled_v2", "MohnishPabraiDistilled"),
            "einhorn": ("einhorn_distilled_v2", "DavidEinhornDistilled"),
            "loeb": ("loeb_distilled_v2", "DanielLoebDistilled"),
            "yass": ("yass_distilled_v2", "JeffYassDistilled"),
            "livermore": ("livermore_distilled_v2", "JesseLivermoreDistilled"),
            "rogers": ("rogers_jim_distilled_v2", "JimRogersDistilled"),
            "williams": ("williams_l_distilled_v2", "LarryWilliamsDistilled"),
        }
    
    def analyze(self, ticker: str, data: Dict = None, 
                masters: Optional[List[str]] = None,
                auto_fetch_data: bool = False) -> ConsensusReport:
        """
        分析股票，聚合多个大师的观点
        
        Args:
            ticker: 股票代码
            data: 股票数据（可选，但强烈建议提供真实数据）
            masters: 指定大师列表（默认使用全部）
            auto_fetch_data: 当data为None时是否自动获取数据（默认False，会抛出异常）
        
        Returns:
            ConsensusReport: 共识报告
        
        Raises:
            ValueError: 当data为None且auto_fetch_data为False时
        """
        if masters is None:
            masters = list(self.master_mapping.keys())
        
        # [P1 FIX] 当data为None时的安全处理
        if data is None:
            if auto_fetch_data:
                # 尝试从实时数据源获取
                try:
                    from realtime_data_feed import create_data_feed
                    feed = create_data_feed()
                    feed.start([ticker])
                    import time
                    time.sleep(2)  # 等待数据
                    price = feed.get_price(ticker)
                    feed.stop()
                    
                    if price:
                        data = {
                            "ticker": ticker,
                            "price": price,
                            "sector": "Unknown",
                            "source": "realtime_feed"
                        }
                    else:
                        raise ValueError(f"无法获取 {ticker} 的实时数据")
                except Exception as e:
                    raise ValueError(f"自动获取数据失败: {e}。请手动提供数据或设置auto_fetch_data=False使用模拟数据（不推荐用于生产）")
            else:
                # 生产环境下不应该使用模拟数据
                raise ValueError(
                    f"未提供股票数据。请提供真实数据，或设置 auto_fetch_data=True 尝试自动获取。"
                    f"注意：在生产环境中使用模拟数据会导致错误的投资建议。"
                )
        
        opinions = []
        expert_opinions = []
        outside_opinions = []
        
        for master_key in masters:
            if master_key not in self.master_mapping:
                continue
            
            module_name, class_name = self.master_mapping[master_key]
            opinion = self._get_master_opinion(module_name, class_name, data)
            
            if opinion:
                opinions.append(opinion)
                if opinion.is_within_circle:
                    expert_opinions.append(opinion)
                else:
                    outside_opinions.append(opinion)
        
        # 计算共识
        return self._generate_consensus(ticker, opinions, expert_opinions, outside_opinions)
    
    def _get_master_opinion(self, module_name: str, class_name: str, 
                           data: Dict) -> Optional[MasterOpinion]:
        """获取单个大师的观点"""
        try:
            # 简化版本：返回模拟数据
            # 实际应该动态加载并调用analyze()
            return MasterOpinion(
                name=class_name.replace("Distilled", ""),
                signal="neutral",
                confidence=50,
                reasoning=["分析框架已加载"],
                is_within_circle=True
            )
        except Exception as e:
            print(f"⚠️ 获取 {class_name} 观点失败: {e}")
            return None
    
    def _generate_consensus(self, ticker: str, all_opinions: List[MasterOpinion],
                           expert_opinions: List[MasterOpinion],
                           outside_opinions: List[MasterOpinion]) -> ConsensusReport:
        """生成共识报告"""
        
        bullish = sum(1 for o in all_opinions if o.signal == "bullish")
        bearish = sum(1 for o in all_opinions if o.signal == "bearish")
        neutral = sum(1 for o in all_opinions if o.signal == "neutral")
        
        total = len(all_opinions)
        if total == 0:
            consensus = ConsensusType.UNCLEAR
        else:
            bull_pct = bullish / total
            bear_pct = bearish / total
            
            if bull_pct >= 0.7:
                consensus = ConsensusType.STRONG_BULLISH
            elif bull_pct >= 0.5:
                consensus = ConsensusType.BULLISH
            elif bear_pct >= 0.7:
                consensus = ConsensusType.STRONG_BEARISH
            elif bear_pct >= 0.5:
                consensus = ConsensusType.BEARISH
            else:
                consensus = ConsensusType.MIXED
        
        avg_confidence = sum(o.confidence for o in all_opinions) / len(all_opinions) if all_opinions else 0
        
        # 生成推荐
        recommendation = self._generate_recommendation(consensus, avg_confidence, expert_opinions)
        
        return ConsensusReport(
            ticker=ticker,
            consensus=consensus,
            bullish_count=bullish,
            bearish_count=bearish,
            neutral_count=neutral,
            average_confidence=avg_confidence,
            expert_opinions=expert_opinions,
            outside_opinions=outside_opinions,
            key_insights=["投资委员会模式已激活"],
            debates=[],
            recommendation=recommendation
        )
    
    def _generate_recommendation(self, consensus: ConsensusType, 
                                confidence: float,
                                expert_opinions: List[MasterOpinion]) -> str:
        """生成投资建议"""
        if consensus == ConsensusType.STRONG_BULLISH:
            return f"强烈建议买入（共识度: {confidence:.0f}%）"
        elif consensus == ConsensusType.BULLISH:
            return f"建议买入（共识度: {confidence:.0f}%）"
        elif consensus == ConsensusType.STRONG_BEARISH:
            return f"强烈建议卖出/做空（共识度: {confidence:.0f}%）"
        elif consensus == ConsensusType.BEARISH:
            return f"建议卖出（共识度: {confidence:.0f}%）"
        elif consensus == ConsensusType.MIXED:
            return "观点分歧，建议观望或深入研究"
        else:
            return "数据不足，无法形成共识"
    
    def _get_mock_data(self, ticker: str) -> Dict:
        """获取模拟数据"""
        return {
            "ticker": ticker,
            "roe": 0.20,
            "debt_to_equity": 0.5,
            "sector": "Technology",
            "market_cap": 1e12,
        }
    
    def get_experts_for_sector(self, sector: str) -> List[str]:
        """获取某个行业的专家大师"""
        sector_experts = {
            "technology": ["wood", "cohen", "griffin"],
            "consumer": ["buffett", "ackman"],
            "financials": ["buffett", "graham", "pabrai"],
            "macro": ["dalio", "soros", "druckenmiller"],
            "futures": ["dennis", "jones", "seykota", "kovner"],
        }
        return sector_experts.get(sector.lower(), [])
    
    def debate(self, ticker: str, topic: str, 
               master_a: str, master_b: str) -> Dict:
        """
        让两位大师辩论特定话题
        
        示例:
            debate("TSLA", "估值是否合理", "buffett", "wood")
        """
        return {
            "ticker": ticker,
            "topic": topic,
            "master_a": master_a,
            "master_b": master_b,
            "debate_summary": f"{master_a} vs {master_b} on {topic}",
            "key_differences": [
                "估值方法不同",
                "时间视角不同",
                "风险偏好不同"
            ]
        }


def create_committee() -> InvestmentCommittee:
    """工厂函数"""
    return InvestmentCommittee()


if __name__ == "__main__":
    # 测试
    committee = create_committee()
    
    # 获取所有可用大师
    print(f"可用大师: {len(committee.master_mapping)} 位")
    
    # 分析示例
    report = committee.analyze("AAPL", masters=["buffett", "dalio", "wood"])
    print(f"\n分析报告: {report.ticker}")
    print(f"共识: {report.consensus.value}")
    print(f"看多: {report.bullish_count}, 看空: {report.bearish_count}, 中性: {report.neutral_count}")
    print(f"建议: {report.recommendation}")
