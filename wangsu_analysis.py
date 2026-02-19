#!/usr/bin/env python3
"""
网宿科技 (300017) - 快速分析
使用AKShare直接获取个股数据
"""

import sys

try:
    import akshare as ak
    import pandas as pd
    
    ticker = "300017"
    
    print("\n" + "="*70)
    print("🇨🇳 网宿科技 (300017) 快速分析")
    print("="*70 + "\n")
    
    # Method 1: Get individual stock info
    print("📋 获取公司基本信息...")
    try:
        info_df = ak.stock_individual_info_em(symbol=ticker)
        if not info_df.empty:
            info = dict(zip(info_df['item'], info_df['value']))
            print(f"  股票名称: {info.get('股票简称', '网宿科技')}")
            print(f"  所属行业: {info.get('行业', '未知')}")
            print(f"  总市值: {info.get('总市值', 'N/A')}")
            print(f"  流通市值: {info.get('流通市值', 'N/A')}")
            print(f"  上市时间: {info.get('上市时间', 'N/A')}")
    except Exception as e:
        print(f"  公司信息获取失败: {e}")
    
    print("")
    
    # Method 2: Get real-time quote
    print("💹 获取实时行情...")
    try:
        # Use individual stock real-time quote
        quote_df = ak.stock_zh_a_hist(symbol=ticker, period="daily", start_date="20250217", adjust="qfq")
        if not quote_df.empty:
            latest = quote_df.iloc[-1]
            prev = quote_df.iloc[-2] if len(quote_df) > 1 else latest
            
            close = float(latest['收盘'])
            prev_close = float(prev['收盘'])
            change_pct = (close - prev_close) / prev_close * 100
            
            emoji = "🟢" if change_pct > 0 else "🔴"
            print(f"  最新价格: ¥{close:.2f}")
            print(f"  {emoji} 涨跌幅: {change_pct:+.2f}%")
            print(f"  今日最高: ¥{float(latest['最高']):.2f}")
            print(f"  今日最低: ¥{float(latest['最低']):.2f}")
            print(f"  成交量: {float(latest['成交量'])/10000:.2f}万手")
            print(f"  成交额: {float(latest['成交额'])/10000:.2f}万元")
    except Exception as e:
        print(f"  行情获取失败: {e}")
    
    print("")
    
    # Method 3: Get financial indicators
    print("💰 获取财务指标...")
    try:
        fin_df = ak.stock_financial_analysis_indicator(symbol=ticker)
        if not fin_df.empty:
            latest = fin_df.iloc[0]
            print(f"  净资产收益率(ROE): {latest.get('净资产收益率(%)', 'N/A')}%")
            print(f"  销售毛利率: {latest.get('销售毛利率(%)', 'N/A')}%")
            print(f"  销售净利率: {latest.get('销售净利率(%)', 'N/A')}%")
            print(f"  资产负债率: {latest.get('资产负债率(%)', 'N/A')}%")
    except Exception as e:
        print(f"  财务指标获取失败: {e}")
    
    print("")
    
    # Method 4: Get news
    print("📰 获取最新新闻...")
    try:
        news_df = ak.stock_news_em(symbol=ticker)
        if not news_df.empty:
            print(f"  最新5条新闻:")
            for i, (_, row) in enumerate(news_df.head(5).iterrows(), 1):
                title = row['标题'][:40] + "..." if len(row['标题']) > 40 else row['标题']
                print(f"    {i}. {title}")
                print(f"       来源: {row['来源']} | {row['发布时间']}")
    except Exception as e:
        print(f"  新闻获取失败: {e}")
    
    print("")
    print("="*70)
    print("💡 数据来源: 东方财富 (AKShare)")
    print("⚠️  仅供参考，不构成投资建议")
    print("="*70 + "\n")
    
except ImportError:
    print("❌ 请先安装AKShare: pip install akshare")
except Exception as e:
    print(f"❌ 分析出错: {e}")
    import traceback
    traceback.print_exc()
