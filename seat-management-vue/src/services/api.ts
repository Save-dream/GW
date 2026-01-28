// API服务基础配置
const API_BASE_URL = 'http://localhost:8000/api';

// 获取存储的token
const getToken = (): string | null => {
  return localStorage.getItem('access_token');
};

// 设置token到本地存储
const setToken = (token: string): void => {
  localStorage.setItem('access_token', token);
};

// 清除token
const clearToken = (): void => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

// 模拟数据
const mockData = {
  venues: [
    {
      id: 1,
      name: '总部大厦',
      address: '北京市朝阳区建国路88号',
      description: '公司总部办公大楼',
      created_at: '2024-01-01T00:00:00Z'
    },
    {
      id: 2,
      name: '研发中心',
      address: '北京市海淀区中关村大街1号',
      description: '研发部门办公场所',
      created_at: '2024-01-02T00:00:00Z'
    }
  ],
  floors: [
    {
      id: 1,
      venue_id: 1,
      name: '1楼',
      description: '一层办公区',
      created_at: '2024-01-01T00:00:00Z'
    },
    {
      id: 2,
      venue_id: 1,
      name: '2楼',
      description: '二层办公区',
      created_at: '2024-01-01T00:00:00Z'
    }
  ],
  areas: [
    {
      id: 1,
      floor_id: 1,
      name: 'A区',
      description: 'A区办公区',
      created_at: '2024-01-01T00:00:00Z'
    },
    {
      id: 2,
      floor_id: 1,
      name: 'B区',
      description: 'B区办公区',
      created_at: '2024-01-01T00:00:00Z'
    }
  ],
  seats: [
    {
      id: 1,
      area_id: 1,
      seat_no: 'A1-01',
      status: 1,
      user_id: null,
      created_at: '2024-01-01T00:00:00Z'
    },
    {
      id: 2,
      area_id: 1,
      seat_no: 'A1-02',
      status: 1,
      user_id: null,
      created_at: '2024-01-01T00:00:00Z'
    }
  ],
  users: [
    {
      id: 1,
      name: '张三',
      email: 'zhangsan@example.com',
      department: '技术部',
      created_at: '2024-01-01T00:00:00Z'
    },
    {
      id: 2,
      name: '李四',
      email: 'lisi@example.com',
      department: '产品部',
      created_at: '2024-01-01T00:00:00Z'
    }
  ],
  logs: {
    logs: [
      {
        id: 1,
        operation_type: 1,
        operation_type_display: '创建',
        operation_remark: '创建了工位A1-01',
        operation_time: '2024-01-01T00:00:00Z',
        seat_no: 'A1-01'
      },
      {
        id: 2,
        operation_type: 2,
        operation_type_display: '绑定',
        operation_remark: '绑定了人员张三到工位A1-01',
        operation_time: '2024-01-01T00:00:00Z',
        seat_no: 'A1-01'
      }
    ]
  }
};

// 基础请求函数
async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  // 生产环境中使用真实API请求
  const token = getToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      // 在开发环境中，如果遇到401错误，使用模拟数据作为备份
      if (process.env.NODE_ENV === 'development' && response.status === 401) {
        console.warn('开发环境：API请求返回401未授权，使用模拟数据');
        
        // 根据URL返回对应的模拟数据
        if (url.includes('/venue/venues')) {
          return mockData.venues as T;
        } else if (url.includes('/floor/floors')) {
          return mockData.floors as T;
        } else if (url.includes('/area/areas')) {
          return mockData.areas as T;
        } else if (url.includes('/seats')) {
          return mockData.seats as T;
        } else if (url.includes('/user/list')) {
          return mockData.users as T;
        } else if (url.includes('/log/logs')) {
          return mockData.logs as T;
        }
        
        return [] as T;
      }
      
      if (response.status === 401) {
        clearToken();
      }
      
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    // 在开发环境中，如果遇到网络错误，使用模拟数据作为备份
    if (process.env.NODE_ENV === 'development') {
      console.warn('开发环境：API请求错误，使用模拟数据', error);
      
      // 根据URL返回对应的模拟数据
      if (url.includes('/venue/venues')) {
        return mockData.venues as T;
      } else if (url.includes('/floor/floors')) {
        return mockData.floors as T;
      } else if (url.includes('/area/areas')) {
        return mockData.areas as T;
      } else if (url.includes('/seats')) {
        return mockData.seats as T;
      } else if (url.includes('/user/list')) {
        return mockData.users as T;
      } else if (url.includes('/log/logs')) {
        return mockData.logs as T;
      }
      
      return [] as T;
    }
    
    console.error('API request error:', error);
    throw error;
  }
}

// 认证相关API
export const authApi = {
  // 登录
  async login(username: string, password: string): Promise<{ access: string; refresh: string }> {
    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '登录失败');
    }

    const data = await response.json();
    setToken(data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  },

  // 登出
  logout(): void {
    clearToken();
  },

  // 刷新token
  async refreshToken(refreshToken: string): Promise<{ access: string }> {
    const response = await fetch('http://localhost:8000/api/token/refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '刷新token失败');
    }

    const data = await response.json();
    setToken(data.access);
    return data;
  },
};

