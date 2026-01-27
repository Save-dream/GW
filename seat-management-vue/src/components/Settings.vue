<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">系统设置</h2>
        <p class="text-gray-500">配置系统参数和偏好设置</p>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border p-6">
      <h3 class="text-lg font-semibold mb-4">基本设置</h3>
      <div class="space-y-4">
        <div class="flex items-center justify-between py-3 border-b">
          <div>
            <p class="font-medium">系统名称</p>
            <p class="text-sm text-gray-500">设置系统显示的名称</p>
          </div>
          <input
            type="text"
            v-model="settings.systemName"
            class="px-4 py-2 border rounded-lg w-64"
          />
        </div>
        <div class="flex items-center justify-between py-3 border-b">
          <div>
            <p class="font-medium">默认语言</p>
            <p class="text-sm text-gray-500">设置系统默认语言</p>
          </div>
          <select class="px-4 py-2 border rounded-lg w-64" v-model="settings.language">
            <option value="zh-CN">简体中文</option>
            <option value="en-US">English</option>
          </select>
        </div>
        <div class="flex items-center justify-between py-3 border-b">
          <div>
            <p class="font-medium">时区设置</p>
            <p class="text-sm text-gray-500">设置系统时区</p>
          </div>
          <select class="px-4 py-2 border rounded-lg w-64" v-model="settings.timezone">
            <option value="Asia/Shanghai">Asia/Shanghai (UTC+8)</option>
            <option value="America/New_York">America/New_York (UTC-5)</option>
          </select>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border p-6">
      <h3 class="text-lg font-semibold mb-4">通知设置</h3>
      <div class="space-y-4">
        <div class="flex items-center justify-between py-3 border-b">
          <div>
            <p class="font-medium">邮件通知</p>
            <p class="text-sm text-gray-500">启用邮件通知功能</p>
          </div>
          <input type="checkbox" class="rounded" v-model="settings.emailNotification" />
        </div>
        <div class="flex items-center justify-between py-3 border-b">
          <div>
            <p class="font-medium">系统消息</p>
            <p class="text-sm text-gray-500">启用系统内消息通知</p>
          </div>
          <input type="checkbox" class="rounded" v-model="settings.systemNotification" />
        </div>
      </div>
    </div>

    <div class="flex justify-end">
      <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700" @click="handleSaveSettings">
        保存设置
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const settings = ref({
  systemName: '工位管理系统',
  language: 'zh-CN',
  timezone: 'Asia/Shanghai',
  emailNotification: true,
  systemNotification: true
})

const handleSaveSettings = () => {
  console.log('保存设置:', settings.value)
  // Here we would typically call the API to save settings
  // For now, we'll just show an alert
  alert('设置已保存')
}
</script>