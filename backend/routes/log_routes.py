"""日志路由"""
from flask import Blueprint, request, jsonify
from services.log_service import LogService
from utils.decorators import token_required
from datetime import datetime

log_bp = Blueprint('log', __name__, url_prefix='/api/logs')


@log_bp.route('', methods=['GET'])
@token_required
def get_logs():
    """获取操作日志列表"""
    # 获取查询参数
    user_id = request.args.get('user_id', type=int)
    operation_type = request.args.get('operation_type')
    result_filter = request.args.get('result')  # 重命名避免冲突
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 解析日期
    start_date = None
    end_date = None
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
        except:
            start_date = datetime.fromtimestamp(int(start_date_str) / 1000)
    
    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
        except:
            end_date = datetime.fromtimestamp(int(end_date_str) / 1000)
    
    # 如果指定了user_id，验证权限
    if user_id and user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权查看该用户日志'
        }), 403
    
    # 如果没有指定user_id，默认只查看当前用户的日志
    if not user_id:
        user_id = request.current_user_id
    
    result = LogService.get_logs(
        user_id=user_id,
        operation_type=operation_type,
        result=result_filter,
        start_date=start_date,
        end_date=end_date,
        page=page,
        per_page=per_page
    )
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': {
            'logs': result['logs'],
            'pagination': {
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'pages': result['pages'],
            }
        }
    })


@log_bp.route('/<int:log_id>', methods=['GET'])
@token_required
def get_log(log_id):
    """获取日志详情"""
    result = LogService.get_log_by_id(log_id)
    
    if not result['success']:
        return jsonify({
            'code': 404,
            'message': result['message']
        }), 404
    
    log = result['log']
    
    # 验证权限：只能查看自己的日志
    if log.user_id and log.user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权查看该日志'
        }), 403
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': log.to_dict(),
    })


@log_bp.route('/user/<int:user_id>', methods=['GET'])
@token_required
def get_user_logs(user_id):
    """获取指定用户的操作日志"""
    # 验证权限：只能查看自己的日志
    if user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权查看该用户日志'
        }), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    result = LogService.get_user_logs(user_id, page=page, per_page=per_page)
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': {
            'logs': result['logs'],
            'pagination': {
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'pages': result['pages'],
            }
        }
    })


@log_bp.route('/statistics', methods=['GET'])
@token_required
def get_statistics():
    """获取日志统计信息"""
    user_id = request.args.get('user_id', type=int)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # 如果指定了user_id，验证权限
    if user_id and user_id != request.current_user_id:
        return jsonify({
            'code': 403,
            'message': '无权查看该用户统计'
        }), 403
    
    # 如果没有指定user_id，默认只查看当前用户的统计
    if not user_id:
        user_id = request.current_user_id
    
    # 解析日期
    start_date = None
    end_date = None
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
        except:
            start_date = datetime.fromtimestamp(int(start_date_str) / 1000)
    
    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
        except:
            end_date = datetime.fromtimestamp(int(end_date_str) / 1000)
    
    result = LogService.get_statistics(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': result['statistics'],
    })


@log_bp.route('/<int:log_id>', methods=['DELETE'])
@token_required
def delete_log(log_id):
    """删除日志"""
    result = LogService.delete_log(log_id, user_id=request.current_user_id)
    
    if not result['success']:
        return jsonify({
            'code': 404 if '不存在' in result['message'] else 403,
            'message': result['message']
        }), 404 if '不存在' in result['message'] else 403
    
    return jsonify({
        'code': 200,
        'message': result['message']
    })


@log_bp.route('/cleanup', methods=['POST'])
@token_required
def cleanup_old_logs():
    """清理旧日志（需要管理员权限，这里暂时允许所有用户）"""
    days = request.json.get('days', 90) if request.is_json else 90
    
    result = LogService.delete_old_logs(days=days)
    
    return jsonify({
        'code': 200,
        'message': result['message'],
        'data': {
            'deleted_count': result['deleted_count']
        }
    })
