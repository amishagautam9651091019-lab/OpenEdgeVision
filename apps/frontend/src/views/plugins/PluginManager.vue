<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import {
  getPluginHealth,
  getPlugins,
  loadPlugin,
  predictPlugin,
  unloadPlugin,
  type DetectionResult,
  type PluginHealth,
  type PluginInfo,
} from '@/api/plugins'

const plugins = ref<PluginInfo[]>([])
const selectedPluginId = ref<string | null>(null)

const healthResult = ref<PluginHealth | null>(null)
const predictionResult = ref<DetectionResult | null>(null)

const loadingPage = ref(false)
const runningAction = ref<string | null>(null)
const errorMessage = ref('')

const streamName = ref('drone01')
const frameId = ref(1)

const selectedPlugin = computed(() =>
  plugins.value.find(
    (plugin) => plugin.id === selectedPluginId.value,
  ),
)

function replacePlugin(updated: PluginInfo): void {
  const index = plugins.value.findIndex(
    (plugin) => plugin.id === updated.id,
  )

  if (index >= 0) {
    plugins.value[index] = updated
  } else {
    plugins.value.push(updated)
  }
}

function selectPlugin(plugin: PluginInfo): void {
  selectedPluginId.value = plugin.id
  healthResult.value = null
  predictionResult.value = null
  errorMessage.value = ''
}

function statusLabel(status: string): string {
  const labels: Record<string, string> = {
    available: '可用',
    loading: '加载中',
    loaded: '已加载',
    error: '异常',
  }

  return labels[status] ?? status
}

function statusClass(status: string): string {
  return `status-${status}`
}

async function refreshPlugins(): Promise<void> {
  loadingPage.value = true
  errorMessage.value = ''

  try {
    plugins.value = await getPlugins()

    if (
      selectedPluginId.value &&
      !plugins.value.some(
        (plugin) =>
          plugin.id === selectedPluginId.value,
      )
    ) {
      selectedPluginId.value = null
    }


    if (!selectedPluginId.value) {

      const firstPlugin = plugins.value[0]

      if (firstPlugin) {
        selectedPluginId.value = firstPlugin.id
      }

    }


  } catch (error) {

    errorMessage.value =
      error instanceof Error
        ? error.message
        : '加载插件列表失败'

  } finally {

    loadingPage.value = false

  }
}

async function handleLoad(
  plugin: PluginInfo,
): Promise<void> {
  runningAction.value = `load:${plugin.id}`
  errorMessage.value = ''

  try {
    const updated = await loadPlugin(plugin.id)
    replacePlugin(updated)

    if (selectedPluginId.value === plugin.id) {
      healthResult.value = await getPluginHealth(
        plugin.id,
      )
    }
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : '插件加载失败'
  } finally {
    runningAction.value = null
  }
}

async function handleUnload(
  plugin: PluginInfo,
): Promise<void> {
  runningAction.value = `unload:${plugin.id}`
  errorMessage.value = ''

  try {
    const updated = await unloadPlugin(plugin.id)
    replacePlugin(updated)

    if (selectedPluginId.value === plugin.id) {
      healthResult.value = await getPluginHealth(
        plugin.id,
      )
      predictionResult.value = null
    }
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : '插件卸载失败'
  } finally {
    runningAction.value = null
  }
}

async function handleHealth(
  plugin: PluginInfo,
): Promise<void> {
  runningAction.value = `health:${plugin.id}`
  errorMessage.value = ''

  try {
    healthResult.value = await getPluginHealth(
      plugin.id,
    )
    selectedPluginId.value = plugin.id
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : '健康检查失败'
  } finally {
    runningAction.value = null
  }
}

async function handlePredict(
  plugin: PluginInfo,
): Promise<void> {
  runningAction.value = `predict:${plugin.id}`
  errorMessage.value = ''
  predictionResult.value = null

  try {
    predictionResult.value = await predictPlugin(
      plugin.id,
      frameId.value,
      streamName.value.trim() || 'drone01',
    )

    frameId.value += 1
    selectedPluginId.value = plugin.id
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : '模拟推理失败'
  } finally {
    runningAction.value = null
  }
}

