<template>
  <div class="home_block1">
    <img src="./image/enjop_title.png" alt="title">
    <img src="./image/enjop_logo.png" alt="logo">
  </div>
  <div class="home_block2">
    <img src="./image/enjop_chart.png" alt="chart">
    <p>このサイトは投稿内容をチェックし、炎上するか判定を行いユーザーの未来をシミュレーションします。</p>
  </div>
  <div class="home_block3">
    <img src="./image/bluesky_logo.png" alt="bluesky_logo">
    <p>このサイトでは、実際にBlueSkyで投稿することができます</p>
  </div>
  <div class="home_block4">
    <img src="./image/post.png" alt="bluesky_logo">
    <button @click="navigateToPost">投稿画面へ</button>
  </div>

</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateToPost = () => {
  router.push('/analyze');
};
</script>


<style scoped>
.home_block1 {
  background-color: #EDFFFD;
  padding: 20px;
  text-align: center;
}

.home_block2 {
  background-color: #BAFAFA;
  padding: 20px;
  text-align: center;
}

.home_block3 {
  background-color: #EDFFFD;
  padding: 20px;
  text-align: center;
}

.home_block4 {
  background-color: #BAFAFA;
  padding: 20px;
  text-align: center;
}

.home_block4 button {
  background-color: #B9BCFC;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

.home_block4 button:hover {
  background-color: #787eef;
  /* ホバー時の色 */
}
</style>