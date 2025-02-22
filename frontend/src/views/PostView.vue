<template>
  <div>
    <h1>投稿画面</h1>
    <textarea v-model="text" placeholder="テキストを入力"></textarea>
    <input type="file" @change="onChooseFile" />
    <button @click="uploadVideo">動画を解析</button>
    <button @click="navigateToResult">結果へ</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const text = ref('');
const videoFile = ref<File | null>(null);

const onChooseFile = (e: Event) => {
  const target = e.target as HTMLInputElement;
  videoFile.value = target.files?.[0] || null;
};

const uploadVideo = () => {
  // 動画アップロードの処理
};

const navigateToResult = () => {
  router.push('/result');
};
</script>

<style scoped>
/* 必要に応じてスタイルを追加 */
</style>
