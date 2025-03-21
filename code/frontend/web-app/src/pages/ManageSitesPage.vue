<template>
  <q-page class="q-px-lg q-py-md">
    <div>
      <div class="row justify-between items-center q-mb-lg">
        <div>
          <h1 class="text-h4 text-bold">Manage Sites</h1>
          <p class="text-subtitle2">
            Track, manage and forecast your customers and orders.
          </p>
        </div>
        <q-btn label="+ Add Camera" color="primary" text-color="white" @click="openAddRTSP"/>
      </div>

      <div class="row">
        <!-- sidebar section -->
        <div class="col-12 col-md-3">
          + <!-- Sites with dropdown style like Figma -->
     <div class="sites-list">
      <div v-for="site in sites" :key="site.id" class="site-item">
        <div
          class="site-header q-py-sm q-px-md"
          @click="toggleSite(site)"
          :class="{ 'site-active': site.expanded }"
        >
          <div class="row items-center justify-between">
            <div>{{ site.name }}</div>
            <q-icon :name="site.expanded ? 'keyboard_arrow_down' : 'keyboard_arrow_right'" />
          </div>
        </div>
        <div v-show="site.expanded" class="camera-list">
         <div
            v-for="camera in site.cameras"
            :key="camera.id"
            class="camera-item q-py-sm q-px-md"
            @click="selectCamera(camera, site)"
            :class="{ 'camera-active': selectedCamera && selectedCamera.id === camera.id }"
          >
            <div class="row items-center justify-between">
              <div>{{ camera.name }}</div>
              <div class="camera-actions">
                <q-btn flat round dense icon="edit" size="sm" @click.stop="openEditCamera(camera)" />
                <q-btn flat round dense icon="delete" size="sm" @click.stop="confirmDeleteCamera(camera)" />
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <q-btn
      label="+ Add New Site"
      flat
      class="add-site-btn full-width q-mt-md"
      @click="openAddSiteDialog"
    />





        </div>

        <div class="col-12 col-md-9">
          + <div class="col-12 col-md-9 q-pl-md">
   <q-card v-if="selectedCamera" class="camera-view-card">
     <q-card-section>
       <div class="row justify-between items-center">
         <div>
           <h2 class="text-h6">{{ selectedCamera.name }}</h2>
           <p class="text-caption q-mt-none">{{ selectedCamera.rtsp_url || '192.168.1.100' }}</p>
         </div>
         <q-btn
           label="Live View"
           color="amber"
           text-color="dark"
           class="live-view-btn"
           @click="startLiveStream"
         />
       </div>
     </q-card-section>

     <div class="bg-grey-8 q-mt-md" style="height: 250px; position: relative;">
       <img
         v-if="streaming"
         ref="imagePlayer"
         style="width: 100%; height: 100%; object-fit: cover;"
         :src="currentFrame"
         alt="Live Stream"
       />
       <div
         v-else
         style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: black; color: white; font-size: 2rem;">
         Loading stream...
       </div>
     </div>

     <div class="row q-mt-md">
       <q-card flat bordered class="col-6 q-pa-md">
         <div class="text-caption text-grey-7">Latitude</div>
         <div class="text-h5 text-bold">{{ currentSiteLatitude }}</div>
       </q-card>
       <q-card flat bordered class="col-6 q-pa-md">
         <div class="text-caption text-grey-7">Longitude</div>
         <div class="text-h5 text-bold">{{ currentSiteLongitude }}</div>
       </q-card>
     </div>
   </q-card>

   <div v-else class="no-camera-selected">
     <p>Select a camera to view details</p>
   </div>
 </div>
        </div>
      </div>

      <!-- Dialogs for adding site and RTSP camera -->
      <q-dialog v-model="addSiteDialog">
        <q-card style="min-width: 400px">
          <q-card-section>
            <div class="text-h6">Add New Site</div>
          </q-card-section>
          <q-card-section>
            <q-form>
              <q-input
                v-model="newSite.name"
                outlined
                label="Site Name"
                class="q-mb-md"
                placeholder="Enter site name"
              />
              <q-input
                v-model="newSite.latitude"
                outlined
                label="Latitude"
                class="q-mb-md"
                placeholder="Enter latitude"
              />
              <q-input
                v-model="newSite.longitude"
                outlined
                label="Longitude"
                class="q-mb-md"
                placeholder="Enter longitude"
              />
            </q-form>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" @click="closeAddSiteDialog" />
            <q-btn flat label="Save" color="primary" @click="saveNewSite" />
          </q-card-actions>
        </q-card>
      </q-dialog>

        <q-card style="min-width: 400px">
          <q-card-section>
            <div class="text-h6">{{ editingCamera ? 'Edit Camera' : 'Add RTSP Camera' }}</div>
          </q-card-section>
          <q-card-section>
            <q-form>
              <q-input
                v-model="newCamera.name"
                outlined
                label="Camera Name"
                class="q-mb-md"
                placeholder="Enter camera name"
              />
              <q-input
                v-model="newCamera.RTSPURL"
                outlined
                label="URL"
                class="q-mb-md"
                placeholder="Enter RTSP URL"
              />

              <q-select
                v-model="newCamera.siteId"
                outlined
                label="Assign to Site"
                :options="siteOptions"
                class="q-mb-md"
                option-label="label"
                option-value="value"
              />
            </q-form>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" @click="closeAddRTSP" />
            <q-btn flat label="Save" color="primary" @click="saveCamera" />
          </q-card-actions>
        </q-card>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {

      selectedCamera: null,
     selectedSite: null,
      addSiteDialog: false,
      addRTSP: false,
      newSite: {
        name: '',
        latitude: '',
        longitude: '',
      },
      newCamera: {
        name: '',
        RTSPURL: '',
        siteId: null,
        id: null
      },
      streaming: false,
      videoSrc: '', // RTSP URL
      sites: [], // List of sites fetched from the server
      socket: null, // WebSocket instance
      currentFrame: '', // Current frame as blob URL
      editingCamera: false,
    };
  },

  computed: {
   currentSiteLatitude() {
     if (this.selectedSite && this.selectedSite.latitude) {
       return this.selectedSite.latitude;
     }
     return '48.8584° N';
   },
   currentSiteLongitude() {
     if (this.selectedSite && this.selectedSite.longitude) {
       return this.selectedSite.longitude;
     }
     return '48.8584° E';
   },

  siteOptions() {
     return this.sites.map(site => ({
       label: site.name,
       value: site.id
     }));
   },
 },




  created() {
    this.fetchSites();
  },
  methods: {
    async startLiveStream() {
      // Set up WebSocket for live stream
      if (this.socket) {
        this.socket.close(); // Close any existing socket
      }

      this.socket = new WebSocket('ws://localhost:8080'); // Adjust to your WebSocket server
      this.socket.binaryType = 'blob'; // Handle binary data

      this.socket.onopen = () => {
        console.log('WebSocket connection established');
        this.streaming = true;

        // Send RTSP URL to the WebSocket server
        if (this.videoSrc) {
          this.socket.send(this.videoSrc);
          console.log('RTSP URL sent to WebSocket server:', this.videoSrc);
        }
      };

      this.socket.onmessage = (event) => {
        console.log('Received video frame from WebSocket server:', event.data);
        // Handle received video frames
        const blob = event.data;
        const newBlobUrl = URL.createObjectURL(blob);

        // Clean up old frame memory
        if (this.currentFrame) {
          URL.revokeObjectURL(this.currentFrame);
        }

        // Set the new frame
        this.currentFrame = newBlobUrl;
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.socket.onclose = () => {
        console.log('WebSocket connection closed');
        this.streaming = false;

        // Clean up current frame memory
        if (this.currentFrame) {
          URL.revokeObjectURL(this.currentFrame);
          this.currentFrame = '';
        }
      };
    },
    openAddSiteDialog() {
      this.addSiteDialog = true;
    },
    closeAddSiteDialog() {
      this.addSiteDialog = false;
      this.resetForm();
    },
    openAddRTSP() {
      this.editingCamera = false;
      this.addRTSP = true;
      this.resetForm();
         // If a site is selected, pre-select it for the new camera
      if (this.selectedSite) {
        this.newCamera.siteId = this.selectedSite.id;
      }
    },
    closeAddRTSP() {
      this.addRTSP = false;
    },
    async saveNewRTSP() {
      try {
        const response = await axios.post('http://16.171.224.57:3002/api/add-camera', {
          name: this.newCamera.name,
          rtsp_url: this.newCamera.RTSPURL,
        });
        console.log('Server Response:', response.data);
        this.closeAddRTSP();

        // Update video source and start live streaming
        this.videoSrc = this.newCamera.RTSPURL;
        console.log('Video Source:', this.videoSrc)
        await this.startLiveStream();
      } catch (error) {
        console.error('Error saving new RTSP:', error);
      }
    },
    async saveNewSite() {
      try {
        const response = await axios.post('http://16.171.224.57:3002/add-site', {
          name: this.newSite.name,
          latitude: this.newSite.latitude,
          longitude: this.newSite.longitude,
        });
        console.log('Server Response:', response.data);
        this.closeAddSiteDialog();
      } catch (error) {
        console.error('Error saving new site:', error);
      }
    },
    async fetchSites() {
      try {
        const response = await axios.get('http://16.171.224.57:3002/sites');
        // Add expanded property to each site for dropdown functionality
        this.sites = (response.data.sites || []).map(site => ({
          ...site,
          expanded: false,
          cameras: site.cameras || []
        }));
      } catch (error) {
        console.error('Error fetching sites:', error);
      }
    },
    resetForm() {
      this.newSite = {
        name: '',
        latitude: '',
        longitude: '',
      };
      this.newCamera = {
        name: '',
        RTSPURL: '',
        siteId: this.selectedSite ? this.selectedSite.id : null,
       id: null
      };
    },
  toggleSite(site) {
    // Toggle expanded state for this site
    site.expanded = !site.expanded;

    // Close all other sites
    this.sites.forEach(s => {
      if (s.id !== site.id) {
        s.expanded = false;
      }
    });
  },


   selectCamera(camera, site) {
    this.selectedCamera = camera;
    this.selectedSite = site;
    this.videoSrc = camera.rtsp_url;
 },


  }

};



</script>

<style>

 .camera-view-card {
   border-radius: 8px;
   overflow: hidden;
 }

 .live-view-btn {
   font-weight: 500;
 }

 .no-camera-selected {
   display: flex;
   align-items: center;
   justify-content: center;
   height: 350px;
   border: 1px dashed #e0e0e0;
   border-radius: 8px;
   color: #9e9e9e;
   font-size: 1.2rem;
 }
 .sites-list {
   border: 1px solid #e0e0e0;
   border-radius: 4px;
   overflow: hidden;
 }

 .site-item {
   border-bottom: 1px solid #e0e0e0;
 }

 .site-header {
   background-color: #f5f5f5;
   cursor: pointer;
   transition: background-color 0.2s;
 }

 .site-active {
   font-weight: 500;
 }

 .camera-list {
   background-color: white;
 }

 .camera-item {
   padding-left: 24px;
   cursor: pointer;
   transition: background-color 0.2s;
 }

 .add-site-btn {
   background-color: #1e1e2f;
   color: white;
   height: 42px;
 }
.q-page {
  background: #f9f9f9;
}

.bg-dark {
  background-color: #1e1e2f;
}

.text-white {
  color: white;
}

.loading-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2rem; /* Make the text large */
  color: white;
}
</style>
