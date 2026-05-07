"""主应用文件"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import db, User, Stock, KlineData, OperationLog
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

# 导入路由蓝图
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.market_routes import market_bp
from routes.trading_routes import trading_bp
from routes.position_routes import position_bp
from routes.backtest_routes import backtest_bp
from routes.log_routes import log_bp

# 导入工具函数
from utils.auth import hash_password
from utils.logging import setup_logging

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///trading_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)

# 配置日志
setup_logging(app)

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(market_bp)
app.register_blueprint(trading_bp)
app.register_blueprint(position_bp)
app.register_blueprint(backtest_bp)
app.register_blueprint(log_bp)


def init_data():
    """初始化数据库数据"""
    # 检查是否已初始化
    if User.query.first():
        return
    
    # 创建演示用户（密码使用哈希存储）
    user = User(
        username='admin',
        password=hash_password('123456'),  # 使用哈希密码
        email='admin@example.com',
        name='管理员',
        balance=200000.0,
        total_assets=500000.0,
    )
    db.session.add(user)
    db.session.commit()
    
    # 创建股票数据
    stocks_data = [
        {'code': '000001', 'name': '平安银行', 'price': 12.5, 'high': 13.0, 'low': 12.0},
        {'code': '000858', 'name': '五粮液', 'price': 95.0, 'high': 98.0, 'low': 92.0},
        {'code': '000651', 'name': '格力电器', 'price': 28.5, 'high': 30.0, 'low': 27.0},
        {'code': '600000', 'name': '浦发银行', 'price': 9.8, 'high': 10.2, 'low': 9.5},
        {'code': '600016', 'name': '民生银行', 'price': 6.5, 'high': 6.8, 'low': 6.2},
        {'code': '600519', 'name': '贵州茅台', 'price': 1950.0, 'high': 2000.0, 'low': 1900.0},
        {'code': '601398', 'name': '工商银行', 'price': 5.2, 'high': 5.5, 'low': 5.0},
        {'code': '601988', 'name': '中国银行', 'price': 3.8, 'high': 4.0, 'low': 3.6},
    ]
    
    for stock_data in stocks_data:
        change = random.uniform(-5, 5)
        stock = Stock(
            code=stock_data['code'],
            name=stock_data['name'],
            price=stock_data['price'],
            change=change,
            change_percent=change / stock_data['price'] * 100,
            high=stock_data['high'],
            low=stock_data['low'],
            volume=random.randint(1000000, 100000000),
            market_cap=random.randint(100000000000, 5000000000000),
            pe=random.uniform(5, 50),
        )
        db.session.add(stock)
    
    db.session.commit()


# 初始化数据库
with app.app_context():
    db.create_all()
    init_data()


# ==================== 健康检查 ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'code': 200, 'message': 'OK'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
