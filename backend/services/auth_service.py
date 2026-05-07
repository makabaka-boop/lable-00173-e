"""认证服务"""
from models import db, User
from utils.auth import hash_password, verify_password, generate_token
from utils.logging import log_operation_sync, OPERATION_TYPES, OPERATION_RESULT, get_client_ip, get_user_agent
from datetime import datetime


class AuthService:
    """认证服务类"""
    
    @staticmethod
    def login(username: str, password: str, ip_address=None, user_agent=None) -> dict:
        """
        用户登录
        返回: {'success': bool, 'user': User, 'token': str, 'message': str}
        """
        if not username or not password:
            log_operation_sync(
                operation_type=OPERATION_TYPES['LOGIN'],
                user_id=None,
                result=OPERATION_RESULT['FAILURE'],
                description=f'登录失败：用户名或密码为空',
                details={'username': username},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '用户名和密码不能为空'}
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            log_operation_sync(
                operation_type=OPERATION_TYPES['LOGIN'],
                user_id=None,
                result=OPERATION_RESULT['FAILURE'],
                description=f'登录失败：用户不存在',
                details={'username': username},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '用户名或密码错误'}
        
        if not verify_password(user.password, password):
            log_operation_sync(
                operation_type=OPERATION_TYPES['LOGIN'],
                user_id=user.id,
                result=OPERATION_RESULT['FAILURE'],
                description=f'登录失败：密码错误',
                details={'username': username},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '用户名或密码错误'}
        
        token = generate_token(user.id)
        
        # 记录成功登录日志
        log_operation_sync(
            operation_type=OPERATION_TYPES['LOGIN'],
            user_id=user.id,
            result=OPERATION_RESULT['SUCCESS'],
            description=f'用户登录成功',
            details={'username': username},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return {
            'success': True,
            'user': user,
            'token': token,
            'message': '登录成功'
        }
    
    @staticmethod
    def logout(user_id=None, ip_address=None, user_agent=None) -> dict:
        """用户退出"""
        if user_id:
            log_operation_sync(
                operation_type=OPERATION_TYPES['LOGOUT'],
                user_id=user_id,
                result=OPERATION_RESULT['SUCCESS'],
                description=f'用户退出登录',
                ip_address=ip_address,
                user_agent=user_agent
            )
        return {'success': True, 'message': '退出成功'}
