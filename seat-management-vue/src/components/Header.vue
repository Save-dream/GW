<template>
  <header class="bg-white border-b px-6 py-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button
          @click="$emit('toggleSidebar')"
          class="p-2 hover:bg-gray-100 rounded-lg"
        >
          <Menu :size="20" />
        </button>
        <div class="relative">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="18" />
          <input
            type="text"
            placeholder="搜索人员、工位、部门..."
            class="pl-10 pr-4 py-2 border rounded-lg w-80 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :value="searchKeyword"
            @input="$emit('updateSearch', ($event.target as HTMLInputElement).value)"
          />
        </div>
      </div>
      <div class="flex items-center gap-4">
        <span class="text-sm text-gray-500">当前用户：管理员</span>
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-full flex items-center justify-center text-white font-bold">
          管
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Menu, Search } from 'lucide-vue-next'

defineProps<{
  showSidebar: boolean
  searchKeyword: string
}>()

defineEmits<{
  toggleSidebar: []
  updateSearch: [keyword: string]
}>()
</script>