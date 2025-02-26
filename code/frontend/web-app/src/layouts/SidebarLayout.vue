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
            <q-item-section>{{ item.label }}</q-item-section>
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
      menuItems: [
        { label: 'Dashboard', icon: 'dashboard', route: '/app/dashboard' },
        { label: 'Upload Training Data', icon: 'upload', route: '/pages/ErrorNotFound.vue' },
        { label: 'Configuration', icon: 'menu_open', route: '/pages/ErrorNotFound.vue' },
        { label: 'Cloud Settings', icon: 'filter_drama', route: '/pages/ErrorNotFound.vue' },
        { label: 'Manage Sites', icon: 'place', route: '/app/manage-sites' },
        { label: 'Alerts Console', icon: 'notifications', route: '/app/alerts-console' },
        { label: 'Action Settings', icon: 'layers', route: '/app/action-settings' },
        { label: 'Settings', icon: 'settings', route: '/pages/ErrorNotFound.vue' },
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
