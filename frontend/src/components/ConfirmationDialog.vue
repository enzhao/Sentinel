<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" persistent max-width="500px">
    <v-card>
      <v-card-title class="text-h5">{{ title }}</v-card-title>
      <v-card-text>
        <p>{{ message }}</p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="$emit('cancel')">Cancel</v-btn>
        <v-btn :color="confirmColor" :loading="loading" @click="$emit('confirm')">
          {{ confirmText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
// This is a generic, reusable confirmation dialog component.
// It can be used for any action that requires user confirmation, like deletion.

defineProps({
  modelValue: { type: Boolean, required: true },
  title: { type: String, required: true },
  message: { type: String, required: true },
  loading: { type: Boolean, default: false },
  confirmText: { type: String, default: 'Confirm' },
  confirmColor: { type: String, default: 'error' },
});

defineEmits(['update:modelValue', 'confirm', 'cancel']);
</script>