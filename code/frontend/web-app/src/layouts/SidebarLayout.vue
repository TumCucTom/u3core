<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      side="left"
      width="260"
      class="bg-white text-dark"
    >
      <!-- u3logo and name -->
      <div class="q-pa-md row items-center" style="min-height: 60px">
        <!-- space for logo -->
        <q-avatar size="42px" class="bg-orange text-white">
          U3
        </q-avatar>
        <div class="text-h6 q-ml-sm">U3Core</div>
      </div>

      <!-- search bar (not sure how this will work but going with client design) -->
      <div class="q-pa-sm">
        <q-input
          outlined
          dense
          v-model="searchTerm"
          placeholder="Search"
          rounded
        >
          <template #prepend>
            <q-icon name="search" class="text-grey" />
          </template>
        </q-input>
      </div>

      <!-- navigation items -->
      <q-list padding>
        <!-- Dashboard -->
        <q-item
          clickable
          tag="router-link"
          to="/app/dashboard"
          v-ripple
        >
            <!-- just placeholder icons for the menu can easily replace later -->
          <q-item-section avatar>
            <q-icon name="bar_chart" class="text-grey" />
          </q-item-section>
          <q-item-section>Dashboard</q-item-section>
        </q-item>

        <!-- Upload Training Data -->
        <q-item
          clickable
          tag="router-link"
          to="/app/training-page"
          v-ripple
        >
          <q-item-section avatar>
            <q-icon name="file_upload" class="text-grey" />
          </q-item-section>
          <q-item-section>Upload Training Data</q-item-section>
        </q-item>

        <!-- Configuration -->
        <q-item
          clickable
          v-ripple
          @click="toggleConfiguration"
          :active="configurationOpen"
        >
          <q-item-section avatar>
            <q-icon name="settings" class="text-grey" />
          </q-item-section>
          <q-item-section>Configuration</q-item-section>
          <q-item-section side>
            <q-icon
              :name="configurationOpen ? 'expand_more' : 'chevron_right'"
              class="text-grey"
            />
          </q-item-section>
        </q-item>


        <transition name="fade">
          <div v-if="configurationOpen" class="q-ml-lg">
            
        <!-- Manage Sites -->
        <q-item
          clickable
          tag="router-link"
          to="/app/manage-sites"
          v-ripple
        >
          <q-item-section avatar>
            <!-- pink bullet -->
            <q-icon
              name="fiber_manual_record"
              color="pink"
              size="12px"
            />
          </q-item-section>
          <q-item-section>Manage Sites</q-item-section>
        </q-item>

        <!-- Camera and AI edge gateway -->
        <div class="q-ml-lg">
          <q-item clickable v-ripple tag="router-link" to="/app/camera">
            <q-item-section avatar>
              <q-icon
                name="fiber_manual_record"
                color="grey-5"
                size="8px"
              />
            </q-item-section>
            <q-item-section>Camera</q-item-section>
          </q-item>
          <q-item clickable v-ripple tag="router-link" to="/app/ai-edge-gateway">
            <q-item-section avatar>
              <q-icon
                name="fiber_manual_record"
                color="grey-5"
                size="8px"
              />
            </q-item-section>
            <q-item-section>Ai Edge Gateway</q-item-section>
          </q-item>
        </div>
          </div>
        </transition>

        <!-- Cloud settings-->
        <q-item
          clickable
          tag="router-link"
          to="/app/cloud-settings"
          v-ripple
        >
          <q-item-section avatar>
            <q-icon name="cloud_queue" class="text-grey" />
          </q-item-section>
          <q-item-section>Cloud Settings</q-item-section>
        </q-item>

         <!-- Alerts console-->
        <q-item
          clickable
          tag="router-link"
          to="/app/alerts-page"
          v-ripple
        >
          <q-item-section avatar>
            <q-icon name="notifications" class="text-grey" />
          </q-item-section>
          <q-item-section>Alerts Console</q-item-section>
        </q-item>

        <!-- alerts settings/action settings-->
        <q-item
          clickable
          tag="router-link"
          to="/app/action-settings"
          v-ripple
        >
          <q-item-section avatar>
            <q-icon name="notifications_active" class="text-grey" />
          </q-item-section>
          <q-item-section>Alerts Settings</q-item-section>
        </q-item>

        <q-item
          clickable
          tag="router-link"
          to="/app/manage-models"
          v-ripple
        >
          <q-item-section avatar>
            <q-icon name="developer_board" class="text-grey" />
          </q-item-section>
          <q-item-section>Manage Models</q-item-section>
        </q-item>

        <q-item
          clickable
          tag="router-link"
          to="/app/settings"
          v-ripple
        >
          <q-item-section avatar>
            <q-icon name="tune" class="text-grey" />
          </q-item-section>
          <q-item-section>Settings</q-item-section>
        </q-item>
      </q-list>

      <!-- User profile at the bottom -->
      <div class="q-mt-auto q-pa-md">
        <q-separator />
        <q-item
          clickable
          tag="router-link"
          to="/app/user-profile"
          v-ripple
          class="q-pt-md"
        >
          <q-item-section avatar>
            <q-avatar size="42px">
              <!-- user avatar can replace with image later -->
              <img
                src="https://placehold.co/60x60"
                alt="User avatar"
              />
            </q-avatar>
          </q-item-section>
          <q-item-section>
            <div>Olivia Rhye</div>
            <div class="text-caption text-grey-7">olivia@untitledui.com</div>
          </q-item-section>
          <q-item-section side>
            <q-icon name="open_in_new" class="text-grey" />
          </q-item-section>
        </q-item>
      </div>
    </q-drawer>

    <!-- Page content -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const leftDrawerOpen = ref(true)
    const searchTerm = ref('')
    const configurationOpen = ref(false)

    function toggleConfiguration() {
      configurationOpen.value = !configurationOpen.value
    }

    return {
      leftDrawerOpen,
      searchTerm,
      configurationOpen,
      toggleConfiguration
    }
  }
}
</script>

<style scoped>
.text-dark {
  color: #1e1e2f;
}
.bg-orange {
  background-color: #e86828;
}
</style>
