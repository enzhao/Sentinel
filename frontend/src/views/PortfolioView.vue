<template>
  <div class="portfolio">
    <h1>Your Portfolio</h1>
    <p v-if="isPortfolioEmpty">Your portfolio is empty, you can start to add holdings.</p>
    <p v-else>Your portfolio is great.</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// This is a placeholder. In the future, this will come from a portfolio store.
const isPortfolioEmpty = ref(true)
</script>

<style scoped>
.portfolio {
  text-align: center;
  margin-top: 50px;
}
</style>
