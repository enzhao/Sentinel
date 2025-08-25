<template>
  <v-container class="target-audience-section py-12">
    <v-row justify="center">
      <v-col cols="12" class="text-center mb-8">
        <h2 class="text-h4 font-weight-bold">{{ title }}</h2>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card class="pa-6 h-100" flat>
          <h3 class="text-h6 font-weight-bold mb-4 text-success">{{ goodFit.title }}</h3>
          <v-list density="compact">
            <v-list-item v-for="(item, index) in goodFit.items" :key="index">
              <template v-slot:prepend>
                <v-icon color="success">mdi-check</v-icon>
              </template>
              <v-list-item-title>{{ item }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card class="pa-6 h-100" flat>
          <h3 class="text-h6 font-weight-bold mb-4 text-error">{{ badFit.title }}</h3>
          <v-list density="compact">
            <v-list-item v-for="(item, index) in badFit.items" :key="index">
              <template v-slot:prepend>
                <v-icon color="error">mdi-close</v-icon>
              </template>
              <v-list-item-title>{{ item }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

interface AudienceList {
  title: string;
  items: string[];
}

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  goodFit: {
    type: Object as () => AudienceList,
    required: true,
  },
  badFit: {
    type: Object as () => AudienceList,
    required: true,
  },
});
</script>

<style scoped>
.target-audience-section {
  background-color: #f5f5f5; /* Light grey background */
}
</style>