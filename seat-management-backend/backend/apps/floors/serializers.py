from rest_framework import serializers
from .models import Floor


class FloorSerializer(serializers.ModelSerializer):
    """
    楼层序列化器
    """
    venue_id = serializers.IntegerField(
        write_only=True,
        label="所属场地ID"
    )
    venue_name = serializers.CharField(
        source='venue.name',
        read_only=True,
        label="所属场地名称"
    )
    
    class Meta:
        model = Floor
        fields = ['id', 'venue_id', 'venue_name', 'floor_no', 'floor_name', 'image_url', 'sort_order', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'venue_name', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        验证楼层编号在场地内是否唯一
        """
        venue_id = data.get('venue_id')
        floor_no = data.get('floor_no')
        
        if self.instance:
            # 更新时排除自身
            if Floor.objects.filter(venue_id=venue_id, floor_no=floor_no).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "该场地内已存在相同的楼层编号",
                    code='floor_no_exists'
                )
        else:
            # 创建时检查
            if Floor.objects.filter(venue_id=venue_id, floor_no=floor_no).exists():
                raise serializers.ValidationError(
                    "该场地内已存在相同的楼层编号",
                    code='floor_no_exists'
                )
        return data
    
    def create(self, validated_data):
        """
        创建楼层
        """
        venue_id = validated_data.pop('venue_id')
        from backend.apps.venues.models import Venue
        venue = Venue.objects.get(id=venue_id)
        floor = Floor.objects.create(venue=venue, **validated_data)
        return floor
    
    def update(self, instance, validated_data):
        """
        更新楼层
        """
        if 'venue_id' in validated_data:
            venue_id = validated_data.pop('venue_id')
            from backend.apps.venues.models import Venue
            instance.venue = Venue.objects.get(id=venue_id)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance