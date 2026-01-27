<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">操作日志</h2>
        <p class="text-gray-500">查看和管理系统操作记录</p>
      </div>
      <button class="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50">
        <Download :size="18" />
        导出日志
      </button>
    </div>

    <div class="bg-white rounded-xl shadow-sm border p-6">
      <div class="flex items-center gap-4 mb-6">
        <input
          type="text"
          placeholder="搜索操作人或对象..."
          class="px-4 py-2 border rounded-lg flex-1 max-w-xs"
          v-model="searchKeyword"
        />
        <select class="px-4 py-2 border rounded-lg" v-model="operationType">
          <option value="">全部操作类型</option>
          <option value="1">绑定人员</option>
          <option value="2">解绑人员</option>
          <option value="3">更换工位</option>
          <option value="4">额外绑定</option>
          <option value="5">批量操作</option>
        </select>
        <input
          type="date"
          class="px-4 py-2 border rounded-lg"
          v-model="startDate"
        />
        <span class="text-gray-500">至</span>
        <input
          type="date"
          class="px-4 py-2 border rounded-lg"
          v-model="endDate"
        />
        <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700" @click="handleSearch">
          搜索
        </button>
      </div>

      <table class="w-full">
        <thead>
          <tr class="border-b">
            <th class="text-left py-3 px-4 font-medium">操作时间</th>
            <th class="text-left py-3 px-4 font-medium">操作人</th>
            <th class="text-left py-3 px-4 font-medium">操作类型</th>
            <th class="text-left py-3 px-4 font-medium">操作对象</th>
            <th class="text-left py-3 px-4 font-medium">变更详情</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in mockLogs" :key="log.id" class="border-b hover:bg-gray-50">
            <td class="py-3 px-4 text-gray-600">{{ log.time }}</td>
            <td class="py-3 px-4">{{ log.operator }}</td>
            <td class="py-3 px-4">
              <span :class="[
                'px-3 py-1 rounded-full text-sm',
                log.operation === '绑定人员' ? 'bg-green-100 text-green-700' :
                log.operation === '更换工位' ? 'bg-blue-100 text-blue-700' :
                log.operation === '解绑人员' ? 'bg-yellow-100 text-yellow-700' :
                'bg-gray-100 text-gray-700'
              ]">
                {{ log.operation }}
              </span>
            </td>
            <td class="py-3 px-4">{{ log.target }}</td>
            <td class="py-3 px-4 text-gray-600">{{ log.detail }}</td>
          </tr>
        </tbody>
      </table>

      <div class="flex items-center justify-between mt-4 pt-4 border-t">
        <span class="text-sm text-gray-500">共 128 条记录</span>
        <div class="flex items-center gap-2">
          <button class="px-3 py-1 border rounded hover:bg-gray-50">上一页</button>
          <button class="px-3 py-1 bg-blue-600 text-white rounded">1</button>
          <button class="px-3 py-1 border rounded hover:bg-gray-50">2</button>
          <button class="px-3 py-1 border rounded hover:bg-gray-50">3</button>
          <button class="px-3 py-1 border rounded hover:bg-gray-50">下一页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Download } from 'lucide-vue-next'
import type { Log } from '../types'

defineProps<{
  mockLogs: Log[]
}>()

const searchKeyword = ref('')
const operationType = ref('')
const startDate = ref('')
const endDate = ref('')

const handleSearch = () => {
  console.log('搜索日志:', {
    searchKeyword: searchKeyword.value,
    operationType: operationType.value,
    startDate: startDate.value,
    endDate: endDate.value
  })
  // Here we would typically call the API to search logs
  // For now, we'll just log the search parameters
  alert('搜索功能已触发，实际项目中会调用后端API')
}
</script>