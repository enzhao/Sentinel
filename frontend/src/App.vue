<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppBar from '@/components/AppBar.vue'
</script>

<template>
  <v-app>
    <AppBar />
    <v-main>
      <v-container fluid>
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>

<style>
/* You can add global styles here if needed */
</style>