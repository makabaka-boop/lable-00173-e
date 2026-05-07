"""日志配置和工具类"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import request
from functools import wraps

# 日志级别映射
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

# 操作类型常量
OPERATION_TYPES = {
    'LOGIN': 'login',
    'LOGOUT': 'logout',
    'USER_CREATE': 'user_create',
    'USER_UPDATE': 'user_update',
    'USER_DELETE': 'user_delete',
    'ORDER_CREATE': 'order_create',
    'ORDER_EXECUTE': 'order_execute',
    'ORDER_CANCEL': 'order_cancel',
    'TRADE_CREATE': 'trade_create',
    'POSITION_CREATE': 'position_create',
    'POSITION_UPDATE': 'position_update',
    'POSITION_DELETE': 'position_delete',
    'BACKTEST_RUN': 'backtest_run',
    'BACKTEST_DELETE': 'backtest_delete',
    'STOCK_VIEW': 'stock_view',
    'MARKET_DATA_VIEW': 'market_data_view',
}

# 操作结果常量
OPERATION_RESULT = {
    'SUCCESS': 'success',
    'FAILURE': 'failure',
    'ERROR': 'error',
}


def setup_logging(app):
    """
    配置应用日志
    """
    # 获取日志级别
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = LOG_LEVELS.get(log_level, logging.INFO)
    
    # 创建logs目录
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 配置日志格式
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件日志处理器（轮转日志）
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(log_format)
    
    # 错误日志处理器
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'error.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    
    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(log_format)
    
    # 配置根日志记录器
    app.logger.setLevel(level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(console_handler)
    
    # 禁用Flask默认日志处理器
    logging.getLogger('werkzeug').setLevel(logging.WARNING)


def get_client_ip():
    """获取客户端IP地址"""
    if request:
        # 尝试从代理头获取真实IP
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
    return None


def get_user_agent():
    """获取用户代理"""
    if request:
        return request.headers.get('User-Agent', '')
    return ''


def log_operation(operation_type, user_id=None, result='success', 
                  description='', details=None, ip_address=None, user_agent=None):
    """
    记录操作日志的装饰器或函数
    
    使用方式1 - 作为装饰器：
        @log_operation(OPERATION_TYPES['LOGIN'])
        def login():
            ...
    
    使用方式2 - 作为函数调用：
        log_operation(OPERATION_TYPES['LOGIN'], user_id=1, result='success')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 执行函数
            try:
                result_value = func(*args, **kwargs)
                
                # 记录成功日志
                _log_to_database(
                    operation_type=operation_type,
                    user_id=user_id or (hasattr(request, 'current_user_id') and request.current_user_id),
                    result=OPERATION_RESULT['SUCCESS'],
                    description=description or f'{operation_type}操作成功',
                    details=details,
                    ip_address=ip_address or get_client_ip(),
                    user_agent=user_agent or get_user_agent()
                )
                
                return result_value
            except Exception as e:
                # 记录失败日志
                _log_to_database(
                    operation_type=operation_type,
                    user_id=user_id or (hasattr(request, 'current_user_id') and request.current_user_id),
                    result=OPERATION_RESULT['ERROR'],
                    description=description or f'{operation_type}操作失败: {str(e)}',
                    details={'error': str(e)},
                    ip_address=ip_address or get_client_ip(),
                    user_agent=user_agent or get_user_agent()
                )
                raise
        
        return wrapper
    
    # 如果直接调用（不是装饰器），记录日志
    if callable(operation_type):
        # 这是装饰器用法
        func = operation_type
        operation_type = func.__name__
        return decorator(func)
    else:
        # 这是函数调用用法
        _log_to_database(
            operation_type=operation_type,
            user_id=user_id,
            result=result,
            description=description,
            details=details,
            ip_address=ip_address or get_client_ip(),
            user_agent=user_agent or get_user_agent()
        )


def _log_to_database(operation_type, user_id=None, result='success',
                     description='', details=None, ip_address=None, user_agent=None):
    """
    将日志记录到数据库
    注意：这个函数需要在Flask应用上下文中调用
    """
    try:
        from models import db, OperationLog
        
        log_entry = OperationLog(
            user_id=user_id,
            operation_type=operation_type,
            result=result,
            description=description,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        # 如果数据库记录失败，至少记录到文件日志
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Failed to log operation to database: {str(e)}')


def log_operation_sync(operation_type, user_id=None, result='success',
                       description='', details=None, ip_address=None, user_agent=None):
    """
    同步记录操作日志（直接调用，不等待）
    用于在服务层直接调用
    """
    _log_to_database(
        operation_type=operation_type,
        user_id=user_id,
        result=result,
        description=description,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
    )
