from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    系统用户模型（管理员）
    """
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="用户名"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="姓名"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="手机号"
    )
    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="邮箱"
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="是否为系统管理员"
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="最后登录时间"
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
        verbose_name = "系统用户"
        verbose_name_plural = "系统用户"

    def __str__(self):
        return self.username