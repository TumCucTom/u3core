<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer show-if-above v-model="drawer" side="left" width="260" class="bg-white text-grey-8">
      <div class="sidebar-header q-pa-md row no-wrap items-center">
        <q-img src="../assets/u3logo2.png" alt="U3Core" style="width: 32px;"/>
        <div class="column header-text">
          <div class="u3-title">U3Core</div>
          <div class="text-subtitle2">Powered by Big Instance</div>
        </div>
      </div>

      <div class="q-pa-sm">
        <q-input v-model="searchQuery" placeholder="Search" dense outlined class="search-input">
          <template v-slot:prepend>
            <q-icon name="search"/>
          </template>
        </q-input>
      </div>

      <q-list dense separator class="menu-list">
        <template v-for="item in filteredItems" :key="item.label">
          <q-expansion-item
            v-if="item.children"
            :label="item.label"
            :icon="item.icon"
            dense
            header-class="sidebar-item"
            :default-opened="isParentActive(item)"
            expand-icon="keyboard_arrow_down"
            collapse-icon="keyboard_arrow_right"
            active-class="bg-grey-2 text-dark"
          >
            <q-list dense class="px-none">
              <q-item
                v-for="child in item.children"
                :key="child.label"
                clickable
                v-ripple
                tag="router-link"
                :to="child.route"
                active-class="bg-grey-2 text-dark"
                class="sidebar-subitem"
              >
                <q-item-section side class="bullet-section">
                  <div class="bullet"></div>
                </q-item-section>
                <q-item-section>{{ child.label }}</q-item-section>
              </q-item>
            </q-list>
          </q-expansion-item>
          <q-item
            v-else
            clickable
            v-ripple
            tag="router-link"
            :to="item.route"
            active-class="bg-grey-2 text-dark"
            class="sidebar-item"
          >
            <q-item-section avatar>
              <q-icon :name="item.icon" />
            </q-item-section>
            <q-item-section>{{ item.label }}</q-item-section>
          </q-item>
        </template>
      </q-list>

      <div class="sidebar-footer q-pa-md border-top row items-center no-wrap">
        <q-item clickable v-ripple class="no-padding footer-item">
          <q-item-section avatar>
            <q-avatar size="32px">
              <img :src="userAvatar" alt="avatar" />
            </q-avatar>
          </q-item-section>
          <q-item-section>
            <div class="text-subtitle2 text-dark">{{ userName }}</div>
            <div class="text-caption text-grey-6">{{ userEmail }}</div>
          </q-item-section>
        </q-item>
        <q-btn flat dense icon="exit_to_app" @click="showLogoutDialog = true" />
      </div>

    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-dialog v-model="showLogoutDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Confirm Logout</div>
        </q-card-section>
        <q-card-section class="q-pt-none">
          Are you sure you want to logout?
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Confirm" color="negative" @click="confirmLogout" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script>
export default {
  data() {
    return {
      drawer: true,
      searchQuery: '',
      showLogoutDialog: false,
      userName: '',
      userEmail: '',
      userAvatar: 'https://via.placeholder.com/150',
      menuItems: [
        { label: 'Dashboard', icon: 'dashboard', children: [
            { label: 'Compliance management', route: '/app/dashboard' },
            { label: 'Energy/Waste management', route: '/app/energy-management' },
            { label: 'Quality Management', route: '/app/quality-management' }
          ]
        },
        { label: 'Alerts Console', icon: 'layers', route: '/app/alerts-page' },
        { label: 'Configuration', icon: 'device_hub', children: [
            { label: 'Manage Sites', route: '/app/manage-sites' },
            { label: 'Manage Cameras', route: '/app/manage-cameras' },
            { label: 'AI Edge Gateway', route: '/app/ai-edge-gateway' }
          ]
        },
        { label: 'Manage Models', icon: 'pie_chart', route: '/app/manage-models' },
        { label: 'Upload Training Data', icon: 'upload', route: '/app/training-page' },
        { label: 'Cloud Parameters', icon: 'cloud_sync', route: '/app/cloud-settings' },
        { label: 'Actions Setting', icon: 'tune', route: '/app/action-settings' },
        { label: 'Settings', icon: 'settings', route: '/app/settings' }
      ]
    }
  },
  computed: {
    filteredItems() {
      const q = this.searchQuery.trim().toLowerCase()
      if (!q) return this.menuItems
      return this.menuItems.map(item => {
        const matchSelf = item.label.toLowerCase().includes(q)
        if (item.children) {
          const kids = item.children.filter(c => c.label.toLowerCase().includes(q))
          if (matchSelf || kids.length) return { ...item, children: kids }
        } else if (matchSelf) {
          return item
        }
        return null
      }).filter(Boolean)
    }
  },
  methods: {
    isParentActive(item) {
      return item.children && item.children.some(c => this.$route.path === c.route)
    },
    sendEmail() {
      this.userEmail = sessionStorage.getItem('emailTransfer') || ''
      this.userName = sessionStorage.getItem('userName') || ''
    },
    confirmLogout() {
      this.showLogoutDialog = false
      this.$router.push('/')
    }
  },
  mounted() {
    this.sendEmail()
  }
}
</script>

<style>
.bg-white { background-color: #ffffff !important; }
.text-grey-8 { color: #424242 !important; }
.text-dark { color: #212121 !important; }
.text-grey-6 { color: #757575 !important; }

.sidebar-header { border-bottom: 1px solid #e0e0e0; }
.header-text { margin-left: 8px; }
.u3-title { font-size: 20px; font-weight: 500; }
.text-subtitle2 { font-size: 14px; }

.search-input .q-field__control { background-color: #f5f5f5; border-radius: 4px; }

.sidebar-item, .sidebar-subitem { border-radius: 4px; padding: 8px 16px; margin: 4px 0; }
.sidebar-subitem { padding-left: 48px; }

.bullet-section { width: 24px; }
.bullet { width: 6px; height: 6px; background-color: #bdbdbd; border-radius: 50%; margin: auto; }

.sidebar-footer { border-top: 1px solid #e0e0e0; }
.footer-item .q-item-section { padding-left: 8px; }
</style>
