<template>
  <q-page class="q-px-lg q-py-md">
    <div>
      <div class="row justify-between items-center q-mb-lg">
        <div>
          <h1 class="text-h4 text-bold">Manage Sites</h1>
          <p class="text-subtitle2">
            Add,edit and view sites/cameras.
          </p>
        </div>
        <q-btn label="+ Add Camera" color="primary" text-color="white" @click="openAddRTSP" class="add-camera-btn"/>
      </div>

      <div class="row">
        <div class="col-12 col-md-3">

          <!-- Only show site list if there are sites -->
          <div v-if="sites.length > 0" class="sites-container">
            <div v-for="site in sites" :key="site.id" class="site-box">
              <div class="site-header" @click="toggleSite(site)">
                <span>{{ site.name }}</span>
                <q-icon :name="site.expanded ? 'keyboard_arrow_down' : 'keyboard_arrow_right'" size="20px" />
              </div>

              <!-- Only show camera list if the site is expanded and has cameras -->
              <div v-if="site.expanded && site.cameras && site.cameras.length > 0" class="camera-list">
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

              <!-- Show message if site has no cameras and is expanded -->
              <div v-else-if="site.expanded" class="no-cameras-message">
                No cameras added to this site yet
              </div>
            </div>
          </div>

          <!-- Add New Site button always visible -->
          <q-btn
            label="+ ADD NEW SITE"
            class="add-site-btn full-width q-mt-md"
            @click="openAddSiteDialog"
          />
        </div>

        <!-- Main content area -->
        <div class="col-12 col-md-9 q-pl-md">
          <q-card v-if="selectedCamera" class="camera-view-card">
            <q-card-section>
              <div class="row justify-between items-center">
                <div>
                  <h2 class="text-h6">{{ selectedCamera.name }}</h2>
                  <p class="text-caption q-mt-none">{{ selectedCamera.rtsp_url || '192.168.1.100' }}</p>
                </div>
                <q-btn
                  label="LIVE VIEW"
                  color="amber"
                  text-color="dark"
                  class="live-view-btn"
                  @click="startLiveStream"
                />
              </div>
            </q-card-section>

            <div class="stream-container">
              <img
                v-if="streaming"
                ref="imagePlayer"
                class="stream-image"
                :src="currentFrame"
                alt="Live Stream"
              />
              <div v-else class="stream-placeholder">
                Loading stream...
              </div>
            </div>

            <q-card-section>
              <div class="row q-col-gutter-md">
                <div class="col-6">
                  <div class="location-card">
                    <div class="text-caption location-label">Latitude</div>
                    <div class="text-h6 location-value">{{ currentSiteLatitude }}</div>
                  </div>
                </div>
                <div class="col-6">
                  <div class="location-card">
                    <div class="text-caption location-label">Longitude</div>
                    <div class="text-h6 location-value">{{ currentSiteLongitude }}</div>
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <div v-else class="no-camera-selected">
            <p v-if="sites.length > 0">Select a camera to view details</p>
            <p v-else>Add a site and camera to view details</p>
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
            <q-form @submit="saveNewSite">
              <q-input
                v-model="newSite.name"
                outlined
                label="Site Name"
                class="q-mb-md"
                placeholder="Enter site name"
                :rules="[val => !!val || 'Site name is required']"
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

      <!-- Camera dialog - fixed placement -->
      <q-dialog v-model="addRTSP">
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
                :rules="[val => !!val || 'Site assignment is required']"
                :disable="sites.length === 0"
                :hint="sites.length === 0 ? 'Please add a site first' : ''"
              />
            </q-form>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" @click="closeAddRTSP" />
            <q-btn flat label="Save" color="primary" @click="saveCamera" :disable="sites.length === 0" />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Confirmation Dialog for Delete -->
      <q-dialog v-model="deleteConfirmDialog">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="negative" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this camera?</span>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="Delete" color="negative" @click="deleteCamera" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      deleteConfirmDialog: false,
      cameraToDelete: null,
      editingCamera: false,
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
    };
  },

  computed: {
    currentSiteLatitude() {
      if (this.selectedSite && this.selectedSite.latitude) {
        return this.selectedSite.latitude;
      }
      return '0° N';
    },
    currentSiteLongitude() {
      if (this.selectedSite && this.selectedSite.longitude) {
        return this.selectedSite.longitude;
      }
      return '0° E';
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
      // If there are no sites, notify user
      if (this.sites.length === 0) {
        this.$q.notify({
          message: 'Please add a site first',
          color: 'warning'
        });
        return;
      }

      this.editingCamera = false;
      this.addRTSP = true;
      this.resetForm();

      // If a site is selected, pre-select it for the new camera
      if (this.selectedSite) {
        this.newCamera.siteId = this.selectedSite.id;
      } else if (this.sites.length > 0) {
        // Otherwise select the first site by default
        this.newCamera.siteId = this.sites[0].id;
      }
    },

    closeAddRTSP() {
      this.addRTSP = false;
      this.editingCamera = false;
      this.resetForm();
    },

    async saveCamera() {
      if (!this.newCamera.siteId) {
        this.$q.notify({
          message: 'Please select a site for this camera',
          color: 'negative'

        });
        return;
      }

      try {
        if (this.editingCamera) {
          // Update existing camera
          await axios.put(`http://127.0.0.1:3002/api/update-camera/${this.newCamera.id}`, {
            name: this.newCamera.name,
            rtsp_url: this.newCamera.RTSPURL,
            site_id: this.newCamera.siteId.value
          });
        } else {
          // Add new camera
          console.log('siteId type:', typeof this.newCamera.siteId, this.newCamera.siteId);
          await axios.post('http://127.0.0.1:3002/api/add-camera', {
            name: this.newCamera.name,
            rtsp_url: this.newCamera.RTSPURL,
            site_id: this.newCamera.siteId.value
          });
        }

        // Refresh the sites data
        await this.fetchSites();

        // If we had a site selected, make sure it's expanded to show the new camera
        if (this.selectedSite) {
          const updatedSite = this.sites.find(s => s.id === this.selectedSite.id);
          if (updatedSite) {
            updatedSite.expanded = true;
          }
        } else {
          // If adding a camera without a selected site, expand the site it was added to
          const targetSite = this.sites.find(s => s.id === this.newCamera.siteId);
          if (targetSite) {
            targetSite.expanded = true;
          }
        }

        // Close the dialog
        this.closeAddRTSP();

        // If adding a new camera, set it as video source
        if (!this.editingCamera) {
          this.videoSrc = this.newCamera.RTSPURL;
          await this.startLiveStream();
        }
      } catch (error) {
        console.error('Error saving camera:', error);
        this.$q.notify({
          message: 'Error saving camera',
          color: 'negative'
        });
      }
    },

    async saveNewSite() {
      try {
        await axios.post('http://127.0.0.1:3002/api/add-site', {

          name: this.newSite.name,
          latitude: this.newSite.latitude,
          longitude: this.newSite.longitude,
        });

        // Refresh the sites data after saving
        await this.fetchSites();

        // Expand the newly added site
        if (this.sites.length > 0) {
          // Get the newly added site
          const newSite = this.sites.find(s => s.name === this.newSite.name) || this.sites[this.sites.length - 1];

          // Expand only the new site
          this.sites.forEach(site => {
            site.expanded = site.id === newSite.id;
          });
        }

        // Close the dialog
        this.closeAddSiteDialog();
        this.$q.notify({
          message: 'Site added successfully',
          color: 'positive'
        });
      } catch (error) {
        console.error('Error saving new site:', error);
        this.$q.notify({
          message: 'Error adding site',
          color: 'negative'
        });
      }
    },

    async fetchSites() {
      try {
        const response = await axios.get('http://127.0.0.1:3002/api/sites');

        // Add expanded property to each site for dropdown functionality
        this.sites = (response.data.sites || []).map(site => ({
          ...site,
          expanded: false,
          cameras: site.cameras || []
        }));

        console.log('Sites fetched:', this.sites);

        // If we previously had a selected site/camera, try to restore the selection
        if (this.selectedSite && this.selectedCamera) {
          const updatedSite = this.sites.find(s => s.id === this.selectedSite.id);
          if (updatedSite) {
            updatedSite.expanded = true;
            this.selectedSite = updatedSite;

            const updatedCamera = updatedSite.cameras.find(c => c.id === this.selectedCamera.id);
            if (updatedCamera) {
              this.selectedCamera = updatedCamera;
            } else {
              this.selectedCamera = null;
            }
          } else {
            this.selectedSite = null;
            this.selectedCamera = null;
          }
        }

      } catch (error) {
        console.error('Error fetching sites:', error);
        this.$q.notify({
          message: 'Error loading sites',
          color: 'negative'
        });


        this.sites = [];
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
        siteId: this.selectedSite ? this.selectedSite.id : (this.sites.length > 0 ? this.sites[0].id : null),
        id: null
      };
    },

    toggleSite(site) {
      // Toggle expanded state for this site
      site.expanded = !site.expanded;
    },

    selectCamera(camera, site) {
      this.selectedCamera = camera;
      this.selectedSite = site;
      this.videoSrc = camera.rtsp_url;
    },

    openEditCamera(camera) {
      this.editingCamera = true;
      this.newCamera = {
        id: camera.id,
        name: camera.name,
        RTSPURL: camera.rtsp_url || '',
        siteId: camera.site_id || null
      };
      this.addRTSP = true;
    },

    confirmDeleteCamera(camera) {
      this.cameraToDelete = camera;
      this.deleteConfirmDialog = true;
    },

    async deleteCamera() {
      if (!this.cameraToDelete) return;

      try {
        await axios.delete(`http://127.0.0.1:3002/api/delete-camera/${this.cameraToDelete.id}`);

        // Remove the camera from the local state
        if (this.selectedSite) {
          this.selectedSite.cameras = this.selectedSite.cameras.filter(
            c => c.id !== this.cameraToDelete.id
          );
        }

        // If this was the selected camera, clear the selection
        if (this.selectedCamera && this.selectedCamera.id === this.cameraToDelete.id) {
          this.selectedCamera = null;
        }

        // Refresh the sites data
        await this.fetchSites();

        // Reset
        this.cameraToDelete = null;

        // Show success message
        this.$q.notify({
          message: 'Camera deleted successfully',
          color: 'positive'
        });
      } catch (error) {
        console.error('Error deleting camera:', error);
        this.$q.notify({
          message: 'Error deleting camera',
          color: 'negative'
        });
      }
    },
  }
};
</script>

