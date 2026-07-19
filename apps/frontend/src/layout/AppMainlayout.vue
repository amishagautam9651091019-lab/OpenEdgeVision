<template>
  <el-container class="app-shell">
    <el-aside width="240px" class="sidebar">
      <div class="brand">
        <div class="brand-mark">OE</div>
        <div>
          <div class="brand-title">OpenEdge Vision</div>
          <div class="brand-subtitle">Edge AI Platform</div>
        </div>
      </div>

      <el-menu
        :default-active="route.path"
        router
        class="sidebar-menu"
        background-color="#0f2747"
        text-color="#c8d5e6"
        active-text-color="#ffffff"
      >
        <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
          <el-icon>
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.label }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="topbar">
        <div>
          <div class="topbar-title">{{ currentTitle }}</div>
          <div class="breadcrumb-text">OpenEdge Vision / {{ currentTitle }}</div>
        </div>

        <div class="topbar-actions">
          <el-tag type="success" effect="plain">Media Runtime</el-tag>
          <span class="version">V0.1</span>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view />
      </el-main>

      <el-footer class="footer"> OpenEdge Vision V0.1 · Open Vision Capability Platform </el-footer>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  Monitor,
  VideoCamera,
  Cpu,
  Connection,
  Bell,
  Box,
  Files,
  UploadFilled,
  Tools,
  Setting,
} from '@element-plus/icons-vue'

const route = useRoute()

const menuItems = [
  { path: '/', label: 'Dashboard', icon: Monitor },
  { path: '/cameras', label: 'Cameras', icon: VideoCamera },
  { path: '/plugins', label: 'AI Plugins', icon: Cpu },
  { path: '/tasks', label: 'Tasks', icon: Connection },
  { path: '/events', label: 'Events', icon: Bell },
  { path: '/models', label: 'Models', icon: Box },
  { path: '/datasets', label: 'Datasets', icon: Files },
  { path: '/deployment', label: 'Deployment', icon: UploadFilled },
  { path: '/developer', label: 'Developer', icon: Tools },
  { path: '/settings', label: 'Settings', icon: Setting },
]

const currentTitle = computed(() => {
  const item = menuItems.find((menu) => menu.path === route.path)
  return item?.label ?? 'OpenEdge Vision'
})
</script>

<style scoped>
.app-shell {
  width: 100%;
  min-height: 100vh;
}

.sidebar {
  min-height: 100vh;
  background: #0f2747;
  box-shadow: 4px 0 18px rgb(15 39 71 / 12%);
}

.brand {
  display: flex;
  height: 76px;
  align-items: center;
  gap: 12px;
  padding: 0 20px;
  border-bottom: 1px solid rgb(255 255 255 / 8%);
}

.brand-mark {
  display: flex;
  width: 38px;
  height: 38px;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: white;
  background: linear-gradient(135deg, #409eff, #1d4ed8);
  font-weight: 700;
}

.brand-title {
  color: white;
  font-size: 16px;
  font-weight: 700;
}

.brand-subtitle {
  margin-top: 3px;
  color: #8fa8c8;
  font-size: 11px;
}

.sidebar-menu {
  border-right: 0;
  padding-top: 10px;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  margin: 4px 12px;
  border-radius: 8px;
  background: #2563eb;
}

.sidebar-menu :deep(.el-menu-item) {
  margin: 4px 12px;
  border-radius: 8px;
}

.topbar {
  display: flex;
  height: 76px;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e8edf4;
  background: white;
}

.topbar-title {
  color: #172033;
  font-size: 20px;
  font-weight: 700;
}

.breadcrumb-text {
  margin-top: 5px;
  color: #9aa7b8;
  font-size: 12px;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.version {
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
}

.main-content {
  min-height: calc(100vh - 120px);
  padding: 24px;
  background: #f3f6fa;
}

.footer {
  height: 44px;
  color: #94a3b8;
  background: white;
  text-align: center;
  font-size: 12px;
  line-height: 44px;
}
</style>
