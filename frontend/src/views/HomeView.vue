<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Create a reactive variable to hold our message
const message = ref('Loading message from backend...')
const errorMessage = ref('')

// Define the backend API URL
// We will make this more dynamic later
const API_URL = import.meta.env.VITE_API_URL + '/api/message'

// The onMounted hook runs once when the component is first loaded
onMounted(async () => {
  try {
    const response = await axios.get(API_URL)
    // Update the message with the content from the database
    message.value = response.data.content
  } catch (error) {
    console.error('Error fetching message:', error)
    errorMessage.value = 'Failed to connect to the backend. Is it running?'
    message.value = '' // Clear the loading message
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