onMounted(() => {
  void refreshPlugins()
})
</script>

<template>
  <section class="plugin-page">
    <header class="page-header">
      <div>
        <h1>AI Plugins</h1>
        <p>
          管理 OpenEdge Vision 算法插件的加载、卸载、
          健康检查和模拟推理。
        </p>
      </div>

      <button
        class="secondary-button"
        :disabled="loadingPage"
        @click="refreshPlugins"
      >
        {{ loadingPage ? '刷新中...' : '刷新列表' }}
      </button>
    </header>

    <div
      v-if="errorMessage"
      class="error-message"
    >
      {{ errorMessage }}
    </div>

    <div
      v-if="loadingPage && plugins.length === 0"
      class="empty-state"
    >
      正在加载插件列表……
    </div>

    <div
      v-else-if="plugins.length === 0"
      class="empty-state"
    >
      当前没有已注册的 AI 插件。
    </div>

    <div
      v-else
      class="page-grid"
    >
      <div class="plugin-list">
        <article
          v-for="plugin in plugins"
          :key="plugin.id"
          class="plugin-card"
          :class="{
            selected:
              selectedPluginId === plugin.id,
          }"
          @click="selectPlugin(plugin)"
        >
          <div class="card-header">
            <div>
              <h2>{{ plugin.name }}</h2>
              <code>{{ plugin.id }}</code>
            </div>

            <span
              class="status-badge"
              :class="statusClass(plugin.status)"
            >
              {{ statusLabel(plugin.status) }}
            </span>
          </div>

          <p class="description">
            {{ plugin.description }}
          </p>

          <dl class="metadata">
            <div>
              <dt>类型</dt>
              <dd>{{ plugin.type }}</dd>
            </div>

            <div>
              <dt>版本</dt>
              <dd>{{ plugin.version }}</dd>
            </div>

            <div>
              <dt>设备</dt>
              <dd>{{ plugin.device }}</dd>
            </div>
          </dl>

          <div class="actions">
            <button
              class="primary-button"
              :disabled="
                plugin.status === 'loaded' ||
                runningAction !== null
              "
              @click.stop="handleLoad(plugin)"
            >
              {{
                runningAction === `load:${plugin.id}`
                  ? '加载中...'
                  : 'Load'
              }}
            </button>

            <button
              class="danger-button"
              :disabled="
                plugin.status !== 'loaded' ||
                runningAction !== null
              "
              @click.stop="handleUnload(plugin)"
            >
              {{
                runningAction === `unload:${plugin.id}`
                  ? '卸载中...'
                  : 'Unload'
              }}
            </button>

            <button
              class="secondary-button"
              :disabled="runningAction !== null"
              @click.stop="handleHealth(plugin)"
            >
              {{
                runningAction === `health:${plugin.id}`
                  ? '检查中...'
                  : 'Health'
              }}
            </button>
          </div>
        </article>
      </div>

      <aside class="detail-panel">
        <template v-if="selectedPlugin">
          <h2>插件测试</h2>

          <div class="form-group">
            <label for="stream-name">视频流名称</label>
            <input
              id="stream-name"
              v-model="streamName"
              type="text"
              placeholder="drone01"
            />
          </div>

          <div class="form-group">
            <label for="frame-id">帧编号</label>
            <input
              id="frame-id"
              v-model.number="frameId"
              type="number"
              min="0"
            />
          </div>

          <button
            class="primary-button full-width"
            :disabled="
              selectedPlugin.status !== 'loaded' ||
              runningAction !== null
            "
            @click="handlePredict(selectedPlugin)"
          >
            {{
              runningAction ===
              `predict:${selectedPlugin.id}`
                ? '推理中...'
                : '执行 Mock Predict'
            }}
          </button>

          <section
            v-if="healthResult"
            class="result-section"
          >
            <h3>Health</h3>

            <dl class="result-grid">
              <div>
                <dt>Healthy</dt>
                <dd>
                  {{
                    healthResult.healthy
                      ? 'true'
                      : 'false'
                  }}
                </dd>
              </div>

              <div>
                <dt>Status</dt>
                <dd>{{ healthResult.status }}</dd>
              </div>

              <div>
                <dt>Loaded</dt>
                <dd>
                  {{
                    healthResult.details.is_loaded
                      ? 'true'
                      : 'false'
                  }}
                </dd>
              </div>

              <div>
                <dt>Device</dt>
                <dd>
                  {{ healthResult.details.device }}
                </dd>
              </div>
            </dl>
          </section>

          <section
            v-if="predictionResult"
            class="result-section"
          >
            <h3>Predict Result</h3>

            <p>
              Stream:
              <strong>
                {{ predictionResult.stream_name }}
              </strong>
            </p>

            <p>
              Inference:
              <strong>
                {{
                  predictionResult.inference_time_ms
                }}
                ms
              </strong>
            </p>

            <div
              v-for="(
                detection, index
              ) in predictionResult.detections"
              :key="index"
              class="detection-item"
            >
              <strong>
                {{ detection.class_name }}
              </strong>

              <span>
                confidence:
                {{ detection.confidence }}
              </span>

              <code>
                x={{ detection.bbox.x }},
                y={{ detection.bbox.y }},
                w={{ detection.bbox.width }},
                h={{ detection.bbox.height }}
              </code>
            </div>
          </section>
        </template>

        <div
          v-else
          class="empty-state"
        >
          选择一个插件查看详情。
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.plugin-page {
  padding: 24px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0 0 8px;
  font-size: 28px;
}

