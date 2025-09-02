<template>
  <v-container fluid>
    <v-row>
      <!-- Placeholder for the upper part of the dashboard -->
      <v-col cols="12" md="4">
        <v-card class="pa-4" height="100%">
          <v-card-title>Overall Performance</v-card-title>
          <v-card-text>Chart placeholder...</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card class="pa-4" height="100%">
          <v-card-title>Key Metric 1</v-card-title>
          <v-card-text>Number or stat placeholder...</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card class="pa-4" height="100%">
          <v-card-title>Key Metric 2</v-card-title>
          <v-card-text>Number or stat placeholder...</v-card-text>
        </v-card>
      </v-col>

      <!-- Embedded Portfolio List View -->
      <v-col cols="12" class="mt-4">
        <PortfolioListView />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import PortfolioListView from '@/views/PortfoliosListView.vue';
// References:
// - product_spec.md#3.1.2.1 (List Retrieval)
// - docs/specs/views_spec.yaml (VIEW_DASHBOARD)
</script>