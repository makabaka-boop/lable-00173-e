from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    balance = db.Column(db.Float, default=200000.0)
    total_assets = db.Column(db.Float, default=500000.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    positions = db.relationship('Position', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    trades = db.relationship('Trade', backref='user', lazy=True, cascade='all, delete-orphan')
    backtests = db.relationship('Backtest', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'bio': self.bio,
            'avatar': self.avatar,
            'balance': self.balance,
            'totalAssets': self.total_assets,
            'createdAt': int(self.created_at.timestamp() * 1000),
        }

class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    change = db.Column(db.Float, default=0.0)
    change_percent = db.Column(db.Float, default=0.0)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, default=0)
    market_cap = db.Column(db.BigInteger, default=0)
    pe = db.Column(db.Float, default=0.0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'price': self.price,
            'change': self.change,
            'changePercent': self.change_percent,
            'high': self.high,
            'low': self.low,
            'volume': self.volume,
            'marketCap': self.market_cap,
            'pe': self.pe,
            'timestamp': int(self.updated_at.timestamp() * 1000),
        }

class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        profit = (self.current_price - self.cost_price) * self.quantity
        profit_percent = ((self.current_price - self.cost_price) / self.cost_price * 100) if self.cost_price > 0 else 0
        market_value = self.current_price * self.quantity
        
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'quantity': self.quantity,
            'costPrice': self.cost_price,
            'currentPrice': self.current_price,
            'profit': profit,
            'profitPercent': profit_percent,
            'marketValue': market_value,
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # buy or sell
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    executed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type,
            'quantity': self.quantity,
            'price': self.price,
            'totalAmount': self.total_amount,
            'status': self.status,
            'timestamp': int(self.created_at.timestamp() * 1000),
            'executedTime': int(self.executed_at.timestamp() * 1000) if self.executed_at else None,
        }

class Trade(db.Model):
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # buy or sell
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type,
            'quantity': self.quantity,
            'price': self.price,
            'totalAmount': self.total_amount,
            'profit': self.profit,
            'timestamp': int(self.created_at.timestamp() * 1000),
        }

class Backtest(db.Model):
    __tablename__ = 'backtests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    strategy = db.Column(db.String(50), nullable=False)
    parameters = db.Column(db.JSON, default={})
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    initial_capital = db.Column(db.Float, nullable=False)
    final_capital = db.Column(db.Float)
    total_return = db.Column(db.Float)
    return_percent = db.Column(db.Float)
    max_drawdown = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)
    win_rate = db.Column(db.Float)
    total_trades = db.Column(db.Integer)
    profitable_trades = db.Column(db.Integer)
    status = db.Column(db.String(20), default='running')  # running, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'strategy': self.strategy,
            'startDate': int(self.start_date.timestamp() * 1000),
            'endDate': int(self.end_date.timestamp() * 1000),
            'initialCapital': self.initial_capital,
            'finalCapital': self.final_capital,
            'totalReturn': self.total_return,
            'returnPercent': self.return_percent,
            'maxDrawdown': self.max_drawdown,
            'sharpeRatio': self.sharpe_ratio,
            'winRate': self.win_rate,
            'totalTrades': self.total_trades,
            'profitableTrades': self.profitable_trades,
            'status': self.status,
            'createdAt': int(self.created_at.timestamp() * 1000),
        }

class KlineData(db.Model):
    __tablename__ = 'kline_data'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)
    
    def to_dict(self):
        return {
            'time': int(self.time.timestamp() * 1000),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
        }

class OperationLog(db.Model):
    """操作日志模型"""
    __tablename__ = 'operation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 可为空，因为有些操作可能没有用户
    operation_type = db.Column(db.String(50), nullable=False)  # 操作类型：login, order_create等
    result = db.Column(db.String(20), nullable=False)  # 操作结果：success, failure, error
    description = db.Column(db.String(500), nullable=False)  # 操作描述
    details = db.Column(db.JSON)  # 详细信息（JSON格式）
    ip_address = db.Column(db.String(50))  # IP地址
    user_agent = db.Column(db.String(500))  # 用户代理
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # 创建时间
    
    # 关联关系
    user = db.relationship('User', backref='operation_logs', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'username': self.user.username if self.user else None,
            'operationType': self.operation_type,
            'result': self.result,
            'description': self.description,
            'details': self.details,
            'ipAddress': self.ip_address,
            'userAgent': self.user_agent,
            'createdAt': int(self.created_at.timestamp() * 1000),
        }
