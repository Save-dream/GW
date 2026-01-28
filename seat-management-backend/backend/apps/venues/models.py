from django.db import models


class Venue(models.Model):
    """
    场地模型
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="场地名称"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="场地编码"
    )
    city = models.CharField(
        max_length=50,
        verbose_name="所在城市"
    )
    address = models.CharField(
        max_length=200,
        verbose_name="详细地址"
    )
    type = models.CharField(
        max_length=50,
        default="租赁办公",
        verbose_name="场地类型"
    )
    floorCount = models.IntegerField(
        default=1,
        verbose_name="楼层数"
    )
    remark = models.TextField(
        blank=True,
        verbose_name="备注说明"
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
        verbose_name = "场地"
        verbose_name_plural = "场地"

    def __str__(self):
        return self.name