<template>
  <section>
    <div class="page-header">
      <div>
        <h1>Dashboard</h1>
        <p>OpenEdge Vision 平台运行概览</p>
      </div>

      <el-tag type="success" effect="dark"> Platform Online </el-tag>
    </div>

    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="metric-label">在线视频流</div>
          <div class="metric-value">2</div>
          <div class="metric-note">drone01 / park01</div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="metric-label">运行任务</div>
          <div class="metric-value">0</div>
          <div class="metric-note">AI任务将在后续开放</div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="metric-label">今日事件</div>
          <div class="metric-value">0</div>
          <div class="metric-note">事件中心尚未启用</div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="metric-label">平台版本</div>
          <div class="metric-value version">V0.1</div>
          <div class="metric-note">Sprint 2 Demo</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="content-card" shadow="never">
      <template #header>
        <strong>视频预览区域</strong>
      </template>

      <el-empty description="Day 4 接入双视频预览" />
    </el-card>
  </section>
</template>

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

.metric-label {
  color: #64748b;
  font-size: 14px;
}

.metric-value {
  margin: 16px 0 8px;
  color: #1d4ed8;
  font-size: 34px;
  font-weight: 700;
}

.metric-value.version {
  font-size: 28px;
}

.metric-note {
  color: #94a3b8;
  font-size: 12px;
}

.content-card {
  margin-top: 20px;
  min-height: 330px;
}
</style>
