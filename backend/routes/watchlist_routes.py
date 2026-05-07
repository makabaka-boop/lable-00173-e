"""自选股路由"""
from flask import Blueprint, request, jsonify
from services.watchlist_service import WatchlistService
from utils.decorators import token_required

watchlist_bp = Blueprint('watchlist', __name__, url_prefix='/api/watchlist')


@watchlist_bp.route('', methods=['GET'])
@token_required
def get_watchlist():
    """获取自选股列表"""
    user_id = request.current_user_id
    result = WatchlistService.get_watchlist(user_id)

    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': [item.to_dict() for item in result['items']],
    })


@watchlist_bp.route('', methods=['POST'])
@token_required
def add_item():
    """添加自选股"""
    user_id = request.current_user_id
    data = request.get_json()

    if not data or 'code' not in data or 'name' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少必要参数: code 和 name'
        }), 400

    result = WatchlistService.add_item(
        user_id=user_id,
        code=data['code'],
        name=data['name'],
        note=data.get('note')
    )

    if not result['success']:
        error_code = result.get('error_code', 400)
        return jsonify({
            'code': error_code,
            'message': result['message']
        }), error_code

    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['item'].to_dict(),
    })


@watchlist_bp.route('/<int:item_id>/note', methods=['PUT'])
@token_required
def update_note(item_id):
    """更新自选股备注"""
    user_id = request.current_user_id
    data = request.get_json()

    note = data.get('note', '') if data else ''

    result = WatchlistService.update_note(user_id, item_id, note)

    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404

    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['item'].to_dict(),
    })


@watchlist_bp.route('/<int:item_id>', methods=['DELETE'])
@token_required
def remove_item(item_id):
    """删除自选股"""
    user_id = request.current_user_id
    result = WatchlistService.remove_item(user_id, item_id)

    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404

    return jsonify({
        'code': 200,
        'message': result['message']
    })


@watchlist_bp.route('/reorder', methods=['PUT'])
@token_required
def reorder():
    """批量重排自选股"""
    user_id = request.current_user_id
    data = request.get_json()

    if not data or 'orders' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少必要参数: orders'
        }), 400

    result = WatchlistService.reorder(user_id, data['orders'])

    if not result['success']:
        return jsonify({
            'code': 500,
            'message': result['message']
        }), 500

    return jsonify({
        'code': 200,
        'message': result['message']
    })


@watchlist_bp.route('/check/<code>', methods=['GET'])
@token_required
def check_exists(code):
    """检查股票是否已在自选股中"""
    user_id = request.current_user_id
    result = WatchlistService.check_exists(user_id, code)

    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': {
            'exists': result['exists'],
            'item': result['item'].to_dict() if result['item'] else None
        }
    })
