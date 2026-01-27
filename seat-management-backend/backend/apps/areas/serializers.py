from rest_framework import serializers
from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """
    区域序列化器
    """
    floor_id = serializers.IntegerField(
        write_only=True,
        label="所属楼层ID"
    )
    floor_name = serializers.CharField(
        source='floor.floor_name',
        read_only=True,
        label="所属楼层名称"
    )
    floor_no = serializers.CharField(
        source='floor.floor_no',
        read_only=True,
        label="所属楼层编号"
    )
    venue_name = serializers.CharField(
        source='floor.venue.name',
        read_only=True,
        label="所属场地名称"
    )
    
    class Meta:
        model = Area
        fields = [
            'id', 'floor_id', 'floor_name', 'floor_no', 'venue_name',
            'area_no', 'area_name', 'area_type', 'allowed_depts',
            'seat_count', 'position_css', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'floor_name', 'floor_no', 'venue_name', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        验证区域编号在楼层内是否唯一
        """
        floor_id = data.get('floor_id')
        area_no = data.get('area_no')
        
        if self.instance:
            # 更新时排除自身
            if Area.objects.filter(floor_id=floor_id, area_no=area_no).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "该楼层内已存在相同的区域编号",
                    code='area_no_exists'
                )
        else:
            # 创建时检查
            if Area.objects.filter(floor_id=floor_id, area_no=area_no).exists():
                raise serializers.ValidationError(
                    "该楼层内已存在相同的区域编号",
                    code='area_no_exists'
                )
        return data
    
    def create(self, validated_data):
        """
        创建区域
        """
        floor_id = validated_data.pop('floor_id')
        from backend.apps.floors.models import Floor
        floor = Floor.objects.get(id=floor_id)
        area = Area.objects.create(floor=floor, **validated_data)
        return area
    
    def update(self, instance, validated_data):
        """
        更新区域
        """
        if 'floor_id' in validated_data:
            floor_id = validated_data.pop('floor_id')
            from backend.apps.floors.models import Floor
            instance.floor = Floor.objects.get(id=floor_id)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance