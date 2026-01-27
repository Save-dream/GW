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
    
    def create(self, request, *args, **kwargs):
        """
        创建场地
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


class VenueRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    场地详情、更新和删除视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        """
        删除场地
        """
        instance = self.get_object()
        # 检查场地是否有关联的楼层
        if instance.floor_set.exists():
            return Response(
                {'detail': '该场地有关联的楼层，无法删除。'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(
            {'detail': '场地删除成功。'},
            status=status.HTTP_200_OK
        )