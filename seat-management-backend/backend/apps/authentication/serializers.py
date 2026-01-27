from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone', 'email', 'is_admin', 'last_login', 'created_at']
        read_only_fields = ['id', 'last_login', 'created_at']


class LoginSerializer(serializers.Serializer):
    """
    登录序列化器
    """
    username = serializers.CharField(
        max_length=50,
        required=True,
        label="用户名"
    )
    password = serializers.CharField(
        max_length=128,
        required=True,
        label="密码",
        write_only=True
    )
    
    def validate(self, data):
        """
        验证用户凭据
        """
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    "用户名或密码错误",
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                "必须提供用户名和密码",
                code='authorization'
            )
        
        data['user'] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    注册序列化器
    """
    password = serializers.CharField(
        max_length=128,
        required=True,
        write_only=True,
        label="密码"
    )
    password2 = serializers.CharField(
        max_length=128,
        required=True,
        write_only=True,
        label="确认密码"
    )
    
    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'email', 'password', 'password2']
    
    def validate(self, data):
        """
        验证密码是否一致
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                "两次输入的密码不一致",
                code='password_mismatch'
            )
        return data
    
    def create(self, validated_data):
        """
        创建用户
        """
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            phone=validated_data.get('phone'),
            email=validated_data.get('email')
        )
        return user