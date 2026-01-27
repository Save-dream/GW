<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- 登录页面 -->
    <template v-if="!isLoggedIn">
      <Login @login-success="handleLoginSuccess" />
    </template>

    <!-- 主页面 -->
    <template v-else>
      <!-- 侧边栏 -->
      <Sidebar
        :show-sidebar="showSidebar"
        :current-view="currentView"
        :menu-items="menuItems"
        @update-view="setCurrentView"
      />

      <!-- 主内容区 -->
      <div class="flex-1 flex flex-col">
        <!-- 顶部导航 -->
        <Header
          :show-sidebar="showSidebar"
          :search-keyword="searchKeyword"
          @toggle-sidebar="toggleSidebar"
          @update-search="handleSearch"
        />

        <!-- 内容区域 -->
        <main class="flex-1 p-6 overflow-auto">
          <!-- 加载状态 -->
          <div v-if="loading" class="flex justify-center items-center h-64">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>

          <!-- 错误提示 -->
          <div v-else-if="error" class="mb-4">
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              <span class="font-bold">错误：</span>
              <span>{{ error }}</span>
            </div>
          </div>

          <!-- 主内容 -->
          <template v-else>
            <Dashboard
              v-if="currentView === 'dashboard'"
              :selected-venue="selectedVenue"
              :seat-stats="seatStats"
              :mock-logs="logs"
              :mock-venues="venues"
              :mock-floors="floors"
              @select-venue="setSelectedVenue"
              @select-floor="handleFloorSelect"
            />

            <VenueManagement
              v-else-if="currentView === 'venue'"
              :mock-venues="venues"
              :mock-floors="floors"
              :mock-areas="areas"
              @add-venue="handleAddVenue"
              @edit-venue="handleEditVenue"
              @view-venue="handleViewVenue"
              @toggle-venue-status="handleToggleVenueStatus"
            />

            <!-- Floor Management View -->
            <div v-else-if="currentView === 'floor'">
              <!-- Venue Selection Step -->
              <div v-if="!selectedVenue" class="bg-white rounded-xl shadow-sm border p-6">
                <h2 class="text-xl font-bold text-gray-800 mb-6">选择场地</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div
                    v-for="venue in venues"
                    :key="venue.id"
                    class="border rounded-lg p-4 cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors"
                    @click="setSelectedVenue(venue)"
                  >
                    <h3 class="font-medium">{{ venue.name }}</h3>
                    <p class="text-sm text-gray-500">{{ venue.address }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Floor Selection Step -->
              <div v-else-if="!selectedFloor" class="bg-white rounded-xl shadow-sm border p-6">
                <div class="flex items-center justify-between mb-6">
                  <h2 class="text-xl font-bold text-gray-800">选择楼层</h2>
                  <button
                    @click="selectedVenue = null"
                    class="text-blue-600 hover:underline"
                  >
                    更换场地
                  </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div
                    v-for="floor in floors.filter(f => f.venueId === selectedVenue.id)"
                    :key="floor.id"
                    class="border rounded-lg p-4 cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors"
                    @click="selectedFloor = floor"
                  >
                    <h3 class="font-medium">{{ floor.floorNo }} - {{ floor.name }}</h3>
                    <p class="text-sm text-gray-500">{{ floor.totalArea }}㎡</p>
                  </div>
                </div>
              </div>
              
              <!-- Floor Map View -->
              <FloorMap
                v-else
                :selected-floor="selectedFloor"
                :selected-venue="selectedVenue"
                :current-floor-areas="currentFloorAreas"
                :selected-area="selectedArea"
                @go-back="goToFloorSelection"
                @select-area="handleAreaSelect"
              />
            </div>
            
            <!-- Area Management View -->
            <div v-else-if="currentView === 'area'">
              <div class="bg-white rounded-xl shadow-sm border p-6">
                <h2 class="text-xl font-bold text-gray-800 mb-6">区域管理</h2>
                <p class="text-gray-500 mb-4">当前场地：{{ selectedVenue?.name }}</p>
                <p class="text-gray-500 mb-6">当前楼层：{{ selectedFloor?.floorNo }} - {{ selectedFloor?.name }}</p>
                
                <div class="space-y-4">
                  <div v-for="area in currentFloorAreas" :key="area.id" class="border rounded-lg p-4">
                    <div class="flex items-center justify-between">
                      <div>
                        <h3 class="font-medium">{{ area.areaNo }} - {{ area.areaName }}</h3>
                        <p class="text-sm text-gray-500">{{ getAreaTypeName(area.areaType) }}</p>
                      </div>
                      <div class="flex items-center gap-2">
                        <span class="text-sm">{{ area.seatCount }}个工位</span>
                        <button class="text-blue-600 hover:underline">编辑</button>
                        <button class="text-red-600 hover:underline">删除</button>
                      </div>
                    </div>
                  </div>
                </div>
                
                <button class="w-full mt-6 py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-500 transition-colors">
                  + 添加新区域
                </button>
              </div>
            </div>

            <SeatManagement
              v-else-if="currentView === 'seat'"
              :selected-area="selectedArea"
              :current-area-seats="currentAreaSeats"
              :selected-seat="selectedSeat"
              @go-back="goToArea"
              @select-seat="handleSeatClick"
            />

            <Binding
              v-else-if="currentView === 'binding'"
              :bind-mode="bindMode"
              :search-keyword="searchKeyword"
              :mock-seats="seats"
              :mock-users="users"
              :mock-floors="floors"
              :mock-areas="areas"
              @update-bind-mode="setBindMode"
              @update-search="setSearchKeyword"
              @select-seat="handleSeatClick"
              @assign-seat="handleUserAssign"
            />

            <Logs
              v-else-if="currentView === 'logs'"
              :mock-logs="logs"
            />

            <SettingsComponent v-else-if="currentView === 'settings'" />
          </template>
        </main>
      </div>
    </template>

    <!-- 场地管理模态框 -->
    <VenueModal
      :visible="showVenueModal"
      :is-edit="isEditMode"
      :venue="currentVenue"
      @close="handleVenueModalClose"
      @submit="handleVenueSubmit"
    />

    <!-- 场地详情模态框 -->
    <VenueDetail
      :visible="showVenueDetail"
      :venue="currentVenue"
      :floors="floors"
      :areas="areas"
      :logs="logs"
      @close="handleVenueDetailClose"
      @edit="handleVenueDetailEdit"
      @toggle-status="handleVenueDetailToggleStatus"
      @delete="handleVenueDetailDelete"
      @add-floor="handleAddFloor"
    />
    
    <!-- 楼层管理模态框 -->
    <FloorModal
      :visible="showFloorModal"
      :is-edit="isEditFloorMode"
      :floor="currentFloor"
      :venue-id="currentFloorVenueId"
      @close="handleFloorModalClose"
      @submit="handleFloorSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import Dashboard from './components/Dashboard.vue'
import VenueManagement from './components/VenueManagement.vue'
import FloorMap from './components/FloorMap.vue'
import SeatManagement from './components/SeatManagement.vue'
import Binding from './components/Binding.vue'
import Logs from './components/Logs.vue'
import SettingsComponent from './components/Settings.vue'
import Login from './components/Login.vue'
import VenueModal from './components/VenueModal.vue'
import VenueDetail from './components/VenueDetail.vue'
import FloorModal from './components/FloorModal.vue'
import { Home, Building2, LayoutGrid, MapPin, Monitor, Link, Clock, Settings } from 'lucide-vue-next'
import api from './services/api'
import { mockVenues, mockFloors, mockAreas, mockSeats, mockUsers, mockLogs } from './data/mockData'

// 状态管理
const currentView = ref<'dashboard' | 'venue' | 'floor' | 'area' | 'seat' | 'binding' | 'logs' | 'settings'>('dashboard')
const bindMode = ref<'seat' | 'person'>('seat')
const searchKeyword = ref('')
const loading = ref(false)
const error = ref<string | null>('')
const showSidebar = ref(true)

// 菜单配置
const menuItems = ref([
  { id: 'dashboard', label: '首页概览', icon: Home },
  { id: 'venue', label: '场地管理', icon: Building2 },
  { id: 'floor', label: '楼层管理', icon: LayoutGrid },
  { id: 'area', label: '区域管理', icon: MapPin },
  { id: 'seat', label: '工位管理', icon: Monitor },
  { id: 'binding', label: '绑定管理', icon: Link },
  { id: 'logs', label: '操作日志', icon: Clock },
  { id: 'settings', label: '系统设置', icon: Settings }
])

// 数据管理
const venues = ref<any[]>(mockVenues)
const floors = ref<any[]>(mockFloors)
const areas = ref<any[]>(mockAreas)
const seats = ref<any[]>(mockSeats)
const users = ref<any[]>(mockUsers)
const logs = ref<any[]>(mockLogs)

// 选中状态
const selectedVenue = ref<any>(null)
const selectedFloor = ref<any>(null)
const selectedArea = ref<any>(null)
const selectedSeat = ref<any>(null)

// 场地管理状态
const showVenueModal = ref(false)
const showVenueDetail = ref(false)
const isEditMode = ref(false)
const currentVenue = ref<any>(null)

// 楼层管理状态
const showFloorModal = ref(false)
const isEditFloorMode = ref(false)
const currentFloor = ref<any>(null)
const currentFloorVenueId = ref<number | undefined>(undefined)

// 计算属性
const currentFloorAreas = computed(() => {
  if (!selectedFloor.value) return []
  return areas.value.filter(area => area.floorId === selectedFloor.value.id)
})

const currentAreaSeats = computed(() => {
  if (!selectedArea.value) return []
  return seats.value.filter(seat => seat.areaId === selectedArea.value.id)
})

const seatStats = computed(() => {
  const total = seats.value.length
  const occupied = seats.value.filter(seat => seat.status === 1).length
  const empty = seats.value.filter(seat => seat.status === 0).length
  const maintenance = seats.value.filter(seat => seat.status === 2).length
  return { total, occupied, empty, maintenance }
})

// 方法
const setCurrentView = (view: string) => {
  currentView.value = view as typeof currentView.value
}

const setBindMode = (mode: typeof bindMode.value) => {
  bindMode.value = mode
}

const setSearchKeyword = (keyword: string) => {
  searchKeyword.value = keyword
}

const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value
}

