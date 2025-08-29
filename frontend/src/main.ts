import './plugins/firebase'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import createSentinelRouter from './router' // Import the factory function
import vuetify from './plugins/vuetify' // path to vuetify export
import i18n from './plugins/i18n' // import i18n
import { useAuthStore } from './stores/auth'

const app = createApp(App)

const router = createSentinelRouter() // Create the router instance

const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(vuetify)
app.use(i18n)

app.mount('#app')

const authStore = useAuthStore(pinia)
authStore.init()
