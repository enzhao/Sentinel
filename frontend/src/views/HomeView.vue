<template>
  <div class="home">
    <h1>Welcome to Sentinel</h1>
    <p>Welcome to Sentinel, a personal investment strategy automation tool for disciplined, long-term retail investors.</p>
    <nav>
      <router-link to="/login">Login</router-link> |
      <router-link to="/signup">Sign Up</router-link>
    </nav>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
nav {
  margin-top: 20px;
}
</style>
