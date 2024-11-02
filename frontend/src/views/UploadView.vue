<script setup lang="ts">
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const onFileChange = (e: any) => {
    const file = e.target.files[0]
    const reader = new FileReader()

    reader.onload = (e: any) => {
        const video = e.target.result
        store.dispatch('uploadVideo', { video })
        router.push('/upload')
    }

    reader.readAsDataURL(file)
}

</script>

<template>
    <div>
        <h2 class="text-h2">動画をアップロード</h2>

        <input type="file" @change="onFileChange" />

        <v-btn @click="router.push('/upload')" variant="elevated">アップロード</v-btn>

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