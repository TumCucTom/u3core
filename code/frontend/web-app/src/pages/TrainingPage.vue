<template>
  <q-page padding class="upload-page">
    <div class="q-mb-lg"> 
      <h1 class="text-h4 text-bold">Upload Training Data</h1>
      <p class="text-subtitle2">Track, manage and forecast your customers and orders</p>
    </div>

    <!-- Tab for switching -->
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

    <!-- Upload data area -->
    <div v-if="activeTab === 'uploadData'">
      <!-- drop area -->
      <div class="q-mt-lg flex flex-center q-pa-md upload-area" @click="handleUploadClick">
        <div class="column items-center text-center">
          <q-icon name="cloud_upload" size="36px" color="primary" />
          <div class="text-body2 text-primary q-my-xs">
            Click to upload
          </div>
          <div class="text-caption text-grey-7">
            or drag and drop<br />
            SVG, PNG, JPG or GIF (max. 800×400px)
          </div>
          <div v-if="fileInfo" class="text-caption text-green q-mt-sm">
            {{ fileInfo }}
          </div>
        </div>
      </div>

      <!-- preview area -->
      <div v-if="uploadedFiles.length > 0" class="file-list q-mt-md">
        <q-item 
          v-for="(file, index) in uploadedFiles" 
          :key="file.id" 
          class="q-mb-sm preview-item"
        >
          <q-item-section>
            <div class="row items-center">
              <q-icon name="insert_drive_file" class="q-mr-sm" />
              <div>
                <div class="text-caption">{{ file.name }}</div>
                <div class="text-caption text-grey-6">
                  {{ file.type }} • {{ formatFileSize(file.size) }}
                  <q-badge :color="getStatusColor(file.status)" class="q-ml-sm">
                    {{ file.status }}
                  </q-badge>
                </div>
                <!-- 标签显示区域 -->
                <div v-if="file.tags?.length" class="q-mt-xs">
                  <q-badge 
                    v-for="(tag, tagIndex) in file.tags" 
                    :key="tagIndex"
                    color="secondary" 
                    class="q-mr-xs cursor-pointer"
                    @click="removeTag(file, tagIndex)"
                  >
                    {{ tag }}
                    <q-tooltip>Click to remove</q-tooltip>
                  </q-badge>
                </div>
                <!-- 标签输入区域 -->
                <div v-if="editingFileId === file.id" class="q-mt-xs row items-center">
                  <q-input
                    v-model="newTag"
                    dense
                    placeholder="Enter tag"
                    class="col"
                    @keyup.enter="addTag(file)"
                  />
                  <q-btn 
                    flat 
                    dense 
                    icon="check" 
                    color="positive" 
                    class="q-ml-sm"
                    @click="addTag(file)"
                  />
                  <q-btn
                    flat
                    dense
                    icon="close"
                    color="negative"
                    class="q-ml-xs"
                    @click="cancelTagEdit"
                  />
                </div>
              </div>
            </div>
          </q-item-section>

          <q-item-section side>
            <div class="row items-center">
              <q-btn 
                round 
                flat 
                icon="local_offer" 
                size="sm" 
                color="grey-6"
                class="q-mr-xs"
                @click="startTagEdit(file.id)"
              />
              <q-btn 
                round 
                flat 
                icon="delete" 
                size="sm" 
                color="grey-6"
                @click="removeFile(index)"
              />
            </div>
          </q-item-section>
        </q-item>
      </div>

      <!-- hidden file input -->
      <input
        type="file"
        ref="fileInput"
        accept=".svg,.jpg,.jpeg,.png,.gif"
        @change="handleFileChange"
        style="display: none"
      />

      <!-- buttons -->
      <div class="q-mt-lg row justify-end">
        <q-btn flat label="Cancel" color="primary" class="q-mr-sm" />
        <q-btn
          label="Start Model Training"
          color="dark"
          @click="handleStartTraining"
        />
      </div>
    </div>

    <!-- Upload Logs area -->
    <div v-else>
      <div class="q-mt-md">
        <q-table
          title="All Uploads"
          :data="[]"
          :columns="columns"
          row-key="modelVersion"
          dense
          flat
        ></q-table>
      </div>
    </div>

    <!-- Training simulator window -->
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

const uploadedFiles = ref([]);
let fileIdCounter = 0;

// 标签相关状态
const editingFileId = ref(null);
const newTag = ref('');

// status manage
const activeTab = ref('uploadData')
const showModelDialog = ref(false)
const modelVersion = ref('')
const siteId = ref('')
const fileInfo = ref('')
const fileInput = ref(null)

