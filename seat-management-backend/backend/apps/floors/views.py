from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Floor
from .serializers import FloorSerializer


class FloorListCreateView(ListCreateAPIView):
    """
    楼层列表和创建视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    
    def get_queryset(self):
        """
        支持按场地过滤
        """
        queryset = super().get_queryset()
        venue_id = self.request.query_params.get('venue_id')
        if venue_id:
            queryset = queryset.filter(venue_id=venue_id)
        return queryset.order_by('venue_id', 'sort_order')
    
    def create(self, request, *args, **kwargs):
        """
        创建楼层
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


class FloorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    楼层详情、更新和删除视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        """
        删除楼层
        """
        instance = self.get_object()
        # 检查楼层是否有关联的区域
        if instance.area_set.exists():
            return Response(
                {'detail': '该楼层有关联的区域，无法删除。'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(
            {'detail': '楼层删除成功。'},
            status=status.HTTP_200_OK
        )