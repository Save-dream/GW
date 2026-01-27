from rest_framework import serializers
from .models import SeatLog


class SeatLogSerializer(serializers.ModelSerializer):
    """
    工位变更日志序列化器
    """
    # 操作类型显示
    operation_type_display = serializers.CharField(
        source='get_operation_type_display',
        read_only=True,
        label="操作类型"
    )
    
    class Meta:
        model = SeatLog
        fields = [
            'id', 'seat_id', 'seat_no', 'operation_type', 'operation_type_display',
            'old_user_id', 'old_user_name', 'new_user_id', 'new_user_name',
            'operator_id', 'operator_name', 'operation_time', 'operation_ip',
            'operation_remark', 'extra_info'
        ]
        read_only_fields = fields


class SeatLogQuerySerializer(serializers.Serializer):
    """
    日志查询序列化器
    """
    seat_no = serializers.CharField(
        required=False,
        label="工位编号"
    )
    operation_type = serializers.IntegerField(
        required=False,
        label="操作类型"
    )
    start_time = serializers.DateTimeField(
        required=False,
        label="开始时间"
    )
    end_time = serializers.DateTimeField(
        required=False,
        label="结束时间"
    )
    operator_id = serializers.CharField(
        required=False,
        label="操作人ID"
    )
    user_id = serializers.CharField(
        required=False,
        label="人员ID（原人员或新人员）"
    )
    page = serializers.IntegerField(
        default=1,
        min_value=1,
        label="页码"
    )
    page_size = serializers.IntegerField(
        default=10,
        min_value=1,
        max_value=100,
        label="每页条数"
    )