.page-header p {
  margin: 0;
  color: #64748b;
}

.page-grid {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(320px, 1fr);
  gap: 24px;
}

.plugin-list {
  display: grid;
  gap: 16px;
}

.plugin-card,
.detail-panel {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 4px 14px rgb(15 23 42 / 6%);
}

.plugin-card {
  padding: 20px;
  cursor: pointer;
}

.plugin-card.selected {
  border-color: #2563eb;
}

.card-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.card-header h2 {
  margin: 0 0 5px;
  font-size: 18px;
}

.description {
  color: #64748b;
}

.metadata,
.result-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.metadata div,
.result-grid div {
  padding: 10px;
  border-radius: 8px;
  background: #f8fafc;
}

dt {
  color: #64748b;
  font-size: 12px;
}

dd {
  margin: 4px 0 0;
  font-weight: 600;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}

button {
  border: 0;
  border-radius: 7px;
  padding: 9px 14px;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.primary-button {
  background: #2563eb;
  color: white;
}

.secondary-button {
  background: #e2e8f0;
  color: #0f172a;
}

.danger-button {
  background: #dc2626;
  color: white;
}

.status-badge {
  height: fit-content;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 12px;
}

.status-available {
  background: #e2e8f0;
}

.status-loading {
  background: #fef3c7;
}

.status-loaded {
  background: #dcfce7;
  color: #166534;
}

.status-error {
  background: #fee2e2;
  color: #991b1b;
}

.detail-panel {
  padding: 20px;
}

.form-group {
  display: grid;
  gap: 6px;
  margin-bottom: 14px;
}

.form-group input {
  border: 1px solid #cbd5e1;
  border-radius: 7px;
  padding: 10px;
}

.full-width {
  width: 100%;
}

.result-section {
  margin-top: 24px;
  padding-top: 18px;
  border-top: 1px solid #e2e8f0;
}

.detection-item {
  display: grid;
  gap: 6px;
  margin-top: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #f8fafc;
}

.error-message {
  margin-bottom: 16px;
  border-radius: 8px;
  padding: 12px;
  background: #fee2e2;
  color: #991b1b;
}

.empty-state {
  padding: 28px;
  text-align: center;
  color: #64748b;
}

@media (max-width: 900px) {
  .page-grid {
    grid-template-columns: 1fr;
  }

  .metadata,
  .result-grid {
    grid-template-columns: 1fr;
  }
}
</style>