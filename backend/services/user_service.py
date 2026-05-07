"""用户服务"""
from models import db, User, Position
from utils.logging import log_operation_sync, OPERATION_TYPES, OPERATION_RESULT
from datetime import datetime
import random


class UserService:
    """用户服务类"""
    
    @staticmethod
    def get_user_profile(user_id: int) -> dict:
        """
        获取用户资料
        返回: {'success': bool, 'user': User, 'message': str}
        """
        user = User.query.get(user_id)
        
        if not user:
            return {'success': False, 'message': '用户不存在'}
        
        return {
            'success': True,
            'user': user,
            'message': '获取成功'
        }
    
    @staticmethod
    def update_user_profile(user_id: int, data: dict, ip_address=None, user_agent=None) -> dict:
        """
        更新用户资料
        返回: {'success': bool, 'user': User, 'message': str}
        """
        user = User.query.get(user_id)
        
        if not user:
            log_operation_sync(
                operation_type=OPERATION_TYPES['USER_UPDATE'],
                user_id=user_id,
                result=OPERATION_RESULT['FAILURE'],
                description=f'更新用户资料失败：用户不存在',
                details={'user_id': user_id},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '用户不存在'}
        
        # 更新允许的字段
        allowed_fields = ['name', 'email', 'phone', 'address', 'bio', 'avatar']
        updated_fields = []
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
                updated_fields.append(field)
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        # 记录更新用户资料日志
        log_operation_sync(
            operation_type=OPERATION_TYPES['USER_UPDATE'],
            user_id=user_id,
            result=OPERATION_RESULT['SUCCESS'],
            description=f'更新用户资料成功',
            details={'updated_fields': updated_fields},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return {
            'success': True,
            'user': user,
            'message': '更新成功'
        }
    
    @staticmethod
    def get_account_stats(user_id: int) -> dict:
        """
        获取账户统计
        返回: {'success': bool, 'data': dict, 'message': str}
        """
        user = User.query.get(user_id)
        
        if not user:
            return {'success': False, 'message': '用户不存在'}
        
        positions = Position.query.filter_by(user_id=user_id).all()
        total_market_value = sum(p.current_price * p.quantity for p in positions)
        total_cost = sum(p.cost_price * p.quantity for p in positions)
        total_profit = total_market_value - total_cost
        total_profit_percent = (total_profit / total_cost * 100) if total_cost > 0 else 0
        
        return {
            'success': True,
            'data': {
                'totalAssets': user.total_assets,
                'cash': user.balance,
                'positions': [p.to_dict() for p in positions],
                'totalProfit': total_profit,
                'totalProfitPercent': total_profit_percent,
                'dayProfit': random.uniform(-5000, 5000),
                'dayProfitPercent': random.uniform(-2, 2),
            },
            'message': '获取成功'
        }
