import Home from "src/pages/LoginPage.vue";
import HomeLayout from "layouts/HomeLayout.vue";
import otp from "src/pages/otPage.vue";
import sitesPage from "src/pages/SitesPage.vue";
import actionsPage from "src/pages/ActionSettingsPage.vue"
import ManageModelsPage from "src/pages/ManageModelsPage.vue"
import ManageSitesPage from "src/pages/ManageSitesPage.vue"

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
  },
  
  {
    //testing sidebar on SitesPage
    path: '/',
    component: () => import('layouts/SidebarLayout.vue'),
    children: [
      //route for dashboard{ path: 'dashboard', component: () => import('pages/DashboardPage.vue') },
      { path: '',
       component: ManageSitesPage
      },
      //route for camera { path: 'configuration/camera', component: () => import('pages/CameraPage.vue') },
      //route for ai edge gateway { path: 'configuration/ai-gateway', component: () => import('pages/AIGatewayPage.vue') },
      //route for alerts console{ path: 'alerts-console', component: () => import('pages/AlertsConsolePage.vue') },
      //route for action settings{ path: 'action-settings', component: () => import('pages/ActionSettingsPage.vue') },
    ],
  },

  // for 404s
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
