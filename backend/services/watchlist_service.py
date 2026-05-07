from models import db, WatchlistItem
from datetime import datetime


class WatchlistService:

    MAX_ITEMS = 50

    @staticmethod
    def list_items(user_id: int) -> dict:
        items = WatchlistItem.query.filter_by(user_id=user_id).order_by(WatchlistItem.sort_order, WatchlistItem.created_at).all()
        return {'success': True, 'items': items, 'message': '获取成功'}

    @staticmethod
    def add_item(user_id: int, code: str, name: str, note: str = '') -> dict:
        count = WatchlistItem.query.filter_by(user_id=user_id).count()
        if count >= WatchlistService.MAX_ITEMS:
            return {'success': False, 'message': f'自选股已达上限{WatchlistService.MAX_ITEMS}条', 'conflict': False}

        existing = WatchlistItem.query.filter_by(user_id=user_id, code=code).first()
        if existing:
            return {'success': False, 'message': '该股票已在自选列表中', 'conflict': True}

        max_order = db.session.query(db.func.max(WatchlistItem.sort_order)).filter_by(user_id=user_id).scalar() or 0
        item = WatchlistItem(
            user_id=user_id,
            code=code,
            name=name,
            note=note,
            sort_order=max_order + 1,
        )
        db.session.add(item)
        db.session.commit()

        return {'success': True, 'item': item, 'message': '添加成功'}

    @staticmethod
    def delete_item(user_id: int, item_id: int) -> dict:
        item = WatchlistItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not item:
            return {'success': False, 'message': '自选股不存在'}

        db.session.delete(item)
        db.session.commit()
        return {'success': True, 'message': '删除成功'}

    @staticmethod
    def update_note(user_id: int, item_id: int, note: str) -> dict:
        item = WatchlistItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not item:
            return {'success': False, 'message': '自选股不存在'}

        item.note = note
        item.updated_at = datetime.utcnow()
        db.session.commit()
        return {'success': True, 'item': item, 'message': '更新成功'}

    @staticmethod
    def reorder_items(user_id: int, item_ids: list) -> dict:
        for idx, item_id in enumerate(item_ids):
            item = WatchlistItem.query.filter_by(id=item_id, user_id=user_id).first()
            if item:
                item.sort_order = idx

        db.session.commit()
        return {'success': True, 'message': '排序成功'}
