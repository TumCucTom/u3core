import Home from "src/pages/LoginPage.vue";
import HomeLayout from "layouts/HomeLayout.vue";
import otp from "src/pages/otPage.vue";
import DashboardPage from "src/pages/DashboardPage.vue";
import ManageSitesPage from "src/pages/ManageSitesPage.vue";
import ManageModelsPage from "src/pages/ManageModelsPage.vue";
import ActionSettingsPage from "src/pages/ActionSettingsPage.vue";
import Verified from "src/pages/VerifiedPassword.vue";
//import { meta } from "eslint-plugin-vue";

const routes = [
  //start off at the login page as the default route
  {
    path: "/",
    component: () => import("layouts/MinimalLayout.vue"),
    children: [
      {
        path: "",
        component: Home,
        meta: {title:"UserLogin"}
      },
      { path: "otp", 
        component: otp,
        meta: {title:"OTP Authentication"}
      },
      { path: "verified-email", 
        component: Verified,
        meta: {title:"Email verification"}
      }, // Action Settings page
    ],
  },

  // sidebar layout for all the other pages
  {
    path: "/app",
    component: () => import("layouts/SidebarLayout.vue"),
    children: [
      { path: "dashboard", 
        component: DashboardPage,
        meta: {title:"Dashboard"}
      }, // Dashboard page
      { path: "manage-sites", 
        component: ManageSitesPage,
        meta: {title:"ManageSites"}
      }, // Manage Sites page
      { path: "manage-models", 
        component: ManageModelsPage,
        meta: {title:"ManageModels"}
      }, // Manage Models page
      { path: "action-settings", 
        component: ActionSettingsPage,
        meta: {title:"ActionSettings"}
      }, // Action Settings page
    ],
  },

  // Catch-all for 404 errors
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
    meta: { title:"ErrorNotFound"}
  },
];

export default routes;
