<template>
    <div>
      <img src="./image/enjop_logo.png" alt="logo">
      <button @click="navigateToConfirmPost">投稿する</button>
    </div>
    <div class="enjo_rate">
        <p>炎上レイト</p>
    </div>

  </template>
  
  <script setup lang="ts">
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const navigateToConfirmPost = () => {
    router.push('/confirm-post');
  };
  </script>
  
  <style scoped>
  /* 必要に応じてスタイルを追加 */
  </style>
  