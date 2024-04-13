import { createMemoryHistory, createRouter } from 'vue-router'

import ListPackages from '@/components/ListPackages.vue'

const routes = [
  { path: '/', component: ListPackages },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router;