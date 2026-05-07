"""市场服务"""
from models import db, Stock, KlineData
from datetime import datetime, timedelta
import random


class MarketService:
    """市场服务类"""
    
    @staticmethod
    def get_stocks() -> dict:
        """
        获取股票列表
        返回: {'success': bool, 'stocks': list, 'message': str}
        """
        stocks = Stock.query.all()
        
        return {
            'success': True,
            'stocks': stocks,
            'message': '获取成功'
        }
    
    @staticmethod
    def get_stock(code: str) -> dict:
        """
        获取单个股票信息
        返回: {'success': bool, 'stock': Stock, 'message': str}
        """
        stock = Stock.query.filter_by(code=code).first()
        
        if not stock:
            return {'success': False, 'message': '股票不存在'}
        
        return {
            'success': True,
            'stock': stock,
            'message': '获取成功'
        }
    
    @staticmethod
    def get_kline(code: str) -> dict:
        """
        获取K线数据
        返回: {'success': bool, 'klines': list, 'message': str}
        """
        klines = KlineData.query.filter_by(code=code).order_by(KlineData.time).all()
        
        if not klines:
            # 生成模拟K线数据
            klines = []
            base_price = 100
            now = datetime.utcnow()
            
            for i in range(60):
                time = now - timedelta(days=60-i)
                change = random.uniform(-5, 5)
                open_price = base_price
                close_price = base_price + change
                high_price = max(open_price, close_price) + random.uniform(0, 3)
                low_price = min(open_price, close_price) - random.uniform(0, 3)
                
                kline = KlineData(
                    code=code,
                    time=time,
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    close=close_price,
                    volume=random.randint(1000000, 10000000),
                )
                klines.append(kline)
                base_price = close_price
            
            db.session.add_all(klines)
            db.session.commit()
        
        return {
            'success': True,
            'klines': klines,
            'message': '获取成功'
        }
