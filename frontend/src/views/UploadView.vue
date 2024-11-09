
<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const file = ref<File | null>(null) // ファイルの状態を管理

// ファイル選択時に呼び出される関数
const onFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    if (target && target.files && target.files.length > 0) {
        file.value = target.files[0] // ファイルを設定
    }
}

// アップロード関数
const uploadVideo = async () => {
    if (!file.value) {
        alert("ファイルが選択されていません")
        return
    }

    // FormDataを使用してファイルを送信
    const formData = new FormData()
    formData.append("file", file.value)

    try {
        // axiosでバックエンドのエンドポイントにファイルをPOST
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/process_video`, formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        })
        console.log("アップロード成功:", response.data)
        alert("動画が正常にアップロードされました。")

    } catch (error) {
        console.error("アップロードエラー:", error)
        alert("動画のアップロードに失敗しました。")
    }
}
</script>

<template>
    <div>
        <h4 class="text-h4">動画をアップロード</h4>

        <input type="file" @change="onFileChange" />

        <v-btn @click="uploadVideo" variant="elevated">アップロード</v-btn>
    </div>
</template>

<style>
@media (min-width: 1024px) {
    .about {
        min-height: 100vh;
        display: flex;
        align-items: center;
    }
}
</style>
