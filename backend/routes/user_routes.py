"""用户路由"""
from flask import Blueprint, request, jsonify
from services.user_service import UserService
from utils.decorators import token_required
from utils.logging import get_client_ip, get_user_agent

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/profile/<int:user_id>', methods=['GET'])
@token_required
def get_user_profile(user_id):
    """获取用户资料"""
    # 验证用户只能访问自己的资料
    if user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权访问该用户资料'
        }), 403
    
    result = UserService.get_user_profile(user_id)
    
    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['user'].to_dict(),
    })


@user_bp.route('/profile/<int:user_id>', methods=['PUT'])
@token_required
def update_user_profile(user_id):
    """更新用户资料"""
    # 验证用户只能更新自己的资料
    if user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权修改该用户资料'
        }), 403
    
    data = request.get_json()
    result = UserService.update_user_profile(
        user_id, 
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
        'data': result['user'].to_dict(),
    })


@user_bp.route('/account-stats/<int:user_id>', methods=['GET'])
@token_required
def get_account_stats(user_id):
    """获取账户统计"""
    # 验证用户只能访问自己的账户统计
    if user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权访问该用户账户统计'
        }), 403
    
    result = UserService.get_account_stats(user_id)
    
    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['data'],
    })
