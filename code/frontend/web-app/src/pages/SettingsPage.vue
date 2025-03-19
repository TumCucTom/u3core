<template>
    <q-page class="settings-page q-px-xl q-py-lg">
      <div class="text-h4">Settings</div>

      <q-tabs
        v-model="currentTab"
        inline-label
        class="q-mt-sm"
        active-color="pink"
        indicator-color="pink"
      >
        <q-tab name="application" label="Application Settings" />
        <q-tab name="camera" label="Camera Edge & device Management" />
        <q-tab name="roles" label="User Roles & Permissions" />
        <q-tab name="privacy" label="Data Privacy & Compliance" />
        <q-tab name="integrations" label="Integrations" />
        <q-tab name="api" label="API" />
      </q-tabs>

      <q-tab-panels v-model="currentTab" animated class="q-mt-md">
        <q-tab-panel name="application">
          <div class="text-h6">Notification settings</div>
          <div class="text-caption text-grey-7 q-mb-lg">
            We may still send you important notifications about your account
            outside of your notification settings.
          </div>

          <q-card flat bordered class="q-pa-md q-mb-sm">
            <div class="row">
              <div class="col-12 col-md-3 text-body2 text-bold">
                All Events
              </div>
              <div class="col-12 col-md-9 text-caption text-grey-7 q-mb-md">
                These are notifications for comments on your posts and replies to your comments.
              </div>
            </div>
            <div class="row q-col-gutter-sm q-pt-sm">
              <div class="col-auto">
                <q-toggle
                  v-model="allEventsPush"
                  color="pink"
                  label="Push"
                />
              </div>
              <div class="col-auto">
                <q-toggle
                  v-model="allEventsEmail"
                  color="pink"
                  label="Email"
                />
              </div>
              <div class="col-auto">
                <q-toggle
                  v-model="allEventsSMS"
                  color="pink"
                  label="SMS"
                />
              </div>
            </div>
          </q-card>

          <q-card flat bordered class="q-pa-md q-mb-sm">
            <div class="row">
              <div class="col-12 col-md-3 text-body2 text-bold">
                Critical Events
              </div>
              <div class="col-12 col-md-9 text-caption text-grey-7 q-mb-md">
                These are notifications for when someone tags you in a comment, post or story.
              </div>
            </div>
            <div class="row q-col-gutter-sm q-pt-sm">
              <div class="col-auto">
                <q-toggle
                  v-model="criticalEventsPush"
                  color="pink"
                  label="Push"
                />
              </div>
              <div class="col-auto">
                <q-toggle
                  v-model="criticalEventsEmail"
                  color="pink"
                  label="Email"
                />
              </div>
              <div class="col-auto">
                <q-toggle
                  v-model="criticalEventsSMS"
                  color="pink"
                  label="SMS"
                />
              </div>
            </div>
          </q-card>

          <q-card flat bordered class="q-pa-md q-mb-sm">
            <div class="row">
              <div class="col-12 col-md-3 text-body2 text-bold">
                Web Hook Integrations
              </div>
              <div class="col-12 col-md-9 text-caption text-grey-7 q-mb-md">
                These are notifications to remind you of updates you might have missed.
              </div>
            </div>
            <div class="row q-col-gutter-sm q-pt-sm">
              <div class="col-auto">
                <q-toggle
                  v-model="webhookPush"
                  color="pink"
                  label="Push"
                />
              </div>
              <div class="col-auto">
                <q-toggle
                  v-model="webhookEmail"
                  color="pink"
                  label="Email"
                />
              </div>
              <div class="col-auto">
                <q-toggle
                  v-model="webhookSMS"
                  color="pink"
                  label="SMS"
                />
              </div>
            </div>
          </q-card>

          <div class="q-my-lg">
            <div class="text-h6">Data Retention</div>
            <div class="text-caption text-grey-7 q-mb-md">
              We may still send you important notifications about your account
              outside of your notification settings.
            </div>

            <div class="column">

              <q-card
                v-for="(plan,) in retentionPlans"
                :key="plan.value"
                flat
                bordered
                class="q-px-md q-pt-md q-pb-sm q-mb-sm"
                :class="{'border-positive': dataRetention === plan.value}"
                style="position: relative;"
                @click="dataRetention = plan.value"
              >
                <q-icon
                  v-if="dataRetention === plan.value"
                  name="check_circle"
                  color="pink"
                  size="md"
                  style="position: absolute; top: 10px; right: 10px;"
                />

                <div class="row items-center q-mb-xs">
                  <q-icon :name="plan.icon" size="md" color="grey-8" class="q-mr-sm" />
                  <div class="text-subtitle2">{{ plan.label }}</div>

                  <q-chip
                    v-if="plan.tag"
                    label="Limited time only"
                    outline
                    color="pink"
                    size="xs"
                    class="q-ml-sm"
                  />
                </div>


                <div class="text-h6 q-my-xs">{{ plan.days }} days</div>
                <div class="text-caption text-grey-7">
                  {{ plan.description }}
                </div>
              </q-card>
            </div>
          </div>

        </q-tab-panel>

        <!-- Camera edge and device management-->
        <q-tab-panel name="camera">
          <div class="text-subtitle1 text-grey-7">
            (Camera Edge & device Management content goes here)
          </div>
        </q-tab-panel>

        <!-- User roles and permissions -->
        <q-tab-panel name="roles">
          <div class="text-subtitle1 text-grey-7">
            (User Roles & Permissions content goes here)
          </div>
        </q-tab-panel>

        <!-- Data privacy and compliance-->
        <q-tab-panel name="privacy">
            <div class="text-h6">Encryption Settings</div>
            <div class="text-caption text-grey-7 q-mb-lg">
              (Data Privacy & Compliance content goes here)
            </div>

            <q-card flat bordered class="q-pa-md q-mb-sm">
              <div class="row">
                <div class="col-12 col-md-3 text-body2 text-bold">
                  Encryption Settings
                </div>
                <div class="col-12 col-md-9 text-caption text-grey-7 q-mb-md">
                  Toggle encryption for data
                </div>
              </div>
              <div class="row q-col-gutter-sm q-pt-sm">
                <div class="col-auto">
                  <q-toggle
                    v-model="dataRest"
                    color="pink"
                    label="At Rest"
                    />
                </div>
                <div class="col-auto">
                  <q-toggle
                    v-model="dataTransit"
                    color="pink"
                    label="In Transit"
                    />
                </div>
              </div>
            </q-card>

        </q-tab-panel>

        <!-- Integrations -->
        <q-tab-panel name="integrations">
          <div class="text-subtitle1 text-grey-7">
            (Integrations content goes here)
          </div>
        </q-tab-panel>

        <!-- API -->
        <q-tab-panel name="api">
          <div class="text-subtitle1 text-grey-7">
            (API content goes here)
          </div>
        </q-tab-panel>

      </q-tab-panels>
    </q-page>
  </template>

  <script setup>
  import { ref } from 'vue'

  // Show which tab is active
  const currentTab = ref('application')


  const allEventsPush = ref(true)
  const allEventsEmail = ref(true)
  const allEventsSMS = ref(false)

  const criticalEventsPush = ref(true)
  const criticalEventsEmail = ref(false)
  const criticalEventsSMS = ref(false)

  const webhookPush = ref(false)
  const webhookEmail = ref(false)
  const webhookSMS = ref(false)


  const dataRetention = ref('basic')

  const dataRest = ref(false)
  const dataTransit = ref(false)

  // Array of sample retention plans
  const retentionPlans = [
    {
      value: 'basic',
      label: 'Basic period',
      days: 7,
      icon: 'eco',
      description: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
      tag: true
    },
    {
      value: 'normal',
      label: 'Normal period',
      days: 30,
      icon: 'schedule',
      description: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
    },
    {
      value: 'enterprise',
      label: 'Enterprise period',
      days: 90,
      icon: 'business',
      description: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
    }
  ]
  </script>

  <style scoped>
  .settings-page {
    margin: 0 auto;
  }

  .border-positive {
    border: 2px solid #f48fb1;
    border-radius: 8px;
  }
  </style>
