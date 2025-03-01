<template>
  <div class="enjo_kanki_block">
    <h2>このまま投稿すると</h2>
    <div class="flex items-center justify-center flex-col mt-8">
      <img src="./image/enjo_kanki.png" alt="enjo_kanki">
    </div>
    <p class="finalCheck">本当に投稿しますか？</p>
    <div class="btnbox">
      <button class="noPostbtn" @click="notpostToBlueSky">投稿しない</button>
      <button class="yesPostbtn" @click="postToBlueSkyWithVideo">投稿する</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Vuexからのテキストの取得
const text = ref();
// Vuexからのファイルの取得
const videoFile = ref();


const notpostToBlueSky = () => {
  // 最初の画面に戻る
  router.push('/');
};

async function postToBlueSkyWithVideo() {
  if (!videoFile.value) return

  const formData = new FormData()
  formData.append('text', text.value)
  formData.append('video', videoFile.value)
  console.log("confirm text", text.value)
  console.log("confirm videoFile", videoFile.value)

  try {
    const response = await axios.post('/api/bluesky_post_video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log(response.data)
    alert('動画をBlueskyに投稿しました')
  } catch (error) {
    console.error(error)
  }

  // 投稿処理を行う
  router.push('/post-complete');
}
</script>

<style scoped>
html,
body {
  background-color: #F8F8F8;
  /* 背景色を全体に適用 */
  margin: 0;
  padding: 0;
  height: 100%;
}

.enjo_kanki_block {
  padding: 20px;
  font-size: 29px;
  text-align: center;
}

.finalCheck {
  padding: 20px;
  color: red;
  text-align: center;
}

.noPostbtn,
.yesPostbtn {
  color: #ffffff;
  border: none;
  font-size: 20px;
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

.btnbox {
  display: flex;
  flex-direction: column;
  /* ボタンを縦並びにする */
  align-items: center;
  /* 中央寄せ */
  gap: 10px;
  /* ボタン同士の間隔をあける */
  margin-top: 20px;
  /* 上に余白をつける */
}
</style>
