import { createRouter, createWebHistory } from 'vue-router'
import HouseView from '../views/HouseView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HouseView
    }
  ]
})

export default router
