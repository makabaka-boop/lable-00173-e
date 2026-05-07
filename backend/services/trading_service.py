"""交易服务"""
from models import db, User, Order, Trade, Position
from utils.logging import log_operation_sync, OPERATION_TYPES, OPERATION_RESULT, get_client_ip, get_user_agent
from datetime import datetime


class TradingService:
    """交易服务类"""
    
    @staticmethod
    def get_orders(user_id: int) -> dict:
        """
        获取订单列表
        返回: {'success': bool, 'orders': list, 'message': str}
        """
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
        return {
            'success': True,
            'orders': orders,
            'message': '获取成功'
        }
    
    @staticmethod
    def create_order(data: dict, ip_address=None, user_agent=None) -> dict:
        """
        创建订单
        返回: {'success': bool, 'order': Order, 'message': str}
        """
        user_id = data.get('user_id')
        
        user = User.query.get(user_id)
        if not user:
            log_operation_sync(
                operation_type=OPERATION_TYPES['ORDER_CREATE'],
                user_id=user_id,
                result=OPERATION_RESULT['FAILURE'],
                description=f'创建订单失败：用户不存在',
                details={'user_id': user_id},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '用户不存在'}
        
        order = Order(
            user_id=user_id,
            code=data.get('code'),
            name=data.get('name'),
            type=data.get('type'),
            quantity=data.get('quantity'),
            price=data.get('price'),
            total_amount=data.get('totalAmount'),
            status='pending',
        )
        
        db.session.add(order)
        db.session.commit()
        
        # 记录创建订单日志
        log_operation_sync(
            operation_type=OPERATION_TYPES['ORDER_CREATE'],
            user_id=user_id,
            result=OPERATION_RESULT['SUCCESS'],
            description=f'创建订单成功：{data.get("type")} {data.get("name")} {data.get("quantity")}股',
            details={
                'order_id': order.id,
                'code': data.get('code'),
                'name': data.get('name'),
                'type': data.get('type'),
                'quantity': data.get('quantity'),
                'price': data.get('price'),
                'total_amount': data.get('totalAmount'),
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return {
            'success': True,
            'order': order,
            'message': '创建成功'
        }
    
    @staticmethod
    def execute_order(order_id: int, ip_address=None, user_agent=None) -> dict:
        """
        执行订单
        返回: {'success': bool, 'order': Order, 'message': str}
        """
        order = Order.query.get(order_id)
        
        if not order:
            log_operation_sync(
                operation_type=OPERATION_TYPES['ORDER_EXECUTE'],
                user_id=None,
                result=OPERATION_RESULT['FAILURE'],
                description=f'执行订单失败：订单不存在',
                details={'order_id': order_id},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '订单不存在'}
        
        order.status = 'completed'
        order.executed_at = datetime.utcnow()
        
        # 创建交易记录
        trade = Trade(
            user_id=order.user_id,
            code=order.code,
            name=order.name,
            type=order.type,
            quantity=order.quantity,
            price=order.price,
            total_amount=order.total_amount,
        )
        
        db.session.add(trade)
        
        # 更新或创建持仓
        position = Position.query.filter_by(user_id=order.user_id, code=order.code).first()
        
        if order.type == 'buy':
            if position:
                # 更新现有持仓
                total_cost = position.cost_price * position.quantity + order.price * order.quantity
                position.quantity += order.quantity
                position.cost_price = total_cost / position.quantity
                position.current_price = order.price
            else:
                # 创建新持仓
                position = Position(
                    user_id=order.user_id,
                    code=order.code,
                    name=order.name,
                    quantity=order.quantity,
                    cost_price=order.price,
                    current_price=order.price,
                )
                db.session.add(position)
        elif order.type == 'sell':
            if position:
                # 减少持仓
                position.quantity -= order.quantity
                position.current_price = order.price
                
                # 如果持仓为0，删除该持仓
                if position.quantity <= 0:
                    db.session.delete(position)
        
        db.session.commit()
        
        # 记录执行订单日志
        log_operation_sync(
            operation_type=OPERATION_TYPES['ORDER_EXECUTE'],
            user_id=order.user_id,
            result=OPERATION_RESULT['SUCCESS'],
            description=f'执行订单成功：{order.type} {order.name} {order.quantity}股',
            details={
                'order_id': order.id,
                'trade_id': trade.id,
                'code': order.code,
                'name': order.name,
                'type': order.type,
                'quantity': order.quantity,
                'price': order.price,
                'total_amount': order.total_amount,
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return {
            'success': True,
            'order': order,
            'message': '执行成功'
        }
    
    @staticmethod
    def cancel_order(order_id: int, ip_address=None, user_agent=None) -> dict:
        """
        取消订单
        返回: {'success': bool, 'order': Order, 'message': str}
        """
        order = Order.query.get(order_id)
        
        if not order:
            log_operation_sync(
                operation_type=OPERATION_TYPES['ORDER_CANCEL'],
                user_id=None,
                result=OPERATION_RESULT['FAILURE'],
                description=f'取消订单失败：订单不存在',
                details={'order_id': order_id},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '订单不存在'}
        
        order.status = 'cancelled'
        db.session.commit()
        
        # 记录取消订单日志
        log_operation_sync(
            operation_type=OPERATION_TYPES['ORDER_CANCEL'],
            user_id=order.user_id,
            result=OPERATION_RESULT['SUCCESS'],
            description=f'取消订单成功：{order.name} {order.quantity}股',
            details={
                'order_id': order.id,
                'code': order.code,
                'name': order.name,
                'type': order.type,
                'quantity': order.quantity,
                'price': order.price,
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return {
            'success': True,
            'order': order,
            'message': '取消成功'
        }
    
    @staticmethod
    def get_trades(user_id: int) -> dict:
        """
        获取交易历史
        返回: {'success': bool, 'trades': list, 'message': str}
        """
        trades = Trade.query.filter_by(user_id=user_id).order_by(Trade.created_at.desc()).all()
        
        return {
            'success': True,
            'trades': trades,
            'message': '获取成功'
        }
