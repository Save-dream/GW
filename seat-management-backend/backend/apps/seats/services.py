import math
from django.db import transaction
from backend.apps.seats.models import Seat
from backend.apps.users.models import User
from backend.apps.logs.models import SeatLog


def generate_seats(area_id, count):
    """
    在指定区域内生成工位网格
    """
    from backend.apps.areas.models import Area
    area = Area.objects.get(id=area_id)
    
    # 计算最优行列布局
    width_ratio = 1.5  # 假设工位宽高比为1.5:1
    cols = math.ceil(math.sqrt(count * width_ratio))
    rows = math.ceil(count / cols)
    
    # 生成工位
    seats = []
    for i in range(count):
        row = i // cols + 1
        col = i % cols + 1
        
        # 计算工位坐标
        position_x = (col - 0.5) / cols
        position_y = (row - 0.5) / rows
        
        # 生成工位编号
        seat_no = f"{area.area_no}-{i+1}"
        
        seat = Seat(
            area_id=area_id,
            seat_no=seat_no,
            seat_status=0,  # 初始状态为闲置
            grid_row=row,
            grid_col=col,
            position_x=position_x,
            position_y=position_y,
            bind_type=0  # 初始未绑定
        )
        seats.append(seat)
    
    # 批量创建工位
    Seat.objects.bulk_create(seats)
    
    # 更新区域工位数
    area.seat_count = count
    area.save()
    
    return count


def bind_user_to_seat(seat_id, user_id, bind_type=1, operator_id="system", operator_name="系统"):
    """
    绑定人员到工位
    """
    with transaction.atomic():
        seat = Seat.objects.select_for_update().get(id=seat_id)
        user = User.objects.get(id=user_id)
        
        # 检查工位状态
        if seat.seat_status != 0:
            raise ValueError("工位未闲置，无法绑定")
        
        # 检查人员状态
        if user.status != 1:
            raise ValueError("人员非在职状态，无法绑定")
        
        # 记录操作前状态
        old_user_id = seat.current_user_id
        old_user_name = seat.current_user_name
        
        # 更新工位信息
        seat.current_user_id = user_id
        seat.current_user_name = user.name
        seat.current_dept_id = user.dept_id
        seat.seat_status = 1  # 状态改为占用
        seat.bind_type = bind_type
        seat.save()
        
        # 记录操作日志
        SeatLog.objects.create(
            seat_id=seat_id,
            seat_no=seat.seat_no,
            operation_type=2 if bind_type == 1 else 5,  # 2:绑定人员, 5:额外绑定
            old_user_id=None,
            old_user_name=None,
            new_user_id=user_id,
            new_user_name=user.name,
            operator_id=operator_id,
            operator_name=operator_name,
            operation_remark=f'绑定用户 {user.name} 到工位 {seat.seat_no}'
        )
        
        return seat


def unbind_user_from_seat(seat_id, operator_id="system", operator_name="系统"):
    """
    解绑人员与工位
    """
    with transaction.atomic():
        seat = Seat.objects.select_for_update().get(id=seat_id)
        
        # 检查工位状态
        if seat.seat_status != 1:
            raise ValueError("工位未被占用，无法解绑")
        
        # 记录操作前状态
        user_id = seat.current_user_id
        user_name = seat.current_user_name
        
        # 更新工位信息
        seat.current_user_id = None
        seat.current_user_name = None
        seat.current_dept_id = None
        seat.seat_status = 0  # 状态改为闲置
        seat.bind_type = 0  # 改为未绑定
        seat.save()
        
        # 记录操作日志
        if user_id:
            SeatLog.objects.create(
                seat_id=seat_id,
                seat_no=seat.seat_no,
                operation_type=3,  # 3:解绑人员
                old_user_id=user_id,
                old_user_name=user_name,
                new_user_id=None,
                new_user_name=None,
                operator_id=operator_id,
                operator_name=operator_name,
                operation_remark=f'解绑用户 {user_name} 从工位 {seat.seat_no}'
            )
        
        return seat


def transfer_user_seat(old_seat_id, new_seat_id, user_id, operator_id="system", operator_name="系统"):
    """
    更换人员工位
    """
    with transaction.atomic():
        old_seat = Seat.objects.select_for_update().get(id=old_seat_id)
        new_seat = Seat.objects.select_for_update().get(id=new_seat_id)
        user = User.objects.get(id=user_id)
        
        # 检查原工位是否属于该用户
        if old_seat.current_user_id != user_id:
            raise ValueError("原工位不属于该用户")
        
        # 检查新工位状态
        if new_seat.seat_status != 0:
            raise ValueError("新工位未闲置，无法更换")
        
        # 解绑原工位
        old_seat.current_user_id = None
        old_seat.current_user_name = None
        old_seat.current_dept_id = None
        old_seat.seat_status = 0  # 状态改为闲置
        old_seat.bind_type = 0  # 改为未绑定
        old_seat.save()
        
        # 绑定新工位
        new_seat.current_user_id = user_id
        new_seat.current_user_name = user.name
        new_seat.current_dept_id = user.dept_id
        new_seat.seat_status = 1  # 状态改为占用
        new_seat.bind_type = 1  # 主工位
        new_seat.save()
        
        # 记录操作日志
        SeatLog.objects.create(
            seat_id=new_seat_id,
            seat_no=new_seat.seat_no,
            operation_type=4,  # 4:更换工位
            old_user_id=user_id,
            old_user_name=user.name,
            new_user_id=user_id,
            new_user_name=user.name,
            operator_id=operator_id,
            operator_name=operator_name,
            operation_remark=f'用户 {user.name} 从工位 {old_seat.seat_no} 更换到工位 {new_seat.seat_no}',
            extra_info={'old_seat_id': old_seat_id, 'old_seat_no': old_seat.seat_no}
        )
        
        return new_seat


def extra_bind_user_to_seat(seat_id, user_id, operator_id="system", operator_name="系统"):
    """
    额外绑定人员到工位
    """
    with transaction.atomic():
        seat = Seat.objects.select_for_update().get(id=seat_id)
        user = User.objects.get(id=user_id)
        
        # 检查工位状态
        if seat.seat_status != 0:
            raise ValueError("工位未闲置，无法绑定")
        
        # 检查人员状态
        if user.status != 1:
            raise ValueError("人员非在职状态，无法绑定")
        
        # 更新工位信息
        seat.current_user_id = user_id
        seat.current_user_name = user.name
        seat.current_dept_id = user.dept_id
        seat.seat_status = 1  # 状态改为占用
        seat.bind_type = 2  # 额外绑定
        seat.save()
        
        # 记录操作日志
        SeatLog.objects.create(
            seat_id=seat_id,
            seat_no=seat.seat_no,
            operation_type=5,  # 5:额外绑定
            old_user_id=None,
            old_user_name=None,
            new_user_id=user_id,
            new_user_name=user.name,
            operator_id=operator_id,
            operator_name=operator_name,
            operation_remark=f'额外绑定用户 {user.name} 到工位 {seat.seat_no}'
        )
        
        return seat


def get_user_seats(user_id):
    """
    获取用户的所有工位
    """
    return Seat.objects.filter(current_user_id=user_id, seat_status=1)


def get_available_seats(area_id=None):
    """
    获取可用工位
    """
    queryset = Seat.objects.filter(seat_status=0)
    if area_id:
        queryset = queryset.filter(area_id=area_id)
    return queryset