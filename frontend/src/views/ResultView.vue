<template>
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
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import LawItem from '../components/LawItem.vue';

const router = useRouter();
const route = useRoute();

interface Law {
  law_id: string;
  law_name: string;
  law_reason: string,
  law_risk_level: number
}

const responseMessage = ref<{
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
  responseMessage.value.rating = Number(route.query.rating) || 2;
  responseMessage.value.comment =  String(route.query.comment || "データなし");
  console.log(responseMessage.value.comment);
  
  if (route.query.laws) {
    try {
      responseMessage.value.laws = JSON.parse(route.query.laws as string);
    } catch (error) {
      console.error("Failed to parse laws:", error);
      responseMessage.value.laws = [];
    }
  }
});

const ratingClass = computed(() => {
  return `bg-rate${responseMessage.value.rating}`;
});

const navigateToConfirmPost = () => {
  router.push('/confirm-post');
};
</script>

<style scoped>
.resultView{
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
