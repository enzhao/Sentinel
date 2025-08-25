<template>
  <v-container class="key-features-section py-12">
    <v-row justify="center">
      <v-col cols="12" class="text-center mb-8">
        <h2 class="text-h4 font-weight-bold">Key Features</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="(feature, index) in features" :key="index" cols="12" md="4">
        <v-card class="pa-6 text-center h-100" flat>
          <v-icon size="64" color="primary" class="mb-4">{{ feature.icon }}</v-icon>
          <h3 class="text-h6 font-weight-bold mb-2">{{ feature.title }}</h3>
          <p class="text-medium-emphasis">{{ feature.description }}</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

interface Feature {
  icon: string;
  title: string;
  description: string;
}

const props = defineProps({
  features: {
    type: Array as () => Feature[],
    required: true,
  },
});
</script>

<style scoped>
.key-features-section {
  background-color: #ffffff; /* White background */
}
</style>
