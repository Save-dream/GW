from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from backend.apps.floors.models import Floor
from backend.apps.areas.models import Area
from backend.apps.seats.models import Seat
from backend.apps.users.models import User
from backend.apps.users.serializers import (
    UserSerializer, UserSyncSerializer, UserQuerySerializer,
    UserChangeSerializer, MySeatSerializer, SearchSerializer
)
from backend.apps.users.services import (
    sync_users, process_user_change, search, get_user_seats, get_seat_with_user
)


class UserFloorListView(APIView):
    """
    获取楼层列表（员工端）
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取楼层列表
        """
        floors = Floor.objects.filter(status=1).order_by('venue_id', 'sort_order')
        
        # 格式化结果
        result = []
        for floor in floors:
            result.append({
                "id": floor.id,
                "venue_id": floor.venue.id,
                "venue_name": floor.venue.name,
                "floor_no": floor.floor_no,
                "floor_name": floor.floor_name,
                "image_url": floor.image_url,
                "sort_order": floor.sort_order,
                "status": floor.status
            })
        
        return Response(
            result,
            status=status.HTTP_200_OK
        )


class UserFloorDetailView(APIView):
    """
    获取楼层详情（含区域、工位）
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, floor_id):
        """
        获取楼层详情
        """
        try:
            floor = Floor.objects.get(id=floor_id, status=1)
        except Floor.DoesNotExist:
            return Response(
                {'detail': '楼层不存在或已停用'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 获取楼层下的所有区域
        areas = Area.objects.filter(floor_id=floor_id, status=1)
        
        # 构建结果
        result = {
            "id": floor.id,
            "venue_id": floor.venue.id,
            "venue_name": floor.venue.name,
            "floor_no": floor.floor_no,
            "floor_name": floor.floor_name,
            "image_url": floor.image_url,
            "areas": []
        }
        
        # 添加区域和工位信息
        for area in areas:
            seats = Seat.objects.filter(area_id=area.id)
            
            area_info = {
                "id": area.id,
                "area_no": area.area_no,
                "area_name": area.area_name,
                "area_type": area.area_type,
                "seat_count": area.seat_count,
                "position_css": area.position_css,
                "seats": []
            }
            
            # 添加工位信息
            for seat in seats:
                seat_info = {
                    "id": seat.id,
                    "seat_no": seat.seat_no,
                    "seat_status": seat.seat_status,
                    "current_user_id": seat.current_user_id,
                    "current_user_name": seat.current_user_name,
                    "grid_row": seat.grid_row,
                    "grid_col": seat.grid_col,
                    "position_x": seat.position_x,
                    "position_y": seat.position_y
                }
                area_info["seats"].append(seat_info)
            
            result["areas"].append(area_info)
        
        return Response(
            result,
            status=status.HTTP_200_OK
        )


class UserSearchView(APIView):
    """
    全局搜索（员工端）
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        全局搜索
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'detail': '搜索关键词不能为空'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 执行搜索
        search_results = search(query)
        
        return Response(
            search_results,
            status=status.HTTP_200_OK
        )


class UserSeatDetailView(APIView):
    """
    获取工位详情（员工端）
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, seat_id):
        """
        获取工位详情
        """
        try:
            seat_info = get_seat_with_user(seat_id)
        except Seat.DoesNotExist:
            return Response(
                {'detail': '工位不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            seat_info,
            status=status.HTTP_200_OK
        )


class UserMySeatView(APIView):
    """
    获取我的工位信息（员工端）
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取我的工位信息
        """
        # 这里假设员工端登录后，用户信息存储在request.user中
        # 实际实现中，可能需要从token中解析用户ID或从OA系统获取
        # 这里简化处理，使用系统用户的username作为OA工号
        user_id = request.user.username
        
        # 获取用户的工位列表
        seats = get_user_seats(user_id)
        
        return Response(
            {"seats": seats},
            status=status.HTTP_200_OK
        )


class UserSyncView(APIView):
    """
    人员同步视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        全量同步人员基础信息
        """
        serializer = UserSyncSerializer(data=request.data)
        if serializer.is_valid():
            users_data = serializer.validated_data['users']
            
            try:
                synced_count = sync_users(users_data)
                return Response(
                    {'detail': f'成功同步 {synced_count} 条人员信息'},
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


class UserListView(APIView):
    """
    获取人员列表（管理员端）
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取人员列表
        """
        users = User.objects.filter(status=1).order_by('dept_id', 'name')
        serializer = UserSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserQueryView(APIView):
    """
    人员查询视图
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        实时查询人员详情
        """
        serializer = UserQuerySerializer(data=request.query_params)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            
            try:
                user = User.objects.get(id=user_id)
                return Response(
                    {
                        "user_id": user.id,
                        "name": user.name,
                        "dept_id": user.dept_id,
                        "dept_name": user.dept_name,
                        "position": user.position,
                        "phone": user.phone,
                        "email": user.email,
                        "status": "在职" if user.status == 1 else "离职"
                    },
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {'detail': '人员不存在'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserChangeView(APIView):
    """
    人员变更通知（Webhook）
    """
    # 注意：实际生产环境中，这里应该添加IP白名单或其他认证机制
    permission_classes = []
    
    def post(self, request):
        """
        处理人员变更通知
        """
        serializer = UserChangeSerializer(data=request.data)
        if serializer.is_valid():
            user_change_data = serializer.validated_data
            
            try:
                success = process_user_change(user_change_data)
                if success:
                    return Response(
                        {'detail': '人员变更处理成功'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'detail': '人员变更处理失败'},
                        status=status.HTTP_400_BAD_REQUEST
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


class DepartmentTreeView(APIView):
    """
    获取部门组织架构
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取部门组织架构
        """
        # 从人员表中提取所有唯一的部门信息
        departments = User.objects.filter(status=1).values('dept_id', 'dept_name').distinct()
        
        # 构建部门树（简化版，实际可能需要从OA系统获取完整的部门树）
        dept_tree = []
        for dept in departments:
            dept_tree.append({
                "dept_id": dept['dept_id'],
                "dept_name": dept['dept_name'],
                "children": []  # 实际实现中，可能需要递归构建子部门
            })
        
        return Response(
            dept_tree,
            status=status.HTTP_200_OK
        )