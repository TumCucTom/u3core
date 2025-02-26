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
          <q-img src="../assets/u3logo2.png" alt="Digital U3" style="width: 40px;" />
          <!-- title -->
          <div class="text-caption text-white" style="font-size: 20px;">Digital U3</div>
        </div>

        <!-- 搜索栏 -->
        <div class="q-pa-md">
          <q-input v-model="searchQuery" placeholder="搜索..." outlined dense class="search-input" />
        </div>

        <!-- sidebar -->
        <q-list dense>
          <q-item clickable v-ripple tag="router-link" to="/app/dashboard" class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>

          <q-item clickable v-ripple tag="router-link" to="/pages/ErrorNotFound.vue" class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="upload" />
            </q-item-section>
            <q-item-section>Upload Training Data</q-item-section>
          </q-item>

          <q-item clickable v-ripple tag="router-link" to="/pages/ErrorNotFound.vue" class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="menu_open" />
            </q-item-section>
            <q-item-section>Configuration</q-item-section>
          </q-item>

          <q-item clickable v-ripple tag="router-link" to="/pages/ErrorNotFound.vue" class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="filter_drama" />
            </q-item-section>
            <q-item-section>Cloud Settings</q-item-section>
          </q-item>

          <q-item clickable v-ripple tag="router-link" to="/app/manage-sites" class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="place" />
            </q-item-section>
            <q-item-section>Manage Sites</q-item-section>
          </q-item>

          <q-item clickable v-ripple tag="router-link" to="/app/alerts-console" class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="notifications" />
            </q-item-section>
            <q-item-section>Alerts Console</q-item-section>
          </q-item>

          <q-item clickable v-ripple tag="router-link" to="/app/action-settings" class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="layers" />
            </q-item-section>
            <q-item-section>Action Settings</q-item-section>
          </q-item>

          <q-item clickable v-ripple tag="router-link" to="/pages/ErrorNotFound.vue" class="q-mb-sm">
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>Settings</q-item-section>
          </q-item>
        </q-list>
      </div>

      <!-- footer -->
      <div class="q-pa-md border-top">
        <q-item clickable v-ripple @click="handleLogout" class="q-pa-sm">
          <q-item-section avatar>
            <q-avatar color="primary" text-color="white">
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
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  data() {
    return {
      leftDrawerOpen: true, // drawer (sidebar) is open by default
      searchQuery: '',
    };
  },
  methods: {
    handleLogout() {
      console.log('Logging out...');
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
</style>
