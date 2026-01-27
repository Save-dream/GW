from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Seat
from .serializers import (
    SeatSerializer, SeatGenerateSerializer, SeatBindSerializer,
    SeatUnbindSerializer, SeatTransferSerializer, SeatExtraBindSerializer
)
from .services import (
    generate_seats, bind_user_to_seat, unbind_user_from_seat,
    transfer_user_seat, extra_bind_user_to_seat
)


class SeatListCreateView(ListCreateAPIView):
    """
    工位列表和创建视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    
    def get_queryset(self):
        """
        支持按区域、楼层、场地过滤
        """
        queryset = super().get_queryset()
        area_id = self.request.query_params.get('area_id')
        floor_id = self.request.query_params.get('floor_id')
        venue_id = self.request.query_params.get('venue_id')
        
        if area_id:
            queryset = queryset.filter(area_id=area_id)
        elif floor_id:
            queryset = queryset.filter(area__floor_id=floor_id)
        elif venue_id:
            queryset = queryset.filter(area__floor__venue_id=venue_id)
        
        return queryset.order_by('area_id', 'seat_no')


class SeatRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    工位详情、更新和删除视图
    """
    permission_classes = [IsAuthenticated]
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    lookup_field = 'id'


class SeatGenerateView(APIView):
    """
    批量生成工位视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        批量生成工位
        """
        serializer = SeatGenerateSerializer(data=request.data)
        if serializer.is_valid():
            area_id = serializer.validated_data['area_id']
            count = serializer.validated_data['count']
            
            try:
                generated_count = generate_seats(area_id, count)
                return Response(
                    {'detail': f'成功生成 {generated_count} 个工位。'},
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


class SeatBindView(APIView):
    """
    绑定人员到工位视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        绑定人员到工位
        """
        serializer = SeatBindSerializer(data=request.data)
        if serializer.is_valid():
            seat_id = serializer.validated_data['seat_id']
            user_id = serializer.validated_data['user_id']
            bind_type = serializer.validated_data['bind_type']
            
            try:
                # 获取操作人信息
                operator_id = request.user.username
                operator_name = request.user.name
                
                seat = bind_user_to_seat(
                    seat_id, user_id, bind_type, operator_id, operator_name
                )
                return Response(
                    {'detail': f'成功将 {seat.current_user_name} 绑定到工位 {seat.seat_no}。'},
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


class SeatUnbindView(APIView):
    """
    解绑人员与工位视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        解绑人员与工位
        """
        serializer = SeatUnbindSerializer(data=request.data)
        if serializer.is_valid():
            seat_id = serializer.validated_data['seat_id']
            
            try:
                # 获取操作人信息
                operator_id = request.user.username
                operator_name = request.user.name
                
                seat = unbind_user_from_seat(
                    seat_id, operator_id, operator_name
                )
                return Response(
                    {'detail': f'成功解绑工位 {seat.seat_no}。'},
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


class SeatTransferView(APIView):
    """
    更换人员工位视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        更换人员工位
        """
        serializer = SeatTransferSerializer(data=request.data)
        if serializer.is_valid():
            old_seat_id = serializer.validated_data['old_seat_id']
            new_seat_id = serializer.validated_data['new_seat_id']
            user_id = serializer.validated_data['user_id']
            
            try:
                # 获取操作人信息
                operator_id = request.user.username
                operator_name = request.user.name
                
                seat = transfer_user_seat(
                    old_seat_id, new_seat_id, user_id, operator_id, operator_name
                )
                return Response(
                    {'detail': f'成功将人员更换到工位 {seat.seat_no}。'},
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


class SeatExtraBindView(APIView):
    """
    额外绑定人员到工位视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        额外绑定人员到工位
        """
        serializer = SeatExtraBindSerializer(data=request.data)
        if serializer.is_valid():
            seat_id = serializer.validated_data['seat_id']
            user_id = serializer.validated_data['user_id']
            
            try:
                # 获取操作人信息
                operator_id = request.user.username
                operator_name = request.user.name
                
                seat = extra_bind_user_to_seat(
                    seat_id, user_id, operator_id, operator_name
                )
                return Response(
                    {'detail': f'成功将 {seat.current_user_name} 额外绑定到工位 {seat.seat_no}。'},
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