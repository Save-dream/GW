from django.urls import path
from .views import WebhookEventCreateView


urlpatterns = [
    # Webhook接收端点（OA系统调用）- 只保留这一个OA系统用户接口
    path('webhook/oa/event', WebhookEventCreateView.as_view(), name='webhook_event_create'),
]