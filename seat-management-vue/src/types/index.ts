export interface Venue {
  id: number
  name: string
  address: string
  status: number
  floorCount: number
}

export interface Floor {
  id: number
  venue_id: number
  venue_name?: string
  floor_name: string
  floor_no: string
  image_url?: string
  sort_order: number
  status: number
}

export interface Area {
  id: number
  floor_id: number
  area_no: string
  area_name: string
  area_type: number
  seat_count: number
  dept_name: string
  position: { top: number; left: number; width: number; height: number }
  status: number
}

export interface Seat {
  id: number
  area_id: number
  seat_no: string
  status: number // 0:闲置 1:占用 2:维修 3:停用
  user_id?: string
  user_name?: string
  dept_name?: string
  position: { row: number; col: number }
  bind_type: number // 0:未绑定 1:主工位 2:额外绑定
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