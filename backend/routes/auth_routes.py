"""认证路由"""
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from utils.logging import get_client_ip, get_user_agent
from utils.decorators import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    result = AuthService.login(
        username, 
        password,
        ip_address=get_client_ip(),
        user_agent=get_user_agent()
    )
    
    if not result['success']:
        return jsonify({
            'code': 401,
            'message': result['message']
        }), 401
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': {
            'user': result['user'].to_dict(),
            'token': result['token'],
        }
    })


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """用户退出"""
    result = AuthService.logout(
        user_id=request.current_user_id,
        ip_address=get_client_ip(),
        user_agent=get_user_agent()
    )
    return jsonify({
        'code': 200,
        'message': result['message']
    })
