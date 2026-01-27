from rest_framework import serializers
from .models import Venue


class VenueSerializer(serializers.ModelSerializer):
    """
    场地序列化器
    """
    class Meta:
        model = Venue
        fields = ['id', 'name', 'address', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """
        验证场地名称是否已存在
        """
        if self.instance:
            # 更新时排除自身
            if Venue.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "场地名称已存在",
                    code='name_exists'
                )
        else:
            # 创建时检查
            if Venue.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    "场地名称已存在",
                    code='name_exists'
                )
        return value