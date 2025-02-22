<template>
    <div class="container">
      <div class="post_complete">
        <h1>投稿完了！！</h1>
        <div class="button_group">
          <button class="toHomebtn" @click="navigateHome">ホーム画面</button>
          <button class="toPostbtn" @click="navigatePost">投稿画面</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const navigateHome = () => {
    router.push('/');
  };
  
  const navigatePost = () => {
    router.push('/post');
  };
  </script>
  
  <style scoped>
  html, body {
    background-color: #EDFFFD; 
    margin: 0;
    padding: 0;
    height: 100%;
  }
  
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* 画面の高さいっぱい */
  }
  
  /*投稿完了エリア*/
  .post_complete {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 10px; 
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* 影 */
    text-align: center;
    width: 300px;
  }
  
  /* ボタン横並び */
  .button_group {
    display: flex;
    justify-content: center;
    gap: 15px; /* 余白 */
  }
  
  .toHomebtn, .toPostbtn {
    background-color: #adb1fc;
    color: black;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
    width: 120px;
    font-size: 16px;
  }
  
  .toHomebtn:hover, .toPostbtn:hover {
    background: #4f57ee;
    color: white;
  }
  </style>
  