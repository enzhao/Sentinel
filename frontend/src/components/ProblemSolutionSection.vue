<template>
  <v-container fluid class="problem-solution-section py-12 bg-grey-lighten-4">
    <v-row justify="center">
      <v-col cols="12" class="text-center mb-8">
        <h2 class="text-h4 font-weight-bold">{{ title }}</h2>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col v-for="(item, index) in items" :key="index" cols="12" md="4">
        <v-card class="pa-6 text-center h-100" flat>
           <v-icon
            v-if="item.icon"
            size="64"
            :color="item.title.includes('Problem') ? 'error' : 'success'"
            class="mb-4"
            >
            {{ item.icon }}
            </v-icon>
<v-icon v-else size="64" class="mb-4"></v-icon>

          <h3 class="text-h6 font-weight-bold mb-2">{{ item.title }}</h3>
          <p class="text-medium-emphasis">{{ item.description }}</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

interface ProblemSolutionItem {
  icon: string;
  title: string;
  description: string;
}

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => ProblemSolutionItem[],
    required: true,
  },
});
</script>

<style scoped>
.problem-solution-section {
  /* Specific styles if needed */
}
</style>
