<template>
  <v-container fluid class="hero-section-container text-center py-12">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-4">{{ title }}</h1>
        <p class="text-subtitle-1 text-md-h6 text-medium-emphasis">{{ subtitle }}</p>
        <v-btn color="primary" size="large" class="mt-8" @click="emit('USER_CLICKS_GET_STARTED')">
          Get Started
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    required: true,
  },
});

const emit = defineEmits<{(event: 'USER_CLICKS_GET_STARTED'): void;}>();
</script>

<style scoped>
.hero-section-container {
  background-color: #e0f2f1; /* Light teal background */
  color: #263238; /* Dark text for contrast */
}
</style>