import { createRouter, createWebHistory } from 'vue-router'

import AppMainlayout from '@/layout/AppMainlayout.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import CameraManager from '@/views/cameras/CameraManager.vue'
import CameraPreview from '@/views/cameras/CameraPreview.vue'
import ComingSoonView from '@/views/common/ComingSoonView.vue'
import PluginManager from '@/views/plugins/PluginManager.vue'

const routes = [
  {
    path: '/',
    component: AppMainlayout,
    children: [
      {
        path: '',
        name: 'dashboard',
        component: DashboardView,
      },
      {
        path: 'cameras',
        name: 'cameras',
        component: CameraManager,
      },
      {
	 path:'cameras/:name/preview',
	 name:'camera-preview',
	 component:CameraPreview,
      },
      {
        path: 'plugins',
        name: 'plugins',
        component: PluginManager,
      },
      {
        path: 'tasks',
        component: ComingSoonView,
        props: {
          title: 'Tasks',
          description: '视频源与算法插件的任务绑定。',
        },
      },
      {
        path: 'events',
        component: ComingSoonView,
        props: {
          title: 'Events',
          description: 'AI检测事件、截图及告警记录。',
        },
      },
      {
        path: 'models',
        component: ComingSoonView,
        props: {
          title: 'Models',
          description: 'ONNX及边缘端模型版本管理。',
        },
      },
      {
        path: 'datasets',
        component: ComingSoonView,
        props: {
          title: 'Datasets',
          description: '小目标、烟雾与违停数据集管理。',
        },
      },
      {
        path: 'deployment',
        component: ComingSoonView,
        props: {
          title: 'Deployment',
          description: '边缘节点部署、升级和运行状态。',
        },
      },
      {
        path: 'developer',
        component: ComingSoonView,
        props: {
          title: 'Developer',
          description: 'Plugin SDK、API和开发者工具。',
        },
      },
      {
        path: 'settings',
        component: ComingSoonView,
        props: {
          title: 'Settings',
          description: '平台配置和系统参数。',
        },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
