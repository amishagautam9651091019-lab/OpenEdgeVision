
<template>
  <section>
    <div class="page-header">
      <div>
        <h1>Cameras API Test</h1>
        <p>管理固定摄像机、无人机和车载视频源</p>
      </div>

      <el-button
        type="primary"
        :loading="loading"
        @click="loadStreams"
      >
        刷新状态
      </el-button>
    </div>

    <el-alert
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
      class="error-alert"
    />

    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="streams"
        style="width: 100%"
      >
        <el-table-column prop="name" label="名称" min-width="140" />

        <el-table-column label="类型" min-width="150">
          <template #default="{ row }">
            {{ row.source_type || '未连接' }}
          </template>
        </el-table-column>

        <el-table-column label="协议" width="100">
          <template #default>RTSP</template>
        </el-table-column>

        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.ready ? 'success' : 'danger'">
              {{ row.ready ? '在线' : '离线' }}
            </el-tag>
          </template>
        </el-table-column>
	 <el-table-column
           label="操作"
           width="160"
           fixed="right"
           >
             <template #default="{ row }">
                <el-button
                   type="primary"
                   link
                   :disabled="!row.ready"
                   @click="openPreview(row.name)"
                >
                 预览
              </el-button>
             </template>
           </el-table-column>


        <el-table-column label="编码" width="120">
          <template #default="{ row }">
            {{ row.tracks?.join(', ') || '-' }}
          </template>
        </el-table-column>

        <el-table-column
          prop="rtsp_url"
          label="RTSP地址"
          min-width="260"
          show-overflow-tooltip
        />

        <template #empty>
          <el-empty description="暂无视频流数据" />
        </template>
      </el-table>
    </el-card>
  </section>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getStreams, type StreamInfo } from '@/api/streams'

console.log('[CameraManager] script executed')

const streams = ref<StreamInfo[]>([])
const loading = ref(false)
const errorMessage = ref('')
const router = useRouter()

let refreshTimer: ReturnType<typeof setInterval> | undefined

function openPreview(streamName:string){
        router.push({
           name:'camera-preview',
           params:{
                name:streamName,
                },
                })
                }


async function loadStreams(): Promise<void> {
  console.log('[CameraManager] loadStreams started')

  loading.value = true
  errorMessage.value = ''

  try {
    const response = await getStreams()

    console.log('[CameraManager] API response:', response)

    streams.value = response.streams

    console.log('[CameraManager] stream count:', streams.value.length)
  } catch (error) {
    console.error('[CameraManager] request failed:', error)

    streams.value = []
    errorMessage.value = '无法连接后端视频流接口，请检查FastAPI和CORS配置'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  console.log('[CameraManager] mounted')

  void loadStreams()

  refreshTimer = setInterval(() => {
    void loadStreams()
  }, 10_000)
})

onUnmounted(() => {
  if (refreshTimer !== undefined) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}

.page-header h1 {
  margin: 0 0 6px;
  font-size: 26px;
}

.page-header p {
  margin: 0;
  color: #8492a6;
}

.error-alert {
  margin-bottom: 16px;
}
</style>
