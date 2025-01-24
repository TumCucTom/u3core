import home from "src/pages/LoginPage.vue";
import otp from "src/pages/otPage.vue";
import DashboardPage from "src/pages/DashboardPage.vue";
import ManageSitesPage from "src/pages/ManageSitesPage.vue";
import ManageModelsPage from "src/pages/ManageModelsPage.vue";
import ActionSettingsPage from "src/pages/ActionSettingsPage.vue";

const routes = [
  //start off at the login page as the default route
  {
    path: "/",
    component: () => import("layouts/MinimalLayout.vue"),
    children: [
      {
        path: "",
        component: home, 
      },
      {
        path: "otp",
        component: otp, // OTP Page
      },
    ],
  },

  // sidebar layout for all the other pages
  {
    path: "/app",
    component: () => import("layouts/SidebarLayout.vue"),
    children: [
      { path: "dashboard", component: DashboardPage }, // Dashboard page
      { path: "manage-sites", component: ManageSitesPage }, // Manage Sites page
      { path: "manage-models", component: ManageModelsPage }, // Manage Models page
      { path: "action-settings", component: ActionSettingsPage }, // Action Settings page
    ],
  },

  // Catch-all for 404 errors
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
