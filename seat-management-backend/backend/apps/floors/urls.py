from django.urls import path
from .views import FloorListCreateView, FloorRetrieveUpdateDestroyView


urlpatterns = [
    # 楼层列表和创建
    path('floors', FloorListCreateView.as_view(), name='floor_list_create'),
    # 楼层详情、更新和删除
    path('floors/<int:id>', FloorRetrieveUpdateDestroyView.as_view(), name='floor_retrieve_update_destroy'),
]