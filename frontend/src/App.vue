
<!--<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import FooterItem from './components/FooterItem.vue'
import HeaderItem from './components/HeaderItem.vue'
import LawItem from './components/LawItem.vue'
import type { Response } from './model/ResponseModel'

const isAnalyzing = ref(false)

const text = ref('')

const videoFile = ref<File | null>(null)
const responseMessage = ref<Response>({
  laws: [
    {
      law_id: '0',
      law_name: 'Law Name',
      law_reason: 'This is Reason',
      law_risk_level: 0
    },
    {
      law_id: '0',
      law_name: 'Law Name',
      law_reason: 'This is Reason',
      law_risk_level: 0
    }
  ],
  comment: '解析コメント',
  rating: 0
})

const uploadVideo = async () => {
  if (!videoFile.value) return

  const formData = new FormData()
  formData.append('file', videoFile.value)
  formData.append('content_str', text.value)

  try {
    isAnalyzing.value = true
    const response = await axios.post('/api/process_video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    isAnalyzing.value = false
    const risk_text = response.data.openai_risk_assessment as string
    console.log(risk_text)

    // remove ```json and ``` from the string
    const risk_text_cleaned = risk_text.slice(7, risk_text.length - 3).replace(/\\n/g, '')
    console.log(risk_text_cleaned)
    responseMessage.value = JSON.parse(risk_text_cleaned)



  } catch (error) {
    console.error(error)
    responseMessage.value = {
      laws: [],
      comment: 'An error occurred while processing the video',
      rating: 0
    }
  }
}

function onChooseFile(e: Event) {
  const target = e.target as HTMLInputElement
  videoFile.value = target.files?.[0] || null
}

function submitText() {
  const tweetText = encodeURIComponent(text.value)
  const tweetUrl = `https://x.com/intent/tweet?text=${tweetText}`
  window.open(tweetUrl, '_blank')
}

async function postToBlueSkyWithVideo() {
  if (!videoFile.value) return

  const formData = new FormData()
  formData.append('text', text.value)
  formData.append('video', videoFile.value)

  try {
    const response = await axios.post('/bluesky_post_video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log(response.data)
    alert('動画をBlueskyに投稿しました')
  } catch (error) {
    console.error(error)
  }
}

</script>

<template>

  <HeaderItem />

  <div class="flex items-center justify-center flex-col mt-8">


    <p>1. テキストを入力</p>
    <textarea v-model="text"
      class="mt-2 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
      style="height: 80px;"></textarea>

    <p class="mt-4">2. 動画ファイルをここにアップロード</p>
    <input type="file" @change="onChooseFile"
      class="mt-2 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400" />
    <p class="mt-8">3. 動画を解析ボタンを押す</p>
    <button @click="uploadVideo" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2">
      動画を解析
    </button>

    <div v-if="isAnalyzing" class="mt-8">
      <p>解析中...</p>
    </div>

    <div class="mt-8 border-2 border-gray-300 p-4 mx-4 my-4">
      <p class="text-center text-xl">解析結果</p>
      <p class="mt-4">{{ responseMessage.comment }}</p>
      <p>炎上しそう度合い: {{ responseMessage.rating }}</p>
      <ul class="justify-center flex flex-wrap flex-col">
        <li v-for="law in responseMessage.laws" :key="law.law_id">
          <LawItem :law="law" />
        </li>
      </ul>
    </div>

    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2" @click="submitText">
      Xに投稿
    </button>

    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2"
      @click="postToBlueSkyWithVideo">
      動画付きでBlueskyに投稿
    </button>

  </div>


  <div class="flex items-center justify-center flex-col my-8">
    <FooterItem />
  </div>
</template>
-->


<template>
  <router-view></router-view>
</template>

<script setup lang="ts">
</script>