from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Venue
from .serializers import VenueSerializer


class VenueListCreateView(ListCreateAPIView):
    """
    场地列表和创建视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    
    def get(self, request, *args, **kwargs):
        """
        获取场地列表，添加权限控制和排序功能
        """
        # 权限控制
        user = request.user
        
        # 检查用户是否为普通员工（非管理员）
        if not user.is_admin and not (hasattr(user, 'role') and user.role == 'hr_admin'):
            return Response(
                {'detail': '权限拒绝，普通员工无权限访问场地管理'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 获取排序参数和状态筛选参数
        order_by = request.query_params.get('order_by', None)
        status_filter = request.query_params.get('status', None)
        
        # 构建查询集
        queryset = self.get_queryset()
        
        # 处理状态筛选
        if status_filter is not None:
            try:
                status_value = int(status_filter)
                queryset = queryset.filter(status=status_value)
            except ValueError:
                pass
        
        # 处理排序
        if order_by == 'floor_count':
            # 按楼层数排序（使用annotate计算每个场地的楼层数）
            from django.db.models import Count
            queryset = queryset.annotate(floor_count=Count('floor_set')).order_by('floor_count')
        elif order_by == '-floor_count':
            # 按楼层数降序排序
            from django.db.models import Count
            queryset = queryset.annotate(floor_count=Count('floor_set')).order_by('-floor_count')
        
        # 序列化数据
        serializer = self.get_serializer(queryset, many=True)
        
        # 为每个场地添加楼层数
        venues_data = serializer.data
        for venue in venues_data:
            venue_id = venue['id']
            floor_count = queryset.get(id=venue_id).floor_set.count() if queryset.filter(id=venue_id).exists() else 0
            venue['floorCount'] = floor_count
        
        return Response(venues_data)
    
    def create(self, request, *args, **kwargs):
        """
        创建场地
        """
        # 权限控制
        user = request.user
        if not user.is_admin:
            return Response(
                {'detail': '权限拒绝，只有系统管理员可以创建场地'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
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


class VenueRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    场地详情、更新和删除视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        """
        获取场地详情
        """
        # 权限控制
        user = request.user
        
        # 检查用户是否为普通员工（非管理员）
        if not user.is_admin and not (hasattr(user, 'role') and user.role == 'hr_admin'):
            return Response(
                {'detail': '权限拒绝，普通员工无权限访问场地管理'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """
        更新场地信息
        """
        # 权限控制
        user = request.user
        
        # 检查用户是否为普通员工（非管理员）
        if not user.is_admin and not (hasattr(user, 'role') and user.role == 'hr_admin'):
            return Response(
                {'detail': '权限拒绝，普通员工无权限编辑场地'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().put(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """
        删除场地
        """
        # 权限控制
        user = request.user
        if not user.is_admin:
            return Response(
                {'detail': '权限拒绝，只有系统管理员可以删除场地'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        
        # 检查场地是否有关联的楼层
        if instance.floor_set.exists():
            return Response(
                {'detail': '该场地有关联的楼层，无法删除。'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查是否为系统唯一场地
        if Venue.objects.count() == 1:
            return Response(
                {'detail': '至少保留一个场地'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(
            {'detail': '场地删除成功。'},
            status=status.HTTP_200_OK
        )