import Home from "src/pages/LoginPage.vue";
import otp from "src/pages/otPage.vue";
import sitesPage from "src/pages/SitesPage.vue";

const routes = [
  // minimal (blank) layout for login and otp pages
  {
    path: '/app',
    component: () => import('layouts/MinimalLayout.vue'),
    children: [
      { 
        path: '', 
        component: otp, 
      },
    ],
  },

  
  { 
    //testing sidebar on SitesPage
    path: '/',
    component: () => import('layouts/SidebarLayout.vue'), 
    children: [
      //route for dashboard{ path: 'dashboard', component: () => import('pages/DashboardPage.vue') }, 
      { path: '',
       component: sitesPage
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
