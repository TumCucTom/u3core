import Home from "src/pages/LoginPage.vue";
import otp from "src/pages/otPage.vue";
import DashboardPage from "src/pages/DashboardPage.vue";
import ManageSitesPage from "src/pages/ManageSitesPage.vue";
import ManageModelsPage from "src/pages/ManageModelsPage.vue";
import ActionSettingsPage from "src/pages/ActionSettingsPage.vue";
import Verified from "src/pages/VerifiedPassword.vue";
import AlertsPage from "src/pages/AlertsPage.vue"
import TrainingPage from "src/pages/TrainingPage.vue"
import CloudSettingsPage from "src/pages/CloudSettings.vue"
import SettingsPage from "src/pages/SettingsPage.vue"

const routes = [
  //start off at the login page as the default route
  {
    path: "/",
    component: () => import("layouts/MinimalLayout.vue"),
    children: [
      {
        path: "",
        component: Home,
        meta: { title: 'U3 Core' },
      },
      {path: "otp", component: otp},
      { path: "verified-email", component: Verified, meta: { title: 'U3 Core' }, }, // Action Settings page
    ],
  },

  // sidebar layout for all the other pages
  {
    path: "/app",
    component: () => import("layouts/SidebarLayout.vue"),
    children: [
      { path: "dashboard", component: DashboardPage,meta: { title: 'U3 Core' }, }, // Dashboard page
      { path: "manage-sites", component: ManageSitesPage,meta: { title: 'U3 Core' }, }, // Manage Sites page
      { path: "manage-models", component: ManageModelsPage,meta: { title: 'U3 Core' }, }, // Manage Models page
      { path: "action-settings", component: ActionSettingsPage,meta: { title: 'U3 Core' }, }, // Action Settings page
      {path : "alerts-page", component: AlertsPage,meta: { title: 'U3 Core' },} ,// Alerts page
      {path : "training-page", component :TrainingPage,meta: { title: 'U3 Core' },},
      {path : "cloud-settings", component :CloudSettingsPage,meta: { title: 'U3 Core' },},
      {path : "settings", component:SettingsPage,meta: { title: 'U3 Core' },},
    ],
  },

  // Catch-all for 404 errors
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
    meta: { title: 'U3 Core' },
  },
];

export default routes;
