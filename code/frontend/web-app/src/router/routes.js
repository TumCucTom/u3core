import Home from "src/pages/Login.vue";
import HomeLayout from "layouts/HomeLayout.vue";

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '',
        component: () => import('pages/IndexPage.vue'),
        component: HomeLayout,
          children: [
            { path: '', component: Home },
          ]}
    ]
  },
  { path: '/ResetPassword', component: () => import('src/pages/ResetPassword.vue') },
  { path: '/VerifiedPassword', component: () => import('src/pages/VerifiedPassword.vue') },
  { path: '/Dashboard', component: () => import('src/pages/DashBoard.vue') },
  { path: '/OTPVerification', component: () => import('src/pages/OTPVerification.vue') },
  { path: '/SetupResetPassword', component: () => import('src/pages/ForgotPassword.vue') },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
