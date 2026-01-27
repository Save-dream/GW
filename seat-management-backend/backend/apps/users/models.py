from django.db import models


class User(models.Model):
    """
    人员模型（从OA系统同步）
    """
    id = models.CharField(
        max_length=50,
        primary_key=True,
        verbose_name="人员ID（OA工号）"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="姓名"
    )
    dept_id = models.CharField(
        max_length=50,
        verbose_name="部门ID"
    )
    dept_name = models.CharField(
        max_length=50,
        verbose_name="部门名称"
    )
    position = models.CharField(
        max_length=50,
        verbose_name="职位"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="手机号"
    )
    email = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="邮箱"
    )
    status = models.SmallIntegerField(
        default=1,
        verbose_name="状态",
        help_text="0:离职, 1:在职"
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
        verbose_name = "人员"
        verbose_name_plural = "人员"

    def __str__(self):
        return f"{self.name} ({self.id})"