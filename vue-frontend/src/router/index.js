// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { userStore } from '../stores/user'

import Home     from '../views/Home.vue'
import About    from '../views/About.vue'
import Projects from '../views/Projects.vue'
import Writing  from '../views/Writing.vue'
import Resume   from '../views/Resume.vue'

// Apps
import Draw         from '../views/Draw.vue'
import Connections  from '../views/Connections/Connections.vue'

// Connections components
import ConnWelcomeHeader  from '../views/Connections/ConnectionsWelcome.vue'
import ConnRegularHeader  from '../views/Connections/ConnectionsHeaderStandard.vue'
import ConnAddPerson      from '../views/Connections/ConnAddPerson.vue'
import ConnLogin          from '../views/Connections/ConnLogin.vue'



const routes = [
    { path: '/',            name: 'Home',     component: Home      },
    { path: '/about',       name: 'Me',       component: About     },
    { path: '/posts',       name: 'Writing',  component: Writing   },
    { path: '/projects',    name: 'Projects', component: Projects  },
    { path: '/resume',      name: 'Resume',   component: Resume    },
    { path: '/draw',        name: 'Draw',         component: Draw,          meta: {fullFlex: true} },
    { path: '/connections',  component: Connections,   meta: {fullFlex: true}, 
        children: [
            {
                path: 'login', 
                name: 'ConnectionsLogin',
                components: {
                    header: ConnRegularHeader,
                    default: ConnLogin,
                }
            },
            {
                path: '', 
                name: 'Connections',
                meta: {requiresAuth: true},
                components: {
                    header: ConnRegularHeader,
                    default: ConnAddPerson,
                }
            },
            {
                path: 'welcome', 
                name: 'ConnectionsWelcome',
                meta: {requiresAuth: true},
                components: {
                    header: ConnWelcomeHeader,
                }
            }
        ]
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to) => {
    // wait until we know login state
    if (userStore.loading) {
        return false; // cancel navigation until loading finishes
    }

    // does any matched route (or its parent) require auth?
    const needsAuth = to.matched.some((r) => r.meta.requiresAuth);

    if (needsAuth && !userStore.user) {
        // not logged in → send them to your Flask login flow
        window.location.href = "/login";
        return false; // cancel the in-SPA navigation
    }

    // otherwise, allow it
    return true;
});

export default router
