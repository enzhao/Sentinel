<template>
  <v-select
    :label="label"
    :items="options"
    :model-value="modelValue"
    @update:modelValue="(value) => $emit('update:modelValue', value)"
    multiple
    chips
    closable-chips
    variant="outlined"
    density="compact"
    class="mb-4"
  ></v-select>
</template>

<script setup lang="ts">
// frontend/src/components/MultiSelect.vue
// A reusable multi-select input field component using Vuetify.
// References: docs/specs/views_spec.yaml (VIEW_USER_SETTINGS)

interface Props {
  label: string;
  options: string[]; // Array of string options
  modelValue: string[]; // Array of selected values
}

defineProps<Props>();
defineEmits(['update:modelValue']);
</script>

<style scoped>
/* Add any specific styling for multi-select fields here if needed */
</style>