from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SeatLogSerializer, SeatLogQuerySerializer
from .services import get_seat_logs, get_seat_log_statistics


class SeatLogListView(APIView):
    """
    工位变更日志列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        查询工位变更日志
        """
        serializer = SeatLogQuerySerializer(data=request.query_params)
        if serializer.is_valid():
            query_params = serializer.validated_data
            
            try:
                # 获取日志列表
                result = get_seat_logs(query_params)
                return Response(
                    result,
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SeatLogStatisticsView(APIView):
    """
    工位变更统计
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取工位变更统计
        """
        # 获取查询参数
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        
        try:
            # 获取统计数据
            result = get_seat_log_statistics(start_time, end_time)
            return Response(
                result,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SeatLogDetailView(APIView):
    """
    工位变更日志详情
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, log_id):
        """
        获取日志详情
        """
        try:
            from .models import SeatLog
            log = SeatLog.objects.get(id=log_id)
            serializer = SeatLogSerializer(log)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except SeatLog.DoesNotExist:
            return Response(
                {'detail': '日志不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )