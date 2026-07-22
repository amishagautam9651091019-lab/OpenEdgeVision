export type PluginStatus =
  | 'available'
  | 'loading'
  | 'loaded'
  | 'error'
  | string

export interface PluginInfo {
  id: string
  name: string
  version: string
  type: string
  status: PluginStatus
  device: string
  description: string

  model_path: string | null
  input_width: number | null
  input_height: number | null
  class_count: number | null
  error_message: string | null
  created_at: string
}

export interface BoundingBox {
  x: number
  y: number
  width: number
  height: number
}

export interface DetectionObject {
  class_id: number
  class_name: string
  confidence: number
  bbox: BoundingBox
}

export interface DetectionResult {
  frame_id: number
  timestamp: number
  stream_name: string
  plugin_id: string
  inference_time_ms: number
  detections: DetectionObject[]
}

export interface PluginHealthDetails {
  plugin_id: string
  healthy: boolean
  status: PluginStatus
  is_loaded: boolean
  device: string
  error_message: string | null
}

export interface PluginHealth {
  plugin_id: string
  healthy: boolean
  status: PluginStatus
  details: PluginHealthDetails
}

interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

interface PluginActionData {
  plugin: PluginInfo
}

const API_PREFIX = '/api/v1/plugins'

async function request<T>(
  url: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      Accept: 'application/json',
      ...(options?.body
        ? { 'Content-Type': 'application/json' }
        : {}),
      ...options?.headers,
    },
  })

  let payload: unknown

  try {
    payload = await response.json()
  } catch {
    throw new Error(
      `服务器返回了非 JSON 响应，HTTP ${response.status}`,
    )
  }

  if (!response.ok) {
    const errorPayload = payload as {
      detail?: string
      message?: string
    }

    throw new Error(
      errorPayload.detail ??
        errorPayload.message ??
        `请求失败，HTTP ${response.status}`,
    )
  }

  const apiPayload = payload as ApiResponse<T>

  if (apiPayload.code !== 0) {
    throw new Error(
      apiPayload.message || '后端业务请求失败',
    )
  }

  return apiPayload.data
}

/**
 * 后端当前列表接口可能直接返回 PluginInfo[]，
 * 也可能返回带 plugins 字段的汇总对象。
 * 这里兼容两种结构。
 */
export async function getPlugins(): Promise<PluginInfo[]> {
  const data = await request<
    PluginInfo[] | {
      plugins: PluginInfo[]
    }
  >(API_PREFIX)

  if (Array.isArray(data)) {
    return data
  }

  return data.plugins ?? []
}

export function getPlugin(
  pluginId: string,
): Promise<PluginInfo> {
  return request<PluginInfo>(
    `${API_PREFIX}/${encodeURIComponent(pluginId)}`,
  )
}

export async function loadPlugin(
  pluginId: string,
): Promise<PluginInfo> {
  const data = await request<PluginActionData>(
    `${API_PREFIX}/${encodeURIComponent(pluginId)}/load`,
    {
      method: 'POST',
      body: JSON.stringify({}),
    },
  )

  return data.plugin
}

export async function unloadPlugin(
  pluginId: string,
): Promise<PluginInfo> {
  const data = await request<PluginActionData>(
    `${API_PREFIX}/${encodeURIComponent(pluginId)}/unload`,
    {
      method: 'POST',
      body: JSON.stringify({}),
    },
  )

  return data.plugin
}

export function getPluginHealth(
  pluginId: string,
): Promise<PluginHealth> {
  return request<PluginHealth>(
    `${API_PREFIX}/${encodeURIComponent(pluginId)}/health`,
  )
}

export function predictPlugin(
  pluginId: string,
  frameId: number,
  streamName: string,
): Promise<DetectionResult> {
  return request<DetectionResult>(
    `${API_PREFIX}/${encodeURIComponent(pluginId)}/predict`,
    {
      method: 'POST',
      body: JSON.stringify({
        frame_id: frameId,
        stream_name: streamName,
      }),
    },
  )
}