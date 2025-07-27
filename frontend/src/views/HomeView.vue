<!-- FILE: /frontend/src/views/HomeView.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const message = ref('Loading message from backend...')
const errorMessage = ref('')
const userProfile = ref(null)

const authStore = useAuthStore()

// This is the single source of truth for the API URL.
const API_BASE_URL = import.meta.env.VITE_API_URL

// --- NEW LOGGING ---
console.log(`[Sentinel Frontend] Initializing...`)
console.log(`[Sentinel Frontend] Backend API URL is set to: ${API_BASE_URL}`)
// --- END NEW LOGGING ---

const fetchUserProfile = async () => {
  if (!authStore.user) {
    alert('You must be logged in!')
    return
  }
  try {
    console.log('[Sentinel Frontend] Fetching user profile (protected)...') // <-- NEW LOG
    const token = await authStore.user.getIdToken()
    const response = await axios.get(`${API_BASE_URL}/api/me`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    userProfile.value = response.data
    console.log('[Sentinel Frontend] Successfully fetched user profile:', response.data) // <-- NEW LOG
  } catch (error) {
    console.error('[Sentinel Frontend] Error fetching user profile:', error) // <-- UPDATED LOG
    alert('Failed to fetch user profile.')
  }
}

onMounted(async () => {
  if (!API_BASE_URL) {
    errorMessage.value = "Error: The backend API URL is not configured."
    console.error('[Sentinel Frontend] VITE_API_URL is not defined!') // <-- NEW LOG
    return
  }
  try {
    console.log('[Sentinel Frontend] Fetching public message...') // <-- NEW LOG
    const response = await axios.get(`${API_BASE_URL}/api/message`)
    message.value = response.data.content
    console.log('[Sentinel Frontend] Successfully fetched public message:', response.data) // <-- NEW LOG
  } catch (error) {
    console.error('[Sentinel Frontend] Error fetching public message:', error) // <-- UPDATED LOG
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
pre {
  text-align: left;
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 4px;
}
</style>
