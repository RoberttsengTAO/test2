import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import './assets/main.css'
import router from './router'

import naive from 'naive-ui'
document.title = "SVP Emulation";
createApp(App)
  .use(naive)
  .use(router)
  .mount('#app')

