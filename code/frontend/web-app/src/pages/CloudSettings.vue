<template>
    <q-page class="cloud-settings-page q-px-xl q-pt-xl q-pb-lg">
      <div class="text-h4">Cloud Settings</div>
      <div class="text-subtitle1 text-grey-7 q-mb-xl">
        Configure cloud settings for anomaly detection.
      </div>
  
      <q-card flat bordered class="q-pb-lg">
  
        <q-form @submit.prevent="submitForm">
          <q-card-section class="q-pa-lg">
            <div class="row q-col-gutter-lg">
              <div class="col-12 col-md-6">
                <q-select
                  v-model="ec2Instance"
                  label="EC2 Instance Type"
                  hint="Enter a valid instance type."
                  :options="ec2Options"
                  filled
                  dense
                  use-input
                />
              </div>
  
              <div class="col-12 col-md-6">
                <q-input
                  v-model="cloudEndpointUrl"
                  label="Cloud Endpoint URL"
                  hint="Enter a valid endpoint url."
                  filled
                  dense
                />
              </div>
            </div>
          </q-card-section>
  
          <q-separator />
  
          <q-card-section class="q-pa-lg">
            <div class="text-subtitle2">Timings Type</div>
            <div class="text-caption text-grey-7 q-mb-md">
              This will be displayed in the report
            </div>
            <q-option-group
              v-model="timingsType"
              type="radio"
              inline
              :options="timingsOptions"
              color="pink"
            />

            <div
              v-if="timingsType === 'shift-based'"
              class="row q-col-gutter-lg q-mt-md"
            >
              <div class="col-12 col-md-6">
                <q-input
                  v-model="startTime"
                  label="Start time"
                  hint="Enter a valid time (HH:MM)."
                  filled
                  dense
                  type="time"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="endTime"
                  label="End time"
                  hint="Enter a valid time (HH:MM)."
                  filled
                  dense
                  type="time"
                />
              </div>
            </div>
          </q-card-section>
  
          <q-separator />
  
          <q-card-section class="q-pa-lg">
            <q-input
              v-model="apiKey"
              label="API Key / Authentication Token"
              hint="This will be displayed in the report"
              filled
              dense
            />
          </q-card-section>
  
          <q-separator />

          <q-card-section class="q-pa-lg">
            <div class="text-subtitle2">Data Retention Policy</div>
            <div class="text-caption text-grey-7 q-mb-md">
              Select Data Retention Policy options
            </div>
            <q-btn-group flat>
              <q-btn
                v-for="option in retentionOptions"
                :key="option.value"
                :label="option.label"
                :color="retentionPolicy === option.value ? 'primary' : 'grey-5'"
                @click="retentionPolicy = option.value"
                class="q-mr-md"
              />
            </q-btn-group>
          </q-card-section>
  
          <q-separator />
  

          <q-card-section class="q-pa-lg">
            <div class="text-subtitle2">Data usage & processed per day</div>
            <div class="text-caption text-grey-7 q-mb-sm">
              Data usage (GB) processed per day
            </div>
            <div class="text-h4">
              {{ dataUsage }} GB
            </div>
          </q-card-section>
  
          <div class="q-pa-lg row justify-end">
            <q-btn flat label="Cancel" color="primary" class="q-mr-sm" />
            <q-btn label="Save Settings" color="dark" type="submit" />
          </div>
  
        </q-form>
      </q-card>
    </q-page>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const ec2Instance = ref('t2.micro')
  const cloudEndpointUrl = ref('https://api.cloudprovider.com/v1/upload')
  const timingsType = ref('shift-based') 
  const startTime = ref('09:00')
  const endTime = ref('17:00')
  const apiKey = ref('ABCD1234XYZ5678')
  const retentionPolicy = ref('7days')
  const dataUsage = ref(0)
  
  const ec2Options = [
    { label: 't2.micro', value: 't2.micro' },
    { label: 't2.small', value: 't2.small' },
    { label: 't2.medium', value: 't2.medium' }
  ]
  
  const timingsOptions = [
    { label: '24 hrs monitoring', value: '24hrs' },
    { label: 'Shift based', value: 'shift-based' }
  ]
  
  const retentionOptions = [
    { label: '7 days', value: '7days' },
    { label: '30 days', value: '30days' },
    { label: '90 days', value: '90days' }
  ]
  
  function submitForm() {
    console.log('EC2 Instance:', ec2Instance.value)
    console.log('Cloud Endpoint URL:', cloudEndpointUrl.value)
    console.log('Timings Type:', timingsType.value)
    console.log('Start Time:', startTime.value)
    console.log('End Time:', endTime.value)
    console.log('API Key:', apiKey.value)
    console.log('Retention Policy:', retentionPolicy.value)
  }
  </script>
  
  <style scoped>
  .cloud-settings-page {
    max-width: 900px;
    margin: 0 auto;
  }
  </style>
  