const setSelectedVenue = (venue: any) => {
  selectedVenue.value = venue
  selectedFloor.value = null
  selectedArea.value = null
  selectedSeat.value = null
}

const handleFloorSelect = (floor: any) => {
  selectedFloor.value = floor
  currentView.value = 'floor'
}

const handleAreaSelect = (area: any) => {
  selectedArea.value = area
  currentView.value = 'seat'
}

const handleSeatClick = (seat: any) => {
  selectedSeat.value = seat
  currentView.value = 'binding'
}

const handleSearch = (keyword: string) => {
  searchKeyword.value = keyword
  currentView.value = 'binding'
  bindMode.value = 'person'
}

const handleUserAssign = (user: any) => {
  console.log('分配工位给用户:', user.name)
  // Here we would typically show a modal to select a seat for this user
  // For now, we'll just log it
  alert(`请为用户 ${user.name} 选择一个工位`)
}

const goToArea = () => {
  currentView.value = 'area'
  selectedSeat.value = null
}

const goToFloorSelection = () => {
  selectedFloor.value = null
  currentView.value = 'floor'
}

const getAreaTypeName = (type: number): string => {
  const typeMap: Record<number, string> = {
    1: '专属区',
    2: '混合区',
    3: '会议室',
    4: '公共区'
  }
  return typeMap[type] || '未知区域'
}

