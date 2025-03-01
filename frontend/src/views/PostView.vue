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
    
      <v-container class="text-center" >
        <v-progress-circular
          v-if="isLoading"
          indeterminate
          color="blue"
          :size =50
          aria-label="ロード中"
        ></v-progress-circular>
      </v-container>

      <v-dialog v-model="dialog" width="500" class="text-center" transition="dialog-bottom-transition" >
        <v-card class="enjo_dialog" :class="ratingClass" >
          <v-card-text>
            <p class="dialog_kanki">ちょっと待って! この動画、炎上するかも...</p>
            <p>リスク評価: {{ responseMessage.rating }}</p>
          </v-card-text>
          <v-divider></v-divider>

          <v-card-actions class="cardActions">
            <v-spacer></v-spacer>
            <img src="./image/enjop_logo.png" height="90" alt="logo">
            <v-btn color="blue darken-1" @click="navigateToResult">
              詳しく見る
            </v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
    

    
</div>
</template>

<script setup lang="ts">
import { ref,computed } from 'vue';
import axios from 'axios'
import { useRouter } from 'vue-router';
import type { Response } from '../model/ResponseModel'
import LoadView from './LoadView.vue';
import { nextTick } from 'vue';

import { useTheme } from 'vuetify';


const theme = useTheme();

const router = useRouter();

//loading用のフラグ
const isLoading = ref(false);

//dialog用のフラグ
const dialog = ref(false);

const isAnalyzing = ref(false)

const text = ref('');

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
  console.log("start isLoading",isLoading.value);
  console.log("start dialog",dialog.value)
  //アップロード
  await uploadVideo();
  //終了
  isLoading.value = false;
  //dialogを表示
  dialog.value=true;

  console.log("end isLoading",isLoading.value);
  console.log("end dialog",dialog.value)
};

//動画アップロード
const uploadVideo = async () => {
  if (!videoFile.value) return

  const formData = new FormData()
  formData.append('file', videoFile.value)
  formData.append('content_str', text.value)
  console.log("file",videoFile.value);
  console.log("content_str",text.value)

  try {
    isAnalyzing.value = true
    const response = await axios.post('/api/process_video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    isAnalyzing.value = false
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
    isLoading.value = false;
    //dialogを表示
    dialog.value=true;
    console.log("mid isLoading",isLoading.value);
    console.log("mid dialog",dialog.value)
    
    //router.push({ path: '/result', query: {rating: responseMessage.value.rating } });

    // **JSON.parse時のエラーハンドリング**
    try {
      const parsedData = JSON.parse(risk_text_cleaned);

      // `laws` が null の場合は空配列を代入
      if (!parsedData.laws) {
        parsedData.laws = [];
      }

      // **laws内の各オブジェクトにデフォルト値を設定**
      parsedData.laws = parsedData.laws.map((law: any) => ({
      law_id: law.law_id ?? "N/A", // law_id がなければ "N/A"
      law_name: law.law_name ?? "不明な法律", // law_name がなければ "不明な法律"
      law_reason: law.law_reason ?? "理由なし", // law_reason がなければ "理由なし"
      law_risk_level: law.law_risk_level ?? 0 // law_risk_level がなければ 0
    }));

      responseMessage.value = parsedData;
    } catch (jsonError) {
      console.error("JSON parse error:", jsonError);
      responseMessage.value = {
        laws: [],
        comment: "解析結果を処理できませんでした",
        rating: 0
      };
    }


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

const ratingClass = computed(() => {
  return `bg-rate${responseMessage.value.rating}`;
});

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

.enjo_dialog {
  display: flex;
  flex-direction: row; /* Arrange child components horizontally */
  justify-content: space-between; /* Distribute space between the components */
  align-items: center;
}

.dialog_kanki {
  font-size: 20px;
  text-align: center;
}

v-dialog {
  margin-top: 80px;
  text-align: center;
  display: flex;
  justify-content: center;
}

v-btn {
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

.cardActions {
  align-items: center;
  justify-content: center;
}

.bg-rate1 { background-color: #F5F5F5; }
.bg-rate2 { background-color: #55D555; }
.bg-rate3 { background-color: #DBF6AF; }
.bg-rate4 { background-color: #FDF9B4; }
.bg-rate5 { background-color: #FF914D; }
.bg-rate6 { background-color: #FF66C4; }
.bg-rate7 { background-color: #FF7466; }
.bg-rate8 { background-color: #EF3223; }
.bg-rate9 { background-color: #8D0A0A; }
.bg-rate10 { background-color: #10000E; }



</style>