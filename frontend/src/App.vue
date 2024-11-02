<script setup lang="ts">
import { RouterView } from 'vue-router'
import Footer from './components/Footer.vue'
</script>

<template>
  <header>
    <v-toolbar color="#FFF" dark="true">
      <v-toolbar-title class="top-logo">SecHack 365</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
    </v-toolbar>
    <v-toolbar color="primary" dark="true">
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>炎上チェッカー</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
  </header>

  <main>
    <RouterView />
  </main>

  <footer>
    <Footer></Footer>
  </footer>

</template>

<style scoped>
.top-logo {
  margin-left: 72px;
  height: fit-content;
}
</style>
