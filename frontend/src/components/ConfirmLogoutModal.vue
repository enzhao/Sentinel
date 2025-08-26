<template>
  <v-dialog v-model="dialog" persistent max-width="400px">
    <v-card>
      <v-card-title class="text-h5">Confirm Logout</v-card-title>
      <v-card-text>
        Are you sure you want to log out?
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="cancelLogout">
          Cancel
        </v-btn>
        <v-btn color="blue darken-1" text @click="confirmLogout" :loading="loading">
          Logout
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { getAuth, signOut } from 'firebase/auth';

// Reference: product_spec.md Chapter 8, docs/specs/ui_flows_spec.yaml FLOW_LOGOUT, docs/specs/views_spec.yaml VIEW_CONFIRM_LOGOUT_MODAL

const dialog = ref(true); // Will be controlled by parent component
const loading = ref(false);

const auth = getAuth();

const emit = defineEmits(['user-confirms-logout', 'user-clicks-cancel']);

const confirmLogout = async () => {
  loading.value = true;
  try {
    await signOut(auth);
    emit('user-confirms-logout'); // Indicate successful logout
    // The router guard will handle navigation to the home page
  } catch (error) {
    console.error('Logout error:', error);
    // Optionally, show an error message to the user
  } finally {
    loading.value = false;
  }
};

const cancelLogout = () => {
  emit('user-clicks-cancel');
};
</script>

<style scoped>
/* Add any specific styles for the logout modal here */
</style>
