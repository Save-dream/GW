export interface Venue {
  id: number
  name: string
  code: string
  city: string
  address: string
  type: '自有物业' | '租赁办公' | '联合办公空间'
  status: 1 | 0 // 1: 启用, 0: 停用
  floorCount: number
  remark?: string
  createdAt?: string
  updatedAt?: string
  createdBy?: string
}

export interface Floor {
  id: number
  venueId: number
  name: string
  floorNo: string
  imageUrl: string
  status: 1 | 0
  areaCount: number
  seatCount: number
}

export interface Area {
  id: number
  floorId: number
  areaNo: string
  areaName: string
  areaType: number
  seatCount: number
  deptName: string
  position: {
    top: number
    left: number
    width: number
    height: number
  }
  status: 1 | 0
}

export interface Seat {
  id: number
  areaId: number
  seatNo: string
  status: 0 | 1 | 2 // 0: 闲置, 1: 占用, 2: 维护
  userId?: string
  userName?: string
  deptName?: string
  position: {
    row: number
    col: number
  }
  bindType: 0 | 1 // 0: 未绑定, 1: 绑定
}

export interface User {
  id: string
  name: string
  deptId: string
  deptName: string
  position: string
  phone: string
  email: string
  status: 1 | 0
}

export interface Log {
  id: number
  operator: string
  operation: string
  target: string
  detail: string
  time: string
}

export interface MenuItem {
  id: string
  label: string
  icon: any
}
