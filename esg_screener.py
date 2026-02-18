#!/usr/bin/env python3
"""
AI Hedge Fund - ESG Screening Module
Environmental, Social, and Governance screening
"""

import os
import sys
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ai_hedge_fund_advanced import AIHedgeFundAdvanced

@dataclass
class ESGScore:
    """ESG scores for a company"""
    ticker: str
    environmental: float  # 0-10
    social: float         # 0-10
    governance: float     # 0-10
    overall: float        # 0-10
    controversy_score: int  # 0-5, 5 is severe
    sector_average: float
    percentile: int       # vs sector peers
    data_quality: str     # HIGH, MEDIUM, LOW

@dataclass
class ESGAlert:
    """ESG concern or violation"""
    ticker: str
    category: str  # ENVIRONMENTAL, SOCIAL, GOVERNANCE
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    issue: str
    description: str
    date_reported: str
    source: str

@dataclass
class ESGReport:
    """Complete ESG analysis"""
    ticker: str
    esg_score: ESGScore
    alerts: List[ESGAlert]
    controversies: List[str]
    strengths: List[str]
    weaknesses: List[str]
    exclusions: List[str]  # Why it might be excluded
    esg_integration_recommendation: str
    approved: bool

class ESGScreener:
    """ESG screening and analysis"""
    
    def __init__(self):
        self.exclusion_threshold = 3.0  # Exclude if overall ESG < 3
        self.controversy_threshold = 4  # Exclude if controversy >= 4
        
        # Exclusion criteria
        self.excluded_sectors = [
            "Thermal Coal",
            "Oil Sands", 
            "Tobacco",
            "Controversial Weapons"
        ]
        
        self.red_flags = {
            "environmental": [
                "Severe environmental violations",
                "High carbon intensity with no transition plan",
                "Deforestation in supply chain",
                "Water pollution incidents"
            ],
            "social": [
                "Child labor in supply chain",
                "Severe human rights violations",
                "Workplace fatalities",
                "Anti-union activities"
            ],
            "governance": [
                "Accounting fraud",
                "Bribery/corruption convictions",
                "CEO-Chairman concentration with no oversight",
                "Related-party transactions abuse"
            ]
        }
    
    def screen_stock(self, ticker: str, 
                    strict_mode: bool = False) -> ESGReport:
        """
        Screen a stock for ESG compliance
        
        In production, this would connect to ESG data providers
        (MSCI, Sustainalytics, Refinitiv, etc.)
        """
        print(f"\n🌱 Screening {ticker} for ESG compliance...", file=sys.stderr)
        
        # In production, fetch from ESG data provider API
        # For now, use simulated data based on sector
        esg_data = self._fetch_esg_data(ticker)
        
        # Calculate scores
        score = self._calculate_esg_score(ticker, esg_data)
        
        # Check for alerts
        alerts = self._check_controversies(ticker, esg_data)
        
        # Determine strengths and weaknesses
        strengths, weaknesses = self._analyze_factors(score, esg_data)
        
        # Check exclusions
        exclusions = self._check_exclusions(score, alerts, esg_data)
        
        # Approval decision
        approved = len(exclusions) == 0
        
        # Generate recommendation
        recommendation = self._generate_recommendation(score, approved, exclusions)
        
        return ESGReport(
            ticker=ticker,
            esg_score=score,
            alerts=alerts,
            controversies=[a.issue for a in alerts if a.severity in ['CRITICAL', 'HIGH']],
            strengths=strengths,
            weaknesses=weaknesses,
            exclusions=exclusions,
            esg_integration_recommendation=recommendation,
            approved=approved
        )
    
    def screen_portfolio(self, tickers: List[str], 
                        esg_minimum: float = 5.0) -> Dict:
        """Screen entire portfolio"""
        results = []
        
        for ticker in tickers:
            try:
                report = self.screen_stock(ticker)
                results.append(report)
            except Exception as e:
                print(f"Error screening {ticker}: {e}", file=sys.stderr)
        
        # Calculate portfolio ESG metrics
        avg_esg = sum(r.esg_score.overall for r in results) / len(results) if results else 0
        approved_count = sum(1 for r in results if r.approved)
        
        # Find excluded stocks
        excluded = [r for r in results if not r.approved]
        
        return {
            "portfolio_esg_score": avg_esg,
            "stocks_screened": len(results),
            "approved": approved_count,
            "excluded": len(excluded),
            "exclusion_rate": len(excluded) / len(results) if results else 0,
            "details": results,
            "excluded_stocks": [
                {
                    "ticker": r.ticker,
                    "reasons": r.exclusions
                }
                for r in excluded
            ],
            "improvement_opportunities": self._find_improvements(results)
        }
    
    def _fetch_esg_data(self, ticker: str) -> Dict:
        """Fetch ESG data (simulated for demo)"""
        # In production: connect to MSCI, Sustainalytics, Refinitiv API
        
        # Simulate based on ticker patterns
        base_score = 6.0
        
        # Adjust based on ticker (demo purposes)
        if ticker in ['TSLA']:
            return {
                'environmental': 8.5,  # EVs
                'social': 5.0,         # Labor concerns
                'governance': 6.0,     # Twitter issues
                'controversy': 3,
                'sector': 'Automotive',
                'data_quality': 'HIGH'
            }
        elif ticker in ['XOM', 'CVX', 'COP']:
            return {
                'environmental': 2.5,  # Oil & gas
                'social': 5.0,
                'governance': 6.0,
                'controversy': 4,
                'sector': 'Energy',
                'data_quality': 'HIGH'
            }
        elif ticker in ['AAPL', 'MSFT', 'GOOGL']:
            return {
                'environmental': 7.0,
                'social': 6.5,
                'governance': 7.5,
                'controversy': 2,
                'sector': 'Technology',
                'data_quality': 'HIGH'
            }
        elif ticker in ['JPM', 'BAC', 'GS']:
            return {
                'environmental': 5.0,  # Financing emissions
                'social': 5.5,
                'governance': 6.5,
                'controversy': 3,
                'sector': 'Financials',
                'data_quality': 'HIGH'
            }
        else:
            return {
                'environmental': base_score + np.random.uniform(-1, 1),
                'social': base_score + np.random.uniform(-1, 1),
                'governance': base_score + np.random.uniform(-1, 1),
                'controversy': np.random.randint(0, 3),
                'sector': 'Unknown',
                'data_quality': 'MEDIUM'
            }
    
    def _calculate_esg_score(self, ticker: str, data: Dict) -> ESGScore:
        """Calculate overall ESG score"""
        env = max(0, min(10, data.get('environmental', 5)))
        soc = max(0, min(10, data.get('social', 5)))
        gov = max(0, min(10, data.get('governance', 5)))
        
        # Weighted average (typical ESG weighting)
        overall = env * 0.30 + soc * 0.30 + gov * 0.40
        
        # Adjust for controversy
        controversy = data.get('controversy', 0)
        if controversy >= 4:
            overall *= 0.7  # Severe penalty
        elif controversy >= 3:
            overall *= 0.85
        
        return ESGScore(
            ticker=ticker,
            environmental=round(env, 1),
            social=round(soc, 1),
            governance=round(gov, 1),
            overall=round(overall, 1),
            controversy_score=controversy,
            sector_average=5.5,  # Would fetch from database
            percentile=int((overall / 10) * 100),
            data_quality=data.get('data_quality', 'MEDIUM')
        )
    
    def _check_controversies(self, ticker: str, data: Dict) -> List[ESGAlert]:
        """Check for ESG controversies"""
        alerts = []
        
        # Environmental
        if data.get('environmental', 10) < 3:
            alerts.append(ESGAlert(
                ticker=ticker,
                category='ENVIRONMENTAL',
                severity='HIGH',
                issue='Poor environmental record',
                description='Significant environmental violations or high emissions intensity',
                date_reported='2024-01-01',
                source='ESG Database'
            ))
        
        # Social
        if data.get('social', 10) < 3:
            alerts.append(ESGAlert(
                ticker=ticker,
                category='SOCIAL',
                severity='HIGH',
                issue='Social concerns',
                description='Labor issues, human rights concerns, or customer disputes',
                date_reported='2024-01-01',
                source='ESG Database'
            ))
        
        # Governance
        if data.get('governance', 10) < 3:
            alerts.append(ESGAlert(
                ticker=ticker,
                category='GOVERNANCE',
                severity='CRITICAL',
                issue='Governance deficiencies',
                description='Board independence issues, accounting concerns, or shareholder rights',
                date_reported='2024-01-01',
                source='ESG Database'
            ))
        
        return alerts
    
    def _analyze_factors(self, score: ESGScore, data: Dict) -> Tuple[List[str], List[str]]:
        """Identify ESG strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        if score.environmental >= 7:
            strengths.append("Strong environmental management")
        elif score.environmental < 4:
            weaknesses.append("Environmental concerns")
        
        if score.social >= 7:
            strengths.append("Good labor practices")
        elif score.social < 4:
            weaknesses.append("Social risks")
        
        if score.governance >= 7:
            strengths.append("Strong governance")
        elif score.governance < 4:
            weaknesses.append("Governance weaknesses")
        
        return strengths, weaknesses
    
    def _check_exclusions(self, score: ESGScore, alerts: List[ESGAlert], data: Dict) -> List[str]:
        """Check exclusion criteria"""
        exclusions = []
        
        if score.overall < self.exclusion_threshold:
            exclusions.append(f"Overall ESG score {score.overall:.1f} below threshold {self.exclusion_threshold}")
        
        if score.controversy_score >= self.controversy_threshold:
            exclusions.append(f"High controversy level ({score.controversy_score}/5)")
        
        critical_alerts = [a for a in alerts if a.severity == 'CRITICAL']
        if critical_alerts:
            exclusions.append(f"Critical ESG issues: {critical_alerts[0].issue}")
        
        sector = data.get('sector', '')
        if sector in self.excluded_sectors:
            exclusions.append(f"Excluded sector: {sector}")
        
        return exclusions
    
    def _generate_recommendation(self, score: ESGScore, approved: bool, exclusions: List[str]) -> str:
        """Generate ESG integration recommendation"""
        if approved:
            if score.overall >= 7:
                return "STRONG BUY - Leader in ESG practices"
            elif score.overall >= 5:
                return "APPROVED - Meets ESG standards"
            else:
                return "APPROVED WITH MONITORING - Marginal ESG score"
        else:
            return f"EXCLUDED - {'; '.join(exclusions[:2])}"
    
    def _find_improvements(self, results: List[ESGReport]) -> List[Dict]:
        """Find ESG improvement opportunities"""
        improvements = []
        
        for r in results:
            if r.esg_score.overall < 7 and r.esg_score.overall >= 5:
                improvements.append({
                    "ticker": r.ticker,
                    "current_score": r.esg_score.overall,
                    "target_score": 7.0,
                    "improvement_areas": r.weaknesses[:2]
                })
        
        return sorted(improvements, key=lambda x: x['current_score'])

def format_esg_report(report: ESGReport) -> str:
    """Format ESG report"""
    status = "✅ APPROVED" if report.approved else "❌ EXCLUDED"
    
    lines = [
        f"\n{'='*80}",
        f"🌱 ESG Screening Report: {report.ticker}",
        f"{'='*80}",
        f"Status: {status}",
        "",
        "📊 ESG Scores (0-10 scale):",
        "-" * 40,
        f"  Environmental:  {report.esg_score.environmental:.1f} {'█' * int(report.esg_score.environmental)}",
        f"  Social:         {report.esg_score.social:.1f} {'█' * int(report.esg_score.social)}",
        f"  Governance:     {report.esg_score.governance:.1f} {'█' * int(report.esg_score.governance)}",
        f"  Overall:        {report.esg_score.overall:.1f} (Percentile: {report.esg_score.percentile}%)",
        f"  Controversy:    {report.esg_score.controversy_score}/5",
        ""
    ]
    
    if report.alerts:
        lines.extend([
            "⚠️  ESG Alerts:",
            "-" * 40
        ])
        for alert in report.alerts:
            emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}[alert.severity]
            lines.append(f"  {emoji} [{alert.category}] {alert.issue}")
        lines.append("")
    
    if report.strengths:
        lines.extend([
            "💪 ESG Strengths:",
            "-" * 40
        ])
        for s in report.strengths:
            lines.append(f"  ✓ {s}")
        lines.append("")
    
    if report.exclusions:
        lines.extend([
            "🚫 Exclusion Reasons:",
            "-" * 40
        ])
        for e in report.exclusions:
            lines.append(f"  • {e}")
        lines.append("")
    
    lines.extend([
        f"💡 Recommendation: {report.esg_integration_recommendation}",
        f"{'='*80}\n"
    ])
    
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Hedge Fund - ESG Screener")
    parser.add_argument("tickers", help="Comma-separated stock tickers")
    parser.add_argument("--portfolio", "-p", action="store_true",
                       help="Screen as portfolio")
    parser.add_argument("--minimum-score", "-m", type=float, default=5.0,
                       help="Minimum ESG score (default 5.0)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    tickers = [t.strip().upper() for t in args.tickers.split(",")]
    screener = ESGScreener()
    
    try:
        if args.portfolio:
            results = screener.screen_portfolio(tickers, args.minimum_score)
            
            if args.json:
                print(json.dumps(results, indent=2, default=lambda o: o.__dict__))
            else:
                print(f"\n{'='*80}")
                print(f"🌱 Portfolio ESG Screening Results")
                print(f"{'='*80}")
                print(f"Portfolio ESG Score: {results['portfolio_esg_score']:.1f}/10")
                print(f"Stocks Screened: {results['stocks_screened']}")
                print(f"Approved: {results['approved']}")
                print(f"Excluded: {results['excluded']} ({results['exclusion_rate']:.1%})")
                print("")
                
                if results['excluded_stocks']:
                    print("Excluded Stocks:")
                    for e in results['excluded_stocks']:
                        print(f"  ❌ {e['ticker']}: {e['reasons'][0]}")
                    print("")
        else:
            for ticker in tickers:
                report = screener.screen_stock(ticker)
                
                if args.json:
                    print(json.dumps(report.__dict__, indent=2, default=lambda o: o.__dict__))
                else:
                    print(format_esg_report(report))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import numpy as np
    main()