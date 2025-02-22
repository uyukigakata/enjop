<template>
    <div class="enjo_kanki_block">
      <h2>このまま投稿すると</h2>
      <img src="./image/enjo_kanki.png" alt="enjo_kanki">
      <p>本当に投稿しますか？</p>
      <button class="noPostbtn" @click="submitPost">投稿しない</button>
      <button class="yesPostbtn" @click="submitPost">投稿する</button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const submitPost = () => {
    // 投稿処理を行う
    router.push('/post-complete');
  };
  </script>
  
<style scoped>
html, body {
background-color: #F8F8F8; /* 背景色を全体に適用 */
margin: 0;
padding: 0;
height: 100%;
}
.enjo_kanki_block{
padding: 20px;
text-align: center;
}

.noPostbtn, .yesPostbtn {
  color: #FFF;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

.noPostbtn {
  background: #BBDFEE; 
}
.noPostbtn:hover {
  background: #4ec4f7; 
}

.yesPostbtn {
  background: rgb(249, 120, 120); 
}
.yesPostbtn:hover {
  background: red; 
}

</style>
