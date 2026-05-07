"""持仓服务"""
from models import db, Position
from datetime import datetime


class PositionService:
    """持仓服务类"""
    
    @staticmethod
    def get_positions(user_id: int) -> dict:
        """
        获取持仓列表
        返回: {'success': bool, 'positions': list, 'message': str}
        """
        positions = Position.query.filter_by(user_id=user_id).all()
        
        return {
            'success': True,
            'positions': positions,
            'message': '获取成功'
        }
    
    @staticmethod
    def create_position(data: dict) -> dict:
        """
        创建持仓
        返回: {'success': bool, 'position': Position, 'message': str}
        """
        position = Position(
            user_id=data.get('user_id'),
            code=data.get('code'),
            name=data.get('name'),
            quantity=data.get('quantity'),
            cost_price=data.get('cost_price'),
            current_price=data.get('current_price'),
        )
        
        db.session.add(position)
        db.session.commit()
        
        return {
            'success': True,
            'position': position,
            'message': '创建成功'
        }
    
    @staticmethod
    def update_position(position_id: int, data: dict) -> dict:
        """
        更新持仓
        返回: {'success': bool, 'position': Position, 'message': str}
        """
        position = Position.query.get(position_id)
        
        if not position:
            return {'success': False, 'message': '持仓不存在'}
        
        allowed_fields = ['quantity', 'cost_price', 'current_price']
        for field in allowed_fields:
            if field in data:
                setattr(position, field, data[field])
        
        position.updated_at = datetime.utcnow()
        db.session.commit()
        
        return {
            'success': True,
            'position': position,
            'message': '更新成功'
        }
