<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">首页概览</h2>
        <p class="text-gray-500">欢迎使用工位座次管理系统</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-500">当前场地：</span>
        <select
            class="px-3 py-2 border rounded-lg bg-white"
            :value="selectedVenue?.id || ''"
            @change="handleVenueSelect"
          >
          <option v-for="v in mockVenues" :key="v.id" :value="v.id">{{ v.name }}</option>
        </select>
      </div>
    </div>

    <div class="grid grid-cols-4 gap-6">
      <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-blue-100">总工位数</p>
            <p class="text-3xl font-bold mt-2">{{ seatStats.total }}</p>
          </div>
          <Armchair :size="48" class="text-blue-200" />
        </div>
      </div>
      <div class="bg-gradient-to-br from-yellow-500 to-orange-500 rounded-xl p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-yellow-100">已占用</p>
            <p class="text-3xl font-bold mt-2">{{ seatStats.occupied }}</p>
          </div>
          <Users :size="48" class="text-yellow-200" />
        </div>
        <p class="text-sm text-yellow-100 mt-2">占用率 {{ ((seatStats.occupied / seatStats.total) * 100).toFixed(1) }}%</p>
      </div>
      <div class="bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-green-100">闲置工位</p>
            <p class="text-3xl font-bold mt-2">{{ seatStats.empty }}</p>
          </div>
          <Check :size="48" class="text-green-200" />
        </div>
      </div>
      <div class="bg-gradient-to-br from-red-500 to-rose-500 rounded-xl p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-red-100">维修中</p>
            <p class="text-3xl font-bold mt-2">{{ seatStats.maintenance }}</p>
          </div>
          <AlertCircle :size="48" class="text-red-200" />
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border p-6">
      <h3 class="text-lg font-semibold mb-4">楼层概览 - {{ selectedVenue?.name || '无' }}</h3>
      <div class="grid grid-cols-5 gap-4">
        <div
          v-for="floor in mockFloors.filter(f => f.venueId === selectedVenue?.id)"
          :key="floor.id"
          class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
          @click="$emit('selectFloor', floor)"
        >
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full flex items-center justify-center mx-auto mb-3">
              <span class="text-2xl font-bold text-blue-600">{{ floor.floorNo }}</span>
            </div>
            <p class="font-medium">{{ floor.name }}</p>
            <p class="text-sm text-gray-500 mt-1">{{ floor.areaCount || 0 }}个区域</p>
            <p class="text-sm text-gray-500">{{ floor.seatCount || 0 }}个工位</p>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border p-6">
      <h3 class="text-lg font-semibold mb-4">最近操作</h3>
      <div class="space-y-3">
        <div
          v-for="log in mockLogs.slice(0, 5)"
          :key="log.id"
          class="flex items-center justify-between py-3 border-b last:border-0"
        >
          <div class="flex items-center gap-4">
            <span :class="[
              'px-3 py-2 rounded-full text-sm',
              log.operation === '绑定人员' ? 'bg-green-100 text-green-700' :
              log.operation === '更换工位' ? 'bg-blue-100 text-blue-700' :
              log.operation === '解绑人员' ? 'bg-yellow-100 text-yellow-700' :
              'bg-gray-100 text-gray-700'
            ]">
              {{ log.operation }}
            </span>
            <span>{{ log.detail }}</span>
          </div>
          <span class="text-sm text-gray-500">{{ log.time }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Armchair, Users, Check, AlertCircle } from 'lucide-vue-next'
import type { Venue, Floor } from '../types'

const props = defineProps<{
  selectedVenue: Venue | null
  seatStats: { total: number; occupied: number; empty: number; maintenance: number }
  mockLogs: any[]
  mockVenues: Venue[]
  mockFloors: Floor[]
}>()

const emit = defineEmits<{
  selectVenue: [venue: Venue]
  selectFloor: [floor: Floor]
}>()

const handleVenueSelect = (event: Event) => {
  const target = event.target as HTMLSelectElement
  const venueId = Number(target.value)
  const venue = props.mockVenues.find(v => v.id === venueId)
  if (venue) {
    emit('selectVenue', venue)
  }
}
</script>