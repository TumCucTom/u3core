<template>
    <q-layout view="lHh Lpr lFf">
      
      <q-drawer show-if-above v-model="drawerOpen" width="250px" bordered>
        <q-scroll-area>
          <q-list dense>
            
            <q-item class="q-mb-md">
              <q-item-section>
                <q-img src="your-logo-path.png" alt="Digital U3" style="width: 150px;" />
              </q-item-section>
            </q-item>
  
           
            <q-item>
              <q-item-section>
                <q-input outlined dense placeholder="Search" prefix="search" />
              </q-item-section>
            </q-item>
  
            
            <q-item clickable v-ripple to="/dashboard">
              <q-item-section avatar>
                <q-icon name="dashboard" />
              </q-item-section>
              <q-item-section>
                Dashboard
              </q-item-section>
            </q-item>
  
            <q-expansion-item icon="settings" label="Configuration" dense>
              <q-item clickable v-ripple to="/configuration/sites">
                <q-item-section>Manage Sites</q-item-section>
              </q-item>
              <q-item clickable v-ripple to="/configuration/camera">
                <q-item-section>Camera</q-item-section>
              </q-item>
              <q-item clickable v-ripple to="/configuration/ai-gateway">
                <q-item-section>AI Edge Gateway</q-item-section>
              </q-item>
            </q-expansion-item>
  
            <q-item clickable v-ripple to="/alerts-console">
              <q-item-section avatar>
                <q-icon name="notifications" />
              </q-item-section>
              <q-item-section>
                Alerts Console
              </q-item-section>
            </q-item>
  
            <q-item clickable v-ripple to="/action-settings">
              <q-item-section avatar>
                <q-icon name="settings" />
              </q-item-section>
              <q-item-section>
                Action Settings
              </q-item-section>
            </q-item>
  
           
            <q-item class="q-mt-xl">
              <q-item-section>
                <div class="text-caption">Olivia Rhye</div>
                <div class="text-caption text-grey">olivia@untitledui.com</div>
              </q-item-section>
              <q-item-section avatar>
                <q-icon name="logout" />
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>
  
      <!-- page content would go here -->
      <q-page-container>
        <router-view />
      </q-page-container>
    </q-layout>
  </template>
  
  <script>
  export default {
    name: "SidebarLayout",
    data() {
      return {
        drawerOpen: true, 
      };
    },
  };
  </script>
  
  <style>

  </style>
  