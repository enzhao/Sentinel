<template>
  <StandardLayout>
    <template #body>
      <v-container fluid>
        <h1 class="text-h4">Dashboard</h1>
        <p>Welcome to your dashboard! More content will be added here soon.</p>
        </v-container>
    </template>
  </StandardLayout>
</template>

<script setup lang="ts">
// 3. Import the layout component
import StandardLayout from '@/components/StandardLayout.vue';

// No other logic is needed!
</script>

<style scoped>
/* Add any specific styles for the dashboard here */
</style>