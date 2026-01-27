<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl">
      <div class="flex items-center justify-between p-6 border-b">
        <h3 class="text-xl font-semibold">
          {{ selectedSeat.status === 1 ? '工位详情' : '绑定人员' }}
        </h3>
        <button
          @click="$emit('close')"
          class="p-2 hover:bg-gray-100 rounded-lg"
        >
          <X :size="20" />
        </button>
      </div>

      <div class="p-6">
        <div class="bg-gray-50 rounded-lg p-4 mb-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-2xl font-bold text-gray-800">{{ selectedSeat.seatNo }}</p>
              <p class="text-gray-500">{{ selectedArea?.areaName }}</p>
            </div>
            <span :class="['px-4 py-2 rounded-full text-lg', getStatusInfo(selectedSeat.status).bg, getStatusInfo(selectedSeat.status).textColor]">
              {{ getStatusInfo(selectedSeat.status).text }}
            </span>
          </div>
        </div>

        <div v-if="bindConflict" class="space-y-4">
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div class="flex items-center gap-2 text-yellow-700">
              <AlertCircle :size="20" />
              <span class="font-medium">该人员已有工位</span>
            </div>
            <p class="text-yellow-600 mt-1">
              {{ bindConflict.user.name }} 已有工位：{{ bindConflict.existingSeats.map(s => s.seatNo).join('、') }}
            </p>
          </div>

          <div class="bg-white border rounded-lg p-4">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-full flex items-center justify-center text-white font-bold">
                {{ bindConflict.user.name[0] }}
              </div>
              <div>
                <p class="font-medium">{{ bindConflict.user.name }}</p>
                <p class="text-sm text-gray-500">{{ bindConflict.user.deptName }} · {{ bindConflict.user.position }}</p>
              </div>
            </div>
          </div>

          <div class="flex gap-4">
            <button
              class="flex-1 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              @click="$emit('confirmBind', bindConflict.user, false)"
            >
              更换工位（解绑原工位）
            </button>
            <button
              class="flex-1 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
              @click="$emit('confirmBind', bindConflict.user, true)"
            >
              额外绑定（保留原工位）
            </button>
          </div>
        </div>

        <div v-else-if="selectedSeat.status === 1" class="space-y-4">
          <div class="bg-white border rounded-lg overflow-hidden">
            <div class="p-4 border-b bg-gray-50">
              <p class="font-medium">当前人员</p>
            </div>
            <div class="p-4">
              <div class="flex items-center gap-4">
                <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-full flex items-center justify-center text-white text-xl font-bold">
                  {{ selectedSeat.userName?.[0] }}
                </div>
                <div>
                  <p class="text-xl font-medium">{{ selectedSeat.userName }}</p>
                  <p class="text-gray-500">{{ selectedSeat.deptName }}</p>
                  <p class="text-sm text-gray-400">工号：{{ selectedSeat.userId }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <button class="py-3 border rounded-lg hover:bg-gray-50 flex items-center justify-center gap-2">
              <Users :size="18" />
              更换工位
            </button>
            <button class="py-3 border rounded-lg hover:bg-gray-50 flex items-center justify-center gap-2">
              <X :size="18" />
              解绑人员
            </button>
          </div>
        </div>

        <div v-else class="space-y-4">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="20" />
            <input
              type="text"
              placeholder="搜索姓名或工号"
              class="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :value="searchUserKeyword"
              @input="$emit('updateSearch', ($event.target as HTMLInputElement).value)"
            />
          </div>

          <div class="space-y-2 max-h-64 overflow-y-auto">
            <div
              v-for="user in filteredUsers"
              :key="user.id"
              class="p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-all"
              @click="$emit('selectUser', user)"
            >
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-full flex items-center justify-center text-white font-medium">
                  {{ user.name[0] }}
                </div>
                <div class="flex-1">
                  <p class="font-medium">{{ user.name }}</p>
                  <p class="text-sm text-gray-500">{{ user.deptName }} · {{ user.position }}</p>
                </div>
                <ArrowRight :size="18" class="text-gray-400" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { X, AlertCircle, Search, Users, ArrowRight } from 'lucide-vue-next'
import type { Seat, Area, User as UserType } from '../types'
import { getStatusInfo } from '../utils/helpers'

defineProps<{
  selectedSeat: Seat
  selectedArea: Area | null
  bindConflict: { user: UserType; existingSeats: Seat[] } | null
  searchUserKeyword: string
  filteredUsers: UserType[]
}>()

defineEmits<{
  close: []
  selectUser: [user: UserType]
  confirmBind: [user: UserType, isExtra: boolean]
  updateSearch: [keyword: string]
}>()
</script>