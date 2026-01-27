<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">场地管理</h2>
        <p class="text-gray-500">管理公司办公场地信息</p>
      </div>
      <button @click="handleAddVenue" class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
        <Plus :size="18" />
        新增场地
      </button>
    </div>

    <div class="space-y-6">
      <div
        v-for="venue in mockVenues"
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
              <span>楼层数：{{ venue.floorCount }}层</span>
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
          <button @click="handleViewDetails(venue)" class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50">
            <Eye :size="16" />
            查看详情
          </button>
          <button @click="handleEditVenue(venue)" class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50">
            <Edit :size="16" />
            编辑
          </button>
          <button @click="handleToggleStatus(venue)" :class="[
            'flex items-center gap-2 px-4 py-2 rounded-lg',
            venue.status === 1 
              ? 'bg-gray-100 text-gray-700 hover:bg-gray-200 border'
              : 'bg-green-100 text-green-700 hover:bg-green-200 border border-green-200'
          ]">
            {{ venue.status === 1 ? '停用' : '启用' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Plus, Building2, Eye, Edit } from 'lucide-vue-next'
import type { Venue, Floor, Area } from '../types'

const props = defineProps<{
  mockVenues: Venue[]
  mockFloors: Floor[]
  mockAreas: Area[]
}>()

const emit = defineEmits<{
  (e: 'add-venue'): void
  (e: 'edit-venue', venue: Venue): void
  (e: 'view-venue', venue: Venue): void
  (e: 'toggle-venue-status', venue: Venue): void
}>()

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

const getTotalSeats = (venueId: number): number => {
  return props.mockFloors
    .filter(floor => floor.venueId === venueId)
    .reduce((sum, floor) => sum + floor.seatCount, 0)
}
</script>