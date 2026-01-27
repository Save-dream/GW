import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from backend.apps.venues.models import Venue
from backend.apps.floors.models import Floor
from backend.apps.areas.models import Area
from backend.apps.seats.models import Seat
from backend.apps.users.models import User
from backend.apps.authentication.models import User as AuthUser
from rest_framework_simplejwt.tokens import RefreshToken


class SeatManagementTest(TestCase):
    """
    工位管理系统测试
    """
    
    def setUp(self):
        """
        测试初始化
        """
        self.client = APIClient()
        
        # 创建认证用户
        self.auth_user = AuthUser.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        
        # 获取JWT token
        refresh = RefreshToken.for_user(self.auth_user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # 创建测试数据
        self.create_test_data()
    
    def create_test_data(self):
        """
        创建测试数据
        """
        # 创建场地
        self.venue = Venue.objects.create(
            name='测试场地',
            address='测试地址'
        )
        
        # 创建楼层
        self.floor = Floor.objects.create(
            venue=self.venue,
            floor_no=1,
            floor_name='测试楼层',
            image_url='test.jpg'
        )
        
        # 创建区域
        self.area = Area.objects.create(
            floor=self.floor,
            area_no=1,
            area_name='测试区域',
            area_type=1,
            seat_count=10
        )
        
        # 创建用户
        self.user = User.objects.create(
            id='user001',
            name='测试用户',
            dept_id='dept001',
            dept_name='测试部门',
            position='测试职位',
            status=1
        )
    
    def test_create_venue(self):
        """
        测试创建场地
        """
        url = reverse('venue_list_create')
        data = {
            'name': '新测试场地',
            'address': '新测试地址'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venue.objects.count(), 2)
    
    def test_create_floor(self):
        """
        测试创建楼层
        """
        url = reverse('floor_list_create')
        data = {
            'venue_id': self.venue.id,
            'floor_no': 2,
            'floor_name': '新测试楼层',
            'image_url': 'new_floor.jpg'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Floor.objects.count(), 2)
    
    def test_create_area(self):
        """
        测试创建区域
        """
        url = reverse('area_list_create')
        data = {
            'floor_id': self.floor.id,
            'area_no': 2,
            'area_name': '新测试区域',
            'area_type': 1,
            'seat_count': 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Area.objects.count(), 2)
    
    def test_generate_seats(self):
        """
        测试批量生成工位
        """
        url = reverse('seat_generate')
        data = {
            'area_id': self.area.id,
            'count': 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Seat.objects.count(), 5)
    
    def test_bind_user_to_seat(self):
        """
        测试绑定用户到工位
        """
        # 先生成一个工位
        seat = Seat.objects.create(
            area=self.area,
            seat_no='A001',
            seat_status=0
        )
        
        # 绑定用户
        url = reverse('seat_bind')
        data = {
            'seat_id': seat.id,
            'user_id': self.user.id,
            'bind_type': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证绑定结果
        seat.refresh_from_db()
        self.assertEqual(seat.current_user_id, self.user.id)
        self.assertEqual(seat.current_user_name, self.user.name)
        self.assertEqual(seat.seat_status, 1)
    
    def test_unbind_user_from_seat(self):
        """
        测试解绑用户从工位
        """
        # 先生成一个工位并绑定用户
        seat = Seat.objects.create(
            area=self.area,
            seat_no='A001',
            seat_status=1,
            current_user_id=self.user.id,
            current_user_name=self.user.name,
            current_dept_id=self.user.dept_id
        )
        
        # 解绑用户
        url = reverse('seat_unbind')
        data = {
            'seat_id': seat.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证解绑结果
        seat.refresh_from_db()
        self.assertIsNone(seat.current_user_id)
        self.assertIsNone(seat.current_user_name)
        self.assertIsNone(seat.current_dept_id)
        self.assertEqual(seat.seat_status, 0)
    
    def test_transfer_seat(self):
        """
        测试更换工位
        """
        # 生成两个工位
        seat1 = Seat.objects.create(
            area=self.area,
            seat_no='A001',
            seat_status=1,
            current_user_id=self.user.id,
            current_user_name=self.user.name,
            current_dept_id=self.user.dept_id
        )
        
        seat2 = Seat.objects.create(
            area=self.area,
            seat_no='A002',
            seat_status=0
        )
        
        # 更换工位
        url = reverse('seat_transfer')
        data = {
            'old_seat_id': seat1.id,
            'new_seat_id': seat2.id,
            'user_id': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证结果
        seat1.refresh_from_db()
        seat2.refresh_from_db()
        
        self.assertIsNone(seat1.current_user_id)
        self.assertEqual(seat1.seat_status, 0)
        
        self.assertEqual(seat2.current_user_id, self.user.id)
        self.assertEqual(seat2.current_user_name, self.user.name)
        self.assertEqual(seat2.seat_status, 1)
    
    def test_user_floor_list(self):
        """
        测试员工端获取楼层列表
        """
        url = reverse('user_floor_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_user_floor_detail(self):
        """
        测试员工端获取楼层详情
        """
        url = reverse('user_floor_detail', args=[self.floor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.floor.id)
    
    def test_user_search(self):
        """
        测试员工端全局搜索
        """
        url = reverse('user_search') + '?q=测试'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_my_seat(self):
        """
        测试员工端获取我的工位
        """
        # 先生成一个工位并绑定当前用户
        seat = Seat.objects.create(
            area=self.area,
            seat_no='A001',
            seat_status=1,
            current_user_id=self.auth_user.username,  # 使用认证用户的username作为OA工号
            current_user_name='admin',
            current_dept_id='dept001'
        )
        
        url = reverse('user_my_seat')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['seats']), 0)


if __name__ == '__main__':
    unittest.main()
