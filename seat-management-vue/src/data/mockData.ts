import type { Venue, Floor, Area, Seat, User, Log } from '../types'

export const mockVenues: Venue[] = [
  { id: 1, name: '总部大楼', code: 'HQ', city: '北京市', address: '北京市朝阳区XX路XX号', type: '自有物业', status: 1, floorCount: 5, remark: '公司总部，核心办公区', createdAt: '2024-01-15 09:30:00', updatedAt: '2024-01-20 14:22:18', createdBy: '系统管理员(admin)' },
  { id: 2, name: '上海分部', code: 'SH', city: '上海市', address: '上海市浦东新区XX路XX号', type: '租赁办公', status: 1, floorCount: 3, remark: '上海地区办公点', createdAt: '2024-02-01 10:00:00', updatedAt: '2024-02-01 10:00:00', createdBy: '系统管理员(admin)' },
  { id: 3, name: '深圳研发中心', code: 'SZ', city: '深圳市', address: '深圳市南山区XX路XX号', type: '联合办公空间', status: 0, floorCount: 2, remark: '深圳研发团队办公点', createdAt: '2024-03-10 11:00:00', updatedAt: '2024-04-01 15:30:00', createdBy: '系统管理员(admin)' },
]

export const mockFloors: Floor[] = [
  { id: 1, venueId: 1, name: '一层', floorNo: '1F', imageUrl: '', status: 1, areaCount: 4, seatCount: 120 },
  { id: 2, venueId: 1, name: '二层', floorNo: '2F', imageUrl: '', status: 1, areaCount: 5, seatCount: 150 },
  { id: 3, venueId: 1, name: '三层', floorNo: '3F', imageUrl: '', status: 1, areaCount: 4, seatCount: 130 },
  { id: 4, venueId: 1, name: '四层', floorNo: '4F', imageUrl: '', status: 1, areaCount: 3, seatCount: 100 },
  { id: 5, venueId: 1, name: '五层', floorNo: '5F', imageUrl: '', status: 1, areaCount: 2, seatCount: 80 },
]

export const mockAreas: Area[] = [
  { id: 1, floorId: 1, areaNo: '101', areaName: '技术部办公室', areaType: 1, seatCount: 20, deptName: '技术部', position: { top: 10, left: 5, width: 35, height: 25 }, status: 1 },
  { id: 2, floorId: 1, areaNo: '102', areaName: '人事部办公区', areaType: 1, seatCount: 15, deptName: '人事部', position: { top: 10, left: 45, width: 25, height: 25 }, status: 1 },
  { id: 3, floorId: 1, areaNo: '103', areaName: '开放工位区', areaType: 4, seatCount: 40, deptName: '', position: { top: 45, left: 5, width: 65, height: 40 }, status: 1 },
  { id: 4, floorId: 1, areaNo: '104', areaName: '会议室A', areaType: 3, seatCount: 0, deptName: '', position: { top: 45, left: 75, width: 20, height: 20 }, status: 1 },
]

export const mockSeats: Seat[] = []

// 区域类型
// const areaTypes = ['专属区', '混合区', '会议室', '公共区']
for (let areaId = 1; areaId <= 4; areaId++) {
  const area = mockAreas.find(a => a.id === areaId)!
  const rows = Math.ceil(Math.sqrt(area.seatCount))
  const cols = Math.ceil(area.seatCount / rows)

  for (let i = 0; i < area.seatCount; i++) {
    const row = Math.floor(i / cols)
    const col = i % cols
    const isOccupied = Math.random() > 0.4
    const isMaintenance = Math.random() > 0.95

    mockSeats.push({
      id: areaId * 100 + i,
      areaId,
      seatNo: `${area.areaNo}-${i + 1}`,
      status: isMaintenance ? 2 : (isOccupied ? 1 : 0),
      userId: isOccupied ? `U${1000 + i}` : undefined,
      userName: isOccupied ? ['张三', '李四', '王芳', '赵伟', '陈静', '刘洋', '杨明', '周杰'][i % 8] : undefined,
      deptName: isOccupied ? ['技术部', '技术部', '人事部', '技术部', '人事部', '技术部', '技术部', '人事部'][i % 8] : undefined,
      position: { row, col },
      bindType: isOccupied ? 1 : 0
    })
  }
}

export const mockUsers: User[] = [
  { id: 'U1001', name: '张三', deptId: 'D01', deptName: '技术部', position: '高级工程师', phone: '138****0001', email: 'zhangsan@company.com', status: 1 },
  { id: 'U1002', name: '李四', deptId: 'D01', deptName: '技术部', position: '工程师', phone: '138****0002', email: 'lisi@company.com', status: 1 },
  { id: 'U1003', name: '王芳', deptId: 'D02', deptName: '人事部', position: '招聘专员', phone: '138****0003', email: 'wangfang@company.com', status: 1 },
  { id: 'U1004', name: '赵伟', deptId: 'D01', deptName: '技术部', position: '技术经理', phone: '138****0004', email: 'zhaowei@company.com', status: 1 },
  { id: 'U1005', name: '陈静', deptId: 'D02', deptName: '人事部', position: 'HR主管', phone: '138****0005', email: 'chenjing@company.com', status: 1 },
  { id: 'U1006', name: '刘洋', deptId: 'D01', deptName: '技术部', position: '架构师', phone: '138****0006', email: 'liuyang@company.com', status: 1 },
]

export const mockLogs: Log[] = [
  { id: 1, operator: '管理员', operation: '绑定人员', target: '张三', detail: '1F-101-1 ← 张三', time: '2026-01-26 10:30:25' },
  { id: 2, operator: '管理员', operation: '更换工位', target: '王芳', detail: '1F-102-3 → 1F-102-5', time: '2026-01-26 10:28:18' },
  { id: 3, operator: '管理员', operation: '解绑人员', target: '李四', detail: '1F-101-5 → 闲置', time: '2026-01-26 10:25:33' },
  { id: 4, operator: '管理员', operation: '额外绑定', target: '赵伟', detail: '1F-101-8（额外）', time: '2026-01-26 10:20:11' },
  { id: 5, operator: '管理员', operation: '批量生成', target: '区域103', detail: '生成40个工位', time: '2026-01-26 09:45:00' },
]