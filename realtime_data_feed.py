#!/usr/bin/env python3
"""
实时数据接入层 - WebSocket行情订阅
支持OKX实时数据，自动缓存，增量更新
"""

import websocket
import json
import threading
import time
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
import redis
import os


@dataclass
class TickData:
    """实时tick数据"""
    symbol: str
    price: float
    bid: float
    ask: float
    volume_24h: float
    high_24h: float
    low_24h: float
    timestamp: datetime
    change_24h: float = 0.0


@dataclass
class KlineData:
    """K线数据"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    timeframe: str = "1m"


class OKXWebSocketFeed:
    """
    OKX WebSocket实时行情接入
    
    使用示例:
        feed = OKXWebSocketFeed()
        feed.subscribe(["NVDA-USDT-SWAP", "BTC-USDT"])
        feed.on_tick = lambda tick: print(f"{tick.symbol}: {tick.price}")
        feed.start()
    """
    
    OKX_WS_URL = "wss://ws.okx.com:8443/ws/v5/public"
    
    def __init__(self, use_redis: bool = False):
        self.ws: Optional[websocket.WebSocketApp] = None
        self.subscriptions: set = set()
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
        # 回调函数
        self.on_tick: Optional[Callable[[TickData], None]] = None
        self.on_kline: Optional[Callable[[KlineData], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        
        # 本地缓存
        self.tick_cache: Dict[str, TickData] = {}
        self.kline_cache: Dict[str, List[KlineData]] = {}
        
        # Redis缓存（可选）- [P1 FIX] 真正测试连接
        self.redis_client = None
        if use_redis:
            try:
                # 使用环境变量配置，支持自定义
                redis_host = os.getenv('REDIS_HOST', 'localhost')
                redis_port = int(os.getenv('REDIS_PORT', 6379))
                redis_db = int(os.getenv('REDIS_DB', 0))
                
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    socket_connect_timeout=5,  # 连接超时5秒
                    socket_timeout=5           # 操作超时5秒
                )
                # 真正测试连接（构造时不会实际连接）
                self.redis_client.ping()
                print(f"✅ Redis连接成功: {redis_host}:{redis_port}/{redis_db}")
            except (redis.ConnectionError, redis.TimeoutError) as e:
                print(f"⚠️ Redis连接失败: {e}，使用内存缓存")
                self.redis_client = None
            except Exception as e:
                print(f"⚠️ Redis初始化错误: {e}，使用内存缓存")
                self.redis_client = None
    
    def subscribe(self, symbols: List[str]):
        """订阅交易对"""
        self.subscriptions.update(symbols)
        if self.ws and self.ws.sock and self.ws.sock.connected:
            self._send_subscriptions()
    
    def unsubscribe(self, symbols: List[str]):
        """取消订阅"""
        for symbol in symbols:
            self.subscriptions.discard(symbol)
    
    def _send_subscriptions(self):
        """发送订阅请求"""
        # 订阅tick行情
        tick_sub = {
            "op": "subscribe",
            "args": [{"channel": "tickers", "instId": s} for s in self.subscriptions]
        }
        self.ws.send(json.dumps(tick_sub))
        
        # 订阅1分钟K线
        kline_sub = {
            "op": "subscribe",
            "args": [{"channel": "candle1m", "instId": s} for s in self.subscriptions]
        }
        self.ws.send(json.dumps(kline_sub))
    
    def _on_message(self, ws, message):
        """处理WebSocket消息"""
        try:
            data = json.loads(message)
            
            # 处理tick数据
            if "arg" in data and data["arg"].get("channel") == "tickers":
                self._handle_tick(data["data"][0])
            
            # 处理K线数据
            elif "arg" in data and "candle" in data["arg"].get("channel", ""):
                self._handle_kline(data["data"][0], data["arg"]["channel"], data["arg"])
                
        except Exception as e:
            if self.on_error:
                self.on_error(e)
    
    def _handle_tick(self, data: dict):
        """处理tick数据"""
        tick = TickData(
            symbol=data["instId"],
            price=float(data["last"]),
            bid=float(data["bidPx"]),
            ask=float(data["askPx"]),
            volume_24h=float(data["vol24h"]),
            high_24h=float(data["high24h"]),
            low_24h=float(data["low24h"]),
            timestamp=datetime.now(),
            change_24h=float(data["last"]) - float(data.get("open24h", 0))
        )
        
        # 更新缓存
        self.tick_cache[tick.symbol] = tick
        
        # Redis缓存
        if self.redis_client:
            self.redis_client.setex(
                f"tick:{tick.symbol}",
                60,  # 60秒过期
                json.dumps({
                    "price": tick.price,
                    "timestamp": tick.timestamp.isoformat()
                })
            )
        
        # 触发回调
        if self.on_tick:
            self.on_tick(tick)
    
    def _handle_kline(self, data: list, channel: str, arg: dict):
        """处理K线数据"""
        # 解析timeframe
        timeframe = channel.replace("candle", "")
        
        # 从arg获取symbol，而不是从data[0]
        symbol = arg.get("instId", "unknown")
        
        kline = KlineData(
            symbol=symbol,
            timestamp=datetime.fromtimestamp(int(data[0])/1000),
            open=float(data[1]),
            high=float(data[2]),
            low=float(data[3]),
            close=float(data[4]),
            volume=float(data[5]),
            timeframe=timeframe
        )
        
        # 更新缓存
        key = f"{kline.symbol}:{timeframe}"
        if key not in self.kline_cache:
            self.kline_cache[key] = []
        self.kline_cache[key].append(kline)
        
        # 只保留最近1000根
        self.kline_cache[key] = self.kline_cache[key][-1000:]
        
        # 触发回调
        if self.on_kline:
            self.on_kline(kline)
    
    def _on_open(self, ws):
        """连接建立"""
        print(f"✅ OKX WebSocket连接成功")
        self._send_subscriptions()
    
    def _on_error(self, ws, error):
        """错误处理"""
        print(f"❌ WebSocket错误: {error}")
        if self.on_error:
            self.on_error(error)
    
    def _on_close(self, ws, close_status_code, close_msg):
        """连接关闭"""
        print(f"⚠️ WebSocket连接关闭: {close_status_code} - {close_msg}")
        self.running = False
    
    def start(self):
        """启动WebSocket连接"""
        self.running = True
        
        self.ws = websocket.WebSocketApp(
            self.OKX_WS_URL,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        
        # 在后台线程运行
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """停止WebSocket连接"""
        self.running = False
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join(timeout=5)
    
    def get_latest_tick(self, symbol: str) -> Optional[TickData]:
        """获取最新tick"""
        return self.tick_cache.get(symbol)
    
    def get_klines(self, symbol: str, timeframe: str = "1m", limit: int = 100) -> List[KlineData]:
        """获取K线历史"""
        key = f"{symbol}:{timeframe}"
        klines = self.kline_cache.get(key, [])
        return klines[-limit:]


class DataFeedManager:
    """
    数据接入管理器 - 统一接口
    """
    
    def __init__(self):
        self.okx_feed = OKXWebSocketFeed(use_redis=False)
        self.data_callbacks: List[Callable] = []
    
    def start(self, symbols: List[str]):
        """启动数据接入"""
        self.okx_feed.subscribe(symbols)
        self.okx_feed.on_tick = self._on_tick
        self.okx_feed.start()
        print(f"🚀 数据接入启动 - 订阅: {symbols}")
    
    def _on_tick(self, tick: TickData):
        """内部tick处理"""
        for callback in self.data_callbacks:
            try:
                callback(tick)
            except Exception as e:
                print(f"⚠️ 回调错误: {e}")
    
    def register_callback(self, callback: Callable[[TickData], None]):
        """注册数据回调"""
        self.data_callbacks.append(callback)
    
    def get_price(self, symbol: str) -> Optional[float]:
        """获取最新价格"""
        tick = self.okx_feed.get_latest_tick(symbol)
        return tick.price if tick else None


# 便捷函数
def create_data_feed() -> DataFeedManager:
    """工厂函数"""
    return DataFeedManager()


if __name__ == "__main__":
    # 测试
    feed = OKXWebSocketFeed()
    feed.subscribe(["NVDA-USDT-SWAP"])
    
    @feed.on_tick
    def on_tick(tick):
        print(f"{tick.symbol}: ${tick.price} | 24h: {tick.change_24h:+.2f}%")
    
    feed.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        feed.stop()
        print("\n✅ 已停止")
