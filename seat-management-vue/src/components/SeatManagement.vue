<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button
          @click="$emit('goBack')"
          class="p-2 hover:bg-gray-100 rounded-lg"
        >
          <ArrowLeft :size="20" />
        </button>
        <div>
          <h2 class="text-2xl font-bold text-gray-800">{{ selectedArea?.area_name }}</h2>
          <p class="text-gray-500">区域 {{ selectedArea?.area_no }} · {{ selectedArea?.area_type !== 3 ? `${selectedArea?.seat_count}个工位` : '' }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          <Plus :size="18" />
          批量生成工位
        </button>
        <button class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50">
          <Download :size="18" />
          导出
        </button>
      </div>
    </div>

    <div class="flex gap-6">
      <div class="flex-1 bg-white rounded-xl shadow-sm border p-6">
        <div class="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg p-4" style="min-height: 400px;">
          <div class="grid gap-2" :style="{
            gridTemplateColumns: `repeat(${Math.ceil(Math.sqrt(currentAreaSeats.length))}, minmax(60px, 1fr))`
          }">
            <div
              v-for="seat in currentAreaSeats"
              :key="seat.id"
              :class="[
                'aspect-square rounded-lg border-2 flex flex-col items-center justify-center cursor-pointer hover:shadow-md transition-all',
                getStatusInfo(seat.status).bg,
                seat.status === 1 ? 'border-yellow-400' : seat.status === 2 ? 'border-red-400' : 'border-green-400',
                selectedSeat?.id === seat.id ? 'ring-2 ring-blue-500 ring-offset-2' : ''
              ]"
              @click="$emit('selectSeat', seat)"
            >
              <span :class="['text-xs font-medium', getStatusInfo(seat.status).textColor]">{{ seat.seat_no.split('-')[1] }}</span>
              <span v-if="seat.status === 1" class="text-xs text-gray-600 truncate max-w-full px-1">{{ seat.occupied_by?.name }}</span>
              <XCircle v-if="seat.status === 2" :size="16" class="text-red-500" />
            </div>
          </div>
        </div>
      </div>

      <div class="w-96">
        <div class="bg-white rounded-xl shadow-sm border p-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold">工位列表</h3>
            <div class="flex items-center gap-2 text-sm">
              <span class="flex items-center gap-1">
                <div class="w-3 h-3 bg-green-500 rounded"></div>
                闲置 {{ currentAreaSeats.filter(s => s.status === 0).length }}
              </span>
              <span class="flex items-center gap-1">
                <div class="w-3 h-3 bg-yellow-500 rounded"></div>
                占用 {{ currentAreaSeats.filter(s => s.status === 1).length }}
              </span>
            </div>
          </div>

          <div class="space-y-2 max-h-96 overflow-y-auto">
            <div
              v-for="seat in currentAreaSeats.slice(0, 10)"
              :key="seat.id"
              :class="[
                'p-3 border rounded-lg cursor-pointer transition-all hover:bg-gray-50',
                selectedSeat?.id === seat.id ? 'border-blue-500 bg-blue-50' : ''
              ]"
              @click="$emit('selectSeat', seat)"
            >
              <div class="flex items-center justify-between">
                <span class="font-medium">{{ seat.seat_no }}</span>
                <span :class="['px-2 py-1 rounded-full text-xs', getStatusInfo(seat.status).bg, getStatusInfo(seat.status).textColor]">
                  {{ getStatusInfo(seat.status).text }}
                </span>
              </div>
              <p v-if="seat.status === 1" class="text-sm text-gray-600 mt-1">{{ seat.occupied_by?.name }} · {{ seat.occupied_by?.department_name }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft, Plus, Download, XCircle } from 'lucide-vue-next'
import type { Area, Seat } from '../types'
import { getStatusInfo } from '../utils/helpers'

defineProps<{
  selectedArea: Area | null
  currentAreaSeats: Seat[]
  selectedSeat: Seat | null
}>()

defineEmits<{
  goBack: []
  selectSeat: [seat: Seat]
}>()
</script>