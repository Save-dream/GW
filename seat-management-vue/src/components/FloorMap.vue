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
          <h2 class="text-2xl font-bold text-gray-800">楼层地图 - {{ selectedFloor?.floorNo }}</h2>
          <p class="text-gray-500">{{ selectedFloor?.name }} · {{ selectedVenue.name }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50">
          <ZoomOut :size="18" />
          缩小
        </button>
        <button class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50">
          <ZoomIn :size="18" />
          放大
        </button>
        <button class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50">
          <Move :size="18" />
          拖动
        </button>
      </div>
    </div>

    <div class="flex gap-6">
      <div class="flex-1 bg-white rounded-xl shadow-sm border p-6">
        <div class="relative bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg" style="height: 500px;">
          <div class="absolute inset-4 border-2 border-dashed border-slate-300 rounded-lg">
            <div class="absolute top-2 left-2 text-sm text-slate-400">楼层平面图区域</div>
          </div>

          <div
            v-for="area in currentFloorAreas"
            :key="area.id"
            :class="[
              'absolute bg-opacity-20 border-2 rounded-lg cursor-pointer hover:opacity-40 transition-opacity',
              getAreaTypeColor(area.areaType).bg,
              getAreaTypeColor(area.areaType).border
            ]"
            :style="{
              top: `${area.position.top}%`,
              left: `${area.position.left}%`,
              width: `${area.position.width}%`,
              height: `${area.position.height}%`,
            }"
            @click="$emit('selectArea', area)"
          >
            <div class="p-3 h-full flex flex-col">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-shadow">{{ area.areaNo }}</span>
                <span class="text-xs bg-white bg-opacity-30 px-2 py-1 rounded text-white">{{ getAreaTypeColor(area.areaType).name }}</span>
              </div>
              <span class="text-white text-shadow text-sm mt-1">{{ area.areaName }}</span>
              <span v-if="area.areaType !== 3" class="text-white text-shadow text-xs mt-auto">{{ area.seatCount }}个工位</span>
            </div>
          </div>

          <div class="absolute bottom-4 right-4 bg-white rounded-lg shadow p-3">
            <p class="text-sm font-medium mb-2">图例</p>
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <div class="w-4 h-4 bg-green-500 rounded"></div>
                <span class="text-sm">闲置</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-4 h-4 bg-yellow-500 rounded"></div>
                <span class="text-sm">占用</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-4 h-4 bg-red-500 rounded"></div>
                <span class="text-sm">维修</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="w-80">
        <div class="bg-white rounded-xl shadow-sm border p-4">
          <h3 class="font-semibold mb-4">区域列表</h3>
          <div class="space-y-2">
            <div
              v-for="area in currentFloorAreas"
              :key="area.id"
              :class="[
                'p-3 border rounded-lg cursor-pointer transition-all hover:shadow-sm',
                selectedArea?.id === area.id ? 'border-blue-500 bg-blue-50' : ''
              ]"
              @click="$emit('selectArea', area)"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div :class="['w-3 h-3 rounded-full', getAreaTypeColor(area.areaType).bg]"></div>
                  <span class="font-medium">{{ area.areaNo }} {{ area.areaName }}</span>
                </div>
                <ChevronDown :size="16" class="text-gray-400" />
              </div>
              <div class="flex items-center justify-between mt-2 text-sm text-gray-500">
                <span>{{ getAreaTypeColor(area.areaType).name }}</span>
                <span>{{ area.areaType !== 3 ? `${area.seatCount}个工位` : '会议室' }}</span>
              </div>
            </div>
          </div>

          <button class="w-full mt-4 py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-500 transition-colors">
            + 圈定新区域
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft, ZoomIn, ZoomOut, Move, ChevronDown } from 'lucide-vue-next'
import type { Floor, Area, Venue } from '../types'
import { getAreaTypeColor } from '../utils/helpers'

defineProps<{
  selectedFloor: Floor | null
  selectedVenue: Venue
  currentFloorAreas: Area[]
  selectedArea: Area | null
}>()

defineEmits<{
  goBack: []
  selectArea: [area: Area]
}>()
</script>