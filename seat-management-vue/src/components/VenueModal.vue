<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-md">
      <div class="p-6 border-b">
        <h3 class="text-xl font-bold">{{ isEdit ? '编辑场地' : currentStep === 1 ? '新增场地' : '确认信息' }}</h3>
      </div>
      
      <div v-if="isEdit || currentStep === 1" class="p-6 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">场地名称 *</label>
          <input 
            v-model="formData.name" 
            type="text" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入场地名称"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">场地编码 *</label>
          <input 
            v-model="formData.code" 
            type="text" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="isEdit"
            placeholder="请输入场地编码"
          />
          <p v-if="isEdit" class="text-xs text-gray-500 mt-1">编码创建后不可变更</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">所在城市 *</label>
          <select 
            v-model="formData.city" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">请选择城市</option>
            <option value="北京市">北京市</option>
            <option value="上海市">上海市</option>
            <option value="广州市">广州市</option>
            <option value="深圳市">深圳市</option>
            <option value="杭州市">杭州市</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">详细地址 *</label>
          <input 
            v-model="formData.address" 
            type="text" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入详细地址"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">场地类型</label>
          <select 
            v-model="formData.type" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="自有物业">自有物业</option>
            <option value="租赁办公">租赁办公</option>
            <option value="联合办公空间">联合办公空间</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">楼层数 *</label>
          <input 
            v-model.number="formData.floorCount" 
            type="number" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入楼层数"
            min="1"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">备注说明</label>
          <textarea 
            v-model="formData.remark" 
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"
            placeholder="请输入备注信息"
          ></textarea>
        </div>
        <div v-if="!isEdit">
          <label class="block text-sm font-medium text-gray-700 mb-1">状态</label>
          <div class="flex items-center gap-4">
            <label class="flex items-center gap-1 cursor-pointer">
              <input v-model="formData.status" type="radio" value="1" />
              <span>立即启用</span>
            </label>
            <label class="flex items-center gap-1 cursor-pointer">
              <input v-model="formData.status" type="radio" value="0" />
              <span>稍后启用</span>
            </label>
          </div>
        </div>
      </div>
      
      <div v-if="!isEdit && currentStep === 2" class="p-6 space-y-4">
        <p class="text-gray-700">请确认以下信息：</p>
        <div class="space-y-3 text-sm">
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">场地名称：</span>
            <span class="font-medium">{{ formData.name }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">场地编码：</span>
            <span class="font-medium">{{ formData.code }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">所在城市：</span>
            <span class="font-medium">{{ formData.city }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">详细地址：</span>
            <span class="font-medium">{{ formData.address }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">场地类型：</span>
            <span class="font-medium">{{ formData.type }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">楼层数：</span>
            <span class="font-medium">{{ formData.floorCount }}层</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">初始状态：</span>
            <span class="font-medium">{{ formData.status === '1' ? '立即启用' : '稍后启用' }}</span>
          </div>
          <div v-if="formData.remark" class="flex justify-between py-2 border-b">
            <span class="text-gray-600">备注说明：</span>
            <span class="font-medium">{{ formData.remark }}</span>
          </div>
        </div>
        <p class="text-xs text-gray-500 mt-4">创建后，您可以在场地详情中添加楼层和配置平面图。</p>
      </div>
      
      <div class="p-6 border-t flex justify-end gap-3">
        <button @click="handleCancel" class="px-4 py-2 border rounded-lg hover:bg-gray-50">取消</button>
        <button v-if="!isEdit && currentStep === 2" @click="handleBack" class="px-4 py-2 border rounded-lg hover:bg-gray-50">上一步</button>
        <button @click="handleSubmit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          {{ isEdit ? '保存更改' : currentStep === 1 ? '下一步' : '确认创建' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import type { Venue } from '../types'

const props = defineProps<{
  visible: boolean
  isEdit: boolean
  venue?: Venue
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'submit', data: any): void
}>()

const currentStep = ref(1)

const formData = reactive({
  name: '',
  code: '',
  city: '',
  address: '',
  type: '租赁办公',
  floorCount: 1,
  remark: '',
  status: '1'
})

watch(() => props.venue, (newVenue) => {
  if (newVenue) {
    formData.name = newVenue.name
    formData.code = newVenue.code
    formData.city = newVenue.city
    formData.address = newVenue.address
    formData.type = newVenue.type
    formData.floorCount = newVenue.floorCount
    formData.remark = newVenue.remark || ''
    formData.status = newVenue.status.toString()
  }
}, { immediate: true })

watch(() => props.visible, (newVisible) => {
  if (newVisible && !props.isEdit) {
    currentStep.value = 1
    Object.assign(formData, {
      name: '',
      code: '',
      city: '',
      address: '',
      type: '租赁办公',
      floorCount: 1,
      remark: '',
      status: '1'
    })
  }
})

const handleCancel = () => {
  emit('close')
}

const handleSubmit = () => {
  if (!props.isEdit) {
    if (currentStep.value === 1) {
      currentStep.value = 2
    } else {
      emit('submit', {
        ...formData,
        status: parseInt(formData.status)
      })
    }
  } else {
    emit('submit', {
      ...formData,
      status: parseInt(formData.status)
    })
  }
}

const handleBack = () => {
  currentStep.value = 1
}
</script>
