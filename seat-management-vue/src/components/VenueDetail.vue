<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col">
      <div class="p-6 border-b flex items-center justify-between">
        <div>
          <h3 class="text-xl font-bold">{{ venue?.name }}</h3>
          <p class="text-sm text-gray-500">编码：{{ venue?.code }} | {{ venue?.city }}·{{ venue?.address }}</p>
        </div>
        <div class="flex items-center gap-3">
          <button @click="handleEdit" class="px-3 py-1 border rounded-lg text-sm hover:bg-gray-50">编辑</button>
          <button 
            @click="handleToggleStatus" 
            :class="[
              'px-3 py-1 rounded-lg text-sm',
              venue?.status === 1 
                ? 'bg-gray-100 text-gray-700 hover:bg-gray-200 border'
                : 'bg-green-100 text-green-700 hover:bg-green-200 border border-green-200'
            ]"
          >
            {{ venue?.status === 1 ? '停用' : '启用' }}
          </button>
          <button @click="handleDelete" class="px-3 py-1 bg-red-100 text-red-700 rounded-lg text-sm hover:bg-red-200 border border-red-200">删除</button>
          <button @click="handleClose" class="p-1 hover:bg-gray-100 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
      </div>
      <div class="border-b">
        <div class="flex">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'px-6 py-3 border-b-2',
              activeTab === tab.id ? 'border-blue-600 text-blue-600 font-medium' : 'border-transparent hover:text-gray-600'
            ]"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>
      <div class="flex-1 overflow-y-auto p-6">
        <!-- 基本信息 -->
        <div v-if="activeTab === 'basic'" class="space-y-6">
          <div class="bg-gray-50 rounded-lg p-6">
            <h4 class="text-lg font-semibold mb-4">基本信息</h4>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500">场地类型</p>
                <p class="font-medium">{{ venue?.type }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">创建时间</p>
                <p class="font-medium">{{ venue?.createdAt || '-' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">更新时间</p>
                <p class="font-medium">{{ venue?.updatedAt || '-' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">创建人</p>
                <p class="font-medium">{{ venue?.createdBy || '-' }}</p>
              </div>
              <div class="col-span-2">
                <p class="text-sm text-gray-500">备注</p>
                <p class="font-medium">{{ venue?.remark || '-' }}</p>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 rounded-lg p-6">
            <h4 class="text-lg font-semibold mb-4">统计概览</h4>
            <div class="grid grid-cols-3 gap-4">
              <div class="bg-white rounded-lg p-4 border">
                <p class="text-2xl font-bold text-blue-600">{{ venue?.floorCount }}层</p>
                <p class="text-sm text-gray-500">楼层数</p>
              </div>
              <div class="bg-white rounded-lg p-4 border">
                <p class="text-2xl font-bold text-blue-600">{{ getAreaCount() }}</p>
                <p class="text-sm text-gray-500">区域数</p>
              </div>
              <div class="bg-white rounded-lg p-4 border">
                <p class="text-2xl font-bold text-blue-600">{{ getTotalSeats() }}</p>
                <p class="text-sm text-gray-500">工位数</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 楼层管理 -->
        <div v-else-if="activeTab === 'floors'" class="space-y-4">
          <div class="flex items-center justify-between">
            <h4 class="text-lg font-semibold">楼层列表</h4>
            <button @click="handleAddFloor" class="flex items-center gap-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              添加楼层
            </button>
          </div>
          <div class="space-y-3">
            <div 
              v-for="floor in getVenueFloors()" 
              :key="floor.id"
              class="bg-white rounded-lg p-4 border flex items-center justify-between"
            >
              <div>
                <h5 class="font-medium">{{ floor.floorNo }} {{ floor.name }}</h5>
                <p class="text-sm text-gray-500">区域数：{{ floor.areaCount }} | 工位数：{{ floor.seatCount }} | 状态：{{ floor.status === 1 ? '启用' : '停用' }}</p>
              </div>
              <div class="flex items-center gap-2">
                <button class="px-3 py-1 border rounded-lg text-sm hover:bg-gray-50">管理楼层</button>
                <button class="px-3 py-1 border rounded-lg text-sm hover:bg-gray-50">查看平面图</button>
                <button class="px-3 py-1 border rounded-lg text-sm hover:bg-gray-50">{{ floor.status === 1 ? '停用' : '启用' }}</button>
              </div>
            </div>
            <div v-if="getVenueFloors().length === 0" class="text-center py-10 text-gray-500">
              暂无楼层数据
            </div>
          </div>
        </div>

        <!-- 操作日志 -->
        <div v-else-if="activeTab === 'logs'" class="space-y-4">
          <h4 class="text-lg font-semibold">操作日志</h4>
          <div class="space-y-3">
            <div 
              v-for="log in logs" 
              :key="log.id"
              class="bg-white rounded-lg p-4 border"
            >
              <div class="flex items-center justify-between">
                <p class="font-medium">{{ log.operation }}</p>
                <p class="text-sm text-gray-500">{{ log.time }}</p>
              </div>
              <p class="text-sm text-gray-600 mt-1">{{ log.detail }}</p>
            </div>
            <div v-if="logs.length === 0" class="text-center py-10 text-gray-500">
              暂无操作日志
            </div>
          </div>
        </div>

        <!-- 数据统计 -->
        <div v-else-if="activeTab === 'stats'" class="space-y-6">
          <h4 class="text-lg font-semibold">数据统计</h4>
          
          <div class="grid grid-cols-2 gap-6">
            <div class="bg-gray-50 rounded-lg p-6">
              <h5 class="font-medium mb-4">工位占用情况</h5>
              <div class="grid grid-cols-3 gap-4">
                <div class="bg-white rounded-lg p-4 border">
                  <p class="text-2xl font-bold text-green-600">{{ getOccupiedSeats() }}</p>
                  <p class="text-sm text-gray-500">已占用</p>
                </div>
                <div class="bg-white rounded-lg p-4 border">
                  <p class="text-2xl font-bold text-gray-600">{{ getEmptySeats() }}</p>
                  <p class="text-sm text-gray-500">闲置</p>
                </div>
                <div class="bg-white rounded-lg p-4 border">
                  <p class="text-2xl font-bold text-orange-600">{{ getMaintenanceSeats() }}</p>
                  <p class="text-sm text-gray-500">维护中</p>
                </div>
              </div>
            </div>
            
            <div class="bg-gray-50 rounded-lg p-6">
              <h5 class="font-medium mb-4">占用率</h5>
              <div class="flex items-center justify-center">
                <div class="relative w-32 h-32">
                  <svg class="w-full h-full transform -rotate-90">
                    <circle cx="64" cy="64" r="56" stroke="#e5e7eb" stroke-width="12" fill="none" />
                    <circle 
                      cx="64" cy="64" r="56" 
                      :stroke="getOccupancyRate() >= 80 ? '#ef4444' : getOccupancyRate() >= 60 ? '#f59e0b' : '#10b981'" 
                      stroke-width="12" 
                      fill="none"
                      :stroke-dasharray="`${getOccupancyRate() * 3.52} 352`"
                      stroke-linecap="round"
                    />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-2xl font-bold">{{ getOccupancyRate() }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-6">
            <h5 class="font-medium mb-4">楼层统计</h5>
            <div class="space-y-3">
              <div 
                v-for="floor in getVenueFloors()" 
                :key="floor.id"
                class="flex items-center justify-between bg-white rounded-lg p-4 border"
              >
                <div class="flex items-center gap-4">
                  <span class="font-medium">{{ floor.floorNo }} {{ floor.name }}</span>
                  <span class="text-sm text-gray-500">{{ floor.areaCount }} 个区域</span>
                </div>
                <div class="flex items-center gap-6">
                  <span class="text-sm">工位：{{ floor.seatCount }}</span>
                  <span class="text-sm text-gray-500">状态：{{ floor.status === 1 ? '启用' : '停用' }}</span>
                </div>
              </div>
              <div v-if="getVenueFloors().length === 0" class="text-center py-6 text-gray-500">
                暂无楼层数据
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Venue, Floor, Area, Log } from '../types'

const props = defineProps<{
  visible: boolean
  venue: Venue | null
  floors: Floor[]
  areas: Area[]
  logs: Log[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'edit', venue: Venue): void
  (e: 'toggle-status', venue: Venue): void
  (e: 'delete', venue: Venue): void
  (e: 'add-floor', venue: Venue): void
}>()

const activeTab = ref('basic')
const tabs = [
  { id: 'basic', label: '基本信息' },
  { id: 'floors', label: '楼层管理' },
  { id: 'logs', label: '操作日志' },
  { id: 'stats', label: '数据统计' }
]

const getVenueFloors = () => {
  if (!props.venue) return []
  return props.floors.filter(floor => floor.venueId === props.venue?.id)
}

const getAreaCount = () => {
  return getVenueFloors().reduce((sum, floor) => sum + floor.areaCount, 0)
}

const getOccupiedSeats = () => {
  return Math.floor(getTotalSeats() * 0.7)
}

const getEmptySeats = () => {
  return Math.floor(getTotalSeats() * 0.25)
}

const getMaintenanceSeats = () => {
  return getTotalSeats() - getOccupiedSeats() - getEmptySeats()
}

const getOccupancyRate = () => {
  const total = getTotalSeats()
  if (total === 0) return 0
  return Math.round((getOccupiedSeats() / total) * 100)
}

const getTotalSeats = () => {
  return getVenueFloors().reduce((sum, floor) => sum + floor.seatCount, 0)
}

const handleClose = () => {
  emit('close')
}

const handleEdit = () => {
  if (props.venue) {
    emit('edit', props.venue)
  }
}

const handleToggleStatus = () => {
  if (props.venue) {
    emit('toggle-status', props.venue)
  }
}

const handleDelete = () => {
  if (props.venue) {
    if (confirm(`确定要删除场地"${props.venue.name}"吗？此操作不可恢复！`)) {
      emit('delete', props.venue)
    }
  }
}

const handleAddFloor = () => {
  if (props.venue) {
    emit('add-floor', props.venue)
  }
}
</script>
