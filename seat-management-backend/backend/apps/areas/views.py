from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Area
from .serializers import AreaSerializer


class AreaListCreateView(ListCreateAPIView):
    """
    区域列表和创建视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    
    def get_queryset(self):
        """
        支持按楼层过滤
        """
        queryset = super().get_queryset()
        floor_id = self.request.query_params.get('floor_id')
        if floor_id:
            queryset = queryset.filter(floor_id=floor_id)
        return queryset.order_by('floor_id', 'area_no')
    
    def create(self, request, *args, **kwargs):
        """
        创建区域
        """
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


class AreaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    区域详情、更新和删除视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        """
        删除区域
        """
        instance = self.get_object()
        # 检查区域是否有关联的工位
        if instance.seat_set.exists():
            return Response(
                {'detail': '该区域有关联的工位，无法删除。'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(
            {'detail': '区域删除成功。'},
            status=status.HTTP_200_OK
        )