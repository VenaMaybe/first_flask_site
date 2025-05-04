import { createApp } from 'vue'
import './style_new.css'
import App from './App.vue'
import router from './router'
import { userStore } from './stores/user'

const app = createApp(App)

userStore.fetch().then(() => {
	app.use(router)
	app.mount('#app')
})
