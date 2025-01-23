import Home from "src/pages/LoginPage.vue";
import HomeLayout from "layouts/HomeLayout.vue";
import blank from "layouts/MinimalLayout.vue"

const routes = [
  {

    path: '/',
    component: () => import('layouts/MinimalLayout.vue'),
    children: [
      { path: '',
        component: Home,
 
        }

    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
