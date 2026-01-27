from django.urls import path
from .views import VenueListCreateView, VenueRetrieveUpdateDestroyView


urlpatterns = [
    # 场地列表和创建
    path('venues', VenueListCreateView.as_view(), name='venue_list_create'),
    # 场地详情、更新和删除
    path('venues/<int:id>', VenueRetrieveUpdateDestroyView.as_view(), name='venue_retrieve_update_destroy'),
]