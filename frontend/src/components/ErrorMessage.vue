<template>
  <v-alert
    v-if="message"
    type="error"
    dense
    text
    class="my-4"
  >
    {{ message }}
  </v-alert>
</template>

<script setup lang="ts">
// frontend/src/components/ErrorMessage.vue
// A generic component to display error messages.
// References: product_spec.md Section 10.3 (Error Handling and Messaging)
interface Props {
  message: string | null;
}

defineProps<Props>();
</script>

<style scoped>
/* Add any specific styling for error messages here if needed */
</style>