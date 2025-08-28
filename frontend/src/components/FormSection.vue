<template>
  <v-card class="mb-4">
    <v-card-title v-if="title">{{ title }}</v-card-title>
    <v-card-text>
      <slot></slot>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
// frontend/src/components/FormSection.vue
// A reusable component to group form fields into logical sections.
// References: docs/specs/views_spec.yaml (VIEW_USER_SETTINGS)

interface Props {
  title?: string;
}

defineProps<Props>();
</script>

<style scoped>
/* Add any specific styling for form sections here if needed */
</style>