// 场地相关API
export const venueApi = {
  // 获取场地列表
  async getVenues() {
    return request<any[]>('/admin/venue/venues');
  },

  // 获取场地详情
  async getVenueDetail(id: number) {
    return request<any>(`/admin/venue/venues/${id}`);
  },

  // 创建场地
  async createVenue(data: any) {
    return request<any>('/admin/venue/venues', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // 更新场地
  async updateVenue(id: number, data: any) {
    return request<any>(`/admin/venue/venues/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  // 删除场地
  async deleteVenue(id: number) {
    return request<any>(`/admin/venue/venues/${id}`, {
      method: 'DELETE',
    });
  },
};

// 楼层相关API
export const floorApi = {
  // 获取楼层列表
  async getFloors(venueId?: number) {
    const url = venueId ? `/admin/floor/floors?venue_id=${venueId}` : '/admin/floor/floors';
    return request<any[]>(url);
  },

  // 获取楼层详情
  async getFloorDetail(id: number) {
    return request<any>(`/admin/floor/floors/${id}`);
  },

  // 创建楼层
  async createFloor(data: any) {
    return request<any>('/admin/floor/floors', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // 更新楼层
  async updateFloor(id: number, data: any) {
    return request<any>(`/admin/floor/floors/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  // 删除楼层
  async deleteFloor(id: number) {
    return request<any>(`/admin/floor/floors/${id}`, {
      method: 'DELETE',
    });
  },
};

// 区域相关API
export const areaApi = {
  // 获取区域列表
  async getAreas(floorId?: number) {
    const url = floorId ? `/admin/area/areas?floor_id=${floorId}` : '/admin/area/areas';
    return request<any[]>(url);
  },

  // 获取区域详情
  async getAreaDetail(id: number) {
    return request<any>(`/admin/area/areas/${id}`);
  },

  // 创建区域
  async createArea(data: any) {
    return request<any>('/admin/area/areas', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // 更新区域
  async updateArea(id: number, data: any) {
    return request<any>(`/admin/area/areas/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  // 删除区域
  async deleteArea(id: number) {
    return request<any>(`/admin/area/areas/${id}`, {
      method: 'DELETE',
    });
  },
};

// 工位相关API
export const seatApi = {
  // 获取工位列表
  async getSeats(areaId?: number) {
    const url = areaId ? `/admin/seats?area_id=${areaId}` : '/admin/seats';
    return request<any[]>(url);
  },

  // 获取工位详情
  async getSeatDetail(id: number) {
    return request<any>(`/admin/seats/${id}`);
  },

  // 创建工位
  async createSeat(data: any) {
    return request<any>('/admin/seats', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // 批量生成工位
  async generateSeats(areaId: number, count: number) {
    return request<any>('/admin/seats/generate', {
      method: 'POST',
      body: JSON.stringify({ area_id: areaId, count }),
    });
  },

  // 绑定工位
  async bindSeat(seatId: number, userId: string, bindType: number = 1) {
    return request<any>('/seat/bind', {
      method: 'POST',
      body: JSON.stringify({ seat_id: seatId, user_id: userId, bind_type: bindType }),
    });
  },

  // 解绑工位
  async unbindSeat(seatId: number) {
    return request<any>('/seat/unbind', {
      method: 'POST',
      body: JSON.stringify({ seat_id: seatId }),
    });
  },

  // 更换工位
  async transferSeat(oldSeatId: number, newSeatId: number, userId: string) {
    return request<any>('/seat/transfer', {
      method: 'POST',
      body: JSON.stringify({ old_seat_id: oldSeatId, new_seat_id: newSeatId, user_id: userId }),
    });
  },
};

// 人员相关API
export const userApi = {
  // 获取人员列表
  async getUsers() {
    return request<any[]>('/admin/user/list');
  },

  // 获取人员详情
  async getUserDetail(id: string) {
    return request<any>(`/admin/user/query?user_id=${id}`);
  },

  // 员工端获取我的工位
  async getMySeats() {
    return request<any>('/user/my-seat');
  },

  // 员工端获取楼层列表
  async getUserFloors() {
    return request<any[]>('/user/floor');
  },

  // 员工端获取楼层详情
  async getUserFloorDetail(id: number) {
    return request<any>(`/user/floor/${id}`);
  },

  // 员工端全局搜索
  async search(q: string) {
    return request<any>(`/user/search?q=${encodeURIComponent(q)}`);
  },
};

// 日志相关API
export const logApi = {
  // 获取操作日志列表
  async getLogs(params?: {
    seat_no?: string;
    operation_type?: number;
    start_time?: string;
    end_time?: string;
    operator_id?: string;
    user_id?: string;
    page?: number;
    page_size?: number;
  }) {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, String(value));
        }
      });
    }
    
    const url = `/admin/log/logs${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
    return request<any>(url);
  },
};

// 导出默认API对象
export default {
  auth: authApi,
  venue: venueApi,
  floor: floorApi,
  area: areaApi,
  seat: seatApi,
  user: userApi,
  log: logApi,
};