// site options
const siteOptions = ['Site A', 'Site B', 'Site C']

// 
const columns = [
  { name: 'modelVersion', label: 'Model version', field: 'modelVersion' },
  { name: 'siteId', label: 'Site Id', field: 'siteId' },
  { name: 'dateUploaded', label: 'Date uploaded', field: 'dateUploaded' },
  { name: 'lastUpdated', label: 'Last updated', field: 'lastUpdated' },
  { name: 'trainingStatus', label: 'Training Status', field: 'trainingStatus' },
  { name: 'action', label: '', field: 'action' }
]

// handle file upload
const handleUploadClick = () => {
  fileInput.value.click()
}

const handleFileChange = (event) => {
  const files = event.target.files
  if (!files.length) return

  Array.from(files).forEach(file => {
    const validTypes = ['image/svg+xml', 'image/jpeg', 'image/png', 'image/gif']
    
    if (validTypes.includes(file.type)) {
      const newFile = {
        id: fileIdCounter++,
        name: file.name,
        type: file.type.split('/')[1].toUpperCase(),
        size: file.size,
        progress: 0,
        status: 'pending',
        raw: file,
        tags: [] // 初始化标签数组
      }
      uploadedFiles.value.push(newFile)
      startUpload(newFile)
    } else {
      fileInfo.value = 'Invalid file type. Please upload SVG, JPG, PNG, or GIF files.'
    }
  })
}

// 标签操作方法
const startTagEdit = (fileId) => {
  editingFileId.value = fileId
  newTag.value = ''
}

const cancelTagEdit = () => {
  editingFileId.value = null
  newTag.value = ''
}

const addTag = (file) => {
  if (newTag.value.trim()) {
    if (!file.tags.includes(newTag.value.trim())) {
      file.tags.push(newTag.value.trim())
    }
    cancelTagEdit()
  }
}

const removeTag = (file, tagIndex) => {
  file.tags.splice(tagIndex, 1)
}

// upload simulation
const startUpload = (file) => {
  file.status = 'uploading'
  const interval = setInterval(() => {
    file.progress = Math.min(file.progress + Math.random() * 20, 95)
    if (file.progress >= 95) {
      clearInterval(interval)
      setTimeout(() => {
        file.progress = 100
        file.status = 'completed'
      }, 500)
    }
  }, 300)
}

// delete the file
const removeFile = (index) => {
  if (confirm('Are you sure you want to remove this file?')) {
    uploadedFiles.value.splice(index, 1)
  }
}

// status color
const getStatusColor = (status) => {
  const statusColors = {
    pending: 'grey',
    uploading: 'primary',
    completed: 'positive',
    error: 'negative'
  }
  return statusColors[status] || 'grey'
}

// formatting file size
const formatFileSize = (bytes) => {
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  return `${size.toFixed(1)} ${units[unitIndex]}`
}

// training modle submission
const handleStartTraining = () => {
  if (!uploadedFiles.value.length) {
    alert('Please select files to upload')
    return
  }
  showModelDialog.value = true
}

const submitModelTraining = () => {
  if (!modelVersion.value || !siteId.value) {
    alert('Please provide all required information')
    return
  }
  console.log('Starting training with:', {
    modelVersion: modelVersion.value,
    siteId: siteId.value,
    files: uploadedFiles.value
  })
  showModelDialog.value = false
}
</script>

<style scoped>
.file-list {
  width: 100%;
  background: transparent;
}

.file-item {
  border-radius: 4px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.12);
  transition: all 0.2s ease;
}

.file-item:hover {
  background: #f8f9fa;
  transform: translateX(2px);
}

.q-badge {
  font-size: 0.7em;
  padding: 2px 6px;
  transition: opacity 0.2s;
}

.q-badge:hover {
  opacity: 0.8;
}

.upload-page {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 24px;
}

.upload-area {
  border: 2px dashed #d3d3d3;
  border-radius: 8px;
  height: 200px;
  cursor: pointer;
  transition: border-color 0.3s ease;
  background: white;
  width: 100%;
}

.preview-area {
  width: 100%;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-top: 16px;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.preview-item {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: transform 0.2s;
  padding: 12px;
}

.preview-item:hover {
  transform: translateX(4px);
}

.q-linear-progress {
  height: 6px;
  border-radius: 3px;
}

.row.justify-end {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

/* 标签输入区域样式 */
.q-input {
  width: 150px;
  margin-top: 8px;
}
</style>
  