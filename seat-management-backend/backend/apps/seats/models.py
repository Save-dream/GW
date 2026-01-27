from django.db import models
from backend.apps.areas.models import Area


class Seat(models.Model):
    """
    工位模型
    """
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name='seat_set',
        verbose_name="所属区域"
    )
    seat_no = models.CharField(
        max_length=20,
        verbose_name="工位编号",
        help_text="如：101-1, 102-2"
    )
    seat_status = models.SmallIntegerField(
        default=0,
        verbose_name="工位状态",
        help_text="0:闲置, 1:占用, 2:维修中, 3:停用"
    )
    grid_row = models.IntegerField(
        default=0,
        verbose_name="网格行号"
    )
    grid_col = models.IntegerField(
        default=0,
        verbose_name="网格列号"
    )
    position_x = models.FloatField(
        default=0.0,
        verbose_name="相对坐标X",
        help_text="0-1之间的值"
    )
    position_y = models.FloatField(
        default=0.0,
        verbose_name="相对坐标Y",
        help_text="0-1之间的值"
    )
    current_user_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="当前绑定人员ID（OA工号）"
    )
    current_user_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="人员姓名（冗余）"
    )
    current_dept_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="部门ID（冗余）"
    )
    bind_type = models.SmallIntegerField(
        default=0,
        verbose_name="绑定类型",
        help_text="0:未绑定, 1:主工位, 2:额外绑定"
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
        verbose_name = "工位"
        verbose_name_plural = "工位"
        unique_together = ('area', 'seat_no')  # 区域内工位编号唯一

    def __str__(self):
        return f"{self.area.floor.venue.name} - {self.area.floor.floor_no} - {self.area.area_no} - {self.seat_no}"