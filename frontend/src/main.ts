/*import './assets/base.css'

import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
*/

import { createApp, defineAsyncComponent } from 'vue';
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import vuetify from './plugins/vuetify';
import App from './App.vue';

// ルーティングの設定 (型を明示)
const routes: RouteRecordRaw[] = [
    { path: '/', component: () => import('./views/HomeView.vue') },
    { path: '/post', component: () => import('./views/PostView.vue') },
    { path: '/loading', component: () => import('./views/LoadView.vue') },
    { path: '/result', component: () => import('./views/ResultView.vue') },
    { path: '/confirm-post', component: () => import('./views/ConfirmPostView.vue') },
    { path: '/post-complete', component: () => import('./views/PostCompleteView.vue') },
  ];
  

// ルーターの作成
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// アプリケーションの作成
const app = createApp(App); 

// ルーターをアプリに登録
app.use(router as any);

// アプリをマウント
app.use(vuetify).mount('#app');

/*
import { createApp } from 'vue';
import PostCompleteView from './views/PostCompleteView.vue';

const app = createApp(PostCompleteView);
app.mount('#app');
*/