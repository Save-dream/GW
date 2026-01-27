export interface Venue {
  id: number
  name: string
  address: string
  status: number
  floorCount: number
}

export interface Floor {
  id: number
  venueId: number
  name: string
  floorNo: string
  imageUrl: string
  status: number
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
  position: { top: number; left: number; width: number; height: number }
  status: number
}

export interface Seat {
  id: number
  areaId: number
  seatNo: string
  status: number // 0:闲置 1:占用 2:维修 3:停用
  userId?: string
  userName?: string
  deptName?: string
  position: { row: number; col: number }
  bindType: number // 0:未绑定 1:主工位 2:额外绑定
}

export interface User {
  id: string
  name: string
  deptId: string
  deptName: string
  position: string
  phone: string
  email: string
  status: number
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