<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">人员绑定</h2>
        <p class="text-gray-500">通过双入口机制实现人员与工位的灵活绑定</p>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border p-6">
      <div class="flex gap-4 mb-6">
        <button
          :class="[
            'flex-1 py-4 rounded-lg border-2 transition-all',
            bindMode === 'seat'
              ? 'border-blue-500 bg-blue-50 text-blue-600'
              : 'border-gray-200 hover:border-gray-300'
          ]"
          @click="$emit('updateBindMode', 'seat')"
        >
          <div class="text-center">
            <Armchair :size="32" class="mx-auto mb-2" />
            <p class="font-medium">工位视角</p>
            <p class="text-sm text-gray-500">先选位置，再选人</p>
          </div>
        </button>
        <button
          :class="[
            'flex-1 py-4 rounded-lg border-2 transition-all',
            bindMode === 'person'
              ? 'border-blue-500 bg-blue-50 text-blue-600'
              : 'border-gray-200 hover:border-gray-300'
          ]"
          @click="$emit('updateBindMode', 'person')"
        >
          <div class="text-center">
            <Users :size="32" class="mx-auto mb-2" />
            <p class="font-medium">人员视角</p>
            <p class="text-sm text-gray-500">先找人，再分配位置</p>
          </div>
        </button>
      </div>

      <div v-if="bindMode === 'seat'">
        <div class="flex items-center gap-4 mb-4">
          <select class="px-4 py-2 border rounded-lg">
            <option>选择楼层</option>
            <option v-for="f in mockFloors" :key="f.id" :value="f.id">{{ f.floorNo }} {{ f.name }}</option>
          </select>
          <select class="px-4 py-2 border rounded-lg">
            <option>选择区域</option>
            <option v-for="a in mockAreas" :key="a.id" :value="a.id">{{ a.areaNo }} {{ a.areaName }}</option>
          </select>
          <label class="flex items-center gap-2">
            <input type="checkbox" class="rounded" />
            <span>仅看闲置</span>
          </label>
        </div>

        <div class="grid grid-cols-8 gap-2">
          <div
            v-for="seat in mockSeats.slice(0, 48)"
            :key="seat.id"
            :class="[
              'aspect-square rounded-lg border-2 flex items-center justify-center cursor-pointer hover:shadow-md',
              getStatusInfo(seat.status).bg,
              seat.status === 1 ? 'border-yellow-400' : seat.status === 2 ? 'border-red-400' : 'border-green-400'
            ]"
            @click="$emit('selectSeat', seat)"
          >
            <span :class="['text-xs font-medium', getStatusInfo(seat.status).textColor]">{{ seat.seatNo.split('-')[1] }}</span>
          </div>
        </div>
      </div>

      <div v-else>
        <div class="relative mb-4">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="20" />
          <input
            type="text"
            placeholder="搜索姓名或工号..."
            class="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            :value="searchKeyword"
            @input="$emit('updateSearch', ($event.target as HTMLInputElement).value)"
          />
        </div>

        <div class="grid grid-cols-3 gap-4">
          <div v-for="user in mockUsers" :key="user.id" class="border rounded-lg p-4 hover:shadow-md transition-all">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-full flex items-center justify-center text-white font-bold">
                {{ user.name[0] }}
              </div>
              <div class="flex-1">
                <p class="font-medium">{{ user.name }}</p>
                <p class="text-sm text-gray-500">{{ user.deptName }}</p>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t">
              <p class="text-sm text-gray-500">工号：{{ user.id }}</p>
              <p class="text-sm text-gray-500">职位：{{ user.position }}</p>
            </div>
            <button class="w-full mt-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm" @click="handleAssignSeat(user)">
              分配/更换工位
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Armchair, Users, Search } from 'lucide-vue-next'
import { defineEmits } from 'vue'
import type { Seat, User as UserType, Floor, Area } from '../types'
import { getStatusInfo } from '../utils/helpers'

defineProps<{
  bindMode: 'seat' | 'person'
  searchKeyword: string
  mockSeats: Seat[]
  mockUsers: UserType[]
  mockFloors: Floor[]
  mockAreas: Area[]
}>()

const emit = defineEmits<{
  updateBindMode: [mode: 'seat' | 'person']
  updateSearch: [keyword: string]
  selectSeat: [seat: Seat]
  assignSeat: [user: UserType]
}>()

const handleAssignSeat = (user: UserType) => {
  console.log('分配工位给:', user.name)
  emit('assignSeat', user)
}
</script>