from rest_framework import serializers
import re
from .models import Venue


class VenueSerializer(serializers.ModelSerializer):
    """
    场地序列化器
    """
    class Meta:
        model = Venue
        fields = ['id', 'name', 'code', 'city', 'address', 'type', 'floorCount', 'remark', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """
        验证场地名称
        """
        # 验证名称长度
        if len(value) < 2 or len(value) > 50:
            raise serializers.ValidationError(
                "场地名称需为2-50字符",
                code='name_length'
            )
        
        # 验证名称唯一性
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
    
    def validate_code(self, value):
        """
        验证场地编码
        """
        # 验证编码不为空（仅在创建时）
        if not self.instance and (not value or len(value.strip()) == 0):
            raise serializers.ValidationError(
                "场地编码不能为空",
                code='code_empty'
            )
        
        # 验证编码格式（仅在创建时）
        if not self.instance and not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "编码只能包含字母、数字、下划线",
                code='code_format'
            )
        
        # 验证编码唯一性
        if self.instance:
            # 更新时排除自身
            if Venue.objects.filter(code=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "编码重复",
                    code='code_exists'
                )
        else:
            # 创建时检查
            if Venue.objects.filter(code=value).exists():
                raise serializers.ValidationError(
                    "编码重复",
                    code='code_exists'
                )
        return value
    
    def update(self, instance, validated_data):
        """
        更新场地信息
        """
        # 移除code字段，阻止修改编码
        if 'code' in validated_data:
            del validated_data['code']
        return super().update(instance, validated_data)