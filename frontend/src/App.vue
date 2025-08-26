<template>
  <v-app>
    <div v-if="authStore.loading" class="loading-container">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>

    <RouterView v-else />
  </v-app>
</template>

<script setup lang="ts">
// The script is now much simpler
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
// The onMounted hook is no longer needed here
</script>

<style>
/* You can add global styles here if needed */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>

