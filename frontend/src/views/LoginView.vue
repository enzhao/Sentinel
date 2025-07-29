<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMessage = ref<string | null>(null)
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  try {
    await authStore.login(email.value, password.value)
  } catch (error: any) {
    errorMessage.value = error.message
  }
}
</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-4">
          <v-card-title class="text-center">Login</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                required
              ></v-text-field>
              <v-alert v-if="errorMessage" type="error" dense>
                {{ errorMessage }}
              </v-alert>
              <v-btn type="submit" color="primary" block class="mt-4">Log In</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>