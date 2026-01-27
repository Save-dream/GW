# 工位管理系统 - Vue版本

这是一个基于Vue 3 + TypeScript + Tailwind CSS的工位管理系统，是从React版本转换而来。

## 技术栈

- **前端框架**: Vue 3.4.0 (Composition API)
- **开发语言**: TypeScript
- **构建工具**: Vite 6.0.1
- **样式框架**: Tailwind CSS v3.4.16
- **图标库**: Lucide Vue Next
- **状态管理**: Vue 3 Composition API (ref, computed)

## 项目结构

```
seat-management-vue/
├── src/
│   ├── components/       # Vue组件
│   │   ├── Sidebar.vue
│   │   ├── Header.vue
│   │   ├── Dashboard.vue
│   │   ├── VenueManagement.vue
│   │   ├── FloorMap.vue
│   │   ├── SeatManagement.vue
│   │   ├── Binding.vue
│   │   ├── Logs.vue
│   │   ├── Settings.vue
│   │   └── BindModal.vue
│   ├── data/            # 模拟数据
│   │   └── mockData.ts
│   ├── types/           # TypeScript类型定义
│   │   └── index.ts
│   ├── utils/           # 工具函数
│   │   └── helpers.ts
│   ├── App.vue          # 主组件
│   ├── main.ts          # 入口文件
│   └── index.css        # 全局样式
├── public/              # 静态资源
├── index.html           # HTML模板
├── package.json         # 项目配置
├── vite.config.ts       # Vite配置
├── tsconfig.json        # TypeScript配置
└── tailwind.config.js   # Tailwind配置
```

## 功能模块

### 1. 首页概览
- 展示系统整体状态统计
- 楼层概览和快速导航
- 最近操作记录

### 2. 场地管理
- 管理公司办公场地信息
- 查看场地统计数据

### 3. 楼层与区域管理
- 可视化楼层平面图
- 区域分布展示
- 区域类型区分

### 4. 工位管理
- 工位网格视图
- 工位状态管理
- 批量操作支持

### 5. 人员绑定
- 双入口绑定机制
- 工位视角和人员视角
- 绑定冲突处理

### 6. 操作日志
- 操作历史记录
- 筛选和导出功能

### 7. 系统设置
- 基本设置配置
- 通知设置

## 安装依赖

```bash
npm install
# 或
pnpm install
# 或
yarn install
```

## 开发模式

```bash
npm run dev
```

项目将在 http://localhost:3000 启动

## 构建生产版本

```bash
npm run build
```

## 预览生产版本

```bash
npm run preview
```

## 代码检查

```bash
npm run lint
```

## 从React转换的主要变化

### 1. 组件结构
- React: 函数组件 + Hooks
- Vue: `<script setup>` + Composition API

### 2. 状态管理
- React: `useState`, `useEffect`
- Vue: `ref`, `computed`, `watch`

### 3. 事件处理
- React: `onClick={() => handleClick()}`
- Vue: `@click="handleClick"`

### 4. 条件渲染
- React: `{condition && <Component />}`
- Vue: `<Component v-if="condition" />`

### 5. 列表渲染
- React: `{items.map(item => <Item key={item.id} />)}`
- Vue: `<Item v-for="item in items" :key="item.id" />`

### 6. 类名绑定
- React: `className={isActive ? 'active' : ''}`
- Vue: `:class="{ active: isActive }"`

### 7. Props和Emits
- React: `props`, `emit` (自定义)
- Vue: `defineProps`, `defineEmits`

## 注意事项

1. **图标库**: 使用 `lucide-vue-next` 替代 `lucide-react`
2. **样式**: 保持与React版本相同的Tailwind CSS样式
3. **类型定义**: TypeScript接口保持不变
4. **模拟数据**: 使用相同的模拟数据结构

## 开发建议

1. 使用 `<script setup>` 语法简化组件代码
2. 利用 `computed` 进行计算属性优化
3. 使用 `defineProps` 和 `defineEmits` 进行类型安全的事件和属性传递
4. 组件拆分保持与React版本相同的粒度

## 许可证

MIT