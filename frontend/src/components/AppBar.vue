<template>
  <v-app-bar app>
    <v-app-bar-nav-icon v-if="leadingAction" @click="emit(leadingAction.event)">
      <v-icon>{{ leadingAction.icon }}</v-icon>
    </v-app-bar-nav-icon>
    <v-app-bar-title>{{ title }}</v-app-bar-title>
    <v-spacer></v-spacer>
    <v-btn v-for="action in actions" :key="action.label" text @click="emit(action.event)">
      {{ action.label }}
    </v-btn>
    <v-btn v-if="alertAction" icon @click="emit(alertAction.event)">
      <v-badge v-if="alertAction.bindings.badgeVisible" color="red" dot overlap>
        <v-icon>{{ alertAction.icon }}</v-icon>
      </v-badge>
      <v-icon v-else>{{ alertAction.icon }}</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

interface Action {
  label?: string;
  icon?: string;
  event: string;
}

interface AlertAction extends Action {
  bindings: {
    badgeVisible: boolean;
  };
}

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  leadingAction: {
    type: Object as () => Action,
    default: null,
  },
  actions: {
    type: Array as () => Action[],
    default: () => [],
  },
  alertAction: {
    type: Object as () => AlertAction,
    default: null,
  },
});

const emit = defineEmits<{(event: string): void;}>();
</script>

<style scoped>
/* Add any specific styles for the app bar here */
</style>