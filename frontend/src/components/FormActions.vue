<template>
  <!--
    Using a generic div with flex utilities instead of v-card-actions.
    This makes the component more reusable and semantically correct when used
    outside of a v-card, such as within a v-footer.
  -->
  <div class="d-flex justify-end pa-2" style="width: 100%;">
    <v-btn
      v-for="action in actions"
      :id="action.id"
      :key="action.event"
      :color="action.color"
      :loading="loading"
      :variant="action.variant"
      @click="$emit(action.event)"
    >
      {{ action.label }}
    </v-btn>
  </div>
</template>
 
<script setup lang="ts">
// frontend/src/components/FormActions.vue
// A reusable component for form action buttons (e.g., Save, Cancel).
// References: docs/specs/views_spec.yaml (VIEW_USER_SETTINGS)

interface FormAction {
  id?: string;
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