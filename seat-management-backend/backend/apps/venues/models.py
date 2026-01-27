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
    address = models.CharField(
        max_length=200,
        verbose_name="场地地址"
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