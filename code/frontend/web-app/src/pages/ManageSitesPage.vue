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
        <q-btn label="+ Add Camera" color="primary" text-color="white" />
      </div>

      <div class="row">
        <!-- sidebar section -->
        <div class="col-12 col-md-3">
          <q-list bordered>
            <!-- dropdown for each site -->
            <q-expansion-item label="Site 01" dense>
              <q-item clickable v-ripple>
                <q-item-section>CAM 01</q-item-section>
              </q-item>
              <q-item clickable v-ripple>
                <q-item-section>CAM 02</q-item-section>
              </q-item>
              <q-item clickable v-ripple>
                <q-item-section>CAM 03</q-item-section>
              </q-item>
              <q-item clickable v-ripple>
                <q-item-section>CAM 04</q-item-section>
              </q-item>
            </q-expansion-item>

            
            <q-expansion-item label="Site 02" dense />
            <q-expansion-item label="Site 03" dense />
            <q-expansion-item label="Site 04" dense />
            <q-expansion-item label="Site 05" dense />
            <q-expansion-item label="Site 06" dense />

            
            <q-btn
              label="+ Add New Site"
              flat
              class="full-width bg-dark text-white q-mt-md"
              @click="openAddSiteDialog"
            />
          </q-list>
        </div>

       
        <div class="col-12 col-md-9">
          <q-card bordered class="q-pa-md">
            
            <div class="row justify-between items-center">
              <h2 class="text-h6">CAM 01 View</h2>
              <q-btn label="Live View" color="amber" flat />
            </div>
            <div class="bg-grey-8 q-mt-md" style="height: 250px;"></div>

            
            <div class="row q-mt-md">
              <q-card flat bordered class="col-6 q-pa-md">
                <div class="text-caption text-grey-7">Latitude</div>
                <div class="text-h5 text-bold">48.8584° N</div>
              </q-card>
              <q-card flat bordered class="col-6 q-pa-md">
                <div class="text-caption text-grey-7">Longitude</div>
                <div class="text-h5 text-bold">48.8584° N</div>
              </q-card>
            </div>
          </q-card>
        </div>
      </div>

      
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
    </div>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      addSiteDialog: false, 
      newSite: {
        name: '',
        latitude: '',
        longitude: '',
      },
    };
  },
  methods: {
    openAddSiteDialog() {
      this.addSiteDialog = true;
    },
    closeAddSiteDialog() {
      this.addSiteDialog = false;
      this.resetForm();
    },
    saveNewSite() {
      console.log('New Site Details:', this.newSite); 
      this.closeAddSiteDialog();
    },
    resetForm() {
      this.newSite = {
        name: '',
        latitude: '',
        longitude: '',
      };
    },
  },
};
</script>

<style>
.q-page {
  background: #f9f9f9;
}

.bg-dark {
  background-color: #1e1e2f;
}

.text-white {
  color: white;
}
</style>
