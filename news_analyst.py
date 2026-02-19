"""
📰 News Analyst Agent
Analyzes external factors and news impact on stocks
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from base import AgentSignal, InvestmentAgent
from data_enhancement import EnhancedStockData


@dataclass
class NewsItem:
    """Single news item"""
    title: str
    url: str
    source: str
    published_date: str
    summary: str = ""
    relevance_score: float = 0.0
    sentiment: str = "neutral"  # positive, negative, neutral


@dataclass
class ExternalFactor:
    """External factor analysis"""
    category: str  # political, military, technological, regulatory, market
    factor_name: str
    impact_level: str  # high, medium, low
    description: str
    recent_developments: List[str] = field(default_factory=list)


@dataclass
class NewsAnalysisReport:
    """Comprehensive news analysis report"""
    ticker: str
    sector: str
    industry: str
    
    # Business scope analysis
    business_areas: List[str] = field(default_factory=list)
    key_products: List[str] = field(default_factory=list)
    
    # External factors
    external_factors: List[ExternalFactor] = field(default_factory=list)
    
    # News summary
    total_news_found: int = 0
    relevant_news_count: int = 0
    recent_news: List[NewsItem] = field(default_factory=list)
    
    # Analysis
    overall_sentiment: str = "neutral"
    sentiment_score: float = 0.0  # -1 to 1
    key_risks_from_news: List[str] = field(default_factory=list)
    key_opportunities: List[str] = field(default_factory=list)
    
    # Political/Regulatory
    political_risk_level: str = "low"  # high, medium, low
    regulatory_changes: List[str] = field(default_factory=list)
    
    # Military/Geopolitical
    geopolitical_exposure: str = "low"
    military_related_news: List[str] = field(default_factory=list)
    
    # Technology/Competition
    tech_disruption_risk: str = "low"
    competitive_threats: List[str] = field(default_factory=list)


class BraveSearchClient:
    """Client for Brave Search API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('BRAVE_API_KEY')
        self.base_url = "https://api.search.brave.com/res/v1/news/search"
    
    def search_news(self, query: str, count: int = 10, offset: int = 0) -> List[Dict]:
        """Search for news using Brave Search API"""
        if not self.api_key:
            print("Warning: BRAVE_API_KEY not set, using mock data", file=sys.stderr)
            return self._mock_search(query, count)
        
        try:
            headers = {
                'Accept': 'application/json',
                'X-Subscription-Token': self.api_key
            }
            
            params = urllib.parse.urlencode({
                'q': query,
                'count': count,
                'offset': offset,
                'search_lang': 'en',
                'freshness': 'py',  # Past year
                'text_decorations': 'false'
            })
            
            url = f"{self.base_url}?{params}"
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=15) as response:
                raw_data = response.read()
                
                # Check if response is gzip encoded
                if response.info().get('Content-Encoding') == 'gzip':
                    import gzip
                    raw_data = gzip.decompress(raw_data)
                
                data = json.loads(raw_data.decode('utf-8'))
                return data.get('results', [])
                
        except Exception as e:
            print(f"Brave Search error: {e}", file=sys.stderr)
            return self._mock_search(query, count)
    
    def _mock_search(self, query: str, count: int) -> List[Dict]:
        """Provide mock search results when API unavailable"""
        return [{
            'title': f'Sample news about {query}',
            'url': 'https://example.com',
            'description': 'This is a placeholder result. Set BRAVE_API_KEY for real news.',
            'age': '1 month ago',
            'source': 'Mock Source'
        }]


