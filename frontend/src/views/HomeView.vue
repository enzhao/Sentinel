<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth' // <-- Import auth store

const message = ref('Loading message from backend...')
const errorMessage = ref('')
const userProfile = ref(null) // <-- To store profile data

const authStore = useAuthStore() // <-- Get the store instance

const API_URL = 'http://127.0.0.1:8000'

// Function to call the protected endpoint
const fetchUserProfile = async () => {
  if (!authStore.user) {
    alert('You must be logged in!')
    return
  }
  try {
    const token = await authStore.user.getIdToken()
    const response = await axios.get(`${API_URL}/api/me`, {
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
  try {
    const response = await axios.get(`${API_URL}/api/message`)
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

