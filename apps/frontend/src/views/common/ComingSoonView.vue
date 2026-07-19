<template>
  <el-card class="coming-card" shadow="never">
    <el-empty>
      <template #description>
        <h2>{{ title }}</h2>
        <p>{{ description }}</p>
        <el-tag type="info">Planned for V0.2+</el-tag>
      </template>
    </el-empty>
  </el-card>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()
</script>

<style scoped>
.coming-card {
  min-height: 620px;
  display: flex;
  align-items: center;
  justify-content: center;
}

h2 {
  margin: 0 0 12px;
  color: #1e293b;
}

p {
  margin: 0 0 18px;
  color: #94a3b8;
}
</style>
