<script setup lang="ts">
import type { Law } from '@/model/ResponseModel';

defineProps<{
  law: Law
}>()

</script>

<template>
  <div class="max-w-sm rounded overflow-hidden shadow-lg m-5">
    <div class="px-6 py-2">
      <div class="font-bold text-lg">{{ law.law_name ?? "不明な法律" }} ({{ law.law_id ?? "N/A"}})</div>
      <p class="text-gray-700 text-base">{{ law.law_reason ?? "理由なし" }}</p>
    </div>
    <div class="px-6">
      <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">{{
        law.law_risk_level ?? 0}}
      </span>
    </div>
  </div>
</template>

<style scoped>
.v-card {
  margin: 20px;
}
</style>
