"""市场路由"""
from flask import Blueprint, jsonify
from services.market_service import MarketService

market_bp = Blueprint('market', __name__, url_prefix='/api/market')


@market_bp.route('/stocks', methods=['GET'])
def get_stocks():
    """获取股票列表"""
    result = MarketService.get_stocks()
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': [s.to_dict() for s in result['stocks']],
    })


@market_bp.route('/stock/<code>', methods=['GET'])
def get_stock(code):
    """获取单个股票信息"""
    result = MarketService.get_stock(code)
    
    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['stock'].to_dict(),
    })


@market_bp.route('/kline/<code>', methods=['GET'])
def get_kline(code):
    """获取K线数据"""
    result = MarketService.get_kline(code)
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': [k.to_dict() for k in result['klines']],
    })
