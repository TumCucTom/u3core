<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer
      show-if-above
      v-model="leftDrawerOpen"
      side="left"
      width="260"
      class="bg-dark text-white column"
    >
      <div class="col q-pt-md">
        <div class="q-pa-md q-mb-md" style="height: 60px; display: flex; align-items: center; gap: 17px;">
          <!-- Logo  -->
          <q-img src="../assets/u3logo2.png" alt="U3 Core" style="width: 40px;" />
          <!-- title -->
          <div class="text-caption text-white" style="font-size: 20px;">U3Core</div>
        </div>

        <!-- Search bar -->
        <div class="q-pa-md" style="max-width: 100%;">
          <q-input v-model="searchQuery" placeholder="Search..." outlined dense class="search-input">
            <template v-slot:prepend>
             <q-icon name="search"></q-icon>
            </template>
           </q-input>
        </div>

        <!-- sidebar -->
        <q-list dense>
          <q-item
            v-for="item in filteredItems"
            :key="item.label"
            clickable
            v-ripple
            tag="router-link"
            :to="item.route"
            class="q-mb-sm"
          >
            <q-item-section avatar>
              <q-icon :name="item.icon" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            tag="router-link"
            to="/app/training-page"
            class="q-mb-sm"
          >
            <q-item-section avatar>
              <q-icon name="upload" />
            </q-item-section>
            <q-item-section>Upload Trainning Data</q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            tag="router-link"
            to="/app/action-settings"
            class="q-mb-sm"
          >
            <q-item-section avatar>
              <q-icon name="menu_open" />
            </q-item-section>
            <q-item-section>Configuration</q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            tag="router-link"
            to="/app/cloud-settings"
            class="q-mb-sm"
          >
            <q-item-section avatar>
              <q-icon name="filter_drama" />
            </q-item-section>
            <q-item-section>Cloud Settings</q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            tag="router-link"
            to="/app/manage-sites"
            class="q-mb-sm"
          >
            <q-item-section avatar>
              <q-icon name="place" />
            </q-item-section>
            <q-item-section>Manage Sites</q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            tag="router-link"
            to="/app/alerts-page"
            class="q-mb-sm"
          >
            <q-item-section avatar>
              <q-icon name="notifications" />
            </q-item-section>
            <q-item-section>Alerts Console</q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            tag="router-link"
            to="/app/action-settings"
          >
            <q-item-section avatar>
              <q-icon name="layers" />
            </q-item-section>
            <q-item-section>Action Settings</q-item-section>
          </q-item>
        </q-list>

        <q-item
          clickable
          v-ripple
          tag="router-link"
          to="/app/settings"
          class="q-mb-sm"
        >
          <q-item-section avatar>
            <q-icon name="settings" />
          </q-item-section>
          <q-item-section>Settings</q-item-section>
        </q-item>
      </div>

    <!-- footer -->
    <div class="q-pa-md border-top-white" style="display: flex; align-items: center;">
        <q-item clickable v-ripple class="q-pa-sm" style="flex: 1;">
          <q-item-section avatar>
            <q-avatar color="primary" text-color="white">
              <q-icon name="person" />
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <div>user name</div>
            <div class="text-caption text-grey">username@email.com</div>
          </q-item-section>
        </q-item>

        <q-btn flat dense icon="exit_to_app" @click="showLogoutDialog = true" />
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Logout Confirmation Dialog -->
    <q-dialog v-model="showLogoutDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">confirm Logout</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          Are you sure you want logout？
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="cancel" color="primary" v-close-popup />
          <q-btn flat label="confirm" color="negative" @click="confirmLogout" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script>
export default {
  data() {
    return {
      leftDrawerOpen: true, // drawer (sidebar) is open by default
      searchQuery: '',
      showLogoutDialog: false, //make sure it wont appear at anytime
      menuItems: [
        { label: 'Dashboard', icon: 'dashboard', route: '/app/dashboard' },
        { label: 'Upload Training Data', icon: 'upload', route: '/app/training-page' },
        { label: 'Configuration', icon: 'menu_open', route: '/pages/ErrorNotFound.vue' },
        { label: 'Cloud Settings', icon: 'filter_drama', route: '/app/cloud-settings' },
        { label: 'Manage Sites', icon: 'place', route: '/app/manage-sites' },
        { label: 'Alerts Console', icon: 'notifications', route: '/app/alerts-page' },
        { label: 'Action Settings', icon: 'layers', route: '/app/action-settings' },
        { label: 'Settings', icon: 'settings', route: '/app/settings' },
      ],
    };
  },
  computed: {
    filteredItems() {
      return this.menuItems.filter((item) =>
        item.label.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    confirmLogout() {
      this.showLogoutDialog = false;
      this.$router.push('/'); // skip to login page
    },
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
.search-input .q-field__control {
  background-color: white;
  color: black;
}
.border-top-white {
  border-top: 1px solid white;
}
</style>
