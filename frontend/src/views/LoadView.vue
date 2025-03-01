<template>
  <v-container class="text-center">
    <v-progress-circular
      indeterminate
      color="blue"
      size="64"
    ></v-progress-circular>
    <p class="mt-4 text-black text-h6">
      現在のテーマ: {{ theme.global.name.value }}
    </p>
    <v-btn @click="toggleTheme">テーマ切り替え</v-btn>
  </v-container>
</template>

<script setup lang="ts">
  import { useTheme } from 'vuetify';

  const theme = useTheme();

  const toggleTheme = () => {
    theme.global.name.value = theme.global.name.value === 'light' ? 'dark' : 'light';
  };
</script>
