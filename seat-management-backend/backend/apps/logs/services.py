from django.db.models import Q
from .models import SeatLog


def create_seat_log(
    seat_id=None, 
    seat_no=None, 
    operation_type=None, 
    old_user_id=None, 
    old_user_name=None, 
    new_user_id=None, 
    new_user_name=None, 
    operator_id=None, 
    operator_name=None, 
    operation_ip=None, 
    operation_remark=None, 
    extra_info=None
):
    """
    创建工位变更日志
    """
    log = SeatLog.objects.create(
        seat_id=seat_id,
        seat_no=seat_no,
        operation_type=operation_type,
        old_user_id=old_user_id,
        old_user_name=old_user_name,
        new_user_id=new_user_id,
        new_user_name=new_user_name,
        operator_id=operator_id,
        operator_name=operator_name,
        operation_ip=operation_ip,
        operation_remark=operation_remark,
        extra_info=extra_info
    )
    return log


def get_seat_logs(query_params):
    """
    查询工位变更日志
    """
    # 构建查询条件
    filters = Q()
    
    # 工位编号
    if query_params.get('seat_no'):
        filters &= Q(seat_no=query_params.get('seat_no'))
    
    # 操作类型
    if query_params.get('operation_type'):
        filters &= Q(operation_type=query_params.get('operation_type'))
    
    # 时间范围
    if query_params.get('start_time'):
        filters &= Q(operation_time__gte=query_params.get('start_time'))
    
    if query_params.get('end_time'):
        filters &= Q(operation_time__lte=query_params.get('end_time'))
    
    # 操作人
    if query_params.get('operator_id'):
        filters &= Q(operator_id=query_params.get('operator_id'))
    
    # 人员ID（原人员或新人员）
    if query_params.get('user_id'):
        user_id = query_params.get('user_id')
        filters &= (Q(old_user_id=user_id) | Q(new_user_id=user_id))
    
    # 分页参数
    page = query_params.get('page', 1)
    page_size = query_params.get('page_size', 10)
    offset = (page - 1) * page_size
    
    # 执行查询
    total = SeatLog.objects.filter(filters).count()
    logs = SeatLog.objects.filter(filters).order_by('-operation_time')[offset:offset+page_size]
    
    # 构建结果
    result = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "logs": []
    }
    
    # 格式化日志
    for log in logs:
        log_info = {
            "id": log.id,
            "seat_id": log.seat_id,
            "seat_no": log.seat_no,
            "operation_type": log.operation_type,
            "operation_type_display": log.get_operation_type_display(),
            "old_user_id": log.old_user_id,
            "old_user_name": log.old_user_name,
            "new_user_id": log.new_user_id,
            "new_user_name": log.new_user_name,
            "operator_id": log.operator_id,
            "operator_name": log.operator_name,
            "operation_time": log.operation_time,
            "operation_ip": log.operation_ip,
            "operation_remark": log.operation_remark,
            "extra_info": log.extra_info
        }
        result["logs"].append(log_info)
    
    return result


def get_seat_log_statistics(start_time=None, end_time=None):
    """
    获取工位变更统计
    """
    # 构建查询条件
    filters = Q()
    
    if start_time:
        filters &= Q(operation_time__gte=start_time)
    
    if end_time:
        filters &= Q(operation_time__lte=end_time)
    
    # 按操作类型统计
    statistics = SeatLog.objects.filter(filters).values('operation_type').annotate(count=Count('id'))
    
    # 构建结果
    result = {
        "total_logs": SeatLog.objects.filter(filters).count(),
        "by_operation_type": []
    }
    
    for stat in statistics:
        operation_type = stat['operation_type']
        # 获取操作类型显示名称
        operation_display = dict(SeatLog.OPERATION_TYPE_CHOICES).get(operation_type, "未知")
        
        result["by_operation_type"].append({
            "operation_type": operation_type,
            "operation_display": operation_display,
            "count": stat['count']
        })
    
    return result


# 导入Count
from django.db.models import Count