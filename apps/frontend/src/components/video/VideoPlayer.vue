<template>
  <div class="video-player">
    <iframe
      v-if="streamName"
      :src="playerUrl"
      class="video-frame"
      allow="autoplay; fullscreen; picture-in-picture"
      allowfullscreen
    />

    <el-empty
      v-else
      description="请选择需要预览的视频流"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  streamName: string
  host?: string
}

const props = withDefaults(defineProps<Props>(), {
  host: window.location.hostname,
})

const playerUrl = computed(() => {
  if (!props.streamName) {
    return ''
  }

  return `http://${props.host}:8889/${props.streamName}`
})
</script>

<style scoped>
.video-player {
  width: 100%;
  min-height: 420px;
  overflow: hidden;
  background: #111;
  border-radius: 8px;
}

.video-frame {
  display: block;
  width: 100%;
  height: 520px;
  border: 0;
  background: #111;
}
</style>