<template>
    <div class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
      <div class="flex flex-col items-center">
        <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
        <p class="mt-4 text-white">処理中...</p>
      </div>
    </div>
  </template>
  
  <style scoped>
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  
  .spinner {
    border: 5px solid rgba(0, 0, 0, 0.1);
    border-left-color: #09f;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    100% {
      transform: rotate(360deg);
    }
  }
  </style>
  