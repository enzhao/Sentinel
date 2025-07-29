import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Initialize the auth store before mounting the app
const authStore = useAuthStore()
authStore.init().then(() => {
  app.mount('#app')
})