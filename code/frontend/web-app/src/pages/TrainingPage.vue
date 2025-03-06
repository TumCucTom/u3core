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
          @click="handleUploadClick"
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
            <div v-if="fileInfo" class ="text-caption text-green q-mt-sm">
              {{ fileInfo }}
            </div>
          </div>
        </div>
  
        <!--File input (hidden)-->
        <input 
          type="file" 
          ref="fileInput" 
          accept=".svg,.jpg,.jpeg,.png,.gif"
           @change="handleFileChange" 
           style="display: none" 
        />
  
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

  <!-- preview area -->
  <div v-if="uploadedFiles.length > 0" class="q-mt-lg">
    <div class="text-h6 q-mb-md">Uploaded Files</div>
    <q-list bordered class="rounded-borders">
      <q-item v-for="(file, index) in uploadedFiles" :key="file.id" class="q-mb-sm">
        <q-item-section>
          <q-item-label>{{ file.name }}</q-item-label>
          <q-item-label caption>
            {{ file.type }} • {{ formatFileSize(file.size) }}
          </q-item-label>
          <q-linear-progress 
            v-if="file.status === 'uploading'"
            :value="file.progress / 100"
            :color="file.progress === 100 ? 'positive' : 'primary'"
            class="q-mt-sm"
          />
        </q-item-section>

        <q-item-section side>
          <div class="row items-center">
            <q-badge 
              :color="getStatusColor(file.status)"
              class="q-mr-sm"
            >
              {{ file.status }}
            </q-badge>
            <q-btn 
              round 
              flat 
              icon="delete" 
              color="negative"
              @click="removeFile(index)"
            />
          </div>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>
  
<script setup>
  import { ref } from 'vue'  

  const uploadedFiles = ref([]);
  let fileIdCounter = 0;

  //show the status of file
  const getStatusColor = (status) => {
    const statusColors = {
      pending: 'grey',
      uploading: 'primary',
      completed: 'positive',
      error: 'negative'
    };
    return statusColors[status] || 'grey';
  };

  // formatting file size
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };
  
  // This function is used to check the file user upload to make sure file type is correct
  const handleFileChange = (event) => {
    const files = event.target.files;
    if (!files) return;

    Array.from(files).forEach(file => {
      const validTypes = ['image/svg+xml', 'image/jpeg', 'image/png', 'image/gif'];
    
    if (validTypes.includes(file.type)) {
        const newFile = {
          id: fileIdCounter++,
          name: file.name,
          type: file.type.split('/')[1].toUpperCase(),
          size: file.size,
          progress: 0,
          status: 'pending',
          rawFile: file
        };
      
        uploadedFiles.value.push(newFile);
        startUpload(newFile); // start upload
      } 
      else {
        fileInfo.value = 'Invalid file type. Please upload SVG, JPG, PNG, or GIF files.';
      }
    });
  };
 
  // Uploading file Simulation
  const startUpload = (file) => {
      file.status = 'uploading';
  
      // Simulation upload progress
      const interval = setInterval(() => {
        file.progress += Math.floor(Math.random() * 20 + 10);
        if (file.progress >= 100) {
          clearInterval(interval);
          file.progress = 100;
          file.status = 'completed';
        }
      }, 300);
  };

  // Delete the file
  const removeFile = (index) => {
    if (confirm('Are you sure you want to remove this file?')) {
      uploadedFiles.value.splice(index, 1);
    }
  };

  // Popup form fields
  const modelVersion = ref('')
  const siteId = ref('')
  const fileInfo = ref('')
  
  // fileinput
  const fileInput = ref(null)

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

  //This function is used to check the submission of model training
  const submitModelTraining = () => {
    if (!modelVersion.value || !siteId.value) {
      alert('please provide all information')
      return
    }
    console.log('start model trainning: ', {
      modelVersion: modelVersion.value,
      siteId: siteId.value,
      file: fileInfo.value
    })
    showModelDialog.value = false
  }

  const handleUploadClick = () => {
    fileInput.value.click()
  }

  const handleStartTraining = () => {
    if (!fileInfo.value) {
      alert('Please select the file you want to upload')
      return
    }
    showModelDialog.value = true
  }
</script>
  
<style scoped>
  .q-item {
    border: 1px solid #eee;
    border-radius: 8px;
  }

  .q-linear-progress {
    height: 8px;
    border-radius: 4px;
  }

  .upload-page {
    margin: 0 auto;
  }
</style>
  