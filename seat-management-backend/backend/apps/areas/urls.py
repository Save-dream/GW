from django.urls import path
from .views import AreaListCreateView, AreaRetrieveUpdateDestroyView


urlpatterns = [
    # 区域列表和创建
    path('areas', AreaListCreateView.as_view(), name='area_list_create'),
    # 区域详情、更新和删除
    path('areas/<int:id>', AreaRetrieveUpdateDestroyView.as_view(), name='area_retrieve_update_destroy'),
]