<template>
  <div id="app">
    <header>
      <nav>
        <router-link to="/">Home</router-link>
        <template v-if="authStore.user">
          | <router-link to="/portfolio">Portfolio</router-link>
          | <a href="#" @click.prevent="authStore.logout()">Logout</a>
        </template>
        <template v-else>
          | <router-link to="/login">Login</router-link>
          | <router-link to="/signup">Sign Up</router-link>
        </template>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>