<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

type AnalysisResult = {
  high_risk_frames: string[];
  openai_risk_assessment: string;
  image_urls:string;
};

const results = ref(null as AnalysisResult | null);

const handleFileUpload = async (e: Event) => {
  const target = (<HTMLInputElement>e.target)
  if (!target.files) {
    return;
  }
  const file = target.files[0];
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`/api/process_video`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.data.error) {
      alert(response.data.error);
      return;
    }

    const docId = response.data.doc_id;

    const analysisResponse = await axios.get(`/api/analyze_images/${docId}`);
    results.value = analysisResponse.data;
  } catch (error) {
    console.error(error);
    // エラー処理
  }
};
</script>


<template>
  <div>
    <h4 class="text-h3 mt-8">炎上検知デモ</h4>

    <input type="file" @change="handleFileUpload" class="mt-6" />
    <div v-if="results">
      <h4 class="text-h4 mt-8">分析結果</h4>

      <!-- 画像表示 -->
      <h3 class="mt-4">読み取った画像:</h3>
      <div v-for="(url, index) in results.image_urls" :key="index" class="image-container">
        <img :src="url" :alt="'Image ' + (index + 1)" style="width: 200px; height: auto;" />
      </div>

      <!-- 高リスクフレーム -->
      <h3 class="mt-4">高リスクフレーム:</h3>
      <div v-for="result in results.high_risk_frames" :key="result">
        <p>{{ result }}において炎上リスクが高いコンテンツが検出されました。</p>
      </div>

      <!-- 総合的な炎上リスク評価 -->
      <h3 class="mt-4">総合的な炎上リスク評価:</h3>
      <p>{{ results.openai_risk_assessment }}</p>
    </div>
  </div>
</template>


<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
