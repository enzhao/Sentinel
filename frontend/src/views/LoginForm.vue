<template>
  <v-dialog v-model="dialog" persistent max-width="500px">
    <v-card>
      <v-card-title class="text-h5">Login to Sentinel</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitLogin">
          <v-text-field
            v-model="formState.email"
            label="Email"
            type="email"
            required
            outlined
            dense
            class="mb-4"
          ></v-text-field>
          <v-text-field
            v-model="formState.password"
            label="Password"
            type="password"
            required
            outlined
            dense
            class="mb-4"
          ></v-text-field>
          <v-alert v-if="formState.error" type="error" dense dismissible class="mb-4">
            {{ formState.error }}
          </v-alert>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="cancelLogin">
              Cancel
            </v-btn>
            <v-btn color="blue darken-1" type="submit" :loading="loading">
              Login
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; 

const dialog = ref(true);
const loading = ref(false);
const formState = reactive({
  email: '',
  password: '',
  error: null as string | null,
});

const router = useRouter();
const authStore = useAuthStore(); // <-- Get the store instance

const emit = defineEmits(['user-submits-login', 'user-clicks-cancel']);

const submitLogin = async () => {
  loading.value = true;
  formState.error = null;
  try {
    // Call the centralized store action
    await authStore.login(formState.email, formState.password);
    emit('user-submits-login');
  } catch (error: any) {
    console.error('Login error:', error.code, error.message);
    switch (error.code) {
      case 'auth/user-not-found':
      case 'auth/wrong-password':
      case 'auth/invalid-credential':
        formState.error = 'Invalid email or password.';
        break;
      // ... (rest of the error handling is the same)
      default:
        formState.error = 'An unexpected error occurred. Please try again.';
        break;
    }
  } finally {
    loading.value = false;
  }
};

const cancelLogin = () => {
  emit('user-clicks-cancel');
  router.push('/');
};
</script>

<style scoped>
/* Add any specific styles for the login form here */
</style>
