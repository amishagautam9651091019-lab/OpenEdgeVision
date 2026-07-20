import request from './http'

export interface StreamInfo {
  name: string
  ready: boolean
  source_type?: string | null
  reader_count?: number
  tracks: string[]
  rtsp_url?: string
  webrtc_url?: string
  hls_url?: string
}

export interface StreamData {
  total: number
  online: number
  offline: number
  streams: StreamInfo[]
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export async function getStreams(): Promise<StreamData> {
  const response = await request.get<ApiResponse<StreamData>>(
    '/api/v1/streams'
  )

  console.log('[streams.ts] response:', response)

  if (!response || !response.data) {
    throw new Error('视频流接口返回为空')
  }

  if (!Array.isArray(response.data.streams)) {
    throw new Error('视频流接口 streams 字段格式错误')
  }

  return response.data
}