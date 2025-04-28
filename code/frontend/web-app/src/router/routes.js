import Home from "src/pages/LoginPage.vue";
import otp from "src/pages/OtPage.vue";
import DashboardPage from "src/pages/DashboardPage.vue";
import ManageCamerasPage from "src/pages/ManageCamerasPage.vue";
import ManageModelsPage from "src/pages/ManageModelsPage.vue";
import ActionSettingsPage from "src/pages/ActionSettingsPage.vue";
import Verified from "src/pages/VerifiedPassword.vue";
//import { meta } from "eslint-plugin-vue";
import AlertsPage from "src/pages/AlertsPage.vue"
import TrainingPage from "src/pages/TrainingPage.vue"
import CloudSettingsPage from "src/pages/CloudSettings.vue"
import SettingsPage from "src/pages/SettingsPage.vue"
import energyPage from "src/pages/EnergyManagement.vue"
import qualityPage from "src/pages/QualityMangement.vue"
import ManageSitesPage from "src/pages/ManageSitesPage.vue"
import AiEdge from "src/pages/AIEdgeGatewayPage.vue"

const routes = [
  //start off at the login page as the default route
  {
    path: "/",
    component: () => import("src/layouts/MinimalLayout.vue"),
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
        meta: {title: 'Email verification' }
      }, // Action Settings page
    ],
  },

  // sidebar layout for all the other pages
  {
    path: "/app",
    component: () => import("src/layouts/SidebarLayout.vue"),
    children: [
      { path: "dashboard",
        component: DashboardPage,
        meta: {title:"Dashboard"}
      }, // Dashboard page
      { path: "manage-cameras",
        component: ManageCamerasPage,
        meta: {title:"ManageCameras"}
      }, // Manage Cameras page
      {
        path: "manage-sites",
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
      { path : "alerts-page",
        component: AlertsPage,
        meta: {title:'AlertsPage'},
      },// Alerts page
      { path : "training-page",
        component :TrainingPage,
        meta: {title:'TrainingPage'},
      },
      { path : "cloud-settings",
        component :CloudSettingsPage,
        meta: {title:'Cloud-settings'},
      },
      { path : "settings",
        component:SettingsPage,
        meta: {title:'settings'},
      },
      {
        path : "energy-management",
        component :energyPage,
        meta: {title:'energy-management'},
      },
      {
        path:"quality-management",
        component:qualityPage,
        meta: {title:'QualityManagement'},
      },
      {
        path: "ai-edge-gateway",
        component: AiEdge,
        meta: {title:'AiEdgeGateway'},
      }
    ]
  },

  // Catch-all for 404 errors
  {
    path: "/:catchAll(.*)*",
    component: () => import("src/pages/ErrorNotFound.vue"),
    meta: { title:"ErrorNotFound"}
  },
];

export default routes;