// 登录状态
const isLoggedIn = ref(false)

// 处理登录成功
const handleLoginSuccess = async () => {
  isLoggedIn.value = true
  // 加载初始数据
  await loadInitialData()
}

// 加载初始数据
const loadInitialData = async () => {
  try {
    await loadVenues()
    await loadUsers()
    await loadLogs()
  } catch (err) {
    console.error('加载数据失败:', err)
    error.value = '加载数据失败，请刷新页面重试'
  }
}

// 检查登录状态
const checkLoginStatus = () => {
  const token = localStorage.getItem('access_token')
  isLoggedIn.value = !!token
}

// 数据加载方法
const loadVenues = async () => {
  try {
    loading.value = true
    error.value = ''
    const data = await api.venue.getVenues()
    venues.value = data
    if (data.length > 0 && !selectedVenue.value) {
      selectedVenue.value = data[0]
      await loadFloors(data[0].id)
    }
  } catch (err) {
    error.value = '加载场地失败'
    console.error('加载场地失败:', err)
  } finally {
    loading.value = false
  }
}

const loadFloors = async (venueId: number) => {
  try {
    loading.value = true
    error.value = ''
    const data = await api.floor.getFloors(venueId)
    floors.value = data
    if (data.length > 0 && !selectedFloor.value) {
      selectedFloor.value = data[0]
      await loadAreas(data[0].id)
    }
  } catch (err) {
    error.value = '加载楼层失败'
    console.error('加载楼层失败:', err)
  } finally {
    loading.value = false
  }
}

