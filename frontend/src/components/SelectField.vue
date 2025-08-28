<template>
  <v-select
    :label="label"
    :items="items"
    :item-title="itemTitle"
    :item-value="itemValue"
    :model-value="modelValue"
    @update:modelValue="(value) => $emit('update:modelValue', value)"
    variant="outlined"
    density="compact"
    class="mb-4"
  ></v-select>
</template>

<script setup lang="ts">
// frontend/src/components/SelectField.vue
// A reusable select input field component using Vuetify.
// References: docs/specs/views_spec.yaml (VIEW_USER_SETTINGS)

interface Props {
  label: string;
  items: any[];
  itemTitle?: string; // Property to use for item text (e.g., 'name')
  itemValue?: string; // Property to use for item value (e.g., 'portfolioId')
  modelValue: any; // The currently selected value
}

defineProps<Props>();
defineEmits(['update:modelValue']);
</script>

<style scoped>
/* Add any specific styling for select fields here if needed */
</style>