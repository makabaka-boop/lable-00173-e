"""回测服务"""
from models import db, User, Backtest
from utils.logging import log_operation_sync, OPERATION_TYPES, OPERATION_RESULT
from datetime import datetime
import random


class BacktestService:
    """回测服务类"""
    
    @staticmethod
    def get_backtest_results(user_id: int) -> dict:
        """
        获取回测结果
        返回: {'success': bool, 'backtests': list, 'message': str}
        """
        backtests = Backtest.query.filter_by(user_id=user_id).order_by(Backtest.created_at.desc()).all()
        
        return {
            'success': True,
            'backtests': backtests,
            'message': '获取成功'
        }
    
    @staticmethod
    def run_backtest(data: dict, ip_address=None, user_agent=None) -> dict:
        """
        运行回测
        返回: {'success': bool, 'backtest': Backtest, 'message': str}
        """
        user_id = data.get('user_id')
        
        user = User.query.get(user_id)
        if not user:
            log_operation_sync(
                operation_type=OPERATION_TYPES['BACKTEST_RUN'],
                user_id=user_id,
                result=OPERATION_RESULT['FAILURE'],
                description=f'运行回测失败：用户不存在',
                details={'user_id': user_id},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '用户不存在'}
        
        # 生成模拟回测结果
        initial_capital = data.get('initialCapital', 100000)
        final_capital = initial_capital * (1 + random.uniform(-0.2, 0.5))
        total_return = final_capital - initial_capital
        return_percent = (total_return / initial_capital) * 100
        
        backtest = Backtest(
            user_id=user_id,
            name=data.get('name'),
            code=data.get('code'),
            strategy=data.get('strategy'),
            parameters=data.get('parameters', {}),
            start_date=datetime.fromtimestamp(data.get('startDate', 0) / 1000),
            end_date=datetime.fromtimestamp(data.get('endDate', 0) / 1000),
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            return_percent=return_percent,
            max_drawdown=random.uniform(-20, 0),
            sharpe_ratio=random.uniform(0.5, 2.5),
            win_rate=random.uniform(40, 80),
            total_trades=random.randint(20, 100),
            profitable_trades=random.randint(10, 60),
            status='completed',
        )
        
        db.session.add(backtest)
        db.session.commit()
        
        # 记录运行回测日志
        log_operation_sync(
            operation_type=OPERATION_TYPES['BACKTEST_RUN'],
            user_id=user_id,
            result=OPERATION_RESULT['SUCCESS'],
            description=f'运行回测成功：{data.get("name")}',
            details={
                'backtest_id': backtest.id,
                'name': data.get('name'),
                'code': data.get('code'),
                'strategy': data.get('strategy'),
                'initial_capital': initial_capital,
                'final_capital': final_capital,
                'return_percent': return_percent,
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return {
            'success': True,
            'backtest': backtest,
            'message': '回测完成'
        }
    
    @staticmethod
    def delete_backtest(backtest_id: int, ip_address=None, user_agent=None) -> dict:
        """
        删除回测结果
        返回: {'success': bool, 'message': str}
        """
        backtest = Backtest.query.get(backtest_id)
        
        if not backtest:
            log_operation_sync(
                operation_type=OPERATION_TYPES['BACKTEST_DELETE'],
                user_id=None,
                result=OPERATION_RESULT['FAILURE'],
                description=f'删除回测失败：回测不存在',
                details={'backtest_id': backtest_id},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return {'success': False, 'message': '回测不存在'}
        
        backtest_name = backtest.name
        user_id = backtest.user_id
        
        db.session.delete(backtest)
        db.session.commit()
        
        # 记录删除回测日志
        log_operation_sync(
            operation_type=OPERATION_TYPES['BACKTEST_DELETE'],
            user_id=user_id,
            result=OPERATION_RESULT['SUCCESS'],
            description=f'删除回测成功：{backtest_name}',
            details={'backtest_id': backtest_id, 'name': backtest_name},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return {
            'success': True,
            'message': '删除成功'
        }
