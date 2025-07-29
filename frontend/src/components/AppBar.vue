<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { isAuthenticated, user } = storeToRefs(authStore)
const router = useRouter()

const drawer = ref(false)

const handleLogout = async () => {
  await authStore.logout()
  // Redirect to home page after logout
  router.push('/')
}

const navItems = [
  { title: 'About', to: '/about', auth: false },
  { title: 'Portfolio', to: '/portfolio', auth: true }
]
</script>

<template>
  <div>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="d-flex d-sm-none"></v-app-bar-nav-icon>
      <v-toolbar-title>
        <router-link to="/" class="white--text text-decoration-none">
          <v-icon icon="mdi-shield-sun" class="mr-2"></v-icon>
          Sentinel
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="d-none d-sm-flex">
        <v-btn v-for="item in navItems.filter(i => !i.auth || isAuthenticated)" :key="item.title" :to="item.to" text>
          {{ item.title }}
        </v-btn>
      </div>
      <v-spacer></v-spacer>
      <div class="d-none d-sm-flex align-center">
        <template v-if="!isAuthenticated">
          <v-btn to="/login" text>Log In</v-btn>
          <v-btn to="/signup" color="secondary">Sign Up</v-btn>
        </template>
        <template v-else>
          <span class="mr-4">{{ user?.email }}</span>
          <v-btn @click="handleLogout" color="secondary">Log Out</v-btn>
        </template>
      </div>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary app>
      <v-list>
        <v-list-item v-for="item in navItems.filter(i => !i.auth || isAuthenticated)" :key="item.title" :to="item.to" @click="drawer = false">
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>
        <template v-if="!isAuthenticated">
          <v-list-item to="/login" @click="drawer = false">
            <v-list-item-title>Log In</v-list-item-title>
          </v-list-item>
          <v-list-item to="/signup" @click="drawer = false">
            <v-list-item-title>Sign Up</v-list-item-title>
          </v-list-item>
        </template>
        <template v-else>
          <v-list-item>
            <v-list-item-title>{{ user?.email }}</v-list-item-title>
          </v-list-item>
          <v-list-item @click="handleLogout">
            <v-list-item-title>Log Out</v-list-item-title>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<style scoped>
.white--text {
  color: white !important;
}
</style>