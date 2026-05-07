from flask import Blueprint, request, jsonify
from services.watchlist_service import WatchlistService
from utils.decorators import token_required

watchlist_bp = Blueprint('watchlist', __name__, url_prefix='/api/watchlist')


@watchlist_bp.route('', methods=['GET'])
@token_required
def list_items():
    result = WatchlistService.list_items(request.current_user_id)
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': [item.to_dict() for item in result['items']],
    })


@watchlist_bp.route('', methods=['POST'])
@token_required
def add_item():
    data = request.get_json()
    code = data.get('code', '').strip()
    name = data.get('name', '').strip()
    note = data.get('note', '').strip()

    if not code or not name:
        return jsonify({'code': 400, 'message': '股票代码和名称不能为空'}), 400

    result = WatchlistService.add_item(request.current_user_id, code, name, note)

    if not result['success']:
        status_code = 409 if result.get('conflict') else 400
        return jsonify({'code': status_code, 'message': result['message']}), status_code

    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['item'].to_dict(),
    }), 201


@watchlist_bp.route('/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(item_id):
    result = WatchlistService.delete_item(request.current_user_id, item_id)
    if not result['success']:
        return jsonify({'code': 404, 'message': result['message']}), 404
    return jsonify({'code': 200, 'message': result['message']})


@watchlist_bp.route('/<int:item_id>/note', methods=['PUT'])
@token_required
def update_note(item_id):
    data = request.get_json()
    note = data.get('note', '').strip()
    result = WatchlistService.update_note(request.current_user_id, item_id, note)
    if not result['success']:
        return jsonify({'code': 404, 'message': result['message']}), 404
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['item'].to_dict(),
    })


@watchlist_bp.route('/reorder', methods=['PUT'])
@token_required
def reorder_items():
    data = request.get_json()
    item_ids = data.get('itemIds', [])
    if not isinstance(item_ids, list):
        return jsonify({'code': 400, 'message': 'itemIds 必须为数组'}), 400

    result = WatchlistService.reorder_items(request.current_user_id, item_ids)
    return jsonify({'code': 200, 'message': result['message']})
