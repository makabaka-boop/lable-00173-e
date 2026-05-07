"""交易路由"""
from flask import Blueprint, request, jsonify
from services.trading_service import TradingService
from utils.decorators import token_required
from utils.logging import get_client_ip, get_user_agent

trading_bp = Blueprint('trading', __name__, url_prefix='/api/trading')


@trading_bp.route('/orders/<int:user_id>', methods=['GET'])
@token_required
def get_orders(user_id):
    """获取订单列表"""
    # 验证用户只能访问自己的订单
    if user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权访问该用户订单'
        }), 403
    
    result = TradingService.get_orders(user_id)
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': [o.to_dict() for o in result['orders']],
    })


@trading_bp.route('/orders', methods=['POST'])
@token_required
def create_order():
    """创建订单"""
    data = request.get_json()
    # 使用认证的用户ID，确保用户只能为自己创建订单
    data['user_id'] = request.current_user_id
    result = TradingService.create_order(
        data,
        ip_address=get_client_ip(),
        user_agent=get_user_agent()
    )
    
    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['order'].to_dict(),
    }), 201


@trading_bp.route('/orders/<int:order_id>/execute', methods=['PUT'])
@token_required
def execute_order(order_id):
    """执行订单"""
    from models import Order
    
    # 验证订单是否属于当前用户
    order = Order.query.get(order_id)
    if not order:
        return jsonify({
            'code': 404,
            'message': '订单不存在'
        }), 404
    
    if order.user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权执行该订单'
        }), 403
    
    result = TradingService.execute_order(
        order_id,
        ip_address=get_client_ip(),
        user_agent=get_user_agent()
    )
    
    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['order'].to_dict(),
    })


@trading_bp.route('/orders/<int:order_id>/cancel', methods=['PUT'])
@token_required
def cancel_order(order_id):
    """取消订单"""
    from models import Order
    
    # 验证订单是否属于当前用户
    order = Order.query.get(order_id)
    if not order:
        return jsonify({
            'code': 404,
            'message': '订单不存在'
        }), 404
    
    if order.user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权取消该订单'
        }), 403
    
    result = TradingService.cancel_order(
        order_id,
        ip_address=get_client_ip(),
        user_agent=get_user_agent()
    )
    
    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['order'].to_dict(),
    })


@trading_bp.route('/trades/<int:user_id>', methods=['GET'])
@token_required
def get_trades(user_id):
    """获取交易历史"""
    # 验证用户只能访问自己的交易历史
    if user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权访问该用户交易历史'
        }), 403
    
    result = TradingService.get_trades(user_id)
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': [t.to_dict() for t in result['trades']],
    })
