<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const message = ref('Loading message from backend...')
const errorMessage = ref('')
const userProfile = ref(null)

const authStore = useAuthStore()

// This is now the single source of truth for the API URL.
// Vite will automatically use the URL from .env.development when running locally,
// and the one from .env.production when building for deployment.
const API_BASE_URL = import.meta.env.VITE_API_URL

const fetchUserProfile = async () => {
  if (!authStore.user) {
    alert('You must be logged in!')
    return
  }
  try {
    const token = await authStore.user.getIdToken()
    const response = await axios.get(`${API_BASE_URL}/api/me`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    userProfile.value = response.data
  } catch (error) {
    console.error('Error fetching user profile:', error)
    alert('Failed to fetch user profile.')
  }
}

onMounted(async () => {
  if (!API_BASE_URL) {
    errorMessage.value = "Error: The backend API URL is not configured."
    return
  }
  try {
    const response = await axios.get(`${API_BASE_URL}/api/message`)
    message.value = response.data.content
  } catch (error) {
    console.error('Error fetching message:', error)
    errorMessage.value = 'Failed to connect to the backend. Is it running?'
    message.value = ''
  }
})
</script>

<template>
  <main>
    <h1>Welcome to Sentinel</h1>
    <div class="message-box">
      <p v-if="message">{{ message }}</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
    <div class="message-box">
      <button @click="fetchUserProfile">Fetch My Profile (Protected)</button>
      <pre v-if="userProfile">{{ userProfile }}</pre>
    </div>
  </main>
</template>

<style scoped>
main {
  text-align: center;
  padding-top: 50px;
}
.message-box {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  display: inline-block;
  min-width: 300px;
}
.error {
  color: red;
}
</style>

