"""日志服务"""
from models import db, OperationLog, User
from datetime import datetime, timedelta
from sqlalchemy import and_, or_


class LogService:
    """日志服务类"""
    
    @staticmethod
    def get_logs(user_id=None, operation_type=None, result=None,
                 start_date=None, end_date=None, page=1, per_page=20):
        """
        获取操作日志列表
        返回: {'success': bool, 'logs': list, 'total': int, 'page': int, 'per_page': int, 'message': str}
        """
        query = OperationLog.query
        
        # 过滤条件
        filters = []
        
        if user_id:
            filters.append(OperationLog.user_id == user_id)
        
        if operation_type:
            filters.append(OperationLog.operation_type == operation_type)
        
        if result:
            filters.append(OperationLog.result == result)
        
        if start_date:
            filters.append(OperationLog.created_at >= start_date)
        
        if end_date:
            # 结束日期包含整天，所以加一天
            filters.append(OperationLog.created_at < end_date + timedelta(days=1))
        
        if filters:
            query = query.filter(and_(*filters))
        
        # 按创建时间倒序排列
        query = query.order_by(OperationLog.created_at.desc())
        
        # 分页
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'success': True,
            'logs': [log.to_dict() for log in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages,
            'message': '获取成功'
        }
    
    @staticmethod
    def get_log_by_id(log_id):
        """
        根据ID获取日志详情
        返回: {'success': bool, 'log': OperationLog, 'message': str}
        """
        log = OperationLog.query.get(log_id)
        
        if not log:
            return {'success': False, 'message': '日志不存在'}
        
        return {
            'success': True,
            'log': log,
            'message': '获取成功'
        }
    
    @staticmethod
    def get_user_logs(user_id, page=1, per_page=20):
        """
        获取指定用户的操作日志
        返回: {'success': bool, 'logs': list, 'total': int, 'message': str}
        """
        return LogService.get_logs(
            user_id=user_id,
            page=page,
            per_page=per_page
        )
    
    @staticmethod
    def get_statistics(user_id=None, start_date=None, end_date=None):
        """
        获取日志统计信息
        返回: {'success': bool, 'statistics': dict, 'message': str}
        """
        query = OperationLog.query
        
        filters = []
        if user_id:
            filters.append(OperationLog.user_id == user_id)
        if start_date:
            filters.append(OperationLog.created_at >= start_date)
        if end_date:
            filters.append(OperationLog.created_at < end_date + timedelta(days=1))
        
        if filters:
            query = query.filter(and_(*filters))
        
        # 总日志数
        total_logs = query.count()
        
        # 按结果统计
        success_count = query.filter(OperationLog.result == 'success').count()
        failure_count = query.filter(OperationLog.result == 'failure').count()
        error_count = query.filter(OperationLog.result == 'error').count()
        
        # 按操作类型统计
        operation_type_stats = {}
        operation_types = db.session.query(OperationLog.operation_type).distinct().all()
        for op_type in operation_types:
            op_type = op_type[0]
            count = query.filter(OperationLog.operation_type == op_type).count()
            operation_type_stats[op_type] = count
        
        # 按日期统计（最近7天）
        date_stats = {}
        for i in range(7):
            date = datetime.utcnow().date() - timedelta(days=i)
            start = datetime.combine(date, datetime.min.time())
            end = datetime.combine(date, datetime.max.time())
            count = query.filter(
                and_(
                    OperationLog.created_at >= start,
                    OperationLog.created_at <= end
                )
            ).count()
            date_stats[date.isoformat()] = count
        
        return {
            'success': True,
            'statistics': {
                'total': total_logs,
                'success': success_count,
                'failure': failure_count,
                'error': error_count,
                'operationTypes': operation_type_stats,
                'dailyStats': date_stats,
            },
            'message': '获取成功'
        }
    
    @staticmethod
    def delete_log(log_id, user_id=None):
        """
        删除日志（只有管理员或日志所有者可以删除）
        返回: {'success': bool, 'message': str}
        """
        log = OperationLog.query.get(log_id)
        
        if not log:
            return {'success': False, 'message': '日志不存在'}
        
        # 验证权限：只有日志所有者可以删除
        if user_id and log.user_id != user_id:
            return {'success': False, 'message': '无权删除该日志'}
        
        db.session.delete(log)
        db.session.commit()
        
        return {
            'success': True,
            'message': '删除成功'
        }
    
    @staticmethod
    def delete_old_logs(days=90):
        """
        删除指定天数之前的旧日志
        返回: {'success': bool, 'deleted_count': int, 'message': str}
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        deleted_count = OperationLog.query.filter(
            OperationLog.created_at < cutoff_date
        ).delete()
        
        db.session.commit()
        
        return {
            'success': True,
            'deleted_count': deleted_count,
            'message': f'成功删除 {deleted_count} 条旧日志'
        }
