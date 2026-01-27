import requests
import json
from datetime import datetime
from django.db import transaction
from .models import OASyncConfig, OASyncTask, WebhookEvent
from backend.apps.users.services import sync_users, process_user_change


def get_oa_sync_config(sync_type):
    """
    获取OA同步配置
    """
    try:
        config = OASyncConfig.objects.get(sync_type=sync_type, is_enabled=True)
        return config
    except OASyncConfig.DoesNotExist:
        return None


def create_sync_task(task_type, task_params=None):
    """
    创建同步任务
    """
    task = OASyncTask.objects.create(
        task_type=task_type,
        task_params=task_params,
        scheduled_time=datetime.now(),
        status=0
    )
    return task


def execute_sync_task(task):
    """
    执行同步任务
    """
    task.status = 1
    task.start_time = datetime.now()
    task.save()
    
    result = {}
    error_message = None
    
    try:
        # 根据任务类型执行不同的同步操作
        if task.task_type == 'user_sync':
            result = sync_users_from_oa()
        elif task.task_type == 'dept_sync':
            result = sync_departments_from_oa()
        else:
            result = {'message': f'未知的同步类型: {task.task_type}'}
        
        task.status = 2
        task.result = result
    except Exception as e:
        task.status = 3
        error_message = str(e)
        task.error_message = error_message
    
    task.end_time = datetime.now()
    task.save()
    
    return task


def sync_users_from_oa():
    """
    从OA系统同步用户
    """
    config = get_oa_sync_config('user_sync')
    if not config:
        raise Exception('用户同步配置不存在或未启用')
    
    # 调用OA API获取用户数据
    headers = {
        'Content-Type': 'application/json'
    }
    
    if config.api_key:
        headers['Authorization'] = f'Bearer {config.api_key}'
    
    response = requests.get(
        config.api_url,
        headers=headers,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f'OA API调用失败: {response.status_code} - {response.text}')
    
    data = response.json()
    users_data = data.get('data', [])
    
    # 同步用户数据
    synced_count = sync_users(users_data)
    
    # 更新配置
    config.last_sync_time = datetime.now()
    config.sync_status = 2
    config.save()
    
    return {
        'synced_count': synced_count,
        'total_users': len(users_data),
        'sync_time': datetime.now().isoformat()
    }


def sync_departments_from_oa():
    """
    从OA系统同步部门
    """
    config = get_oa_sync_config('dept_sync')
    if not config:
        raise Exception('部门同步配置不存在或未启用')
    
    # 调用OA API获取部门数据
    headers = {
        'Content-Type': 'application/json'
    }
    
    if config.api_key:
        headers['Authorization'] = f'Bearer {config.api_key}'
    
    response = requests.get(
        config.api_url,
        headers=headers,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f'OA API调用失败: {response.status_code} - {response.text}')
    
    data = response.json()
    departments_data = data.get('data', [])
    
    # 这里可以添加部门同步逻辑
    # 由于我们的系统中部门信息是从用户表中提取的，这里主要是记录同步状态
    
    # 更新配置
    config.last_sync_time = datetime.now()
    config.sync_status = 2
    config.save()
    
    return {
        'total_departments': len(departments_data),
        'sync_time': datetime.now().isoformat()
    }


def process_webhook_event(event):
    """
    处理Webhook事件
    """
    event.status = 1
    event.save()
    
    error_message = None
    
    try:
        event_data = event.event_data
        
        # 根据事件类型处理
        if event.event_type in [1, 2, 3]:  # 用户相关事件
            # 构建用户变更数据
            user_change_data = {
                'user_id': event_data.get('user_id'),
                'name': event_data.get('name'),
                'dept_id': event_data.get('dept_id'),
                'dept_name': event_data.get('dept_name'),
                'position': event_data.get('position'),
                'phone': event_data.get('phone'),
                'email': event_data.get('email'),
                'status': event_data.get('status', '在职'),
                'change_type': '入职' if event.event_type == 1 else '离职' if event.event_type == 3 else '调岗'
            }
            
            # 处理用户变更
            process_user_change(user_change_data)
        
        event.status = 2
    except Exception as e:
        event.status = 3
        error_message = str(e)
        event.error_message = error_message
        event.retry_count += 1
    
    event.processed_at = datetime.now()
    event.save()
    
    return event


def trigger_oa_sync(sync_type, force=False):
    """
    触发OA同步
    """
    config = get_oa_sync_config(sync_type)
    if not config:
        return {'success': False, 'message': '同步配置不存在或未启用'}
    
    # 检查是否需要同步
    if not force:
        last_sync = config.last_sync_time
        if last_sync:
            sync_interval = config.sync_interval
            time_since_last_sync = (datetime.now() - last_sync).total_seconds()
            if time_since_last_sync < sync_interval:
                return {'success': False, 'message': f'同步间隔未到，上次同步时间: {last_sync}'}
    
    # 创建并执行同步任务
    task = create_sync_task(sync_type)
    task = execute_sync_task(task)
    
    if task.status == 2:
        return {'success': True, 'message': '同步任务已启动', 'task_id': task.id}
    else:
        return {'success': False, 'message': '同步任务启动失败'}


def get_pending_webhook_events():
    """
    获取待处理的Webhook事件
    """
    events = WebhookEvent.objects.filter(status__in=[0, 3]).order_by('received_at')
    return events


def retry_failed_webhook_events():
    """
    重试失败的Webhook事件
    """
    events = WebhookEvent.objects.filter(status=3, retry_count__lt=3).order_by('received_at')
    
    for event in events:
        process_webhook_event(event)
    
    return len(events)


def get_sync_statistics():
    """
    获取同步统计信息
    """
    # 获取最近的同步任务
    recent_tasks = OASyncTask.objects.order_by('-created_at')[:10]
    
    # 获取同步配置状态
    configs = OASyncConfig.objects.all()
    
    # 构建统计信息
    statistics = {
        'recent_tasks': [],
        'configs': []
    }
    
    for task in recent_tasks:
        task_info = {
            'task_type': task.task_type,
            'status': task.status,
            'status_display': task.get_status_display(),
            'scheduled_time': task.scheduled_time.isoformat(),
            'start_time': task.start_time.isoformat() if task.start_time else None,
            'end_time': task.end_time.isoformat() if task.end_time else None,
            'error_message': task.error_message
        }
        statistics['recent_tasks'].append(task_info)
    
    for config in configs:
        config_info = {
            'sync_type': config.sync_type,
            'api_url': config.api_url,
            'sync_interval': config.sync_interval,
            'last_sync_time': config.last_sync_time.isoformat() if config.last_sync_time else None,
            'sync_status': config.sync_status,
            'is_enabled': config.is_enabled,
            'error_message': config.error_message
        }
        statistics['configs'].append(config_info)
    
    return statistics