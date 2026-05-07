"""装饰器工具"""
from functools import wraps
from flask import request, jsonify
from utils.auth import extract_token_from_header, verify_token


def token_required(f):
    """需要token认证的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'code': 401, 'message': '缺少认证token'}), 401
        
        token = extract_token_from_header(auth_header)
        if not token:
            return jsonify({'code': 401, 'message': 'token格式错误'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'message': 'token无效或已过期'}), 401
        
        # 将认证的用户ID添加到request对象中，供路由函数使用
        request.current_user_id = payload['user_id']
        
        return f(*args, **kwargs)
    
    return decorated_function
