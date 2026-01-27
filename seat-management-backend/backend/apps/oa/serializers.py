from rest_framework import serializers
from .models import OASyncConfig, OASyncTask, WebhookEvent


class OASyncConfigSerializer(serializers.ModelSerializer):
    """
    OA同步配置序列化器
    """
    class Meta:
        model = OASyncConfig
        fields = [
            'id', 'sync_type', 'api_url', 'api_key', 'sync_interval',
            'last_sync_time', 'sync_status', 'error_message', 'is_enabled',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_sync_time', 'sync_status', 'error_message', 'created_at', 'updated_at']


class OASyncTaskSerializer(serializers.ModelSerializer):
    """
    OA同步任务序列化器
    """
    # 状态显示
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True,
        label="状态"
    )
    
    class Meta:
        model = OASyncTask
        fields = [
            'id', 'task_type', 'task_params', 'status', 'status_display',
            'result', 'error_message', 'scheduled_time', 'start_time',
            'end_time', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'result', 'error_message', 'start_time', 'end_time', 'created_at']


class WebhookEventSerializer(serializers.ModelSerializer):
    """
    Webhook事件序列化器
    """
    # 事件类型显示
    event_type_display = serializers.CharField(
        source='get_event_type_display',
        read_only=True,
        label="事件类型"
    )
    # 状态显示
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True,
        label="状态"
    )
    
    class Meta:
        model = WebhookEvent
        fields = [
            'id', 'event_type', 'event_type_display', 'event_data',
            'status', 'status_display', 'retry_count', 'error_message',
            'received_at', 'processed_at'
        ]
        read_only_fields = fields


class OASyncTriggerSerializer(serializers.Serializer):
    """
    OA同步触发序列化器
    """
    sync_type = serializers.CharField(
        required=True,
        label="同步类型"
    )
    force = serializers.BooleanField(
        default=False,
        label="是否强制同步"
    )


class WebhookEventCreateSerializer(serializers.Serializer):
    """
    Webhook事件创建序列化器
    """
    event_type = serializers.IntegerField(
        required=True,
        label="事件类型"
    )
    event_data = serializers.JSONField(
        required=True,
        label="事件数据"
    )
    signature = serializers.CharField(
        required=False,
        label="签名"
    )