<template>
    <q-layout view="lHh Lpr lFf">
      <q-drawer
        show-if-above
        v-model="leftDrawerOpen"
        side="left"
        width=260
        class="bg-dark text-white"
      >
        
        <div class="q-pa-md q-mb-md" style="height: 60px;">
          <!-- space to put logo later -->
        </div>
  
        <!-- side bar -->
        <q-list dense>
          <q-item clickable v-ripple class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>
  
          <q-item clickable v-ripple expand-separator>
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>Configuration</q-item-section>
          </q-item>
  
          <q-item clickable v-ripple class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="notifications" />
            </q-item-section>
            <q-item-section>Alerts Control</q-item-section>
          </q-item>
  
          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="layers" />
            </q-item-section>
            <q-item-section>Action Settings</q-item-section>
          </q-item>
        </q-list>
  
        
        <div class="q-pa-md q-mt-auto">
          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-avatar>
                <!-- can put user avatar here -->
                <q-icon name="person" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <div>user name</div>
              <div class="text-caption text-grey">username@email.com</div>
            </q-item-section>
            <q-item-section side>
              <q-icon name="exit_to_app" />
            </q-item-section>
          </q-item>
        </div>
      </q-drawer>
  
      <q-page-container>
        <router-view/>
      </q-page-container>
    </q-layout>
  </template>
  
  <script>
  export default {
    data() {
      return {
        leftDrawerOpen: true,
      };
    },
  };
  </script>
  
  <style>
  .bg-dark {
    background-color: #1e1e2f; 
  }
  .text-white {
    color: #ffffff;
  }
  .text-grey {
    color: #a0a0b0;
  }
  </style>