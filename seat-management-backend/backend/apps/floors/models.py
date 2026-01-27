from django.db import models
from backend.apps.venues.models import Venue


class Floor(models.Model):
    """
    楼层模型
    """
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name='floor_set',
        verbose_name="所属场地"
    )
    floor_no = models.CharField(
        max_length=10,
        verbose_name="楼层编号",
        help_text="如：1F, 2F"
    )
    floor_name = models.CharField(
        max_length=50,
        verbose_name="楼层名称"
    )
    image_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="平面图URL"
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name="排序序号"
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
        verbose_name = "楼层"
        verbose_name_plural = "楼层"
        unique_together = ('venue', 'floor_no')  # 场地内楼层编号唯一

    def __str__(self):
        return f"{self.venue.name} - {self.floor_no} ({self.floor_name})"