<template>
  <v-card-actions class="justify-end">
    <v-btn
      v-for="action in actions"
      :key="action.event"
      :color="action.color"
      :loading="loading"
      @click="$emit(action.event)"
    >
      {{ action.label }}
    </v-btn>
  </v-card-actions>
</template>
 
<script setup lang="ts">
// frontend/src/components/FormActions.vue
// A reusable component for form action buttons (e.g., Save, Cancel).
// References: docs/specs/views_spec.yaml (VIEW_USER_SETTINGS)

interface FormAction {
  label: string;
  event: string; // The event name to emit on click
  variant?: 'text' | 'flat' | 'elevated' | 'tonal' | 'outlined' | 'plain';
  color?: string;
}

interface Props {
  actions: FormAction[];
  loading?: boolean;
}

defineProps<Props>();
defineEmits<{
  (event: string): void;
}>();
</script>

<style scoped>
/* Add any specific styling for form actions here if needed */
</style>