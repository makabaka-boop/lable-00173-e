"""回测路由"""
from flask import Blueprint, request, jsonify
from services.backtest_service import BacktestService
from utils.decorators import token_required
from utils.logging import get_client_ip, get_user_agent

backtest_bp = Blueprint('backtest', __name__, url_prefix='/api/backtest')


@backtest_bp.route('/results/<int:user_id>', methods=['GET'])
@token_required
def get_backtest_results(user_id):
    """获取回测结果"""
    # 验证用户只能访问自己的回测结果
    if user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权访问该用户回测结果'
        }), 403
    
    result = BacktestService.get_backtest_results(user_id)
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': [b.to_dict() for b in result['backtests']],
    })


@backtest_bp.route('/run', methods=['POST'])
@token_required
def run_backtest():
    """运行回测"""
    data = request.get_json()
    # 使用认证的用户ID，确保用户只能为自己运行回测
    data['user_id'] = request.current_user_id
    result = BacktestService.run_backtest(
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
        'data': result['backtest'].to_dict(),
    }), 201


@backtest_bp.route('/results/<int:backtest_id>', methods=['DELETE'])
@token_required
def delete_backtest(backtest_id):
    """删除回测结果"""
    from models import Backtest
    
    # 验证回测结果是否属于当前用户
    backtest = Backtest.query.get(backtest_id)
    if not backtest:
        return jsonify({
            'code': 404,
            'message': '回测不存在'
        }), 404
    
    if backtest.user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权删除该回测结果'
        }), 403
    
    result = BacktestService.delete_backtest(
        backtest_id,
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
        'message': result['message']
    })
