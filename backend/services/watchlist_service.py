"""自选股服务"""
from models import db, WatchlistItem, Stock

MAX_ITEMS = 50


class WatchlistService:
    """自选股服务类"""

    @staticmethod
    def get_watchlist(user_id: int) -> dict:
        """
        获取用户自选股列表（按 sort_order 排序）
        返回: {'success': bool, 'items': list, 'message': str}
        """
        items = WatchlistItem.query.filter_by(user_id=user_id).order_by(WatchlistItem.sort_order).all()

        return {
            'success': True,
            'items': items,
            'message': '获取成功'
        }

    @staticmethod
    def add_item(user_id: int, code: str, name: str, note: str = None) -> dict:
        """
        添加自选股
        返回: {'success': bool, 'item': WatchlistItem, 'message': str, 'error_code': int}
        """
        existing = WatchlistItem.query.filter_by(user_id=user_id, code=code).first()
        if existing:
            return {
                'success': False,
                'message': '该股票已在自选股中',
                'error_code': 409
            }

        count = WatchlistItem.query.filter_by(user_id=user_id).count()
        if count >= MAX_ITEMS:
            return {
                'success': False,
                'message': f'自选股最多只能添加 {MAX_ITEMS} 只股票',
                'error_code': 400
            }

        max_order = db.session.query(
            db.func.coalesce(db.func.max(WatchlistItem.sort_order), -1)
        ).filter_by(user_id=user_id).scalar()

        item = WatchlistItem(
            user_id=user_id,
            code=code,
            name=name,
            note=note,
            sort_order=max_order + 1
        )
        db.session.add(item)
        db.session.commit()

        return {
            'success': True,
            'item': item,
            'message': '添加成功'
        }

    @staticmethod
    def update_note(user_id: int, item_id: int, note: str) -> dict:
        """
        更新自选股备注
        返回: {'success': bool, 'item': WatchlistItem, 'message': str}
        """
        item = WatchlistItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not item:
            return {
                'success': False,
                'message': '自选股不存在'
            }

        item.note = note
        db.session.commit()

        return {
            'success': True,
            'item': item,
            'message': '更新成功'
        }

    @staticmethod
    def remove_item(user_id: int, item_id: int) -> dict:
        """
        删除自选股
        返回: {'success': bool, 'message': str}
        """
        item = WatchlistItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not item:
            return {
                'success': False,
                'message': '自选股不存在'
            }

        db.session.delete(item)
        db.session.commit()

        return {
            'success': True,
            'message': '删除成功'
        }

    @staticmethod
    def reorder(user_id: int, orders: list) -> dict:
        """
        批量重排自选股
        orders: [{'id': 1, 'sortOrder': 0}, ...]
        返回: {'success': bool, 'message': str}
        """
        try:
            for order in orders:
                item = WatchlistItem.query.filter_by(
                    id=order['id'],
                    user_id=user_id
                ).first()
                if item:
                    item.sort_order = order['sortOrder']
            db.session.commit()

            return {
                'success': True,
                'message': '排序成功'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'排序失败: {str(e)}'
            }

    @staticmethod
    def check_exists(user_id: int, code: str) -> dict:
        """
        检查股票是否已在自选股中
        返回: {'success': bool, 'exists': bool, 'item': WatchlistItem, 'message': str}
        """
        item = WatchlistItem.query.filter_by(user_id=user_id, code=code).first()

        return {
            'success': True,
            'exists': item is not None,
            'item': item,
            'message': '检查成功'
        }
