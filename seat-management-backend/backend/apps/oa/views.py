from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    OASyncConfigSerializer, OASyncTaskSerializer, WebhookEventSerializer,
    OASyncTriggerSerializer, WebhookEventCreateSerializer
)
from .services import (
    get_oa_sync_config, create_sync_task, execute_sync_task, trigger_oa_sync,
    process_webhook_event, get_pending_webhook_events, retry_failed_webhook_events,
    get_sync_statistics
)
from .models import OASyncConfig, OASyncTask, WebhookEvent


class OASyncConfigListView(APIView):
    """
    OA同步配置列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取OA同步配置列表
        """
        configs = OASyncConfig.objects.all()
        serializer = OASyncConfigSerializer(configs, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class OASyncConfigDetailView(APIView):
    """
    OA同步配置详情
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, config_id):
        """
        获取OA同步配置详情
        """
        try:
            config = OASyncConfig.objects.get(id=config_id)
            serializer = OASyncConfigSerializer(config)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except OASyncConfig.DoesNotExist:
            return Response(
                {'detail': '配置不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class OASyncConfigCreateView(APIView):
    """
    OA同步配置创建
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        创建OA同步配置
        """
        serializer = OASyncConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OASyncConfigUpdateView(APIView):
    """
    OA同步配置更新
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, config_id):
        """
        更新OA同步配置
        """
        try:
            config = OASyncConfig.objects.get(id=config_id)
            serializer = OASyncConfigSerializer(config, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except OASyncConfig.DoesNotExist:
            return Response(
                {'detail': '配置不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class OASyncTaskListView(APIView):
    """
    OA同步任务列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取OA同步任务列表
        """
        tasks = OASyncTask.objects.order_by('-scheduled_time')[:50]
        serializer = OASyncTaskSerializer(tasks, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class OASyncTaskDetailView(APIView):
    """
    OA同步任务详情
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id):
        """
        获取OA同步任务详情
        """
        try:
            task = OASyncTask.objects.get(id=task_id)
            serializer = OASyncTaskSerializer(task)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except OASyncTask.DoesNotExist:
            return Response(
                {'detail': '任务不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class OASyncTriggerView(APIView):
    """
    触发OA同步
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        触发OA同步
        """
        serializer = OASyncTriggerSerializer(data=request.data)
        if serializer.is_valid():
            sync_type = serializer.validated_data['sync_type']
            force = serializer.validated_data['force']
            
            result = trigger_oa_sync(sync_type, force)
            
            if result['success']:
                return Response(
                    result,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    result,
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class WebhookEventListView(APIView):
    """
    Webhook事件列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取Webhook事件列表
        """
        events = WebhookEvent.objects.order_by('-received_at')[:50]
        serializer = WebhookEventSerializer(events, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class WebhookEventDetailView(APIView):
    """
    Webhook事件详情
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, event_id):
        """
        获取Webhook事件详情
        """
        try:
            event = WebhookEvent.objects.get(id=event_id)
            serializer = WebhookEventSerializer(event)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except WebhookEvent.DoesNotExist:
            return Response(
                {'detail': '事件不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class WebhookEventCreateView(APIView):
    """
    Webhook事件创建
    """
    # 注意：实际生产环境中，这里应该添加IP白名单或其他认证机制
    permission_classes = []
    
    def post(self, request):
        """
        创建Webhook事件
        """
        serializer = WebhookEventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event_type = serializer.validated_data['event_type']
            event_data = serializer.validated_data['event_data']
            
            # 创建事件
            event = WebhookEvent.objects.create(
                event_type=event_type,
                event_data=event_data
            )
            
            # 异步处理事件
            process_webhook_event(event)
            
            return Response(
                {'detail': '事件已接收并开始处理'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class WebhookEventProcessView(APIView):
    """
    处理Webhook事件
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, event_id):
        """
        手动处理Webhook事件
        """
        try:
            event = WebhookEvent.objects.get(id=event_id)
            process_webhook_event(event)
            
            serializer = WebhookEventSerializer(event)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except WebhookEvent.DoesNotExist:
            return Response(
                {'detail': '事件不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class WebhookEventRetryView(APIView):
    """
    重试失败的Webhook事件
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        重试失败的Webhook事件
        """
        retry_count = retry_failed_webhook_events()
        
        return Response(
            {'success': True, 'retry_count': retry_count},
            status=status.HTTP_200_OK
        )


class OASyncStatisticsView(APIView):
    """
    OA同步统计
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取OA同步统计信息
        """
        statistics = get_sync_statistics()
        return Response(
            statistics,
            status=status.HTTP_200_OK
        )