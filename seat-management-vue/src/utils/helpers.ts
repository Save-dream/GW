export const getStatusInfo = (status: number) => {
  switch (status) {
    case 0: return { color: 'bg-green-500', text: '闲置', bg: 'bg-green-50', textColor: 'text-green-600' }
    case 1: return { color: 'bg-yellow-500', text: '占用', bg: 'bg-yellow-50', textColor: 'text-yellow-600' }
    case 2: return { color: 'bg-red-500', text: '维修', bg: 'bg-red-50', textColor: 'text-red-600' }
    default: return { color: 'bg-gray-400', text: '停用', bg: 'bg-gray-50', textColor: 'text-gray-600' }
  }
}

export const getAreaTypeColor = (type: number) => {
  switch (type) {
    case 1: return { bg: 'bg-blue-500', border: 'border-blue-600', name: '专属区' }
    case 2: return { bg: 'bg-purple-500', border: 'border-purple-600', name: '混合区' }
    case 3: return { bg: 'bg-orange-500', border: 'border-orange-600', name: '会议室' }
    default: return { bg: 'bg-gray-500', border: 'border-gray-600', name: '公共区' }
  }
}