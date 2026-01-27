<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-md">
      <div class="p-6 border-b">
        <h3 class="text-xl font-bold">{{ isEdit ? '编辑楼层' : '添加楼层' }}</h3>
      </div>
      <div class="p-6 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">楼层编号 *</label>
          <input 
            v-model="formData.floorNo" 
            type="text" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入楼层编号，如：1F、2F"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">楼层名称 *</label>
          <input 
            v-model="formData.name" 
            type="text" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入楼层名称"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">区域数 *</label>
          <input 
            v-model.number="formData.areaCount" 
            type="number" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入区域数"
            min="1"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">工位数 *</label>
          <input 
            v-model.number="formData.seatCount" 
            type="number" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入工位数"
            min="0"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">状态</label>
          <div class="flex items-center gap-4">
            <label class="flex items-center gap-1 cursor-pointer">
              <input v-model="formData.status" type="radio" value="1" />
              <span>启用</span>
            </label>
            <label class="flex items-center gap-1 cursor-pointer">
              <input v-model="formData.status" type="radio" value="0" />
              <span>停用</span>
            </label>
          </div>
        </div>
      </div>
      <div class="p-6 border-t flex justify-end gap-3">
        <button @click="handleCancel" class="px-4 py-2 border rounded-lg hover:bg-gray-50">取消</button>
        <button @click="handleSubmit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          {{ isEdit ? '保存更改' : '添加楼层' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { Floor } from '../types'

const props = defineProps<{
  visible: boolean
  isEdit: boolean
  floor?: Floor
  venueId?: number
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'submit', data: any): void
}>()

const formData = reactive({
  floorNo: '',
  name: '',
  areaCount: 1,
  seatCount: 0,
  status: '1',
  imageUrl: ''
})

watch(() => props.floor, (newFloor) => {
  if (newFloor && props.isEdit) {
    formData.floorNo = newFloor.floorNo
    formData.name = newFloor.name
    formData.areaCount = newFloor.areaCount
    formData.seatCount = newFloor.seatCount
    formData.status = newFloor.status.toString()
    formData.imageUrl = newFloor.imageUrl
  }
}, { immediate: true })

watch(() => props.visible, (newVisible) => {
  if (newVisible && !props.isEdit) {
    Object.assign(formData, {
      floorNo: '',
      name: '',
      areaCount: 1,
      seatCount: 0,
      status: '1',
      imageUrl: ''
    })
  }
})

const handleCancel = () => {
  emit('close')
}

const handleSubmit = () => {
  emit('submit', {
    ...formData,
    venue_id: props.venueId,
    status: parseInt(formData.status)
  })
}
</script>