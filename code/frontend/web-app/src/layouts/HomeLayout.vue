<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <q-layout view="hHh lpR lFf">
      <q-header style="height:100px" :class="$q.dark.isActive ? 'bg-dark' : 'bg-white'" reveal bordered>
        <div class="column">
            <div class="col self-center">
                <q-btn flat>
                <img src="~/assets/spaceNXT.png" style="height:5.5rem" @click="hyperlink"/>
                </q-btn>
            </div>
            <div class ="col self-end">
                <q-btn
                    dense
                    flat
                    @click="$q.dark.toggle()"
                    class="q-pl-lg"
                >
                <q-avatar size="4rem" :class="select == -2 ? 'text-light-blue-3' : 'text-grey-6'" @mouseover="select = -2" @mouseleave="select = 0"
                        :icon="$q.dark.isActive ? 'fa-solid fa-moon' : 'fa-regular fa-moon'"/>
                </q-btn>
          </div>
        </div>
      </q-header>

      <q-page-container>
        <router-view/>
      </q-page-container>

    </q-layout>
 </template>

<script>
import axios from 'axios'
import { useQuasar } from 'quasar';
import { watch } from 'vue'

export default {
  setup () {
    const $q = useQuasar()

    watch(() => $q.dark.isActive, val => {
      console.log(val ? 'On dark mode' : 'On light mode')
    })
  },

  methods: {
    hyperlink() {
        window.open("https://spacenxtlabs.com", "_blank");
    },

    }
}
</script>

  <!--<style lang="stylus">-->
  <!--.menu-link color #1da1f2-->

  <!--//background #2f353a-->
  <!--</style>-->
