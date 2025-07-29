import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' // path to vuetify export
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

// Initialize the auth store before mounting the app
const authStore = useAuthStore()
authStore.init().then(() => {
  app.mount('#app')
})
