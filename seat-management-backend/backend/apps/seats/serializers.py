from rest_framework import serializers
from .models import Seat


class SeatSerializer(serializers.ModelSerializer):
    """
    工位序列化器
    """
    area_id = serializers.IntegerField(
        write_only=True,
        label="所属区域ID"
    )
    area_name = serializers.CharField(
        source='area.area_name',
        read_only=True,
        label="所属区域名称"
    )
    area_no = serializers.CharField(
        source='area.area_no',
        read_only=True,
        label="所属区域编号"
    )
    floor_name = serializers.CharField(
        source='area.floor.floor_name',
        read_only=True,
        label="所属楼层名称"
    )
    floor_no = serializers.CharField(
        source='area.floor.floor_no',
        read_only=True,
        label="所属楼层编号"
    )
    venue_name = serializers.CharField(
        source='area.floor.venue.name',
        read_only=True,
        label="所属场地名称"
    )
    
    class Meta:
        model = Seat
        fields = [
            'id', 'area_id', 'area_name', 'area_no',
            'floor_name', 'floor_no', 'venue_name',
            'seat_no', 'seat_status', 'grid_row', 'grid_col',
            'position_x', 'position_y', 'current_user_id',
            'current_user_name', 'current_dept_id', 'bind_type',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'area_name', 'area_no', 'floor_name', 'floor_no',
            'venue_name', 'current_user_id', 'current_user_name',
            'current_dept_id', 'bind_type', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        """
        创建工位
        """
        area_id = validated_data.pop('area_id')
        from backend.apps.areas.models import Area
        area = Area.objects.get(id=area_id)
        seat = Seat.objects.create(area=area, **validated_data)
        return seat
    
    def update(self, instance, validated_data):
        """
        更新工位
        """
        if 'area_id' in validated_data:
            area_id = validated_data.pop('area_id')
            from backend.apps.areas.models import Area
            instance.area = Area.objects.get(id=area_id)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class SeatGenerateSerializer(serializers.Serializer):
    """
    工位生成序列化器
    """
    area_id = serializers.IntegerField(
        required=True,
        label="区域ID"
    )
    count = serializers.IntegerField(
        required=True,
        min_value=1,
        label="生成数量"
    )


class SeatBindSerializer(serializers.Serializer):
    """
    工位绑定序列化器
    """
    seat_id = serializers.IntegerField(
        required=True,
        label="工位ID"
    )
    user_id = serializers.CharField(
        required=True,
        label="人员ID（OA工号）"
    )
    bind_type = serializers.IntegerField(
        default=1,
        label="绑定类型",
        help_text="1:主工位, 2:额外绑定"
    )


class SeatUnbindSerializer(serializers.Serializer):
    """
    工位解绑序列化器
    """
    seat_id = serializers.IntegerField(
        required=True,
        label="工位ID"
    )


class SeatTransferSerializer(serializers.Serializer):
    """
    工位更换序列化器
    """
    old_seat_id = serializers.IntegerField(
        required=True,
        label="原工位ID"
    )
    new_seat_id = serializers.IntegerField(
        required=True,
        label="新工位ID"
    )
    user_id = serializers.CharField(
        required=True,
        label="人员ID（OA工号）"
    )


class SeatExtraBindSerializer(serializers.Serializer):
    """
    工位额外绑定序列化器
    """
    seat_id = serializers.IntegerField(
        required=True,
        label="工位ID"
    )
    user_id = serializers.CharField(
        required=True,
        label="人员ID（OA工号）"
    )