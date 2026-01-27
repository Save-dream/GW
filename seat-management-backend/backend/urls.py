from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.permissions import AllowAny


# 创建不需要认证的视图类
class TokenObtainPairViewAllowAny(TokenObtainPairView):
    permission_classes = [AllowAny]

class TokenRefreshViewAllowAny(TokenRefreshView):
    permission_classes = [AllowAny]

class TokenVerifyViewAllowAny(TokenVerifyView):
    permission_classes = [AllowAny]


urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),
    
    # JWT认证
    path('api/token', TokenObtainPairViewAllowAny.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshViewAllowAny.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyViewAllowAny.as_view(), name='token_verify'),
    
    # 认证应用
    path('api/auth/', include('backend.apps.authentication.urls')),
    
    # 场地应用
    path('api/admin/venue/', include('backend.apps.venues.urls')),
    
    # 楼层应用
    path('api/admin/floor/', include('backend.apps.floors.urls')),
    
    # 区域应用
    path('api/admin/area/', include('backend.apps.areas.urls')),
    
    # 工位应用
    path('api/admin/', include('backend.apps.seats.urls')),
    
    # 人员应用
    path('api/', include('backend.apps.users.urls')),
    
    # 日志应用
    path('api/admin/log/', include('backend.apps.logs.urls')),
    
    # OA应用
    path('api/', include('backend.apps.oa.urls')),
]