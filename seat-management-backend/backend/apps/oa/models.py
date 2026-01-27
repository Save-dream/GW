from django.db import models


class OASyncConfig(models.Model):
    """
    OA系统同步配置模型
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name="配置ID"
    )
    sync_type = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="同步类型",
        help_text="如：user_sync, dept_sync 等"
    )
    api_url = models.CharField(
        max_length=255,
        verbose_name="API地址"
    )
    api_key = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="API密钥"
    )
    sync_interval = models.IntegerField(
        default=3600,
        verbose_name="同步间隔（秒）",
        help_text="默认3600秒（1小时）"
    )
    last_sync_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="最后同步时间"
    )
    sync_status = models.SmallIntegerField(
        default=0,
        verbose_name="同步状态",
        help_text="0:未同步, 1:同步中, 2:同步成功, 3:同步失败"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="错误信息"
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name="是否启用"
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
        verbose_name = "OA同步配置"
        verbose_name_plural = "OA同步配置"

    def __str__(self):
        return f"{self.sync_type} - {self.api_url}"


class OASyncTask(models.Model):
    """
    OA系统同步任务模型
    """
    TASK_STATUS_CHOICES = (
        (0, '待执行'),
        (1, '执行中'),
        (2, '执行成功'),
        (3, '执行失败'),
    )
    
    id = models.AutoField(
        primary_key=True,
        verbose_name="任务ID"
    )
    task_type = models.CharField(
        max_length=50,
        verbose_name="任务类型",
        help_text="如：user_sync, dept_sync 等"
    )
    task_params = models.JSONField(
        blank=True,
        null=True,
        verbose_name="任务参数"
    )
    status = models.SmallIntegerField(
        choices=TASK_STATUS_CHOICES,
        default=0,
        verbose_name="任务状态"
    )
    result = models.JSONField(
        blank=True,
        null=True,
        verbose_name="执行结果"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="错误信息"
    )
    scheduled_time = models.DateTimeField(
        verbose_name="计划执行时间"
    )
    start_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="开始执行时间"
    )
    end_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="结束执行时间"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )

    class Meta:
        verbose_name = "OA同步任务"
        verbose_name_plural = "OA同步任务"
        ordering = ['-scheduled_time']

    def __str__(self):
        return f"{self.task_type} - {self.get_status_display()}"


class WebhookEvent(models.Model):
    """
    Webhook事件记录模型
    """
    EVENT_TYPE_CHOICES = (
        (1, '用户创建'),
        (2, '用户更新'),
        (3, '用户删除'),
        (4, '部门创建'),
        (5, '部门更新'),
        (6, '部门删除'),
        (7, '其他事件'),
    )
    
    STATUS_CHOICES = (
        (0, '待处理'),
        (1, '处理中'),
        (2, '处理成功'),
        (3, '处理失败'),
    )
    
    id = models.AutoField(
        primary_key=True,
        verbose_name="事件ID"
    )
    event_type = models.SmallIntegerField(
        choices=EVENT_TYPE_CHOICES,
        verbose_name="事件类型"
    )
    event_data = models.JSONField(
        verbose_name="事件数据"
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name="处理状态"
    )
    retry_count = models.IntegerField(
        default=0,
        verbose_name="重试次数"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="错误信息"
    )
    received_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="接收时间"
    )
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="处理时间"
    )

    class Meta:
        verbose_name = "Webhook事件"
        verbose_name_plural = "Webhook事件"
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.get_status_display()}"