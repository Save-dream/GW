from django.db import transaction
from django.db.models import Q
from .models import User
from backend.apps.seats.models import Seat


def sync_users(users_data):
    """
    同步人员信息
    """
    synced_count = 0
    
    with transaction.atomic():
        for user_data in users_data:
            user_id = user_data.get('user_id')
            if not user_id:
                continue
            
            # 转换状态
            status = 1 if user_data.get('status') == '在职' else 0
            
            # 更新或创建用户
            user, created = User.objects.update_or_create(
                id=user_id,
                defaults={
                    'name': user_data.get('name', ''),
                    'dept_id': user_data.get('dept_id', ''),
                    'dept_name': user_data.get('dept_name', ''),
                    'position': user_data.get('position', ''),
                    'phone': user_data.get('phone', ''),
                    'email': user_data.get('email', ''),
                    'status': status
                }
            )
            
            # 如果用户离职，解绑所有工位
            if status == 0:
                unbind_user_seats(user_id)
            
            synced_count += 1
    
    return synced_count


def unbind_user_seats(user_id):
    """
    解绑用户的所有工位
    """
    seats = Seat.objects.filter(current_user_id=user_id)
    for seat in seats:
        seat.current_user_id = None
        seat.current_user_name = None
        seat.current_dept_id = None
        seat.seat_status = 0
        seat.bind_type = 0
        seat.save()


def process_user_change(user_change_data):
    """
    处理人员变更
    """
    user_id = user_change_data.get('user_id')
    if not user_id:
        return False
    
    # 转换状态
    status = 1 if user_change_data.get('status') == '在职' else 0
    
    # 更新用户信息
    user, created = User.objects.update_or_create(
        id=user_id,
        defaults={
            'name': user_change_data.get('name', ''),
            'dept_id': user_change_data.get('dept_id', ''),
            'dept_name': user_change_data.get('dept_name', ''),
            'position': user_change_data.get('position', ''),
            'phone': user_change_data.get('phone', ''),
            'email': user_change_data.get('email', ''),
            'status': status
        }
    )
    
    # 如果用户离职，解绑所有工位
    if status == 0:
        unbind_user_seats(user_id)
    
    return True


def search(query):
    """
    全局搜索人员和工位
    """
    # 搜索人员
    users = User.objects.filter(
        Q(name__icontains=query) | Q(id__icontains=query) | Q(dept_name__icontains=query)
    ).filter(status=1)[:10]
    
    # 搜索工位
    seats = Seat.objects.filter(
        Q(seat_no__icontains=query) | Q(current_user_name__icontains=query)
    )[:10]
    
    # 格式化结果
    user_results = []
    for user in users:
        user_results.append({
            "id": user.id,
            "name": user.name,
            "dept_id": user.dept_id,
            "dept_name": user.dept_name,
            "position": user.position,
            "phone": user.phone,
            "email": user.email,
            "status": user.status
        })
    
    seat_results = []
    for seat in seats:
        seat_results.append({
            "id": seat.id,
            "seat_no": seat.seat_no,
            "seat_status": seat.seat_status,
            "current_user_id": seat.current_user_id,
            "current_user_name": seat.current_user_name,
            "current_dept_id": seat.current_dept_id,
            "area_name": seat.area.area_name,
            "floor_name": seat.area.floor.floor_name,
            "venue_name": seat.area.floor.venue.name
        })
    
    return {
        "users": user_results,
        "seats": seat_results
    }


def get_user_seats(user_id):
    """
    获取用户的所有工位
    """
    seats = Seat.objects.filter(current_user_id=user_id, seat_status=1)
    
    # 格式化结果
    seat_results = []
    for seat in seats:
        seat_results.append({
            "id": seat.id,
            "seat_no": seat.seat_no,
            "area_name": seat.area.area_name,
            "floor_name": seat.area.floor.floor_name,
            "venue_name": seat.area.floor.venue.name,
            "bind_type": seat.bind_type
        })
    
    return seat_results


def get_seat_with_user(seat_id):
    """
    获取带人员信息的工位详情
    """
    seat = Seat.objects.get(id=seat_id)
    
    # 构建结果
    result = {
        "id": seat.id,
        "area_id": seat.area.id,
        "area_no": seat.area.area_no,
        "area_name": seat.area.area_name,
        "floor_name": seat.area.floor.floor_name,
        "floor_no": seat.area.floor.floor_no,
        "venue_name": seat.area.floor.venue.name,
        "seat_no": seat.seat_no,
        "seat_status": seat.seat_status,
        "grid_row": seat.grid_row,
        "grid_col": seat.grid_col,
        "position_x": seat.position_x,
        "position_y": seat.position_y,
        "current_user_id": seat.current_user_id,
        "current_user_name": seat.current_user_name,
        "current_dept_id": seat.current_dept_id,
        "bind_type": seat.bind_type
    }
    
    # 如果工位被占用，添加人员详细信息
    if seat.current_user_id:
        try:
            user = User.objects.get(id=seat.current_user_id)
            result.update({
                "current_dept_name": user.dept_name,
                "position": user.position,
                "phone": user.phone,
                "email": user.email
            })
        except User.DoesNotExist:
            pass
    
    return result