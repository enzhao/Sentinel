<template>
  <v-container class="text-center">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <h1 class="text-h3 font-weight-bold mb-4">Welcome to Sentinel</h1>
        <p class="text-h6 font-weight-light">
          Your personal investment strategy automation tool.
        </p>
        <p class="mt-4">
          Sentinel empowers you to define and automate your long-term investment philosophy,
          acting as an unemotional guardrail to help you stay the course.
        </p>
        <div class="mt-8">
          <v-btn to="/signup" color="primary" size="large" class="mr-4">Get Started</v-btn>
          <v-btn to="/about" size="large">Learn More</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
// No script logic needed for this simple home page
</script>

<style scoped>
.v-container {
  padding-top: 5rem;
  padding-bottom: 5rem;
}
</style>