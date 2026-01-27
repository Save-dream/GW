from django.urls import path
from .views import (
    UserFloorListView, UserFloorDetailView, UserSearchView,
    UserSeatDetailView, UserMySeatView, UserSyncView,
    UserListView, UserQueryView, UserChangeView, DepartmentTreeView
)


urlpatterns = [
    # 员工端 - 楼层列表
    path('user/floor', UserFloorListView.as_view(), name='user_floor_list'),
    # 员工端 - 楼层详情
    path('user/floor/<int:floor_id>', UserFloorDetailView.as_view(), name='user_floor_detail'),
    # 员工端 - 全局搜索
    path('user/search', UserSearchView.as_view(), name='user_search'),
    # 员工端 - 工位详情
    path('user/seat/<int:seat_id>', UserSeatDetailView.as_view(), name='user_seat_detail'),
    # 员工端 - 我的工位
    path('user/my-seat', UserMySeatView.as_view(), name='user_my_seat'),
    # 人员同步 - 全量同步
    path('admin/user/sync', UserSyncView.as_view(), name='admin_user_sync'),
    # 人员管理 - 获取人员列表
    path('admin/user/list', UserListView.as_view(), name='admin_user_list'),
    # 人员同步 - 实时查询
    path('admin/user/query', UserQueryView.as_view(), name='admin_user_query'),
    # 人员同步 - Webhook（接收OA变更通知）
    path('webhook/user-change', UserChangeView.as_view(), name='webhook_user_change'),
    # 部门组织架构
    path('admin/department/tree', DepartmentTreeView.as_view(), name='admin_department_tree'),
]