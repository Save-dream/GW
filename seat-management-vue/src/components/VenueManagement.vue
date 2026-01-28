<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">场地管理</h2>
        <p class="text-gray-500">管理公司办公场地信息</p>
      </div>
      <div class="flex items-center gap-3">
        <!-- 排序按钮 -->
        <button 
          @click="handleSort" 
          class="flex items-center gap-2 px-3 py-1.5 border rounded-lg hover:bg-gray-50"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sort"><path d="m3 9 4 4-4 4"/><path d="m21 9-4 4 4 4"/></svg>
          按楼层排序
          <span>{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
        </button>
        <!-- 新增场地按钮（仅系统管理员可见） -->
        <button 
          v-if="userRole === 'system_admin'" 
          @click="handleAddVenue" 
          class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus :size="18" />
          新增场地
        </button>
      </div>
    </div>

    <div class="space-y-6">
      <div
        v-for="venue in sortedVenues"
        :key="venue.id"
        class="bg-white rounded-xl shadow-sm border p-6"
      >
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-3">
              <Building2 :size="24" class="text-blue-600" />
              <h3 class="text-xl font-semibold">{{ venue.name }}{{ venue.status === 0 ? '（已停用）' : '' }}</h3>
            </div>
            <p class="text-gray-500 mt-1">地址：{{ venue.address }}</p>
            <div class="flex items-center gap-6 mt-2 text-sm text-gray-600">
              <span>楼层数：{{ venue.floor_count }}层</span>
              <span>总工位数：{{ getTotalSeats(venue.id) }}</span>
              <span :class="[
                'flex items-center gap-1',
                venue.status === 1 ? 'text-green-600' : 'text-gray-500'
              ]">
                {{ venue.status === 1 ? '✅ 启用' : '⏸️ 停用' }}
              </span>
            </div>
          </div>
        </div>

        <div class="flex gap-2 mt-4 pt-4 border-t">
          <!-- 查看详情按钮（所有管理员可见） -->
          <button @click="handleViewDetails(venue)" class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50">
            <Eye :size="16" />
            查看详情
          </button>
          <!-- 编辑按钮（仅系统管理员可见） -->
          <button 
            v-if="userRole === 'system_admin'" 
            @click="handleEditVenue(venue)" 
            class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50"
          >
            <Edit :size="16" />
            编辑
          </button>
          <!-- 启用/停用按钮（仅系统管理员可见） -->
          <button 
            v-if="userRole === 'system_admin'" 
            @click="handleToggleStatus(venue)" 
            :class="[
              'flex items-center gap-2 px-4 py-2 rounded-lg',
              venue.status === 1 
                ? 'bg-gray-100 text-gray-700 hover:bg-gray-200 border'
                : 'bg-green-100 text-green-700 hover:bg-green-200 border border-green-200'
            ]"
          >
            {{ venue.status === 1 ? '停用' : '启用' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Plus, Building2, Eye, Edit } from 'lucide-vue-next'
import type { Venue, Floor, Area } from '../types'

const props = defineProps<{
  venues: Venue[]
  floors: Floor[]
  areas: Area[]
}>()

const emit = defineEmits<{
  (e: 'add-venue'): void
  (e: 'edit-venue', venue: Venue): void
  (e: 'view-venue', venue: Venue): void
  (e: 'toggle-venue-status', venue: Venue): void
  (e: 'sort-venues', order: string): void
}>()

// 用户角色（模拟数据，实际应从登录状态获取）
const userRole = ref('system_admin') // 可选值：system_admin, hr_admin, normal_employee

// 排序状态
const sortOrder = ref<'asc' | 'desc'>('asc')

// 计算排序后的场地列表
const sortedVenues = computed(() => {
  const venues = [...props.venues]
  return venues.sort((a, b) => {
    if (sortOrder.value === 'asc') {
      return (a.floor_count || 0) - (b.floor_count || 0)
    } else {
      return (b.floor_count || 0) - (a.floor_count || 0)
    }
  })
})

const handleAddVenue = () => {
  emit('add-venue')
  console.log('新增场地')
}

const handleEditVenue = (venue: Venue) => {
  emit('edit-venue', venue)
  console.log('编辑场地:', venue.name)
}

const handleViewDetails = (venue: Venue) => {
  emit('view-venue', venue)
  console.log('查看详情:', venue.name)
}

const handleToggleStatus = (venue: Venue) => {
  emit('toggle-venue-status', venue)
  console.log('切换状态:', venue.name, venue.status === 1 ? '停用' : '启用')
}

const handleSort = () => {
  // 切换排序顺序
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  // 触发排序事件
  emit('sort-venues', sortOrder.value === 'asc' ? 'floor_count' : '-floor_count')
  console.log('排序方式:', sortOrder.value === 'asc' ? '升序' : '降序')
}

const getTotalSeats = (venueId: number): number => {
  const venueFloorIds = props.floors
    .filter(floor => floor.venue_id === venueId)
    .map(floor => floor.id)
  return props.areas
    .filter(area => venueFloorIds.includes(area.floor_id))
    .reduce((sum, area) => sum + area.seat_count, 0)
}
</script>