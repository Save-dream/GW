<template>
  <div :class="[showSidebar ? 'w-64' : 'w-16', 'bg-gradient-to-b from-slate-800 to-slate-900 text-white transition-all duration-300 flex flex-col']">
    <div class="p-4 border-b border-slate-700">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg flex items-center justify-center">
          <Building2 :size="24" />
        </div>
        <div v-if="showSidebar">
          <h1 class="font-bold text-lg">工位管理系统</h1>
          <p class="text-xs text-slate-400">Seat Management</p>
        </div>
      </div>
    </div>

    <nav class="flex-1 py-4">
      <button
        v-for="item in menuItems"
        :key="item.id"
        @click="$emit('updateView', item.id)"
        :class="[
          'w-full px-4 py-3 flex items-center gap-3 transition-all duration-200',
          currentView === item.id
            ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white'
            : 'text-slate-300 hover:bg-slate-700 hover:text-white'
        ]"
      >
        <component :is="item.icon" :size="20" />
        <span v-if="showSidebar">{{ item.label }}</span>
      </button>
    </nav>

    <div class="p-4 border-t border-slate-700">
      <button @click="$emit('logout')" class="w-full flex items-center gap-3 text-slate-300 hover:text-white transition-colors">
        <LogOut :size="20" />
        <span v-if="showSidebar">退出登录</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Building2, LogOut } from 'lucide-vue-next'
import type { MenuItem } from '../types'

defineProps<{
  showSidebar: boolean
  currentView: string
  menuItems: MenuItem[]
}>()

defineEmits<{
  updateView: [view: string]
  toggleSidebar: []
  logout: []
}>()
</script>