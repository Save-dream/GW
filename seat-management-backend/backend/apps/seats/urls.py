from django.urls import path
from .views import (
    SeatListCreateView, SeatRetrieveUpdateDestroyView,
    SeatGenerateView, SeatBindView, SeatUnbindView,
    SeatTransferView, SeatExtraBindView
)


urlpatterns = [
    # 工位列表和创建
    path('seats', SeatListCreateView.as_view(), name='seat_list_create'),
    # 工位详情、更新和删除
    path('seats/<int:id>', SeatRetrieveUpdateDestroyView.as_view(), name='seat_retrieve_update_destroy'),
    # 批量生成工位
    path('seats/generate', SeatGenerateView.as_view(), name='seat_generate'),
    # 绑定人员
    path('seat/bind', SeatBindView.as_view(), name='seat_bind'),
    # 解绑人员
    path('seat/unbind', SeatUnbindView.as_view(), name='seat_unbind'),
    # 更换工位
    path('seat/transfer', SeatTransferView.as_view(), name='seat_transfer'),
    # 额外绑定
    path('seat/extra-bind', SeatExtraBindView.as_view(), name='seat_extra_bind'),
]