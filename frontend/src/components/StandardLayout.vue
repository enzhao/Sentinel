<template>
  <v-app>
    <v-main>
      <slot name="header"></slot>
      <v-container fluid>
        <slot name="body"></slot>
      </v-container>
      <slot name="fab"></slot>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
// No specific script logic needed for a basic layout component
</script>

<style scoped>
/* Add any specific styles for the layout here */
</style>