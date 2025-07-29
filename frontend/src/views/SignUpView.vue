<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="handleSignup">
      <input type="text" placeholder="Username" v-model="username" required minlength="3" />
      <input type="email" placeholder="Email" v-model="email" required />
      <input type="password" placeholder="Password" v-model="password" required minlength="6" />
      <button type="submit">Sign Up</button>
    </form>
     <p>
      Already have an account? <router-link to="/login">Log In</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')

const handleSignup = async () => {
  try {
    await authStore.signup(username.value, email.value, password.value)
    alert('Signup successful! Please log in.')
  } catch (error) {
    alert(error)
  }
}
</script>

<style scoped>
.signup-container { max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }
input { display: block; width: 95%; padding: 10px; margin-bottom: 10px; }
button { width: 100%; padding: 10px; }
p { margin-top: 15px; text-align: center; }
</style>