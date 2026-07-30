<template>
  <div class="camera-preview-page">

    <!-- 顶部返回 -->
    <el-page-header
      content="视频预览"
      @back="goBack"
    />

    <!-- 视频区域 -->
    <el-card class="video-card">

      <template #header>
        <div class="header">

          <div class="camera-title">

            <span class="name">
              {{ stream.name }}
            </span>


            <!-- 在线状态 -->
            <el-tag
              v-if="stream.ready"
              type="success"
              class="status-tag"
            >
              在线
            </el-tag>


            <el-tag
              v-else
              type="danger"
              class="status-tag"
            >
              离线
            </el-tag>


          </div>


          <el-tag type="info">
            WebRTC + AI
          </el-tag>


        </div>

      </template>


      <!-- AI视频播放器 -->

      <AIStreamPlayer
        :stream-name="streamName"
      />


    </el-card>



    <!-- 视频信息 -->

    <el-card class="info-card">

      <template #header>
        视频信息
      </template>


      <el-descriptions
        :column="2"
        border
      >

        <el-descriptions-item label="名称">
          {{ stream.name }}
        </el-descriptions-item>


        <el-descriptions-item label="状态">

          <el-tag
            v-if="stream.ready"
            type="success"
          >
            在线
          </el-tag>

          <el-tag
            v-else
            type="danger"
          >
            离线
          </el-tag>

        </el-descriptions-item>



        <el-descriptions-item label="类型">
          {{ stream.source_type || '-' }}
        </el-descriptions-item>



        <el-descriptions-item label="协议">
          RTSP
        </el-descriptions-item>



        <el-descriptions-item label="编码">

          {{
            stream.tracks &&
            stream.tracks.length > 0
              ? stream.tracks.join(',')
              : '-'
          }}

        </el-descriptions-item>



        <el-descriptions-item label="读取数量">
          {{ stream.reader_count ?? 0 }}
        </el-descriptions-item>



        <el-descriptions-item label="RTSP地址">

          <span class="url">
            {{ stream.rtsp_url || '-' }}
          </span>

        </el-descriptions-item>



        <el-descriptions-item label="WebRTC地址">

          <span class="url">
            {{ stream.webrtc_url || '-' }}
          </span>

        </el-descriptions-item>



        <el-descriptions-item label="HLS地址">

          <span class="url">
            {{ stream.hls_url || '-' }}
          </span>

        </el-descriptions-item>


      </el-descriptions>


    </el-card>


  </div>
</template>



<script setup lang="ts">

import {
  computed,
  onMounted,
  ref
} from 'vue'


import {
  useRoute,
  useRouter
} from 'vue-router'


import VideoPlayer 
from '@/components/video/VideoPlayer.vue'

import AIStreamPlayer
from '@/components/video/AIStreamPlayer.vue'


import {
  getStreams,
  type StreamInfo
} from '@/api/streams'



const route = useRoute()

const router = useRouter()



/**
 * 当前视频名称
 */
const streamName = computed(()=>{

  return String(
    route.params.name || ''
  )

})



/**
 * 所有视频流
 */
const streams = ref<StreamInfo[]>([])



/**
 * 当前视频流信息
 */
const stream = computed<StreamInfo>(()=>{


  const current =
    streams.value.find(
      item =>
        item.name === streamName.value
    )


  if(current){

    return current

  }


  return {

    name: streamName.value,

    ready:false,

    source_type:null,

    reader_count:0,

    tracks:[]

  }


})



/**
 * 加载视频状态
 */
async function loadStream(){


  try {


    const res =
      await getStreams()



    console.log(
      'CameraPreview streams:',
      res
    )



    streams.value =
      res.streams || []



  } catch(error){


    console.error(
      'load streams failed:',
      error
    )


    streams.value=[]


  }


}



/**
 * 返回摄像头列表
 */
function goBack(){

  router.push('/cameras')

}



onMounted(()=>{


  loadStream()


})



</script>



<style scoped>


.camera-preview-page{

  padding:20px;

}



.video-card{

  margin-top:20px;

}



.info-card{

  margin-top:20px;

}



.header{

  display:flex;

  justify-content:space-between;

  align-items:center;

}



.camera-title{

  display:flex;

  align-items:center;

}



.name{

  font-size:20px;

  font-weight:600;

}



.status-tag{

  margin-left:15px;

}



.url{

  word-break:break-all;

  color:#666;

}



</style>
