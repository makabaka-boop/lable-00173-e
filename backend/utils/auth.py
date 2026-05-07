"""认证相关的工具函数"""
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# JWT密钥，从环境变量获取，如果没有则使用默认值（生产环境必须设置）
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24  # Token过期时间：24小时


def hash_password(password: str) -> str:
    """生成密码哈希"""
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """验证密码"""
    return check_password_hash(password_hash, password)


def generate_token(user_id: int) -> str:
    """生成JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    """
    验证JWT token
    返回payload字典，如果token无效或过期则返回None
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def extract_token_from_header(auth_header: str) -> str:
    """
    从Authorization header中提取token
    格式: Bearer <token>
    """
    if not auth_header:
        return None
    
    parts = auth_header.split(' ')
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    return parts[1]
