#!/usr/bin/env python3
"""
OKX Data Adapter for AI Hedge Fund Skill

将 OKX 的数字货币数据转换为统一格式，供所有投资大师分析
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Optional
import os

# Try to load dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, use environment variables directly

# OKX API 配置
API_KEY = os.getenv('OKX_API_KEY', '')
API_SECRET = os.getenv('OKX_API_SECRET', '')
BASE_URL = "https://www.okx.com"


class OKXDataAdapter:
    """
    OKX 数字货币数据适配器
    
    将 OKX API 返回的数据转换为统一的格式，
    供 Phase 1 和 Phase 2 的所有 Agent 使用
    """
    
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or API_KEY
        self.api_secret = api_secret or API_SECRET
        self.base_url = BASE_URL
        self.session = requests.Session()
        
        # 公共数据不需要 API key
        self.use_auth = bool(self.api_key and self.api_secret)
    
    def get_ticker_info(self, symbol: str) -> Dict:
        """
        获取单个交易对的实时信息
        
        Args:
            symbol: 交易对，如 "BTC-USDT", "NVDA-USDT-SWAP"
        
        Returns:
            Dict: 包含价格、24h变化、成交量等
        """
        # 首先尝试 SPOT，如果不存在则尝试 SWAP
        for inst_id in [symbol, f"{symbol}-SWAP"]:
            url = f"{self.base_url}/api/v5/market/ticker"
            params = {"instId": inst_id}
            
            try:
                response = self.session.get(url, params=params, timeout=10)
                data = response.json()
                
                if data.get("code") == "0" and data.get("data"):
                    ticker = data["data"][0]
                    return {
                        "symbol": inst_id,
                        "inst_type": "SWAP" if "-SWAP" in inst_id else "SPOT",
                        "last_price": float(ticker.get("last", 0)),
                        "bid_price": float(ticker.get("bidPx", 0)),
                        "ask_price": float(ticker.get("askPx", 0)),
                        "volume_24h": float(ticker.get("vol24h", 0)),
                        "turnover_24h": float(ticker.get("volCcy24h", 0)),
                        "high_24h": float(ticker.get("high24h", 0)),
                        "low_24h": float(ticker.get("low24h", 0)),
                        "change_24h_pct": float(ticker.get("sodUtc0", 0)) if ticker.get("sodUtc0") else 0,
                        "open_price": float(ticker.get("open24h", 0)),
                        "timestamp": datetime.now().isoformat()
                    }
            except Exception as e:
                print(f"Error fetching ticker {inst_id}: {e}")
        
        return {"symbol": symbol, "error": "Failed to fetch data"}
    
    def get_klines(self, symbol: str, bar: str = "4H", limit: int = 300) -> Optional[pd.DataFrame]:
        """
        获取 K线数据
        
        Args:
            symbol: 交易对，如 "BTC-USDT", "NVDA-USDT-SWAP"
            bar: K线周期，如 "1m", "5m", "1H", "4H", "1D"
            limit: 返回数据条数，最大 300
        
        Returns:
            pd.DataFrame: K线数据
        """
        # 首先尝试 SPOT，如果不存在则尝试 SWAP
        for inst_id in [symbol, f"{symbol}-SWAP"]:
            url = f"{self.base_url}/api/v5/market/history-candles"
            params = {"instId": inst_id, "bar": bar, "limit": limit}
            
            try:
                response = self.session.get(url, params=params, timeout=30)
                data = response.json()
                
                if data.get("code") == "0" and data.get("data"):
                    # OKX K线返回9列: timestamp, open, high, low, close, vol, vol_ccy, vol_ccy_quote, confirm
                    columns = [
                        "timestamp", "open", "high", "low", "close",
                        "volume", "volume_ccy", "volume_quote", "confirm"
                    ]
                    df = pd.DataFrame(data["data"], columns=columns)
                    
                    # 转换数据类型
                    df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
                    for col in ["open", "high", "low", "close", "volume"]:
                        df[col] = df[col].astype(float)
                    
                    return df.sort_values("timestamp").reset_index(drop=True)
            except Exception as e:
                print(f"Error fetching klines {inst_id}: {e}")
        
        return None
    
    def calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """
        计算技术指标
        
        Returns:
            Dict: 包含各种技术指标的值
        """
        if df is None or len(df) < 20:
            return {}
        
        latest = df.iloc[-1]
        indicators = {}
        
        # 基础价格数据
        indicators["current_price"] = latest["close"]
        indicators["open_price"] = latest["open"]
        indicators["high_price"] = latest["high"]
        indicators["low_price"] = latest["low"]
        indicators["volume"] = latest["volume"]
        
        # 均线
        for period in [5, 10, 20, 30, 60, 120, 200]:
            if len(df) >= period:
                df[f"MA{period}"] = df["close"].rolling(window=period).mean()
                indicators[f"MA{period}"] = df[f"MA{period}"].iloc[-1]
        
        # EMA
        for period in [7, 12, 25, 99]:
            if len(df) >= period:
                df[f"EMA{period}"] = df["close"].ewm(span=period, adjust=False).mean()
                indicators[f"EMA{period}"] = df[f"EMA{period}"].iloc[-1]
        
        # MACD
        if len(df) >= 26:
            ema12 = df["close"].ewm(span=12, adjust=False).mean()
            ema26 = df["close"].ewm(span=26, adjust=False).mean()
            df["MACD"] = ema12 - ema26
            df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
            df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
            
            indicators["MACD"] = df["MACD"].iloc[-1]
            indicators["MACD_Signal"] = df["MACD_Signal"].iloc[-1]
            indicators["MACD_Hist"] = df["MACD_Hist"].iloc[-1]
        
        # RSI
        if len(df) >= 14:
            delta = df["close"].diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df["RSI"] = 100 - (100 / (1 + rs))
            indicators["RSI"] = df["RSI"].iloc[-1]
        
        # Bollinger Bands
        if len(df) >= 20:
            df["BB_MA"] = df["close"].rolling(window=20).mean()
            df["BB_std"] = df["close"].rolling(window=20).std()
            df["BB_upper"] = df["BB_MA"] + 2 * df["BB_std"]
            df["BB_lower"] = df["BB_MA"] - 2 * df["BB_std"]
            indicators["BB_upper"] = df["BB_upper"].iloc[-1]
            indicators["BB_MA"] = df["BB_MA"].iloc[-1]
            indicators["BB_lower"] = df["BB_lower"].iloc[-1]
        
        # ATR (Average True Range)
        if len(df) >= 14:
            high_low = df["high"] - df["low"]
            high_close = np.abs(df["high"] - df["close"].shift())
            low_close = np.abs(df["low"] - df["close"].shift())
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            df["ATR"] = true_range.rolling(window=14).mean()
            indicators["ATR"] = df["ATR"].iloc[-1]
            # ATR as percentage of price
            indicators["atr_percent"] = (indicators["ATR"] / indicators["current_price"]) * 100
        
        # 波动率
        if len(df) >= 20:
            returns = df["close"].pct_change()
            indicators["volatility_20d"] = returns.rolling(window=20).std() * np.sqrt(365) * 100
        
        # 成交量变化
        if len(df) >= 5:
            indicators["volume_ma5"] = df["volume"].rolling(window=5).mean().iloc[-1]
            indicators["volume_ratio"] = indicators["volume"] / indicators["volume_ma5"] if indicators["volume_ma5"] > 0 else 1
        
        # 均线交叉信号
        indicators["ma_cross_gold"] = False
        indicators["ma_cross_death"] = False
        if "MA20" in indicators and "MA50" in indicators:
            if len(df) >= 51:
                ma20_prev = df["MA20"].iloc[-2]
                ma50_prev = df["MA50"].iloc[-2]
                ma20_curr = indicators["MA20"]
                ma50_curr = indicators["MA50"]
                if ma20_prev < ma50_prev and ma20_curr > ma50_curr:
                    indicators["ma_cross_gold"] = True
                elif ma20_prev > ma50_prev and ma20_curr < ma50_curr:
                    indicators["ma_cross_death"] = True
        
        # 趋势方向
        indicators["trend_direction"] = "neutral"
        if "MA20" in indicators and "MA50" in indicators and "MA200" in indicators:
            price = indicators["current_price"]
            if price > indicators["MA20"] > indicators["MA50"] > indicators["MA200"]:
                indicators["trend_direction"] = "up"
            elif price < indicators["MA20"] < indicators["MA50"] < indicators["MA200"]:
                indicators["trend_direction"] = "down"
        
        # 支撑阻力（基于近期高低点）
        if len(df) >= 20:
            indicators["resistance_20d"] = df["high"].rolling(window=20).max().iloc[-1]
            indicators["support_20d"] = df["low"].rolling(window=20).min().iloc[-1]
        
        return indicators
    
    def get_complete_analysis_data(self, symbol: str, bar: str = "4H") -> Dict:
        """
        获取完整的分析数据
        
        Args:
            symbol: 交易对，如 "BTC-USDT"
            bar: K线周期
        
        Returns:
            Dict: 包含 ticker info + indicators，可直接传给 Agent 分析
        """
        # 获取 K线数据
        df = self.get_klines(symbol, bar=bar, limit=300)
        
        # 计算技术指标
        indicators = self.calculate_indicators(df)
        
        # 获取实时行情
        ticker = self.get_ticker_info(symbol)
        
        # 合并数据
        result = {
            "symbol": symbol,
            "asset_type": "crypto",
            "exchange": "OKX",
            "timestamp": datetime.now().isoformat(),
            "timeframe": bar,
            
            # 基础价格数据
            "current_price": indicators.get("current_price", ticker.get("last_price", 0)),
            "bid_price": ticker.get("bid_price", 0),
            "ask_price": ticker.get("ask_price", 0),
            "open_price": indicators.get("open_price", 0),
            "high_price": indicators.get("high_price", 0),
            "low_price": indicators.get("low_price", 0),
            "volume": indicators.get("volume", 0),
            "volume_ratio": indicators.get("volume_ratio", 1),
            
            # 24h 变化
            "change_24h_pct": ticker.get("change_24h_pct", 0),
            "high_24h": ticker.get("high_24h", 0),
            "low_24h": ticker.get("low_24h", 0),
            
            # 均线
            "MA5": indicators.get("MA5", 0),
            "MA10": indicators.get("MA10", 0),
            "MA20": indicators.get("MA20", 0),
            "MA30": indicators.get("MA30", 0),
            "MA60": indicators.get("MA60", 0),
            "MA120": indicators.get("MA120", 0),
            "MA200": indicators.get("MA200", 0),
            
            # 均线交叉
            "ma_cross_gold": indicators.get("ma_cross_gold", False),
            "ma_cross_death": indicators.get("ma_cross_death", False),
            
            # MACD
            "MACD": indicators.get("MACD", 0),
            "MACD_Signal": indicators.get("MACD_Signal", 0),
            "MACD_Hist": indicators.get("MACD_Hist", 0),
            
            # RSI
            "RSI": indicators.get("RSI", 50),
            
            # Bollinger Bands
            "BB_upper": indicators.get("BB_upper", 0),
            "BB_MA": indicators.get("BB_MA", 0),
            "BB_lower": indicators.get("BB_lower", 0),
            
            # ATR
            "ATR": indicators.get("ATR", 0),
            "atr_percent": indicators.get("atr_percent", 5),
            
            # 趋势
            "trend_direction": indicators.get("trend_direction", "neutral"),
            
            # 支撑阻力
            "resistance_20d": indicators.get("resistance_20d", 0),
            "support_20d": indicators.get("support_20d", 0),
            
            # 波动率
            "volatility_20d": indicators.get("volatility_20d", 0),
            
            # 市场数据（用于宏观分析）
            "market_cap": 0,  # Crypto 没有统一的市值
            "beta": 1.0,  # Crypto 默认 beta
            "pe_ratio": 0,  # Crypto 没有 P/E
            
            # 用于 Ray Dalio 的宏观数据（需要额外数据源）
            "inflation_trend": "neutral",
            "growth_trend": "neutral",
            "vix": 0,  # Crypto 没有 VIX，用 0
        }
        
        return result


def analyze_crypto(ticker: str, timeframe: str = "4H") -> Dict:
    """
    便捷函数：分析数字货币
    
    Args:
        ticker: 交易对，如 "BTC-USDT"
        timeframe: 时间周期，如 "1H", "4H", "1D"
    
    Returns:
        Dict: 完整的分析数据
    """
    adapter = OKXDataAdapter()
    return adapter.get_complete_analysis_data(ticker, bar=timeframe)


if __name__ == "__main__":
    # 测试
    print("=== Testing OKX Data Adapter ===")
    adapter = OKXDataAdapter()
    
    # 测试获取 BTC 数据
    print("\nFetching BTC-USDT data...")
    data = adapter.get_complete_analysis_data("BTC-USDT", bar="4H")
    
    print(f"\nSymbol: {data['symbol']}")
    print(f"Current Price: ${data['current_price']:.2f}")
    print(f"RSI: {data['RSI']:.1f}")
    print(f"MACD: {data['MACD']:.2f}")
    print(f"Trend: {data['trend_direction']}")
    print(f"ATR %: {data['atr_percent']:.2f}%")
