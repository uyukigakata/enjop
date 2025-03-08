<template>
    <!-- currentStep == 0 -->
    <div v-if="currentStep === 0">
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
                <button @click="startUpload"
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2">
                    投稿
                </button>
            </div>

            <v-container class="text-center">
                <v-progress-circular v-if="isLoading" indeterminate color="blue" :size=50
                    aria-label="ロード中"></v-progress-circular>
            </v-container>

            <v-dialog v-model="dialog" width="500" class="text-center" transition="dialog-bottom-transition">
                <v-card class="enjo_dialog" :class="ratingClass">
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
    </div>
    <div v-else-if="currentStep === 1">
        <div class="resultView">
            <div class="result min-h-screen" :class="ratingClass">
                <div class="flex items-center justify-center flex-col mt-8 w-full">
                    <img src="./image/enjop_logo.png" alt="logo">
                </div>
                <div class="enjo_rate">
                    <p>炎上レイト：{{ responseMessage.rating }}</p>
                    <p class="text-center text-xl">理由文</p>
                </div>
                <div>
                    <p class="mt-4 ml-4 mr-4 mb-4 p-4 rounded-lg bg-white">{{ responseMessage.comment }}</p>
                    <ul class="justify-center flex flex-wrap flex-col">
                        <li v-for="law in responseMessage.laws" :key="law.law_id" class="w-full mb-4">
                            <div class="m-4 ml-8 mr-8 p-4 border-2 border-gray-300 rounded-lg shadow-md bg-white">
                                <LawItem :law="law" />
                            </div>
                        </li>
                    </ul>
                </div>
                <button class="toConfirmPost" @click="navigateToConfirmPost">投稿する</button>
            </div>
        </div>
    </div>
    <div v-if="currentStep === 2">
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
    </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import type { Response } from '../model/ResponseModel';

import { useTheme } from 'vuetify';



const currentStep = ref(0);

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
            law_id: '1',
            law_name: 'Law Name',
            law_reason: 'This is Reason',
            law_risk_level: 1
        }
    ],
    comment: '解析コメントあいうえお',
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
    console.log("start isLoading", isLoading.value);
    console.log("start dialog", dialog.value)
    //アップロード
    await uploadVideo();
    //終了
    isLoading.value = false;
    //dialogを表示
    dialog.value = true;

    console.log("end isLoading", isLoading.value);
    console.log("end dialog", dialog.value)
};

//動画アップロード
const uploadVideo = async () => {
    if (!videoFile.value) return

    const formData = new FormData()
    formData.append('file', videoFile.value)
    formData.append('content_str', text.value)
    console.log("file", videoFile.value);
    console.log("content_str", text.value)

    try {
        isAnalyzing.value = true
        // デバッグ用に一時的に削除
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
        dialog.value = true;
        console.log("mid isLoading", isLoading.value);
        console.log("mid dialog", dialog.value)

        //router.push({ path: '/result', query: {rating: responseMessage.value.rating } });

        // **JSON.parse時のエラーハンドリング**
        // デバッグ用に一時的に削除
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
    currentStep.value = 1;

    //router.push({ path: '/result', query: {rating: responseMessage.value.rating } });
    /*const lawsJson = JSON.stringify(responseMessage.value.laws);

    router.push({
        path: '/result',
        query: {
            rating: responseMessage.value.rating,
            comment: responseMessage.value.comment,
            laws: lawsJson, // Pass the serialized laws
        },
    });*/
};

const ratingClass = computed(() => {
    return `bg-rate${responseMessage.value.rating}`;
});

import axios from 'axios';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import LawItem from '../components/LawItem.vue';

const route = useRoute();

interface Law {
    law_id: string;
    law_name: string;
    law_reason: string,
    law_risk_level: number
}

const resultMessage = ref<{
    laws: Law[];
    comment: string;
    rating: number;
}>({
    laws: [],
    comment: "データなし",
    rating: 2,
});

onMounted(() => {
    console.log("route.query.laws:", route.query.laws);
    resultMessage.value.rating = Number(route.query.rating) || 2;
    resultMessage.value.comment = String(route.query.comment || "データなし");
    console.log(resultMessage.value.comment);

    if (route.query.laws) {
        try {
            resultMessage.value.laws = JSON.parse(route.query.laws as string);
        } catch (error) {
            console.error("Failed to parse laws:", error);
            resultMessage.value.laws = [];
        }
    }
});

const navigateToConfirmPost = () => {
    currentStep.value = 2;
    // router.push('/confirm-post');
};

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
.postView {
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
    background-color: #9196f8;
    /* ボタンホバー時の色 */
}

.enjo_dialog {
    display: flex;
    flex-direction: row;
    /* Arrange child components horizontally */
    justify-content: space-between;
    /* Distribute space between the components */
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
    background-color: #9196f8;
    /* ボタンホバー時の色 */
}

.cardActions {
    align-items: center;
    justify-content: center;
}

.bg-rate1 {
    background-color: #F5F5F5;
}

.bg-rate2 {
    background-color: #058605;
}

.bg-rate3 {
    background-color: #55d555;
}

.bg-rate4 {
    background-color: #a6f6a6;
}

.bg-rate5 {
    background-color: #bafafa;
}

.bg-rate6 {
    background-color: #fffd30;
}

.bg-rate7 {
    background-color: #FF7466;
}

.bg-rate8 {
    background-color: #EF3223;
}

.bg-rate9 {
    background-color: #8D0A0A;
}

.bg-rate10 {
    background-color: #10000E;
}

.resultView {
    text-align: center;
}

.min-h-screen {
    min-height: 100vh;
    justify-content: center;
    align-items: center;
}

.enjo_rate {
    font-size: 29px;
    background-color: #ffffff;
    padding: 20px;
    max-width: 80%;
    text-align: center;
    margin: 20px auto;
}

.toConfirmPost {
    background-color: #B9BCFC;
    color: black;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 10px;
    width: 120px;
    font-size: 16px;
}

.toConfirmPost:hover {
    background: #4f57ee;
    color: white;
}
</style>