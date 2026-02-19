"""
🇨🇳 China News Adapter
Fetches news from Chinese financial media
"""

import re
import json
import urllib.request
import urllib.parse
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ChinaNewsItem:
    """Chinese news item"""
    title: str
    content: str
    source: str
    publish_time: str
    url: str = ""
    sentiment: str = "neutral"
    relevance_score: float = 0.0


class ChinaNewsAdapter:
    """Adapter for Chinese financial news sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    def _fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL content"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Fetch error: {e}", file=sys.stderr)
            return None
    
    def search_sina_finance(self, keyword: str, count: int = 10) -> List[ChinaNewsItem]:
        """Search news from Sina Finance"""
        news_items = []
        
        try:
            # Sina Finance search API
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"https://search.sina.com.cn/?q={encoded_keyword}&c=finance&from=channel&ie=utf-8"
            
            html = self._fetch_url(url)
            if not html:
                return news_items
            
            # Parse news items (simple regex-based parsing)
            # Note: This is a simplified version. Real implementation might need BeautifulSoup
            pattern = r'<h2><a[^>]*href="([^"]*)"[^>]*>(.*?)</a></h2>'
            matches = re.findall(pattern, html)
            
            for i, (url, title) in enumerate(matches[:count]):
                # Clean HTML tags
                title = re.sub(r'<[^>]+>', '', title).strip()
                if title:
                    item = ChinaNewsItem(
                        title=title,
                        content="",
                        source="新浪财经",
                        publish_time="最近",
                        url=url if url.startswith('http') else f"https:{url}"
                    )
                    news_items.append(item)
            
        except Exception as e:
            print(f"Sina Finance error: {e}", file=sys.stderr)
        
        return news_items
    
    def search_eastmoney(self, keyword: str, count: int = 10) -> List[ChinaNewsItem]:
        """Search news from Eastmoney"""
        news_items = []
        
        try:
            # Eastmoney news API
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"https://searchapi.eastmoney.com/api/suggest/get?input={encoded_keyword}&type=14&count={count}"
            
            html = self._fetch_url(url)
            if not html:
                return news_items
            
            # Try to parse JSON response
            try:
                data = json.loads(html)
                if 'QuotationCodeTable' in data and 'Data' in data['QuotationCodeTable']:
                    for item_data in data['QuotationCodeTable']['Data'][:count]:
                        item = ChinaNewsItem(
                            title=item_data.get('Name', ''),
                            content="",
                            source="东方财富",
                            publish_time="最近",
                            url=f"https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/Index?type=web&code={item_data.get('Code', '')}"
                        )
                        news_items.append(item)
            except:
                pass
            
            # Fallback: Use Eastmoney news list API
            try:
                # Get latest news for the stock
                stock_code = keyword
                if '.' in stock_code:
                    stock_code = stock_code.split('.')[0]
                
                # Determine market prefix
                if stock_code.startswith('6'):
                    code_prefix = 'SH' + stock_code
                else:
                    code_prefix = 'SZ' + stock_code
                
                news_url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_FCI_MainData&columns=SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,NOTICE_DATE,NOTICE_TITLE&filter=(SECUCODE%3D%22{code_prefix}%22)"
                
                news_html = self._fetch_url(news_url)
                if news_html:
                    news_data = json.loads(news_html)
                    if 'result' in news_data and 'data' in news_data['result']:
                        for news_item in news_data['result']['data'][:count]:
                            item = ChinaNewsItem(
                                title=news_item.get('NOTICE_TITLE', ''),
                                content="",
                                source="东方财富",
                                publish_time=news_item.get('NOTICE_DATE', ''),
                                url=""
                            )
                            news_items.append(item)
            except Exception as e:
                print(f"Eastmoney news error: {e}", file=sys.stderr)
            
        except Exception as e:
            print(f"Eastmoney error: {e}", file=sys.stderr)
        
        return news_items
    
    def get_stock_news_akshare(self, ticker: str, count: int = 10) -> List[ChinaNewsItem]:
        """Get stock news using AKShare"""
        news_items = []
        
        try:
            import akshare as ak
            
            ticker_clean = ticker.upper().replace('.SZ', '').replace('.SH', '')
            
            # Get stock news
            try:
                df = ak.stock_news_em(symbol=ticker_clean)
                if not df.empty:
                    for _, row in df.head(count).iterrows():
                        item = ChinaNewsItem(
                            title=row.get('标题', ''),
                            content=row.get('内容', '')[:500],
                            source=row.get('来源', ''),
                            publish_time=row.get('发布时间', ''),
                            url=row.get('链接', '')
                        )
                        
                        # Simple sentiment analysis
                        title_content = item.title + item.content
                        if any(word in title_content for word in ['涨停', '大涨', '突破', '利好', '增长', '盈利']):
                            item.sentiment = 'positive'
                        elif any(word in title_content for word in ['跌停', '大跌', '下跌', '利空', '亏损', '暴雷']):
                            item.sentiment = 'negative'
                        
                        news_items.append(item)
            except Exception as e:
                print(f"AKShare news error: {e}", file=sys.stderr)
            
        except ImportError:
            print("AKShare not available", file=sys.stderr)
        
        return news_items
    
    def get_industry_news(self, industry: str, count: int = 10) -> List[ChinaNewsItem]:
        """Get industry-related news"""
        news_items = []
        
        try:
            import akshare as ak
            
            # Map industry names
            industry_map = {
                'CDN': '互联网服务',
                '云计算': '互联网服务',
                '软件': '软件开发',
                '半导体': '半导体',
                '医药': '医药制造',
                '银行': '银行',
                '保险': '保险',
                '券商': '证券',
                '新能源': '新能源',
                '汽车': '汽车整车',
                '房地产': '房地产开发',
            }
            
            chinese_name = industry_map.get(industry, industry)
            
            # Try to get industry news
            try:
                df = ak.stock_sector_fund_flow_rank()
                if not df.empty:
                    # Add some industry-level insights
                    item = ChinaNewsItem(
                        title=f"{chinese_name}行业资金流向分析",
                        content="行业资金流入/流出情况",
                        source="东方财富",
                        publish_time="最近"
                    )
                    news_items.append(item)
            except:
                pass
            
        except ImportError:
            pass
        
        return news_items
    
    def get_major_news(self, count: int = 20) -> List[ChinaNewsItem]:
        """Get major financial news"""
        news_items = []
        
        try:
            import akshare as ak
            
            # Get major news
            try:
                df = ak.stock_zt_pool_em(date="20240218")
                # This gets limit-up stocks, indicating market sentiment
            except:
                pass
            
            # Get market overview news
            try:
                df = ak.stock_zh_index_daily(symbol="sh000001")  # 上证指数
                # Could use this for market trend analysis
            except:
                pass
            
        except ImportError:
            pass
        
        return news_items
    
    def analyze_news(self, news_items: List[ChinaNewsItem]) -> Dict:
        """Analyze news sentiment and extract key information"""
        if not news_items:
            return {
                'sentiment': 'neutral',
                'sentiment_score': 0.0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'key_topics': [],
                'summary': '无相关新闻'
            }
        
        # Count sentiments
        positive = sum(1 for n in news_items if n.sentiment == 'positive')
        negative = sum(1 for n in news_items if n.sentiment == 'negative')
        neutral = len(news_items) - positive - negative
        
        # Calculate score
        total = len(news_items)
        if total > 0:
            score = (positive - negative) / total
        else:
            score = 0.0
        
        # Determine overall sentiment
        if score > 0.2:
            sentiment = 'positive'
        elif score < -0.2:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Extract key topics (simple keyword extraction)
        all_text = ' '.join([n.title for n in news_items])
        
        # Common financial keywords
        keywords = ['业绩', '增长', '盈利', '亏损', '订单', '合作', '扩张', 
                   '裁员', '重组', '并购', 'IPO', '分红', '财报', '展望']
        
        key_topics = []
        for kw in keywords:
            if kw in all_text:
                key_topics.append(kw)
        
        # Create summary
        if positive > negative:
            summary = f"新闻偏向正面 ({positive}/{total}正面)"
        elif negative > positive:
            summary = f"新闻偏向负面 ({negative}/{total}负面)"
        else:
            summary = f"新闻情绪中性 ({neutral}/{total}中性)"
        
        return {
            'sentiment': sentiment,
            'sentiment_score': score,
            'positive_count': positive,
            'negative_count': negative,
            'neutral_count': neutral,
            'key_topics': key_topics[:5],
            'summary': summary,
            'total_news': total
        }
    
    def get_stock_news_report(self, ticker: str, name: str = "") -> Dict:
        """Generate comprehensive news report for a stock"""
        all_news = []
        
        # Get stock-specific news
        stock_news = self.get_stock_news_akshare(ticker, count=10)
        all_news.extend(stock_news)
        
        # Search by name if provided
        if name:
            sina_news = self.search_sina_finance(name, count=5)
            all_news.extend(sina_news)
            
            eastmoney_news = self.search_eastmoney(name, count=5)
            all_news.extend(eastmoney_news)
        
        # Deduplicate
        seen_titles = set()
        unique_news = []
        for news in all_news:
            if news.title not in seen_titles:
                seen_titles.add(news.title)
                unique_news.append(news)
        
        # Analyze
        analysis = self.analyze_news(unique_news)
        
        return {
            'ticker': ticker,
            'name': name,
            'analysis': analysis,
            'news_items': unique_news[:10],
            'sources': list(set(n.source for n in unique_news))
        }


# Standalone test
if __name__ == "__main__":
    adapter = ChinaNewsAdapter()
    
    # Test with 网宿科技
    print("Fetching Chinese news for 网宿科技 (300017)...")
    report = adapter.get_stock_news_report("300017", "网宿科技")
    
    print(f"\n新闻分析:")
    print(f"总体情感: {report['analysis']['sentiment']}")
    print(f"情感得分: {report['analysis']['sentiment_score']:.2f}")
    print(f"正面新闻: {report['analysis']['positive_count']}")
    print(f"负面新闻: {report['analysis']['negative_count']}")
    print(f"关键话题: {', '.join(report['analysis']['key_topics'])}")
    
    print(f"\n最新新闻:")
    for i, news in enumerate(report['news_items'][:5], 1):
        print(f"{i}. [{news.sentiment}] {news.title}")
        print(f"   来源: {news.source} | {news.publish_time}")
