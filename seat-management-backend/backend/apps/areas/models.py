from django.db import models
from backend.apps.floors.models import Floor


class Area(models.Model):
    """
    区域模型
    """
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        related_name='area_set',
        verbose_name="所属楼层"
    )
    area_no = models.CharField(
        max_length=20,
        verbose_name="区域编号",
        help_text="如：101, 102"
    )
    area_name = models.CharField(
        max_length=50,
        verbose_name="区域名称"
    )
    area_type = models.SmallIntegerField(
        default=1,
        verbose_name="区域类型",
        help_text="1:专属区, 2:混合区, 3:会议室, 4:公共区"
    )
    allowed_depts = models.TextField(
        default='[]',
        verbose_name="允许的部门ID列表",
        help_text="JSON格式，如：[\"D01\", \"D02\"]"
    )
    seat_count = models.IntegerField(
        default=0,
        verbose_name="计划工位数"
    )
    position_css = models.TextField(
        default='{}',
        verbose_name="位置样式",
        help_text="JSON格式，如：{\"top\": \"10px\", \"left\": \"10px\", \"width\": \"100px\", \"height\": \"100px\"}"
    )
    status = models.SmallIntegerField(
        default=1,
        verbose_name="状态",
        help_text="0:停用, 1:启用"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )

    class Meta:
        verbose_name = "区域"
        verbose_name_plural = "区域"
        unique_together = ('floor', 'area_no')  # 楼层内区域编号唯一

    def __str__(self):
        return f"{self.floor.venue.name} - {self.floor.floor_no} - {self.area_no} ({self.area_name})"