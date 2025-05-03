// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import Home     from '../views/Home.vue'
import About    from '../views/About.vue'
import Projects from '../views/Projects.vue'
import Writing  from '../views/Writing.vue'
import Resume   from '../views/Resume.vue'

const routes = [
    { path: '/',      	 name: 'Home',     component: Home  },
    { path: '/about', 	 name: 'Me', 	   component: About },
    { path: '/projects', name: 'Projects', component: Projects },
    { path: '/posts', 	 name: 'Writing',  component: Writing },
    { path: '/resume', 	 name: 'Resume',   component: Resume },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