const loadAreas = async (floorId: number) => {
  try {
    loading.value = true
    error.value = ''
    const data = await api.area.getAreas(floorId)
    areas.value = data
    if (data.length > 0 && !selectedArea.value) {
      selectedArea.value = data[0]
      await loadSeats(data[0].id)
    }
  } catch (err) {
    error.value = '加载区域失败'
    console.error('加载区域失败:', err)
  } finally {
    loading.value = false
  }
}

const loadSeats = async (areaId: number) => {
  try {
    loading.value = true
    error.value = ''
    const data = await api.seat.getSeats(areaId)
    seats.value = data
  } catch (err) {
    error.value = '加载工位失败'
    console.error('加载工位失败:', err)
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  try {
    loading.value = true
    error.value = ''
    const data = await api.user.getUsers()
    users.value = data
  } catch (err) {
    error.value = '加载人员失败'
    console.error('加载人员失败:', err)
  } finally {
    loading.value = false
  }
}

const loadLogs = async () => {
  try {
    loading.value = true
    error.value = ''
    const data = await api.log.getLogs()
    
    logs.value = (data.logs || []).map((log: any) => ({
      id: log.id,
      operation: log.operation_type_display,
      detail: log.operation_remark || buildLogDetail(log),
      time: formatLogTime(log.operation_time),
      seat_no: log.seat_no
    }))
  } catch (err) {
    error.value = '加载日志失败'
    console.error('加载日志失败:', err)
  } finally {
    loading.value = false
  }
}

const buildLogDetail = (log: any): string => {
  const operationMap: Record<number, string> = {
    1: '创建工位',
    2: `绑定人员：${log.new_user_name}`,
    3: `解绑人员：${log.old_user_name}`,
    4: `更换工位：${log.old_user_name} -> ${log.new_user_name}`,
    5: `额外绑定：${log.new_user_name}`,
    6: '批量生成工位',
    7: '修改工位信息',
    8: '删除工位',
    9: 'OA系统同步'
  }
  return operationMap[log.operation_type] || '未知操作'
}

const formatLogTime = (time: string): string => {
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}

// 场地管理事件处理
const handleAddVenue = () => {
  console.log('新增场地')
  isEditMode.value = false
  currentVenue.value = null
  showVenueModal.value = true
}

const handleEditVenue = (venue: any) => {
  console.log('编辑场地:', venue.name)
  isEditMode.value = true
  currentVenue.value = venue
  showVenueModal.value = true
}

const handleViewVenue = async (venue: any) => {
  console.log('查看详情:', venue.name)
  currentVenue.value = venue
  await loadFloors(venue.id)
  await loadAreasForVenue(venue.id)
  showVenueDetail.value = true
}

const loadAreasForVenue = async (venueId: number) => {
  try {
    const venueFloors = floors.value.filter(f => f.venueId === venueId)
    for (const floor of venueFloors) {
      await loadAreas(floor.id)
    }
  } catch (err) {
    console.error('加载区域失败:', err)
  }
}

const handleToggleVenueStatus = (venue: any) => {
  console.log('切换状态:', venue.name, venue.status === 1 ? '停用' : '启用')
  const newStatus = venue.status === 1 ? 0 : 1
  const venueIndex = venues.value.findIndex(v => v.id === venue.id)
  if (venueIndex !== -1) {
    venues.value[venueIndex].status = newStatus
  }
}

const handleVenueSubmit = (data: any) => {
  console.log('提交场地数据:', data)
  if (isEditMode.value && currentVenue.value) {
    // 编辑场地
    const venueIndex = venues.value.findIndex(v => v.id === currentVenue.value.id)
    if (venueIndex !== -1) {
      venues.value[venueIndex] = {
        ...venues.value[venueIndex],
        ...data,
        updatedAt: new Date().toLocaleString('zh-CN')
      }
    }
  } else {
    // 新增场地
    const newVenue = {
      id: venues.value.length + 1,
      ...data,
      createdAt: new Date().toLocaleString('zh-CN'),
      updatedAt: new Date().toLocaleString('zh-CN'),
      createdBy: '系统管理员(admin)'
    }
    venues.value.push(newVenue)
  }
  showVenueModal.value = false
}

const handleVenueDetailEdit = (venue: any) => {
  showVenueDetail.value = false
  handleEditVenue(venue)
}

const handleVenueDetailToggleStatus = (venue: any) => {
  handleToggleVenueStatus(venue)
}

const handleVenueDetailDelete = (venue: any) => {
  console.log('删除场地:', venue.name)
  const venueIndex = venues.value.findIndex(v => v.id === venue.id)
  if (venueIndex !== -1) {
    venues.value.splice(venueIndex, 1)
    // 同时删除相关的楼层数据
    floors.value = floors.value.filter(f => f.venueId !== venue.id)
  }
  showVenueDetail.value = false
}

const handleVenueModalClose = () => {
  showVenueModal.value = false
}

const handleVenueDetailClose = () => {
  showVenueDetail.value = false
}

const handleAddFloor = (venue: any) => {
  console.log('添加楼层:', venue.name)
  isEditFloorMode.value = false
  currentFloor.value = null
  currentFloorVenueId.value = venue.id
  showFloorModal.value = true
}

const handleFloorSubmit = async (data: any) => {
  console.log('提交楼层数据:', data)
  try {
    loading.value = true
    error.value = ''
    
    if (isEditFloorMode.value && currentFloor.value) {
      // 编辑楼层
      await api.floor.updateFloor(currentFloor.value.id, data)
      const floorIndex = floors.value.findIndex(f => f.id === currentFloor.value.id)
      if (floorIndex !== -1) {
        floors.value[floorIndex] = {
          ...floors.value[floorIndex],
          ...data
        }
      }
    } else {
      // 新增楼层
      const newFloorData = await api.floor.createFloor(data)
      floors.value.push(newFloorData)
    }
    
    // 重新加载日志以显示最新记录
    await loadLogs()
    showFloorModal.value = false
  } catch (err) {
    console.error('提交楼层数据失败:', err)
    error.value = '提交楼层数据失败'
  } finally {
    loading.value = false
  }
}

const handleFloorModalClose = () => {
  showFloorModal.value = false
}

// 初始化
onMounted(() => {
  checkLoginStatus()
  if (isLoggedIn.value) {
    loadInitialData()
  }
})
</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: 'Inter', 'system-ui', 'sans-serif';
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>