class NewsAnalyst(InvestmentAgent):
    """
    News Analyst Agent - Tier 1
    Analyzes external factors and news impact
    """
    
    def __init__(self):
        super().__init__(
            "News & External Factors Analyst",
            "Analyzes political, military, technological, and regulatory news impact"
        )
        self.search_client = BraveSearchClient()
    
    def analyze_business_scope(self, ticker: str, data: EnhancedStockData) -> Dict:
        """Analyze company business scope to identify relevant external factors"""
        sector = data.sector or "Unknown"
        
        # Define external factors by sector
        sector_factors = {
            'Technology': {
                'factors': [
                    ('regulatory', 'Antitrust Regulation', 'high'),
                    ('technological', 'AI Disruption', 'high'),
                    ('political', 'Data Privacy Laws', 'medium'),
                    ('geopolitical', 'China-US Tech Tensions', 'high'),
                    ('market', 'Cloud Computing Competition', 'medium'),
                ],
                'keywords': ['antitrust', 'regulation', 'AI', 'artificial intelligence', 
                           'cybersecurity', 'data privacy', 'cloud', 'semiconductor']
            },
            'Healthcare': {
                'factors': [
                    ('regulatory', 'FDA Approval Process', 'high'),
                    ('political', 'Healthcare Policy Changes', 'high'),
                    ('technological', 'Gene Therapy Breakthroughs', 'medium'),
                    ('regulatory', 'Drug Pricing Reform', 'high'),
                    ('market', 'Patent Expirations', 'medium'),
                ],
                'keywords': ['FDA', 'clinical trial', 'drug approval', 'healthcare policy',
                           'medicare', 'patent', 'generic competition', 'vaccine']
            },
            'Industrials': {
                'factors': [
                    ('geopolitical', 'Defense Spending', 'high'),
                    ('regulatory', 'Environmental Regulations', 'medium'),
                    ('political', 'Infrastructure Spending', 'high'),
                    ('geopolitical', 'Supply Chain Disruptions', 'high'),
                    ('technological', 'Automation Trends', 'medium'),
                ],
                'keywords': ['defense contract', 'infrastructure', 'supply chain',
                           'aerospace', 'tariff', 'trade war', 'automation']
            },
            'Financials': {
                'factors': [
                    ('regulatory', 'Banking Regulations', 'high'),
                    ('political', 'Interest Rate Policy', 'high'),
                    ('regulatory', 'Fintech Disruption', 'medium'),
                    ('market', 'Economic Recession Risk', 'high'),
                    ('political', 'Tax Policy Changes', 'medium'),
                ],
                'keywords': ['interest rate', 'fed', 'regulation', 'fintech',
                           'recession', 'inflation', 'banking', 'merger']
            },
            'Energy': {
                'factors': [
                    ('political', 'Climate Policy', 'high'),
                    ('geopolitical', 'Oil Supply Disruptions', 'high'),
                    ('regulatory', 'Carbon Regulations', 'high'),
                    ('technological', 'Renewable Energy Transition', 'high'),
                    ('geopolitical', 'Middle East Tensions', 'high'),
                ],
                'keywords': ['oil price', 'OPEC', 'renewable', 'climate', 'carbon',
                           'natural gas', 'geopolitical', 'sanctions']
            },
            'Consumer': {
                'factors': [
                    ('economic', 'Consumer Spending Trends', 'high'),
                    ('regulatory', 'Consumer Protection Laws', 'medium'),
                    ('technological', 'E-commerce Disruption', 'medium'),
                    ('market', 'Inflation Impact', 'high'),
                    ('geopolitical', 'Supply Chain Issues', 'medium'),
                ],
                'keywords': ['consumer spending', 'inflation', 'retail', 'supply chain',
                           'e-commerce', 'consumer confidence', 'tariff']
            }
        }
        
        # Get factors for this sector
        sector_info = sector_factors.get(sector, {
            'factors': [
                ('regulatory', 'Industry Regulation', 'medium'),
                ('market', 'Competitive Landscape', 'medium'),
                ('economic', 'Macroeconomic Conditions', 'medium'),
            ],
            'keywords': ['earnings', 'revenue', 'growth', 'competition']
        })
        
        return {
            'sector': sector,
            'factors': sector_info['factors'],
            'keywords': sector_info['keywords']
        }
    
    def search_relevant_news(self, ticker: str, business_info: Dict) -> List[NewsItem]:
        """Search for relevant news based on business scope"""
        all_news = []
        
        # Search queries based on ticker and keywords
        search_queries = [
            f"{ticker} stock news",
            f"{ticker} earnings news 2024 2025",
        ]
        
        # Add sector-specific searches
        sector = business_info['sector']
        keywords = business_info['keywords'][:3]  # Top 3 keywords
        
        for keyword in keywords:
            search_queries.append(f"{ticker} {keyword} news")
        
        # Add political/regulatory searches
        search_queries.extend([
            f"{ticker} regulation policy",
            f"{ticker} geopolitical risk",
        ])
        
        # Execute searches (limit to avoid rate limits)
        for query in search_queries[:5]:
            try:
                results = self.search_client.search_news(query, count=5)
                for result in results:
                    news_item = NewsItem(
                        title=result.get('title', ''),
                        url=result.get('url', ''),
                        source=result.get('source', 'Unknown'),
                        published_date=result.get('age', 'Unknown'),
                        summary=result.get('description', '')[:200]
                    )
                    all_news.append(news_item)
            except Exception as e:
                print(f"Search error for '{query}': {e}", file=sys.stderr)
        
        # Remove duplicates and sort by relevance
        seen_urls = set()
        unique_news = []
        for news in all_news:
            if news.url not in seen_urls:
                seen_urls.add(news.url)
                unique_news.append(news)
        
        return unique_news[:15]  # Return top 15 unique news items
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Simple sentiment analysis based on keywords"""
        positive_words = ['growth', 'profit', 'beat', 'strong', 'bullish', 
                         'innovation', 'breakthrough', 'partnership', 'expansion',
                         'record', 'surge', 'rally', 'upgrade', 'outperform']
        
        negative_words = ['loss', 'miss', 'weak', 'bearish', 'decline', 
                         'lawsuit', 'investigation', 'recall', 'downgrade',
                         'underperform', 'cut', 'layoff', 'bankruptcy', 'crisis']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive', min(0.9, 0.3 + (pos_count - neg_count) * 0.1)
        elif neg_count > pos_count:
            return 'negative', max(-0.9, -0.3 - (neg_count - pos_count) * 0.1)
        else:
            return 'neutral', 0.0
    
    def analyze_external_factors(self, news_items: List[NewsItem], 
                                 business_info: Dict) -> List[ExternalFactor]:
        """Analyze external factors from news"""
        factors = []
        
        # Create factor categories from business scope
        for category, factor_name, default_impact in business_info['factors']:
            factor = ExternalFactor(
                category=category,
                factor_name=factor_name,
                impact_level=default_impact,
                description=f"Key {category} factor for {business_info['sector']} sector"
            )
            
            # Find relevant news for this factor
            factor_keywords = {
                'political': ['policy', 'government', 'legislation', 'trump', 'biden', 'congress'],
                'regulatory': ['FDA', 'regulation', 'antitrust', 'compliance', 'SEC'],
                'geopolitical': ['war', 'tensions', 'sanctions', 'trade war', 'china', 'russia'],
                'technological': ['AI', 'breakthrough', 'innovation', 'disruption', 'patent'],
                'military': ['defense', 'contract', 'pentagon', 'NATO', 'military spending'],
                'economic': ['inflation', 'recession', 'fed', 'interest rate', 'GDP']
            }
            
            keywords = factor_keywords.get(category, [])
            relevant_news = []
            
            for news in news_items:
                title_summary = (news.title + " " + news.summary).lower()
                if any(kw in title_summary for kw in keywords):
                    relevant_news.append(f"{news.title} ({news.source})")
            
            factor.recent_developments = relevant_news[:3]
            factors.append(factor)
        
        return factors
    
    def generate_news_analysis(self, ticker: str, data: EnhancedStockData) -> NewsAnalysisReport:
        """Generate comprehensive news analysis report"""
        report = NewsAnalysisReport(
            ticker=ticker,
            sector=data.sector or "Unknown",
            industry=data.financials.industry if hasattr(data.financials, 'industry') else "Unknown"
        )
        
        # Step 1: Analyze business scope
        business_info = self.analyze_business_scope(ticker, data)
        report.business_areas = [f[1] for f in business_info['factors']]
        
        # Step 2: Search for relevant news
        news_items = self.search_relevant_news(ticker, business_info)
        report.total_news_found = len(news_items)
        
        # Step 3: Analyze sentiment for each news item
        sentiments = []
        for news in news_items:
            sentiment, score = self.analyze_sentiment(news.title + " " + news.summary)
            news.sentiment = sentiment
            sentiments.append(score)
        
        # Calculate overall sentiment
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            report.sentiment_score = avg_sentiment
            if avg_sentiment > 0.2:
                report.overall_sentiment = 'positive'
            elif avg_sentiment < -0.2:
                report.overall_sentiment = 'negative'
            else:
                report.overall_sentiment = 'neutral'
        
        report.recent_news = news_items[:10]  # Top 10 news
        report.relevant_news_count = len([n for n in news_items if n.relevance_score > 0.5])
        
        # Step 4: Analyze external factors
        report.external_factors = self.analyze_external_factors(news_items, business_info)
        
        # Step 5: Extract risks and opportunities
        for news in news_items:
            text = (news.title + " " + news.summary).lower()
            
            # Check for risk keywords
            risk_keywords = ['risk', 'concern', 'warning', 'decline', 'lawsuit', 
                           'investigation', 'recall', 'shortage', 'disruption']
            if any(rk in text for rk in risk_keywords):
                report.key_risks_from_news.append(news.title)
            
            # Check for opportunity keywords
            opp_keywords = ['growth', 'opportunity', 'breakthrough', 'partnership',
                          'expansion', 'innovation', 'milestone', 'approval']
            if any(ok in text for ok in opp_keywords):
                report.key_opportunities.append(news.title)
        
        # Limit lists
        report.key_risks_from_news = report.key_risks_from_news[:5]
        report.key_opportunities = report.key_opportunities[:5]
        
        # Assess specific risk categories
        political_keywords = ['policy', 'government', 'regulation', 'legislation']
        military_keywords = ['defense', 'military', 'pentagon', 'war', 'conflict']
        tech_keywords = ['technology', 'disruption', 'AI', 'competition']
        
        for news in news_items:
            text = (news.title + " " + news.summary).lower()
            
            if any(pk in text for pk in political_keywords):
                if news.sentiment == 'negative':
                    report.political_risk_level = 'high'
                    report.regulatory_changes.append(news.title)
            
            if any(mk in text for mk in military_keywords):
                report.geopolitical_exposure = 'medium'
                report.military_related_news.append(news.title)
            
            if any(tk in text for tk in tech_keywords):
                if news.sentiment == 'negative':
                    report.tech_disruption_risk = 'medium'
                    report.competitive_threats.append(news.title)
        
        return report
    
    def analyze_enhanced(self, data: EnhancedStockData) -> AgentSignal:
        """Generate news analysis signal"""
        ticker = data.ticker
        
        # Generate comprehensive news analysis
        report = self.generate_news_analysis(ticker, data)
        
        # Calculate score based on analysis
        score = 50  # Neutral base
        reasoning_parts = []
        
        # Sentiment impact
        if report.overall_sentiment == 'positive':
            score += 15
            reasoning_parts.append(f"Positive news sentiment ({len(report.recent_news)} articles analyzed)")
        elif report.overall_sentiment == 'negative':
            score -= 15
            reasoning_parts.append(f"Negative news sentiment detected")
        
        # External factors impact
        high_impact_factors = [f for f in report.external_factors if f.impact_level == 'high']
        if high_impact_factors:
            reasoning_parts.append(f"{len(high_impact_factors)} high-impact external factors identified")
        
        # Political/Regulatory risk
        if report.political_risk_level == 'high':
            score -= 20
            reasoning_parts.append("High political/regulatory risk")
        elif report.political_risk_level == 'low':
            score += 5
            reasoning_parts.append("Low political risk environment")
        
        # Geopolitical exposure
        if report.geopolitical_exposure == 'high':
            score -= 15
            reasoning_parts.append("High geopolitical exposure")
        elif report.geopolitical_exposure == 'low':
            score += 5
        
        # Tech disruption
        if report.tech_disruption_risk == 'high':
            score -= 10
            reasoning_parts.append("Technology disruption risk")
        
        # Risks from news
        if len(report.key_risks_from_news) > 3:
            score -= 10
            reasoning_parts.append(f"Multiple risks identified in news ({len(report.key_risks_from_news)})")
        
        # Opportunities
        if len(report.key_opportunities) > 3:
            score += 10
            reasoning_parts.append(f"Multiple opportunities in news ({len(report.key_opportunities)})")
        
        # Clamp score
        score = max(10, min(95, score))
        
        if score >= 65:
            signal = "bullish"
        elif score <= 35:
            signal = "bearish"
        else:
            signal = "neutral"
        
        # Create detailed reasoning
        detailed_reasoning = "; ".join(reasoning_parts) if reasoning_parts else "No significant news impact"
        
        # Add news summary to reasoning
        if report.recent_news:
            top_news = report.recent_news[0]
            detailed_reasoning += f". Recent: {top_news.title[:80]}..."
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning=detailed_reasoning,
            key_metrics={
                "sentiment": report.overall_sentiment,
                "sentiment_score": report.sentiment_score,
                "news_count": report.total_news_found,
                "political_risk": report.political_risk_level,
                "geopolitical_exposure": report.geopolitical_exposure,
                "tech_risk": report.tech_disruption_risk,
                "external_factors": len(report.external_factors),
                "risks_identified": len(report.key_risks_from_news),
                "opportunities": len(report.key_opportunities)
            }
        )


def format_news_report(report: NewsAnalysisReport) -> str:
    """Format news analysis report for display"""
    lines = []
    
    lines.append(f"\n{'='*70}")
    lines.append(f"📰 NEWS & EXTERNAL FACTORS ANALYSIS: {report.ticker}")
    lines.append(f"{'='*70}\n")
    
    # Business scope
    lines.append(f"Sector: {report.sector}")
    lines.append(f"Key Business Areas: {', '.join(report.business_areas[:5])}")
    lines.append("")
    
    # Sentiment
    sentiment_emoji = {'positive': '🟢', 'negative': '🔴', 'neutral': '🟡'}[report.overall_sentiment]
    lines.append(f"{sentiment_emoji} Overall News Sentiment: {report.overall_sentiment.upper()}")
    lines.append(f"   Sentiment Score: {report.sentiment_score:+.2f}")
    lines.append(f"   Articles Analyzed: {report.total_news_found}")
    lines.append("")
    
    # External Factors
    lines.append("🌍 EXTERNAL FACTORS:")
    for factor in report.external_factors:
        impact_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[factor.impact_level]
        lines.append(f"  {impact_emoji} [{factor.category.upper()}] {factor.factor_name}")
        if factor.recent_developments:
            for dev in factor.recent_developments[:2]:
                lines.append(f"      • {dev[:60]}...")
    lines.append("")
    
    # Risk Assessment
    lines.append("⚠️  RISK ASSESSMENT:")
    lines.append(f"  Political/Regulatory Risk: {report.political_risk_level.upper()}")
    lines.append(f"  Geopolitical Exposure: {report.geopolitical_exposure.upper()}")
    lines.append(f"  Technology Disruption Risk: {report.tech_disruption_risk.upper()}")
    lines.append("")
    
    # Key News
    if report.recent_news:
        lines.append("📰 RECENT NEWS HIGHLIGHTS:")
        for i, news in enumerate(report.recent_news[:5], 1):
            sentiment_emoji = {'positive': '🟢', 'negative': '🔴', 'neutral': '🟡'}[news.sentiment]
            lines.append(f"  {i}. {sentiment_emoji} {news.title[:60]}...")
            lines.append(f"     Source: {news.source} | {news.published_date}")
        lines.append("")
    
    # Key Risks & Opportunities
    if report.key_risks_from_news:
        lines.append("🚨 KEY RISKS FROM NEWS:")
        for risk in report.key_risks_from_news[:3]:
            lines.append(f"  • {risk[:70]}...")
        lines.append("")
    
    if report.key_opportunities:
        lines.append("✨ KEY OPPORTUNITIES:")
        for opp in report.key_opportunities[:3]:
            lines.append(f"  • {opp[:70]}...")
        lines.append("")
    
    lines.append(f"{'='*70}\n")
    
    return "\n".join(lines)
