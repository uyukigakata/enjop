<template>
  <div class="postView">
    <div class="flex items-center justify-center flex-col mt-8">
      <p>1. テキストを入力</p>
      <textarea v-model="text"
        class="mt-2 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
        style="height: 80px;"></textarea>
      <div class="fileupload">
        <p class="mt-4">2. 動画ファイルをここにアップロード</p>
        <input type="file" @change="onChooseFile"
        class="mt-2 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400" />
      </div>
      <button @click="startUpload" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2">
        投稿
      </button>
    </div>
  </div>

    <LoadView v-if="isLoading" />
    <v-dialog  v-model="dialog" width="500">
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          解析結果
        </v-card-title>

        <v-card-text>
          <p>{{ responseMessage.comment }}</p>
          <p>リスク評価: {{ responseMessage.rating }}</p>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" @click="navigateToResult" >
            詳しく見る
          </v-btn>
          <v-btn color="grey" @click="dialog = false">
            閉じる
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  
</template>

<script setup lang="ts">
import { ref,computed } from 'vue';
import axios from 'axios'
import { useRouter } from 'vue-router';
import type { Response } from '../model/ResponseModel'
import LoadView from './LoadView.vue';


const router = useRouter();

//loading用のフラグ
const isLoading = ref(false);
//dialog用のフラグ
const dialog = ref(false);

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


const onChooseFile = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0] || null;
  videoFile.value = file;
};

const startUpload = async () => {
  //ロード開始
  isLoading.value = true;
  //アップロード
  await uploadVideo();
  //終了
  isLoading.value = false;
  //dialogを表示
  dialog.value=true;
};

//動画アップロード
const uploadVideo = async () => {
  if (!videoFile.value) return

  const formData = new FormData()
  formData.append('file', videoFile.value)
  formData.append('content_str', text.value)

  try {
    const response = await axios.post('/api/process_video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // リスク取得
    const risk_text = response.data.openai_risk_assessment as string
    console.log("rist_text!!!!!!!!!!!!")
    console.log(risk_text)

    //const risk_text_cleaned = risk_text.slice(7, risk_text.length - 3).replace(/\\n/g, '')
    const risk_text_cleaned = risk_text.replace(/\\n/g, ''); // 改行コードを削除するだけ
    responseMessage.value = JSON.parse(risk_text_cleaned)
    console.log("responseMessage.value!!!!!!!!!!!!")
    console.log(responseMessage.value)
    //dialog表示
    dialog.value = true;
    
    //router.push({ path: '/result', query: {rating: responseMessage.value.rating } });


  } catch (error) {
    console.error(error)
    responseMessage.value = {
      laws: [],
      comment: 'An error occurred while processing the video',
      rating: 0
    }
  }
}

const navigateToResult = () => {
  //router.push({ path: '/result', query: {rating: responseMessage.value.rating } });
  const lawsJson = JSON.stringify(responseMessage.value.laws);

  router.push({
    path: '/result',
    query: {
      rating: responseMessage.value.rating,
      comment: responseMessage.value.comment,
      laws: lawsJson, // Pass the serialized laws
    },
  });
};


</script>

<style scoped>
.postView{
  text-align: center;
}

button {
  background-color: #B9BCFC;
  border: none;
  color: white;
  font-size: 16px;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
  width: 120px;
}

button:hover {
  background-color: #9196f8; /* ボタンホバー時の色 */
}

</style>