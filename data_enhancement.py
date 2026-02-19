"""
Enhanced Data Fetcher for AI Hedge Fund
Integrates features from stock-analysis skill
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd


@dataclass
class EarningsData:
    """Earnings surprise analysis"""
    actual_eps: Optional[float] = None
    expected_eps: Optional[float] = None
    surprise_pct: Optional[float] = None
    surprise_score: float = 50.0  # 0-100
    explanation: str = ""
    beats_last_4q: int = 0
    avg_reaction_pct: float = 0.0


@dataclass
class AnalystData:
    """Analyst consensus data"""
    consensus_rating: str = "unknown"  # strong_buy, buy, hold, sell, strong_sell
    num_analysts: int = 0
    price_target: Optional[float] = None
    current_price: Optional[float] = None
    upside_pct: Optional[float] = None
    score: float = 50.0
    summary: str = ""


@dataclass
class DividendData:
    """Dividend analysis"""
    yield_pct: Optional[float] = None
    annual_dividend: Optional[float] = None
    payout_ratio: Optional[float] = None
    payout_status: str = "unknown"  # safe, moderate, high, unsustainable, no_dividend
    growth_5y: Optional[float] = None
    consecutive_years: Optional[int] = None
    ex_dividend_date: Optional[str] = None
    safety_score: int = 0
    income_rating: str = "unknown"  # excellent, good, moderate, poor, no_dividend


@dataclass
class FinancialMetrics:
    """Additional financial metrics from stock-analysis"""
    # Profitability
    operating_margin: Optional[float] = None
    gross_margin: Optional[float] = None
    profit_margin: Optional[float] = None
    ebitda_margin: Optional[float] = None
    
    # Debt & Liquidity
    debt_to_equity: Optional[float] = None
    debt_to_assets: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    
    # Cash Flow
    free_cash_flow: Optional[float] = None  # in millions
    operating_cash_flow: Optional[float] = None
    cash: Optional[float] = None
    
    # Growth
    revenue_growth_yoy: Optional[float] = None
    earnings_growth_yoy: Optional[float] = None
    
    # Efficiency
    return_on_equity: Optional[float] = None
    return_on_assets: Optional[float] = None
    asset_turnover: Optional[float] = None
    
    # Valuation extras
    forward_pe: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_sales: Optional[float] = None
    price_to_cash_flow: Optional[float] = None
    enterprise_value: Optional[float] = None
    
    # Investment & Innovation (NEW)
    rd_expense: Optional[float] = None  # in millions
    rd_to_revenue: Optional[float] = None  # R&D as % of revenue
    capex: Optional[float] = None  # Capital expenditure in millions
    capex_to_revenue: Optional[float] = None
    intangibles: Optional[float] = None  # Goodwill + Intangible assets
    tangible_book_value: Optional[float] = None
    
    # Balance Sheet Strength (NEW)
    total_assets: Optional[float] = None  # in millions
    total_liabilities: Optional[float] = None  # in millions
    shareholders_equity: Optional[float] = None  # in millions
    net_debt: Optional[float] = None  # in millions
    working_capital: Optional[float] = None  # in millions
    
    # Per Share Metrics (NEW)
    book_value_per_share: Optional[float] = None
    cash_per_share: Optional[float] = None
    revenue_per_share: Optional[float] = None
    
    # Health score
    financial_health_score: int = 50  # 0-100
    health_explanation: str = ""
    innovation_score: int = 50  # 0-100 (NEW)
    innovation_explanation: str = ""


@dataclass
class MacroData:
    """Macro market context"""
    vix_level: Optional[float] = None
    vix_status: str = "unknown"  # calm, elevated, fear, panic
    spy_trend_10d: float = 0.0
    qqq_trend_10d: float = 0.0
    market_regime: str = "unknown"  # bull, bear, choppy
    score: float = 50.0
    explanation: str = ""


@dataclass
class EnhancedStockData:
    """Extended stock data with all enhancements"""
    ticker: str = ""
    current_price: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    beta: Optional[float] = None
    roe: Optional[float] = None
    debt_to_equity: Optional[float] = None
    operating_margin: Optional[float] = None
    current_ratio: Optional[float] = None
    sector: str = ""
    market_cap: Optional[float] = None
    
    # Enhanced data
    earnings: EarningsData = field(default_factory=EarningsData)
    analyst: AnalystData = field(default_factory=AnalystData)
    dividend: DividendData = field(default_factory=DividendData)
    macro: MacroData = field(default_factory=MacroData)
    financials: FinancialMetrics = field(default_factory=FinancialMetrics)
    
    # Technical data
    avg_50: Optional[float] = None
    avg_200: Optional[float] = None
    rsi: Optional[float] = None
    volume: Optional[float] = None
    avg_volume: Optional[float] = None


class EnhancedDataFetcher:
    """Fetch comprehensive stock data with enhancements"""
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
    
    def get_enhanced_data(self, ticker: str) -> EnhancedStockData:
        """Fetch all enhanced data for a ticker"""
        data = EnhancedStockData(ticker=ticker)
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Basic data
            data.current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            data.pe_ratio = info.get('trailingPE')
            data.pb_ratio = info.get('priceToBook')
            data.beta = info.get('beta')
            data.roe = info.get('returnOnEquity')
            data.debt_to_equity = info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else None
            data.operating_margin = info.get('operatingMargins')
            data.current_ratio = info.get('currentRatio')
            data.sector = info.get('sector', '')
            data.market_cap = info.get('marketCap')
            
            # Fetch enhanced modules
            data.earnings = self._fetch_earnings(stock, info)
            data.analyst = self._fetch_analyst_data(stock, info)
            data.dividend = self._fetch_dividend_data(stock, info)
            data.macro = self._fetch_macro_data()
            data.financials = self._fetch_financial_metrics(stock, info)
            
            # Technical data
            hist = stock.history(period="1y")
            if not hist.empty:
                data.avg_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else None
                data.avg_200 = hist['Close'].rolling(200).mean().iloc[-1] if len(hist) >= 200 else None
                data.volume = hist['Volume'].iloc[-1]
                data.avg_volume = hist['Volume'].rolling(20).mean().iloc[-1]
                
                # RSI calculation
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                data.rsi = 100 - (100 / (1 + rs.iloc[-1])) if not rs.empty else None
                
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
        
        return data
    
    def _fetch_earnings(self, stock: yf.Ticker, info: Dict) -> EarningsData:
        """Fetch earnings surprise data"""
        earnings = EarningsData()
        
        try:
            # Get earnings history
            earnings_hist = stock.earnings_dates
            if earnings_hist is not None and not earnings_hist.empty:
                # Filter out rows with missing data (future dates have NaN for Reported EPS)
                valid_earnings = earnings_hist.dropna(subset=['Reported EPS', 'EPS Estimate'])
                
                if not valid_earnings.empty:
                    # Get most recent earnings with actual data
                    recent = valid_earnings.iloc[0]
                    earnings.actual_eps = recent.get('Reported EPS')
                    earnings.expected_eps = recent.get('EPS Estimate')
                    
                    if earnings.actual_eps and earnings.expected_eps:
                        earnings.surprise_pct = ((earnings.actual_eps - earnings.expected_eps) 
                                                / abs(earnings.expected_eps) * 100)
                        # Score: positive surprise = bullish
                        if earnings.surprise_pct > 10:
                            earnings.surprise_score = 90
                            earnings.explanation = f"Huge beat: +{earnings.surprise_pct:.1f}%"
                        elif earnings.surprise_pct > 5:
                            earnings.surprise_score = 85
                            earnings.explanation = f"Strong beat: +{earnings.surprise_pct:.1f}%"
                        elif earnings.surprise_pct > 0:
                            earnings.surprise_score = 65
                            earnings.explanation = f"Beat: +{earnings.surprise_pct:.1f}%"
                        elif earnings.surprise_pct > -5:
                            earnings.surprise_score = 45
                            earnings.explanation = f"Miss: {earnings.surprise_pct:.1f}%"
                        else:
                            earnings.surprise_score = 25
                            earnings.explanation = f"Big miss: {earnings.surprise_pct:.1f}%"
            
            # Get historical beat rate (use valid earnings only)
            if not valid_earnings.empty and len(valid_earnings) >= 4:
                beats = 0
                for _, row in valid_earnings.head(4).iterrows():
                    actual = row.get('Reported EPS')
                    expected = row.get('EPS Estimate')
                    if actual and expected and actual > expected:
                        beats += 1
                earnings.beats_last_4q = beats
                
        except Exception as e:
            earnings.explanation = f"Earnings data unavailable: {str(e)[:50]}"
        
        return earnings
    
    def _fetch_analyst_data(self, stock: yf.Ticker, info: Dict) -> AnalystData:
        """Fetch analyst consensus data"""
        analyst = AnalystData()
        
        try:
            analyst.current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            analyst.price_target = info.get('targetMeanPrice')
            analyst.num_analysts = info.get('numberOfAnalystOpinions', 0)
            
            # Rating mapping
            recommendation = info.get('recommendationKey', '')
            rating_map = {
                'strong_buy': ('strong_buy', 90),
                'buy': ('buy', 75),
                'hold': ('hold', 50),
                'sell': ('sell', 25),
                'strong_sell': ('strong_sell', 10),
            }
            
            if recommendation in rating_map:
                analyst.consensus_rating, analyst.score = rating_map[recommendation]
            else:
                analyst.consensus_rating = 'unknown'
                analyst.score = 50
            
            # Calculate upside
            if analyst.price_target and analyst.current_price and analyst.current_price > 0:
                analyst.upside_pct = ((analyst.price_target - analyst.current_price) 
                                     / analyst.current_price * 100)
            
            # Summary
            if analyst.num_analysts > 0:
                analyst.summary = (f"{analyst.num_analysts} analysts: {analyst.consensus_rating}, "
                                  f"target ${analyst.price_target:.2f} "
                                  f"({analyst.upside_pct:+.1f}% upside)")
            else:
                analyst.summary = "No analyst coverage"
                
        except Exception as e:
            analyst.summary = "Analyst data unavailable"
        
        return analyst
    
    def _fetch_dividend_data(self, stock: yf.Ticker, info: Dict) -> DividendData:
        """Fetch dividend analysis data"""
        dividend = DividendData()
        
        try:
            # Handle dividend yield (yfinance sometimes returns as decimal, sometimes as percentage)
            div_yield = info.get('dividendYield')
            if div_yield:
                # If > 10, it's definitely a percentage (e.g., 39 means 39%)
                # If 1-10, could be either - check if it makes sense (< 10% is reasonable)
                # If < 1, it's a decimal (e.g., 0.005 = 0.5%)
                if div_yield > 10:
                    dividend.yield_pct = div_yield  # Already percentage
                elif div_yield > 1:
                    # Ambiguous - likely already percentage for most stocks
                    dividend.yield_pct = div_yield
                else:
                    dividend.yield_pct = div_yield * 100  # Convert decimal to percentage
            else:
                dividend.yield_pct = None
            
            dividend.annual_dividend = info.get('dividendRate')
            dividend.ex_dividend_date = str(info.get('exDividendDate')) if info.get('exDividendDate') else None
            
            # Validate dividend yield - if unreasonably high (>15%), recalculate from dividend/price
            if dividend.yield_pct and dividend.yield_pct > 15:
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                if dividend.annual_dividend and current_price and current_price > 0:
                    dividend.yield_pct = (dividend.annual_dividend / current_price) * 100
            
            # Payout ratio (same logic)
            payout = info.get('payoutRatio')
            if payout:
                dividend.payout_ratio = payout if payout > 1 else payout * 100
            else:
                dividend.payout_ratio = None
            
            if dividend.payout_ratio:
                if dividend.payout_ratio < 40:
                    dividend.payout_status = 'safe'
                    dividend.safety_score = 90
                elif dividend.payout_ratio < 60:
                    dividend.payout_status = 'moderate'
                    dividend.safety_score = 70
                elif dividend.payout_ratio < 80:
                    dividend.payout_status = 'high'
                    dividend.safety_score = 50
                else:
                    dividend.payout_status = 'unsustainable'
                    dividend.safety_score = 30
            else:
                dividend.payout_status = 'no_dividend'
                dividend.safety_score = 0
            
            # Income rating
            if not dividend.yield_pct:
                dividend.income_rating = 'no_dividend'
            elif dividend.yield_pct > 4:
                dividend.income_rating = 'excellent'
            elif dividend.yield_pct > 2.5:
                dividend.income_rating = 'good'
            elif dividend.yield_pct > 1:
                dividend.income_rating = 'moderate'
            else:
                dividend.income_rating = 'poor'
                
        except Exception as e:
            dividend.income_rating = 'unknown'
        
        return dividend
    
    def _fetch_macro_data(self) -> MacroData:
        """Fetch macro market context"""
        macro = MacroData()
        
        try:
            # VIX
            vix = yf.Ticker("^VIX")
            vix_hist = vix.history(period="5d")
            if not vix_hist.empty:
                macro.vix_level = vix_hist['Close'].iloc[-1]
                
                if macro.vix_level < 15:
                    macro.vix_status = 'calm'
                    macro.score = 75
                elif macro.vix_level < 25:
                    macro.vix_status = 'elevated'
                    macro.score = 50
                elif macro.vix_level < 35:
                    macro.vix_status = 'fear'
                    macro.score = 30
                else:
                    macro.vix_status = 'panic'
                    macro.score = 15
            
            # SPY trend
            spy = yf.Ticker("SPY")
            spy_hist = spy.history(period="15d")
            if len(spy_hist) >= 11:
                spy_10d_ago = spy_hist['Close'].iloc[-11]
                spy_now = spy_hist['Close'].iloc[-1]
                macro.spy_trend_10d = (spy_now - spy_10d_ago) / spy_10d_ago * 100
            
            # QQQ trend
            qqq = yf.Ticker("QQQ")
            qqq_hist = qqq.history(period="15d")
            if len(qqq_hist) >= 11:
                qqq_10d_ago = qqq_hist['Close'].iloc[-11]
                qqq_now = qqq_hist['Close'].iloc[-1]
                macro.qqq_trend_10d = (qqq_now - qqq_10d_ago) / qqq_10d_ago * 100
            
            # Market regime
            if macro.spy_trend_10d > 2 and macro.vix_level and macro.vix_level < 20:
                macro.market_regime = 'bull'
                macro.explanation = 'Bull market: rising prices, low volatility'
            elif macro.spy_trend_10d < -3 or (macro.vix_level and macro.vix_level > 30):
                macro.market_regime = 'bear'
                macro.explanation = 'Bear market: falling prices, high volatility'
            else:
                macro.market_regime = 'choppy'
                macro.explanation = 'Choppy market: mixed signals'
                
        except Exception as e:
            macro.explanation = "Macro data unavailable"
        
        return macro
    
    def _fetch_financial_metrics(self, stock: yf.Ticker, info: Dict) -> FinancialMetrics:
        """Fetch comprehensive financial metrics"""
        financials = FinancialMetrics()
        
        try:
            # Profitability Margins
            financials.operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
            financials.gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
            financials.profit_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else None
            financials.ebitda_margin = info.get('ebitdaMargins', 0) * 100 if info.get('ebitdaMargins') else None
            
            # Debt & Liquidity
            financials.debt_to_equity = info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else None
            financials.debt_to_assets = info.get('debtToAssets', 0) if info.get('debtToAssets') else None
            financials.current_ratio = info.get('currentRatio')
            financials.quick_ratio = info.get('quickRatio')
            
            # Cash Flow (in millions)
            financials.free_cash_flow = info.get('freeCashflow') / 1e6 if info.get('freeCashflow') else None
            financials.operating_cash_flow = info.get('operatingCashflow') / 1e6 if info.get('operatingCashflow') else None
            financials.cash = info.get('totalCash') / 1e6 if info.get('totalCash') else None
            
            # Growth
            financials.revenue_growth_yoy = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
            financials.earnings_growth_yoy = info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else None
            
            # Efficiency
            financials.return_on_equity = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else None
            financials.return_on_assets = info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else None
            financials.asset_turnover = info.get('assetTurnover')
            
            # Check for leverage-driven ROE and add warning
            if financials.return_on_equity and financials.return_on_assets and financials.return_on_assets > 0:
                leverage_ratio = financials.return_on_equity / financials.return_on_assets
                if leverage_ratio > 5:
                    financials.health_explanation += f"; Warning: ROE is {leverage_ratio:.1f}x ROA (leverage-driven)"
            
            # Valuation extras
            financials.forward_pe = info.get('forwardPE')
            financials.peg_ratio = info.get('pegRatio')
            financials.price_to_sales = info.get('priceToSalesTrailing12Months')
            financials.price_to_cash_flow = info.get('priceToCashFlow')
            financials.enterprise_value = info.get('enterpriseValue') / 1e9 if info.get('enterpriseValue') else None  # in billions
            
            # Investment & Innovation (NEW)
            financials.rd_expense = info.get('researchDevelopment') / 1e6 if info.get('researchDevelopment') else None
            revenue = info.get('totalRevenue', 0)
            if revenue and financials.rd_expense:
                financials.rd_to_revenue = (financials.rd_expense * 1e6 / revenue) * 100
            financials.capex = info.get('capitalExpenditures') / 1e6 if info.get('capitalExpenditures') else None
            if revenue and financials.capex:
                financials.capex_to_revenue = (abs(financials.capex) * 1e6 / revenue) * 100
            financials.intangibles = (info.get('goodWill', 0) + info.get('intangibleAssets', 0)) / 1e6 if (info.get('goodWill') or info.get('intangibleAssets')) else None
            financials.tangible_book_value = info.get('tangibleBookValue')
            
            # Balance Sheet Strength (NEW)
            financials.total_assets = info.get('totalAssets') / 1e6 if info.get('totalAssets') else None
            financials.total_liabilities = info.get('totalLiabilities') / 1e6 if info.get('totalLiabilities') else None
            financials.shareholders_equity = info.get('totalStockholderEquity') / 1e6 if info.get('totalStockholderEquity') else None
            financials.net_debt = info.get('netDebt') / 1e6 if info.get('netDebt') else None
            financials.working_capital = info.get('workingCapital') / 1e6 if info.get('workingCapital') else None
            
            # Per Share Metrics (NEW)
            financials.book_value_per_share = info.get('bookValue')
            financials.cash_per_share = info.get('cashPerShare')
            financials.revenue_per_share = info.get('revenuePerShare')
            
            # Calculate financial health score
            score = 50
            factors = []
            
            # Profitability (max +20)
            if financials.operating_margin and financials.operating_margin > 20:
                score += 10
                factors.append("Strong operating margin")
            elif financials.operating_margin and financials.operating_margin < 5:
                score -= 10
                factors.append("Low operating margin")
            
            if financials.return_on_equity and financials.return_on_equity > 15:
                score += 10
                factors.append("High ROE")
            elif financials.return_on_equity and financials.return_on_equity < 5:
                score -= 10
                factors.append("Low ROE")
            
            # Debt (max +/-15)
            if financials.debt_to_equity and financials.debt_to_equity < 0.5:
                score += 10
                factors.append("Low debt")
            elif financials.debt_to_equity and financials.debt_to_equity > 1.5:
                score -= 15
                factors.append("High debt load")
            
            # Liquidity (max +15)
            if financials.current_ratio and financials.current_ratio > 2:
                score += 10
                factors.append("Strong liquidity")
            elif financials.current_ratio and financials.current_ratio < 1:
                score -= 10
                factors.append("Weak liquidity")
            
            # Cash flow (max +10)
            if financials.free_cash_flow and financials.free_cash_flow > 0:
                score += 10
                factors.append("Positive free cash flow")
            elif financials.free_cash_flow and financials.free_cash_flow < 0:
                score -= 10
                factors.append("Negative free cash flow")
            
            financials.financial_health_score = max(0, min(100, score))
            financials.health_explanation = "; ".join(factors) if factors else "Average financial health"
            
            # Calculate innovation score (NEW)
            innov_score = 50
            innov_factors = []
            
            # R&D Investment (max +25)
            if financials.rd_to_revenue:
                if financials.rd_to_revenue > 20:
                    innov_score += 25
                    innov_factors.append(f"Heavy R&D: {financials.rd_to_revenue:.1f}%")
                elif financials.rd_to_revenue > 10:
                    innov_score += 15
                    innov_factors.append(f"Strong R&D: {financials.rd_to_revenue:.1f}%")
                elif financials.rd_to_revenue > 5:
                    innov_score += 5
                    innov_factors.append(f"Moderate R&D: {financials.rd_to_revenue:.1f}%")
            
            # CapEx Investment (max +15)
            if financials.capex_to_revenue and financials.capex_to_revenue > 10:
                innov_score += 15
                innov_factors.append(f"High CapEx: {financials.capex_to_revenue:.1f}%")
            elif financials.capex_to_revenue and financials.capex_to_revenue > 5:
                innov_score += 5
                innov_factors.append(f"Moderate CapEx: {financials.capex_to_revenue:.1f}%")
            
            # Tech sector bonus
            sector = info.get('sector', '')
            if sector in ['Technology', 'Healthcare', 'Biotechnology', 'Communications']:
                innov_score += 10
                innov_factors.append("Innovation sector")
            
            financials.innovation_score = max(0, min(100, innov_score))
            financials.innovation_explanation = "; ".join(innov_factors) if innov_factors else "Standard innovation level"
            
        except Exception as e:
            financials.health_explanation = f"Financial data unavailable: {str(e)[:50]}"
        
        return financials
