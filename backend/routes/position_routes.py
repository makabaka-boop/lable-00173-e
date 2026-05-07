"""持仓路由"""
from flask import Blueprint, request, jsonify
from services.position_service import PositionService
from utils.decorators import token_required

position_bp = Blueprint('position', __name__, url_prefix='/api/positions')


@position_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_positions(user_id):
    """获取持仓列表"""
    # 验证用户只能访问自己的持仓
    if user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权访问该用户持仓'
        }), 403
    
    result = PositionService.get_positions(user_id)
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': [p.to_dict() for p in result['positions']],
    })


@position_bp.route('', methods=['POST'])
@token_required
def create_position():
    """创建持仓"""
    data = request.get_json()
    # 使用认证的用户ID，确保用户只能为自己创建持仓
    data['user_id'] = request.current_user_id
    result = PositionService.create_position(data)
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['position'].to_dict(),
    }), 201


@position_bp.route('/<int:position_id>', methods=['PUT'])
@token_required
def update_position(position_id):
    """更新持仓"""
    from models import Position
    
    # 验证持仓是否属于当前用户
    position = Position.query.get(position_id)
    if not position:
        return jsonify({
            'code': 404,
            'message': '持仓不存在'
        }), 404
    
    if position.user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权修改该持仓'
        }), 403
    
    data = request.get_json()
    result = PositionService.update_position(position_id, data)
    
    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['position'].to_dict(),
    })
