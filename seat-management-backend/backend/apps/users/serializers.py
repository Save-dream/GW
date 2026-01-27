from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    人员序列化器
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'dept_id', 'dept_name', 'position', 'phone', 'email', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSyncSerializer(serializers.Serializer):
    """
    人员同步序列化器
    """
    users = serializers.ListField(
        child=serializers.DictField(),
        required=True,
        label="人员列表"
    )


class UserQuerySerializer(serializers.Serializer):
    """
    人员查询序列化器
    """
    user_id = serializers.CharField(
        required=True,
        label="人员ID（OA工号）"
    )


class UserChangeSerializer(serializers.Serializer):
    """
    人员变更序列化器（Webhook）
    """
    user_id = serializers.CharField(
        required=True,
        label="人员ID（OA工号）"
    )
    name = serializers.CharField(
        required=True,
        label="姓名"
    )
    dept_id = serializers.CharField(
        required=True,
        label="部门ID"
    )
    dept_name = serializers.CharField(
        required=True,
        label="部门名称"
    )
    position = serializers.CharField(
        required=True,
        label="职位"
    )
    phone = serializers.CharField(
        required=False,
        label="手机号"
    )
    email = serializers.CharField(
        required=False,
        label="邮箱"
    )
    status = serializers.CharField(
        required=True,
        label="状态",
        help_text="在职, 离职"
    )
    change_type = serializers.CharField(
        required=True,
        label="变更类型",
        help_text="入职, 离职, 调岗"
    )


class SeatWithUserSerializer(serializers.Serializer):
    """
    带人员信息的工位序列化器
    """
    id = serializers.IntegerField(
        read_only=True,
        label="工位ID"
    )
    seat_no = serializers.CharField(
        read_only=True,
        label="工位编号"
    )
    area_name = serializers.CharField(
        read_only=True,
        label="所属区域名称"
    )
    floor_name = serializers.CharField(
        read_only=True,
        label="所属楼层名称"
    )
    venue_name = serializers.CharField(
        read_only=True,
        label="所属场地名称"
    )
    bind_type = serializers.IntegerField(
        read_only=True,
        label="绑定类型"
    )


class MySeatSerializer(serializers.Serializer):
    """
    我的工位序列化器
    """
    seats = SeatWithUserSerializer(
        many=True,
        read_only=True,
        label="我的工位列表"
    )


class SearchSerializer(serializers.Serializer):
    """
    搜索结果序列化器
    """
    users = UserSerializer(
        many=True,
        read_only=True,
        label="人员搜索结果"
    )
    seats = serializers.ListField(
        child=serializers.DictField(),
        read_only=True,
        label="工位搜索结果"
    )