<style>
.q-page {
  background: #f9f9f9;
}

/* Site list styling */
.sites-container {
  width: 100%;
}

.site-box {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  margin-bottom: 10px;
  background-color: white;
  overflow: hidden;
}

.site-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  font-weight: 500;
  background-color: #f5f5f5;
}

.camera-list {
  background-color: white;
  border-top: 1px solid #e0e0e0;
}

.camera-item {
  padding: 10px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.camera-item:hover {
  background-color: #f5f5f5;
}

.camera-active {
  background-color: #e3f2fd;
}

.camera-actions {
  opacity: 0;
  transition: opacity 0.2s;
}

.camera-item:hover .camera-actions {
  opacity: 1;
}

.no-cameras-message {
  padding: 12px 16px;
  color: #9e9e9e;
  font-style: italic;
  text-align: center;
  border-top: 1px solid #e0e0e0;
}

/* Button styling  */
.add-site-btn {
  background-color: #1e1e2f;
  color: white;
  height: 45px;
  font-weight: 500;
  letter-spacing: 0.5px;
  border-radius: 6px;
}

.add-camera-btn {
  background-color: #2979ff;
  padding: 10px 16px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* Camera view styling */
.camera-view-card {
  border-radius: 8px;
  overflow: hidden;
}

.stream-container {
  height: 350px;
  background-color: #2d3748;
  position: relative;
}

.stream-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.stream-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: white;
  font-size: 1.5rem;
}

.live-view-btn {
  font-weight: 500;
  letter-spacing: 0.5px;
}

.location-card {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 16px;
}

.location-label {
  color: #757575;
  margin-bottom: 4px;
}

.location-value {
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
</style>