from django.urls import path
from .views import LoginView, RegisterView, LogoutView, CustomTokenRefreshView, UserInfoView


urlpatterns = [
    # 登录
    path('login', LoginView.as_view(), name='login'),
    # 注册
    path('register', RegisterView.as_view(), name='register'),
    # 登出
    path('logout', LogoutView.as_view(), name='logout'),
    # 刷新Token
    path('refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    # 获取用户信息
    path('user/info', UserInfoView.as_view(), name='user_info'),
]