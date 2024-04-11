import { createMemoryHistory, createRouter } from 'vue-router'

import GraphicsPage from '@/components/GraphicsPage.vue'

const routes = [
  { path: '/', component: GraphicsPage },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router;