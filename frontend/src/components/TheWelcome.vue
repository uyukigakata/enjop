<script setup lang="ts">
</script>

<template>
  <div class="spacer"></div>

  <v-card color="" variant="elevated" class="mx-auto">
    <v-card-item>
      <div>
        <div class="text-overline mb-1">
          Welcome
        </div>
        <div class="text-h6 mb-1">
          このサイトについて
        </div>
        <div class="text-caption">このサイトは動画をアップロードすることで炎上しそうかどうかを判定するサイトです。</div>
      </div>
    </v-card-item>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn onclick="location.href='/upload'" color="primary">
        使ってみる
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<style scoped>
.spacer {
  margin-top: 30px;
}
</style>