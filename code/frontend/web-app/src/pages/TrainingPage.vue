<template>
    <q-page padding class="upload-page">
  
      
      <div class="text-h4">Upload Training Data</div>
      <div class="text-subtitle1 text-grey-7 q-mt-xs">
        Upload model data.
      </div>
  
      <!-- Tab for switching:  -->
      <div class="q-mt-md">
        <q-btn-group flat>
          <q-btn
            :flat="activeTab !== 'uploadData'"
            color="primary"
            label="Upload Data"
            @click="activeTab = 'uploadData'"
          />
          <q-btn
            :flat="activeTab !== 'uploadLogs'"
            color="primary"
            label="Upload logs"
            @click="activeTab = 'uploadLogs'"
          />
        </q-btn-group>
      </div>
  
      <!-- Upload -->
      <div v-if="activeTab === 'uploadData'">
        <!-- Drop area -->
        <div
          class="q-mt-lg flex flex-center q-pa-md"
          style="
            border: 2px dashed #d3d3d3;
            border-radius: 8px;
            height: 200px;
            cursor: pointer;
          "
          @click="showModelDialog = true"
        >
          <div class="column items-center text-center">
            <q-icon name="cloud_upload" size="36px" color="primary" />
            <div class="text-body2 text-primary q-my-xs">
              Click to upload
            </div>
            <div class="text-caption text-grey-7">
              or drag and drop<br />
              SVG, PNG, JPG or GIF (max. 800×400px)
            </div>
          </div>
        </div>
  

  
        <!-- Start model training -->
        <div class="q-mt-lg row justify-end">
          <q-btn flat label="Cancel" color="primary" class="q-mr-sm" />
          <q-btn
            label="Start Model Training"
            color="dark"
            @click="handleStartTraining"
          />
        </div>
      </div>
  
      <!-- Upload logs content when tabbed, -->
      <div v-else>
        <div class="q-mt-md">
  
  
          <!-- Empty table (no data) -->
          <q-table
            title="All Uploads"
            :data="[]"
            :columns="columns"
            row-key="modelVersion"
            dense
            flat
          >

          </q-table>
        </div>
      </div>
  
      <!-- Popup dialog for training -->
      <q-dialog v-model="showModelDialog" persistent>
        <q-card style="min-width: 400px;">
          <q-card-section class="row items-center">
            <q-icon name="lock" size="md" class="q-mr-sm" />
            <div class="text-h6">Model Training</div>
          </q-card-section>
          <q-card-section>
            Create a new site with all the required information.
          </q-card-section>
  
          <q-card-section>
            <q-input
              v-model="modelVersion"
              label="Model version*"
              filled
              dense
              class="q-mb-sm"
            />
            <q-select
              v-model="siteId"
              :options="siteOptions"
              label="Site Id"
              filled
              dense
            />
          </q-card-section>
  
          <q-card-actions align="right">
            <q-btn flat label="Cancel" @click="showModelDialog = false" />
            <q-btn label="Submit" color="dark" @click="submitModelTraining" />
          </q-card-actions>
        </q-card>
      </q-dialog>
  
    </q-page>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // Tabs
  const activeTab = ref('uploadData') // or 'uploadLogs'
  
  // Dialog control
  const showModelDialog = ref(false)
  
  
  // Table columns (empty data)
  const columns = [
    { name: 'modelVersion', label: 'Model version', field: 'modelVersion' },
    { name: 'siteId', label: 'Site Id', field: 'siteId' },
    { name: 'dateUploaded', label: 'Date uploaded', field: 'dateUploaded' },
    { name: 'lastUpdated', label: 'Last updated', field: 'lastUpdated' },
    { name: 'trainingStatus', label: 'Training Status', field: 'trainingStatus' },
    { name: 'action', label: '', field: 'action' }
  ]
  

  
  // Popup form fields
  const modelVersion = ref('')
  const siteId = ref('')
  
  // Demo logic
  function handleStartTraining() {

  }
  
  function submitModelTraining() {
    console.log('Submitting model version:', modelVersion.value)
    console.log('For site:', siteId.value)
    // api call here ?
    showModelDialog.value = false
  }
  </script>
  
  <style scoped>
  .upload-page {
    max-width: 900px;
    margin: 0 auto;
  }
  </style>
  