from django.urls import path
from .views import (
    SeatLogListView, SeatLogStatisticsView, SeatLogDetailView
)


urlpatterns = [
    # 日志列表查询
    path('logs', SeatLogListView.as_view(), name='seat_log_list'),
    # 日志详情
    path('logs/<int:log_id>', SeatLogDetailView.as_view(), name='seat_log_detail'),
    # 日志统计
    path('logs/statistics', SeatLogStatisticsView.as_view(), name='seat_log_statistics'),
]